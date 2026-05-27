.PHONY: sync lock up down run

sync:
	uv sync

lock:
	uv lock

up:
	docker compose up --build

down:
	docker compose down

run:
	uv run --env PYTHONPATH=src python -m app.main
