#!/usr/bin/env bash
set -euo pipefail

# Start React app for local network testing from any browser on PHC LAN.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/interface/frontend/web"

if [ ! -d node_modules ]; then
  npm install
fi

npm run dev -- --host 0.0.0.0 --port 5173
