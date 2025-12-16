#!/bin/sh
# Start script for Railway deployment
# Uses PORT from environment or defaults to 8000

PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
WORKERS="${WORKERS:-1}"

echo "Starting server on $HOST:$PORT with $WORKERS workers"
exec uvicorn main:app --host "$HOST" --port "$PORT" --workers "$WORKERS"
