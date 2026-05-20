#!/usr/bin/env bash
set -euo pipefail

# Start FastAPI backend on LAN-accessible host for PHC intranet usage.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT_DIR/.venv/bin/activate"
cd "$ROOT_DIR"
uvicorn interface.backend.main:app --host 0.0.0.0 --port 8000 --reload
