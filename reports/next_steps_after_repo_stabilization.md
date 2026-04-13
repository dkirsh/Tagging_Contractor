# Next Steps After Other Repos Stabilize

This plan assumes other repos (model training, data pipelines, deployment) stabilize and can integrate extraction pipelines.

## 1) Integrate Phase 0 extraction
- Hook Phase 0 model tasks into the image processing pipeline.
- Validate top 10 tags with labeled data and log precision/recall.
- Lock thresholds + abstain rules for production.

## 2) Expand to Phase 1 (image + depth)
- Integrate depth/layout estimation.
- Validate spatial tags with multi‑view datasets.

## 3) Implement computed metrics (Phase 2)
- Implement metric modules and validate numeric outputs.
- Add metric confidence gating.

## 4) Metadata and sensor gating (Phase 3/4)
- Build metadata ingestion for surveys/annotations.
- Connect sensor pipelines for sound/smell/touch if available.

## 5) Add extraction QA gates
- Add automated audits: evidence type, abstain reasons, model versioning.
- Add a regression dashboard with drift/false positive checks.

## 6) Publish updated handoff bundles
- Refresh handoff zips with new model tasks and labeling guidance.

## 7) Expand evaluation
- Increase label coverage and add hard negatives.
- Add cross‑domain bias checks.
