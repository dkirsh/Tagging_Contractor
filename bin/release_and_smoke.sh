#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VER="vUNKNOWN"
if [[ -f "VERSION.txt" ]]; then
  VER="$(tr -d ' \r\n\t' < VERSION.txt)"
fi

./bin/tc release "$VER"
./bin/prod_smoke.sh
