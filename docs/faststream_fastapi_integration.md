# FastAPI + FastStream integration

This template uses **RabbitRouter** to run FastAPI and FastStream in a **single process** with shared dependency injection and Postgres persistence.

## Pattern used in this repo

```python
# infrastructure/messaging/rabbit.py
rabbit_router = RabbitRouter(url=rabbitmq_uri)
rabbit_broker = rabbit_router.broker

# api/v1/messages.py — HTTP enqueues via MessageService
@messages_router.post("/messages")
async def create_message(
    message: MessageCreateDTO,
    message_service: MessageServiceDep,
) -> MessageStatusResponseDTO:
    await message_service.enqueue(message)

# consumers/message_handler.py — subscriber persists via MessageService
@rabbit_router.subscriber(queue=messages_queue, exchange=messages_exchange)
async def handle_message(
    message: Message,
    message_service: MessageServiceDep,
) -> None:
    await message_service.process(message)

# main.py — single entry point
def create_app() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.include_router(messages_router)
    application.include_router(rabbit_router)
    return application

@asynccontextmanager
async def lifespan(app):
    await PostgresSessionFactory.initialize()
    await rabbit_broker.start()
    yield
    await rabbit_broker.stop()
    await PostgresSessionFactory.close()
```

Key points:

- `RabbitRouter` is included in FastAPI via `app.include_router(rabbit_router)`.
- The broker and database session factory start/stop in FastAPI lifespan.
- HTTP handlers and subscribers share the same broker and can use FastAPI `Depends()`.

## Alternative: separate worker process

For heavier workloads you can split HTTP and consumers into two processes:

1. **API process** — FastAPI publishes messages (as in this template).
2. **Worker process** — `faststream run worker:app` runs only subscribers.

That adds a second entry point and manual queue/exchange declaration on worker startup, but scales consumers independently from HTTP.

See [examples/faststream_fastapi_integration.md](../examples/faststream_fastapi_integration.md) for a worker example and the [FastStream docs](https://faststream.ag2.ai/latest/integrations/fastapi/) for details.
