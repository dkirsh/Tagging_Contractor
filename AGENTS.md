# Tagging_Contractor — Agent Contract

## Golden command (single truth)
- ./bin/prod_smoke.sh

## What “GO” means
GO requires:
- ./bin/prod_smoke.sh completes successfully
- ./bin/tc doctor --prod => GO
- ./bin/tc health => GO
- curl http://localhost:8401/version returns JSON

## Safety / governance
- No deletions. If replacement is necessary, archive the old file under _archive/<timestamp>/...
- Do not bypass release gates. Fix root causes and rerun.
- Prefer minimal, reversible changes.

## Allowed commands (non-destructive)
- ./bin/prod_smoke.sh
- ./install.sh
- ./bin/tc doctor --prod
- ./bin/tc health
- docker compose ps / up / down / build
- curl to localhost:8401/ and localhost:8501/

## Forbidden without explicit permission
- rm, git reset --hard, git clean -fdx, deleting archives, wiping folders
