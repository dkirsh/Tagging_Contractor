Tagging_Contractor - Docker pip resilience pack (v2)

What this does
- Makes Docker builds more resilient on slow/spotty networks by setting pip retries + timeouts
  INSIDE the Docker build (still fully Dockerized).
- Keeps optional heavy ML deps (torch, transformers) OFF by default to avoid flaky core installs.

Files included
- Dockerfile.api
- Dockerfile.ui

How to apply (from repo root)
  cp Dockerfile.api Dockerfile.api.bak.$(date +%Y%m%d_%H%M%S)
  cp Dockerfile.ui  Dockerfile.ui.bak.$(date +%Y%m%d_%H%M%S)
  unzip -o TC_terminal_hardening_pack_v2_docker_pip_resilience.zip

Optional ML deps (only if needed)
  docker compose build --build-arg INSTALL_ML_DEPS=1 trs_api

Optional tuning
  docker compose build --build-arg PIP_DEFAULT_TIMEOUT=900 --build-arg PIP_RETRIES=15 trs_api
  docker compose build --build-arg PIP_DEFAULT_TIMEOUT=900 --build-arg PIP_RETRIES=15 trs_ui
