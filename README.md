# Сервис для обработки заказов

## Запуск в Docker

Скопируйте `.env.example` в `.env`, при необходимости отредактируйте значения. Затем:

```bash
docker compose up --build
```

## Сервисы:
* api-service: REST-шлюз (FastAPI)
* order-service: создание и управление заказами
* notification-service: обработка событий о заказах и отправка уведомлений

### `api_service`:

**HTTP endpoints**:
* `POST /orders` -- создание заказа через `order-service`
* `GET /orders` --- получение списка заказов для конкретного пользователя
* `GET /order` -- получение информации о статусе заказа

### `order_service`:

**FastStream endpoints**:
* `/orders` -- создание