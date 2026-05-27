# FastAPI + FastStream examples

Reference implementations and patterns for integrating FastAPI with FastStream.

| Example | Description |
|---------|-------------|
| [faststream_fastapi_integration.md](faststream_fastapi_integration.md) | Single-process `RabbitRouter`, shared DI, separate worker |
| [using_multiple_brokers.md](using_multiple_brokers.md) | Multiple RabbitMQ brokers/routers in one application |

The runnable template lives in [`src/app/`](../src/app/):

- **api/** — HTTP endpoints
- **services/** — application logic
- **consumers/** — FastStream subscribers
- **infrastructure/messaging/** — broker setup
