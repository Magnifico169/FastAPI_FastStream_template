# FastStream Template

**FastAPI + FastStream (RabbitMQ) + Postgres** in a single process. An HTTP endpoint accepts JSON, publishes a domain message to RabbitMQ, and a FastStream subscriber persists it via `MessageService`.

## Flow

```text
POST /messages  →  MessageService.enqueue  →  RabbitMQ  →  message_handler  →  Postgres
```

## Project structure

```text
FastStreamTemplate/
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── alembic/
├── .env.example
└── src/app/
    ├── main.py                              # create_app(), lifespan
    ├── api/v1/messages.py                   # POST /messages
    ├── api/exception_handlers.py
    ├── consumers/message_handler.py         # RabbitMQ subscriber
    ├── services/message_service.py
    ├── domain/                                # models, DTOs, enums, exceptions
    └── infrastructure/
        ├── messaging/rabbit.py              # RabbitRouter, broker
        ├── settings/                          # RabbitMQ, Postgres
        └── persistence/                       # ORM, repository, session
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- RabbitMQ and Postgres (local or via Docker)

## Quick start

1. Copy environment file:

   ```bash
   cp .env.example .env
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Start Postgres, RabbitMQ, and the app:

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

   Check app logs for: `Message processed and saved: id=... text=hello`.

## Run locally (without Docker for the app)

Start infrastructure (e.g. `docker compose up rabbitmq postgres -d`), then set in `.env`:

```text
RABBITMQ_HOST=localhost
POSTGRES_HOST=localhost
```

Run migrations and the app:

```bash
uv run alembic upgrade head
uv run --env PYTHONPATH=src python -m app.main
```

Or via Makefile:

```bash
make run
```

## How to extend

1. **Add an HTTP endpoint** — add a route under `src/app/api/v1/` and use `MessageService` or `rabbit_broker.publish` from `infrastructure.messaging.rabbit`.
2. **Add a consumer** — add `@rabbit_router.subscriber(...)` in `src/app/consumers/` and import the module in `main.py`.
3. **Separate worker process** — split consumers into a standalone `faststream run` worker; see [docs/faststream_fastapi_integration.md](docs/faststream_fastapi_integration.md).

## Docker services

| Service    | Port        | Description              |
|------------|-------------|--------------------------|
| `rabbitmq` | 5672, 15672 | AMQP + management UI     |
| `postgres` | 5432        | Message persistence      |
| `app`      | 8000        | FastAPI application      |

## Makefile shortcuts

```bash
make sync   # uv sync
make up     # docker compose up --build
make down   # docker compose down
```
