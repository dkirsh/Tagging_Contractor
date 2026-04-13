# Status Dashboard

Last updated: 20260128_110942

## Semantics completeness (overall)
- P0: 0
- P1: 0
- P2: 424

## Usability targets
- Definition long: 424/424
- Aliases >=8: 424/424
- Examples pos>=3: 424/424
- Examples neg>=3: 424/424
- Scope includes>=3: 424/424
- Scope excludes>=3: 424/424
- Extraction notes 2D: 424/424
- Extraction notes 3D: 424/424

## Extraction phases
- phase_0_image_2d: 26
- phase_1_image_3d: 112
- phase_2_computed: 35
- phase_3_metadata: 21
- phase_4_sensor: 230

## Handoff bundles
- reports/handoff_phase0.zip
- reports/handoff_phase1.zip
- reports/handoff_phase2_computed.zip
- reports/handoff_phase3_metadata.zip
- reports/handoff_phase4_sensor.zip

## Nightly snapshot (optional)
Run this locally or via cron/launchd to keep reports fresh:

```
python3 tools/run_audit_snapshot.py --repo-root . --out-dir reports/snapshots --update-dashboard
```
