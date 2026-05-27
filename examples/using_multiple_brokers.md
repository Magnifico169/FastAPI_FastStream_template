# Using multiple brokers

Sometimes one service connects to **more than one RabbitMQ broker** — for example, consuming from a legacy system and publishing to an internal bus.

## When you need multiple brokers

- Migrating from an old broker to a new one (dual-write / dual-read period)
- Integrating with an external partner's RabbitMQ cluster
- Separating domain events from integration events

## Pattern: one RabbitRouter per broker

Each broker gets its own `RabbitRouter` (or `RabbitBroker`):

```python
from fastapi import FastAPI
from faststream.rabbit.fastapi import RabbitRouter

internal_router = RabbitRouter("amqp://guest:guest@internal:5672/")
external_router = RabbitRouter("amqp://guest:guest@external:5672/")

internal_broker = internal_router.broker
external_broker = external_router.broker

app = FastAPI()
app.include_router(internal_router)
app.include_router(external_router)
```

Subscribers are bound to the router they belong to:

```python
@internal_router.subscriber(queue="orders", exchange="orders_exchange")
async def handle_internal_order(msg: dict) -> None:
    ...

@external_router.subscriber(queue="partner_events", exchange="partner_exchange")
async def handle_partner_event(msg: dict) -> None:
    ...
```

HTTP handlers publish to the correct broker explicitly:

```python
await internal_broker.publish(payload, queue="orders", exchange="orders_exchange")
await external_broker.publish(payload, queue="partner_events", exchange="partner_exchange")
```

## Lifespan: start/stop all brokers

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await internal_broker.start()
    await external_broker.start()
    yield
    await external_broker.stop()
    await internal_broker.stop()
```

## DI considerations

- Use **separate dependency functions** per broker context (e.g. `get_internal_service`, `get_external_service`).
- Avoid sharing one service class that silently picks a broker — be explicit in constructor injection.
- Settings: one `RabbitMQSettings` class with prefixed env vars, or two dedicated settings classes:

```python
class InternalRabbitMQSettings(RabbitMQSettings):
    model_config = SettingsConfigDict(env_prefix="INTERNAL_RABBITMQ_")

class ExternalRabbitMQSettings(RabbitMQSettings):
    model_config = SettingsConfigDict(env_prefix="EXTERNAL_RABBITMQ_")
```

## Recommendation for this template

The default template uses **one broker** ([`src/app/infrastructure/messaging/rabbit.py`](../src/app/infrastructure/messaging/rabbit.py)). Add a second router only when a real integration requires it — multiple brokers increase operational and testing complexity.

## Related

- [faststream_fastapi_integration.md](faststream_fastapi_integration.md) — single-broker setup used in this repo
