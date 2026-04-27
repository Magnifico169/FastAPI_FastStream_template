# FastStream monorepo (user + store)

Репозиторий разделён на:

- `common` — Pydantic-схемы, domain-модели, настройки, общий доступ к БД (SQLAlchemy), брокер RabbitMQ.
- `services/user_service` — API и воркер для сценария **покупателя** (пользователи, заказы).
- `services/store_service` — API и воркер для **магазина** (каталог / склад, CRUD товаров).

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Установка зависимостей

Из корня репозитория:

```bash
uv sync
```

Сгенерировать зафиксированный lockfile (для `--frozen` в CI/Docker по желанию):

```bash
uv lock
```

## Локальный запуск

1. Скопируйте `.env.example` в `.env` и задайте `POSTGRES_PASSWORD`, `RABBITMQ_DEFAULT_PASS` и т.д.

2. Сервисы (порты: пользователь `8000`, магазин `8001`):

```bash
# User API
uv run --package user-service python -m user_service.main

# User worker
uv run --package user-service faststream run user_service.application.faststream_app:app

# Store API
uv run --package store-service python -m store_service.main

# Store worker
uv run --package store-service faststream run store_service.application.faststream_app:app
```

`PYTHONPATH` при работе из корня обычно не нужен: пакеты ставятся editable через `uv sync`.

## Docker

```bash
make up
# или: docker compose up --build
```

Сервисы: `user-api` (:8000), `user-worker`, `store-api` (:8001), `store-worker`, `postgres`, `rabbitmq`.
