#!/bin/sh
set -eu
cd /app
export PYTHONPATH="/app/common/src${PYTHONPATH:+:$PYTHONPATH}"
uv run alembic -c /app/alembic.ini upgrade head
exec "$@"
