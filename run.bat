@echo off
REM Double-click to start the demo. No setup needed beyond Python.
cd /d %~dp0
if not exist .venv (
  echo Creating virtual environment (first run only)...
  python -m venv .venv
)
.venv\Scripts\pip install -q fastapi uvicorn
echo Starting demo at http://localhost:8000 ...
.venv\Scripts\python -m uvicorn app:app --port 8000 --app-dir backend
