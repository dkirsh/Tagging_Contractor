#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VER="vUNKNOWN"
[[ -f "VERSION.txt" ]] && VER="$(tr -d ' \r\n\t' < VERSION.txt)"

echo "== PROD SMOKE =="
echo "Repo: $ROOT"
echo "Version: $VER"

mkdir -p _archive/_smoke
FP_FILE="_archive/_smoke/last_fingerprint.txt"

FP="$(
  ( \
    shasum -a 256 Dockerfile.api Dockerfile.ui docker-compose.yml VERSION.txt \
      backend/requirements.txt frontend_streamlit/requirements.txt 2>/dev/null || true; \
    find backend/app core frontend_streamlit -type f -print0 2>/dev/null \
      | LC_ALL=C sort -z \
      | xargs -0 shasum -a 256 2>/dev/null || true \
  ) | shasum -a 256 | awk '{print $1}'
)"

PREV_FP="$(cat "$FP_FILE" 2>/dev/null || true)"

ZIP="release_artifacts/Tagging_Contractor_${VER}.zip"
SHA="release_artifacts/Tagging_Contractor_${VER}_sha256.txt"
if [[ -f "$ZIP" && -f "$SHA" ]]; then
  export ZIP SHA
  python3 - <<'PY'
from pathlib import Path
import hashlib, os

zip_path = Path(os.environ["ZIP"])
sha_path = Path(os.environ["SHA"])
h = hashlib.sha256(zip_path.read_bytes()).hexdigest()

txt = sha_path.read_text(encoding="utf-8", errors="replace")
expected = None
for line in txt.splitlines():
    line = line.strip()
    if not line:
        continue
    tok = line.split()
    if len(tok) >= 1 and all(c in "0123456789abcdef" for c in tok[0].lower()) and len(tok[0]) == 64:
        expected = tok[0].lower()
        break

print("ZIP sha256:", h)
print("Expected :", expected)
if expected != h:
    raise SystemExit("NO-GO: sha256 mismatch")
print("OK: sha256 matches")
PY
else
  echo "NOTE: release artifact not verified (missing $ZIP or $SHA)"
fi

if [[ "${FORCE_REBUILD:-0}" = "1" || "$FP" != "$PREV_FP" ]]; then
  echo "Rebuild: YES (changed inputs or FORCE_REBUILD=1)"
  ./install.sh
  echo "$FP" > "$FP_FILE"
else
  echo "Rebuild: NO (inputs unchanged)"
  docker compose up -d --no-build
fi

./bin/tc doctor --prod
./bin/tc health
docker compose ps

if command -v curl >/dev/null 2>&1; then
  echo "API /version:"
  curl -sS "http://localhost:8401/version" || true
  echo
fi

echo "OK: prod smoke complete"
echo 'Open UI:     open "http://localhost:8501"'
echo 'Open health: open "http://localhost:8401/health"'
