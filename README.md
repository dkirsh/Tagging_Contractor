# Terminal hardening pack

This pack adds paste-proof, one-command workflows and makes ML dependencies optional by default.

## Install & verify (one command)
./bin/prod_smoke.sh

## Release & verify (one command)
./bin/release_and_smoke.sh

## Optional ML deps
docker compose build --build-arg INSTALL_ML_DEPS=1 trs_api

## Extraction Handoff Bundles

- Phase 0 (image-only): `reports/handoff_phase0.zip`
- Phase 1 (image + depth/3D): `reports/handoff_phase1.zip`
- Phase 2 (computed metrics): `reports/handoff_phase2_computed.zip`
- Phase 3 (metadata-reported): `reports/handoff_phase3_metadata.zip`
- Phase 4 (sensor-required): `reports/handoff_phase4_sensor.zip`

See `Tagging_Contractor_What_it_is_and_How_to_use_it.md` for usage guidance.
