FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml ./
COPY common ./common
COPY services ./services
COPY alembic.ini ./
COPY alembic ./alembic
COPY scripts/docker-entrypoint-migrate.sh /app/docker-entrypoint-migrate.sh
ENV UV_LINK_MODE=copy
RUN uv lock && uv sync --frozen \
    && chmod +x /app/docker-entrypoint-migrate.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/docker-entrypoint-migrate.sh"]
CMD ["uv", "run", "--package", "user-service", "python", "-m", "user_service.main"]
