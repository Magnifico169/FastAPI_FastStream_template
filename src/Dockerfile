FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

USER appuser

COPY --chown=appuser:appuser ../pyproject.toml ./
COPY --chown=appuser:appuser ../README.md ./

ENV UV_PROJECT_ENVIRONMENT=.uv_env
RUN uv sync

COPY --chown=appuser:appuser .. .

#CMD ["uv", "run", "python", "-m", "main"]
