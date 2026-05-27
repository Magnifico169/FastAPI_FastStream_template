# FastAPI + FastStream integration

This template uses **RabbitRouter** to run FastAPI and FastStream in a **single process** with shared dependency injection.

## Pattern used in this repo

```python
# messaging.py
rabbit_router = RabbitRouter(url=rabbitmq_uri)
rabbit_broker = rabbit_router.broker

# api/routes.py — HTTP publishes a message
await rabbit_broker.publish(message, queue=messages_queue, exchange=messages_exchange)

# consumers/handler.py — subscriber processes it
@rabbit_router.subscriber(queue=messages_queue, exchange=messages_exchange)
async def handle_message(message: MessageCreate) -> None:
    logger.info("Received message: %s", message.text)

# main.py — single entry point
app.include_router(api_router)
app.include_router(rabbit_router)

@asynccontextmanager
async def lifespan(app):
    await rabbit_broker.start()
    yield
    await rabbit_broker.stop()
```

Key points:

- `RabbitRouter` is included in FastAPI via `app.include_router(rabbit_router)`.
- The broker is started/stopped in FastAPI lifespan.
- HTTP handlers and subscribers share the same broker and can use FastAPI `Depends()`.

## Alternative: separate worker process

For heavier workloads you can split HTTP and consumers into two processes:

1. **API process** — FastAPI publishes messages (as in this template).
2. **Worker process** — `faststream run app.faststream_app:app` runs only subscribers.

That adds a second entry point and manual queue/exchange declaration on worker startup, but scales consumers independently from HTTP.

See the [FastStream docs](https://faststream.ag2.ai/latest/integrations/fastapi/) for details.
