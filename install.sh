#!/usr/bin/env bash
set -euo pipefail

# Robustly locate repo root whether this script lives in repo root or ./bin
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "${SCRIPT_DIR}/VERSION.txt" ]]; then
  ROOT="${SCRIPT_DIR}"
elif [[ -f "${SCRIPT_DIR}/../VERSION.txt" ]]; then
  ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
else
  ROOT="$(pwd)"
fi
cd "${ROOT}"

echo "== Tagging_Contractor Turnkey Installer =="
echo "Repo: ${ROOT}"
if [[ -f "VERSION.txt" ]]; then
  echo "Version: $(tr -d ' \r\n\t' < VERSION.txt)"
fi
echo

chmod +x ./bin/tc 2>/dev/null || true

# Up should be idempotent; it should build+start services as needed.
./bin/tc up

# Post-checks (fast and unambiguous)
./bin/tc doctor --prod
./bin/tc health

echo
echo 'Open UI:     open "http://localhost:8501"'
echo 'Open health: open "http://localhost:8401/health"'
