# FastStream monorepo (user + store)

## What this project is

This repository is a **uv workspace** with three Python packages: shared **`common`** library and two services, **`user_service`** and **`store_service`**. Each service ships a **FastAPI** app and a **FastStream** (RabbitMQ) worker.

The flow is: HTTP handlers accept JSON, publish domain messages to **RabbitMQ** queues, and **FastStream** subscribers perform database work (Postgres via **SQLAlchemy**). The **user** side covers registration and orders; the **store** side maintains product inventory. Both use the same database and shared schemas in `common`.

## Project structure (schematic)

```text
FastStreamTemplate/
|-- pyproject.toml
|-- uv.lock
|-- alembic.ini
|-- Makefile
|-- docker-compose.yml
|-- .env.example
|-- .env                    # you create: copy from .env.example
|-- common/
|   +-- pyproject.toml
|   +-- src/common/
|       |-- domain/         # Pydantic domain types (User, Order, Product, …)
|       |-- schemas/        # API / message schemas
|       |-- persistence/    # SQLAlchemy session, base repository, ORM models
|       +-- messaging/      # Rabbit broker, exchanges / queues, FastStream router
|-- services/
|   |-- user_service/
|   |   |-- pyproject.toml
|   |   +-- src/user_service/
|   |       |-- main.py                    # FastAPI, port 8000
|   |       |-- application/
|   |       |   +-- faststream_app.py     # FastStream app (worker)
|   |       |-- api/v1/                   # user_routes, order_routes
|   |       +-- consumers/                 # Rabbit subscribers (e.g. customer_routes)
|   +-- store_service/
|       |-- pyproject.toml
|       +-- src/store_service/
|           |-- main.py                    # FastAPI, port 8001
|           |-- application/
|           |   +-- faststream_app.py
|           +-- api/v1/                    # inventory_routes
|           +-- consumers/
+-- alembic/
    +-- env.py
```

(Exact file counts can vary; this matches the main layout.)

## What you need to run

- **Python** 3.12+
- **uv** — [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- **Postgres** and **RabbitMQ** — running locally, in Docker, or remote, as long as your `.env` can reach them

## Environment (`.env`)

1. From the repository root, copy the example file:

   ```bash
   cp .env.example .env
   ```

2. Set at least the secrets and hosts your deployment needs. The template defines:

   | Area | Variables (from `.env.example`) |
   |------|----------------------------------|
   | Postgres | `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DRIVER` |
   | RabbitMQ (broker URL pieces) | `RABBITMQ_SCHEME`, `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `RABBITMQ_VHOST` |
   | Docker Rabbit image | `RABBITMQ_DEFAULT_USER`, `RABBITMQ_DEFAULT_PASS` |

3. If you use **Docker Compose** for Postgres but run **apps on the host**, map the published DB port: set `POSTGRES_HOST=localhost` and `POSTGRES_PORT=5433` (see `docker-compose.yml`: `5433:5432`).

## Install dependencies

```bash
uv sync
```

Refresh the lockfile when dependencies change (optional for local dev; useful for frozen installs):

```bash
uv lock
```

Shortcuts: `make sync`, `make lock` (see `Makefile`).

## Database migrations

With Postgres up and environment variables loaded:

```bash
uv run alembic upgrade head
```

## How to start (local)

RabbitMQ and Postgres must be reachable. You usually do **not** need `PYTHONPATH` after `uv sync` (workspace packages are installed in editable mode).

| Role | Command |
|------|--------|
| User API (**8000**) | `uv run --package user-service python -m user_service.main` |
| User worker | `uv run --package user-service faststream run user_service.application.faststream_app:app` |
| Store API (**8001**) | `uv run --package store-service python -m store_service.main` |
| Store worker | `uv run --package store-service faststream run store_service.application.faststream_app:app` |

For end-to-end behaviour, start **both** APIs and **both** workers, plus the broker and database.

## Docker

```bash
make up
# or: docker compose up --build
```

| Compose service | Notes |
|-----------------|--------|
| `postgres` | Host port **5433** → container 5432 |
| `rabbitmq` | **5672** (AMQP), **15672** (management UI) |
| `user-api` | **8000** (`/health` for health checks) |
| `user-worker` | User FastStream app |
| `store-api` | **8001** |
| `store-worker` | Store FastStream app |

`user-worker`, `store-api`, and `store-worker` are ordered after a healthy `user-api` / Rabbit where `docker-compose.yml` specifies it.

Stop:

```bash
make down
# or: docker compose down
```
