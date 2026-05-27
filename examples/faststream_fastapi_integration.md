# FastAPI + FastStream integration

FastStream integrates with FastAPI through **RabbitRouter**, giving a single DI container and lifecycle for HTTP and message handlers.

## 1. Separate lifecycles (not recommended for new projects)

FastAPI and FastStream can run as independent apps with their own brokers:

```python
from fastapi import FastAPI
from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
stream_app = FastStream(broker)

@broker.subscriber("orders")
async def handle_order(msg: dict) -> None:
    print(f"[BROKER] {msg}")

api_app = FastAPI()

@api_app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok"}
```

Drawbacks: two DI systems, two entry points, duplicated configuration.

## 2. RabbitRouter in a single process (this template)

This is the pattern used in [`src/app/`](../src/app/):

```python
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from faststream.rabbit.fastapi import RabbitRouter

rabbit_router = RabbitRouter("amqp://guest:guest@localhost:5672/")
rabbit_broker = rabbit_router.broker

@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_broker.start()
    yield
    await rabbit_broker.stop()

app = FastAPI(lifespan=lifespan)
app.include_router(rabbit_router)

def get_service() -> str:
    return "shared-context"

@app.post("/messages")
async def create_message(service: str = Depends(get_service)) -> dict[str, str]:
    await rabbit_broker.publish({"text": "hello"}, queue="messages_queue")
    return {"status": "processing"}

@rabbit_router.subscriber("messages_queue")
async def handle_message(msg: dict, service: str = Depends(get_service)) -> None:
    print(f"[BROKER] {msg}, service={service}")
```

Key points:

- `app.include_router(rabbit_router)` registers subscribers.
- Broker starts in FastAPI lifespan.
- HTTP routes and subscribers share `Depends()`.

See [`src/app/main.py`](../src/app/main.py), [`src/app/api/v1/messages.py`](../src/app/api/v1/messages.py), [`src/app/consumers/message_handler.py`](../src/app/consumers/message_handler.py).

## 3. Separate worker process

For production scaling, split HTTP and consumers:

**API process** — publishes messages (same as this template).

**Worker process** — only subscribers:

```python
# worker.py
from faststream import FastStream
from app.infrastructure.messaging.rabbit import rabbit_broker, messages_exchange, messages_queue
from app.consumers import message_handler  # noqa: F401

app = FastStream(rabbit_broker)

@app.after_startup
async def declare_topology() -> None:
    exchange = await rabbit_broker.declare_exchange(messages_exchange)
    queue = await rabbit_broker.declare_queue(messages_queue)
    await queue.bind(exchange)
```

Run:

```bash
faststream run worker:app
```

Trade-off: independent scaling, but manual queue/exchange declaration and a second deployable unit.

## Further reading

- [FastStream FastAPI integration docs](https://faststream.ag2.ai/latest/integrations/fastapi/)
