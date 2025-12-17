#!/usr/bin/env zsh
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v uvicorn >/dev/null 2>&1; then
  echo "uvicorn not found in PATH. Ensure the venv is active or run:"
  echo "  .venv/bin/python -m pip install fastapi uvicorn"
fi

exec .venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 8000
