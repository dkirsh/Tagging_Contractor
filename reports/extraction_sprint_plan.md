# Extraction Sprint Plan (Simulated Panel-Aligned)

## Context
This plan sequences extraction implementation by evidence type and model feasibility. It is aligned to the simulated expert panel guidance and the generated execution plans.

## Sprint 0 (Complete) — Semantics & Extractability Foundation
- Completed: semantics completeness, usability audit, extractability matrix, phase 0/1 plans, model map.
- Outputs:
  - `reports/tag_phase0_execution_plan.*`
  - `reports/tag_phase1_execution_plan.*`
  - `reports/tag_extraction_backlog.*`
  - `reports/model_capability_map.*`

## Sprint 1 — Phase 0 Image-Only Pilot (Image 2D)
**Goal:** Implement extraction for phase_0_image_2d tags and validate with a small labeled set.

**Inputs:**
- `reports/tag_phase0_execution_plan.*`
- `reports/tag_phase0_model_tasks.*`
- `reports/tag_extraction_labeling_checklist.*`

**Tasks:**
1) Build baseline pipelines per model family (object detection, materials, texture, color, defects, style).
2) Apply abstain rules and thresholds per tag.
3) Label pilot dataset (100–200 images per top tag).
4) Evaluate with precision-first thresholds.

**Success Criteria:**
- Precision >= 0.80 for top 10 tags at recall >= 0.30.
- Abstain rate < 35% on clean images.

## Sprint 2 — Phase 1 Image-3D (Depth/Layout)
**Goal:** Implement extraction for phase_1_image_3d tags using depth/layout estimation.

**Inputs:**
- `reports/tag_phase1_execution_plan.*`
- `reports/tag_phase1_model_tasks.*`
- `reports/tag_phase1_labeling_checklist.*`

**Tasks:**
1) Build depth/layout estimation pipeline.
2) Implement affordance/spatial metrics (isovist, enclosure, openness proxies).
3) Validate with multi-view/depth datasets.

**Success Criteria:**
- Metric correlation >= 0.6 with labeled or computed ground truth.
- Abstain on missing geometry.

## Sprint 3 — Phase 2 Computed Metrics
**Goal:** Deliver computed metrics from geometry/appearance pipelines.

**Inputs:**
- `reports/tag_phase_2_computed_execution_plan.*`
- `reports/tag_phase_2_computed_labeling_checklist.*`

**Tasks:**
1) Implement metric computation modules.
2) Validate numeric outputs with test scenes.

**Success Criteria:**
- MAE below agreed bounds; high confidence gating.

## Sprint 4 — Phase 3 Metadata-Reported Tags
**Goal:** Build metadata ingestion and evidence gating.

**Inputs:**
- `reports/tag_phase_3_metadata_execution_plan.*`
- `reports/tag_phase_3_metadata_labeling_checklist.*`

**Tasks:**
1) Metadata schemas for surveys, annotations, provenance.
2) Evidence validation rules.

**Success Criteria:**
- 100% tags in this phase must be metadata-derived (no image inference).

## Sprint 5 — Phase 4 Sensor-Required Tags
**Goal:** Integrate sensor pipelines (audio/tactile/olfactory).

**Inputs:**
- `reports/tag_phase_4_sensor_execution_plan.*`
- `reports/tag_phase_4_sensor_labeling_checklist.*`

**Tasks:**
1) Sensor data ingestion.
2) Measurement normalization and thresholding.

**Success Criteria:**
- Sensor validation tests pass; no image-only inference.
