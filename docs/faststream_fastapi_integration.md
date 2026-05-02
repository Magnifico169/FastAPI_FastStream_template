FastStream can be seamlessly integrated with other frameworks and runtimes, providing a unified way to combine event-driven and request-driven architectures. In particular, it works well alongside frameworks like FastAPI, as well as task processing tools such as TaskIQ and similar async ecosystems.

Let’s start with a simple example of a small service where FastStream and FastAPI are used together, each managing its own lifecycle and dependency injection:

```python
from fastapi import FastAPI
from faststream import FastStream
from faststream.rabbit import RabbitBroker

# FastStream part
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
stream_app = FastStream(broker)

@broker.subscriber("orders")
async def handle_order(msg: dict):
    print(f"[BROKER] {msg}")

# FastAPI part
api_app = FastAPI()

@api_app.get("/")
async def root():
    return {"status": "ok"}
```

In this setup, FastAPI and FastStream coexist but remain independent systems. Each has its own lifecycle, its own dependency injection mechanism, and its own entry point. While this works, it is not always convenient to maintain two separate DI systems — one for FastAPI and another for FastStream.

To address this, FastStream provides tight integration with FastAPI, allowing you to reuse FastAPI’s dependency injection system and unify the application structure.

Here’s how you can do it using `RabbitRouter`:

```python
from fastapi import FastAPI, Depends
from faststream.rabbit.fastapi import RabbitRouter

router = RabbitRouter("amqp://guest:guest@localhost:5672/")

app = FastAPI()
app.include_router(router)

# access broker via router
broker = router.broker

# shared dependency
def get_user():
    return {"name": "John"}

# FastAPI route
@app.get("/")
async def root(user=Depends(get_user)):
    return {"user": user}

# FastStream subscriber using FastAPI DI
@router.subscriber("orders")
async def handle_order(msg: dict, user=Depends(get_user)):
    print(f"[BROKER] {msg}, user={user}")
```

In this approach:

* `RabbitRouter` integrates directly into the FastAPI application via `include_router`.
* The broker is available as `router.broker`.
* FastStream handlers can use FastAPI’s dependency injection (`Depends`).
* There is a single lifecycle and a single DI container shared across both HTTP and message-based handlers.

This results in a cleaner architecture where FastAPI becomes the central entry point, and FastStream naturally extends it with event-driven capabilities.
