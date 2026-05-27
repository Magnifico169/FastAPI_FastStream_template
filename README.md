# FastStream Template

Minimal **FastAPI + FastStream (RabbitMQ)** example in a single process. An HTTP endpoint accepts JSON, publishes a message to RabbitMQ, and a FastStream subscriber processes it.

## Flow

```text
POST /messages  →  rabbit_broker.publish  →  RabbitMQ  →  @rabbit_router.subscriber
```

## Project structure

```text
FastStreamTemplate/
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── src/app/
    ├── main.py           # FastAPI app, broker lifecycle
    ├── messaging.py      # RabbitRouter, exchange, queue
    ├── settings.py       # RabbitMQ config
    ├── schemas.py        # Request/response models
    ├── api/routes.py     # POST /messages
    └── consumers/handler.py  # Message subscriber
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- RabbitMQ (local or via Docker)

## Quick start

1. Copy environment file:

   ```bash
   cp .env.example .env
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Start RabbitMQ and the app:

   ```bash
   docker compose up --build
   ```

4. Send a message:

   ```bash
   curl -X POST http://localhost:8000/messages \
     -H "Content-Type: application/json" \
     -d '{"text":"hello"}'
   ```

   Expected response: `202 Accepted` with `{"status":"processing"}`.

   Check app logs for: `Received message: hello`.

## Run locally (without Docker for the app)

Start RabbitMQ (e.g. via `docker compose up rabbitmq -d`), then set in `.env`:

```text
RABBITMQ_HOST=localhost
```

Run the app:

```bash
uv run --env PYTHONPATH=src python -m app.main
```

Or via Makefile:

```bash
make run
```

## How to extend

1. **Add an HTTP endpoint** — create a route in `src/app/api/routes.py` and publish via `rabbit_broker.publish`.
2. **Add a consumer** — add `@rabbit_router.subscriber(...)` in `src/app/consumers/` and import the module in `main.py`.
3. **Separate worker process** — for production you can split consumers into a standalone `faststream run` worker; see [docs/faststream_fastapi_integration.md](docs/faststream_fastapi_integration.md).

## Docker services

| Service   | Port  | Description              |
|-----------|-------|--------------------------|
| `rabbitmq`| 5672, 15672 | AMQP + management UI |
| `app`     | 8000  | FastAPI application      |

## Makefile shortcuts

```bash
make sync   # uv sync
make up     # docker compose up --build
make down   # docker compose down
```
