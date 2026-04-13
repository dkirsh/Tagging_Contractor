#!/usr/bin/env bash
set -euo pipefail

on_error() {
  local exit_code=$?
  local line_no=${1:-unknown}
  local cmd=${2:-unknown}
  echo ""
  echo "========================================"
  echo "INSTALL FAILED"
  echo "========================================"
  echo "Exit code: ${exit_code}"
  echo "Line: ${line_no}"
  echo "Command: ${cmd}"
  echo ""
  echo "Debug hints:"
  echo "- Confirm Docker is installed and running: docker info"
  echo "- Confirm docker compose works: docker compose version"
  echo "- Re-run with: bash -x ./install_turnkey.sh"
  echo ""
  exit ${exit_code}
}
trap 'on_error $LINENO "$BASH_COMMAND"' ERR

log() {
  printf "[%s] %s
" "$(date '+%H:%M:%S')" "$*"
}

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

log "Tagging_Contractor Turnkey Installer"
log "Repo: $ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker not found. Install Docker Desktop and retry."
  exit 2
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: docker compose not available. Update Docker Desktop and retry."
  exit 2
fi

if [[ ! -f ".env" && -f ".env.example" ]]; then
  log "Creating .env from .env.example..."
  cp .env.example .env
fi

if [[ "${TC_INSTALL_ML_DEPS:-0}" == "1" ]]; then
  log "Building API image with ML deps (INSTALL_ML_DEPS=1)..."
  docker compose build --build-arg INSTALL_ML_DEPS=1 trs_api
else
  log "Skipping ML deps build (set TC_INSTALL_ML_DEPS=1 to enable)."
fi

log "Starting services..."
./bin/tc up

log "Running health checks..."
./bin/tc doctor --prod
./bin/tc health

log "Install complete."

cat <<'EOF'

AI/ML notes:
- If you already have a Gemini key, run:
    export GEMINI_API_KEY=YOUR_KEY
- Or OpenAI:
    export OPENAI_API_KEY=YOUR_KEY
- Optional ML deps are available in the API container. To enable them:
    TC_INSTALL_ML_DEPS=1 ./install_turnkey.sh

More help: see INSTALL_AI.md

Open UI:
  http://localhost:8501
Health check:
  http://localhost:8401/health

EOF
