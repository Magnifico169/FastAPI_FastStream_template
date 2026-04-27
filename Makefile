.PHONY: sync lock up down

sync:
	uv sync

lock:
	uv lock

up:
	docker compose up --build

down:
	docker compose down
