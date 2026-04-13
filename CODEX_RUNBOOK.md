# Codex Runbook — Tagging_Contractor

## Standard startup
1) Run: ./bin/prod_smoke.sh
2) If NO-GO:
   - read the failing section
   - propose minimal fix consistent with AGENTS.md (no deletions; archive instead)
   - apply fix
   - rerun ./bin/prod_smoke.sh

## Quick checks
- docker compose ps
- curl -sS http://localhost:8401/health
- curl -sS http://localhost:8401/version
