FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock README.md alembic.ini ./
COPY alembic ./alembic
COPY scripts ./scripts
COPY src ./src
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app/src
RUN uv sync --frozen --no-group dev \
    && chmod +x scripts/docker-entrypoint-migrate.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["scripts/docker-entrypoint-migrate.sh"]
CMD ["uv", "run", "python", "-m", "app.main"]
