#!/bin/bash
# Double-click (or run ./run.sh) to start the demo. No setup needed beyond Python.
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  echo "Creating virtual environment (first run only)..."
  python3 -m venv .venv
fi
.venv/bin/pip install -q fastapi uvicorn
echo "Starting demo at http://localhost:8000 ..."
.venv/bin/python -m uvicorn app:app --port 8000 --app-dir backend
