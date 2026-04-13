# Extraction Decisions Log (Simulated Panel Context)

This log records decisions that benefit from expert review. Each decision includes a simulated panel note for traceability.

## Decision 001 — Pilot precision target and recall floor
**Decision:** Sprint 1 success requires Precision >= 0.80 with Recall >= 0.30 for top 10 phase_0 tags.
**Rationale:** Precision-first to avoid false positives; recall floor ensures non-trivial coverage.
**Simulated panel note:** CV/ML recommended precision-first; QA recommended abstain thresholds.
**Review risk:** May be too strict for early texture/material detectors.

## Decision 002 — Evidence gating by phase
**Decision:** Hard gating by evidence type: image_2d, image_3d, computed, metadata, sensor.
**Rationale:** Prevent invalid inference from images alone.
**Simulated panel note:** Lighting, acoustics, and HCI experts flagged strict non-visual requirements.
**Review risk:** Over-restricts tags if metadata sources are delayed.

## Decision 003 — Phase 0 tag feasibility
**Decision:** Treat 26 phase_0 tags as image_2d feasible using baseline CV models.
**Rationale:** Derived from extractability matrix and execution plan.
**Simulated panel note:** Architecture expert warned about open_plan; CV suggested abstain rules.
**Review risk:** Some spatial tags may require depth.

## Decision 004 — Thresholding rules
**Decision:** Use heuristic thresholds (e.g., material area >= 0.20) with abstain rules.
**Rationale:** Provide initial operational cutoffs for pilots.
**Simulated panel note:** CV recommended per-tag calibration; QA flagged risk of bias.
**Review risk:** Must be tuned with labeled data.

## Decision 005 — Computed metrics and photometric tags
**Decision:** No image-only inference for computed metrics; require computed pipelines.
**Rationale:** Panel consensus on calibration needs.
**Simulated panel note:** Lighting expert stressed measurement requirements.
**Review risk:** If calibration unavailable, extraction delayed.

## Decision 006 — Affective/cognitive tags
**Decision:** Metadata only; abstain for image-only.
**Rationale:** Bias and validity concerns.
**Simulated panel note:** HCI expert emphasized user reports.
**Review risk:** Requires survey infrastructure.

## Decision 007 — Sensor-dependent tags
**Decision:** Sound/smell/touch require sensor input; abstain otherwise.
**Rationale:** Non-visual domain.
**Simulated panel note:** Acoustics and tactile experts agreed on hard block.
**Review risk:** Must ensure sensors are available in data pipeline.
