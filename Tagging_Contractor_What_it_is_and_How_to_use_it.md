# Tagging_Contractor — What It Is and How to Use It

## Executive summary
Tagging_Contractor is the “semantic contract” layer for built‑environment perception. It defines what each tag means, how it should be used, and what evidence is required to extract it. The goal is to make tag creation, auditing, and extraction planning repeatable, scalable, and safe against silent regressions.

## Why this repo exists (justification)
- **Consistency:** A tag is not “just a label.” Without definitions, scope, and examples, different teams will use the same tag inconsistently.
- **Auditability:** Research and production need measurable standards. This repo provides audits and gates that prevent regressions.
- **Model readiness:** Extraction teams need clear evidence requirements (2D, 3D, computed, metadata, sensor) before any model work begins.
- **Scale:** Hundreds of tags require systematic coverage, not manual one‑offs. Tools in this repo batch‑generate, audit, and track progress.
- **Safety:** The “semantics gate” blocks releases when definitions or relation‑linked completeness would drop.

## What is in the registry
- Canonical tag registry: `core/trs-core/v0.2.8/registry/registry_v0.2.8.json`
- Semantics fields per tag: definitions, aliases, positive/negative examples, scope includes/excludes, extraction notes (2D and 3D)
- Auditing tools to verify completeness and usability

## How it was built (process overview)
1) **Audit current state** — `./bin/tc audit-tags`, `./bin/tc audit-semantics`, `./bin/tc audit-usability`.
2) **Generate missing semantics** — batch tools create conservative, deterministic semantics for missing fields.
3) **Apply to registry** — `tools/apply_seed_semantics.py` merges changes without overwriting non‑empty fields.
4) **Re‑audit and gate** — `./bin/tc audit-semantics` + `./bin/tc doctor --prod` enforce minimum coverage.
5) **Plan extraction** — `./bin/tc audit-extraction-plan` generates evidence maps and phased execution plans.
6) **Package handoff** — phase‑specific bundles for model or data teams.

## Key commands (local)
- `./bin/tc audit-tags` — core audit report
- `./bin/tc audit-semantics` — semantics completeness gate
- `./bin/tc audit-usability` — usability audit report
- `./bin/tc audit-usability-backlog` — ranked backlog for usability improvements
- `./bin/tc audit-extraction-plan` — evidence + model family extraction roadmap
- `./bin/tc doctor --prod` — enforces the semantics gate

## Reports to track status
- `reports/tag_status_overview.md` — summary table of counts and completeness targets
- `reports/tag_semantics_completeness_summary.md` — bucket totals (P0/P1/P2)
- `reports/tag_usability_summary.md` — usability stats (definitions, aliases, examples, scope, notes)
- `reports/tag_extraction_roadmap_summary.md` — extraction readiness by evidence type

## Handoff packages (zips)
These zip bundles contain execution plans, model tasks, and labeling checklists.

- **Phase 0 (image‑only):** `reports/handoff_phase0.zip`
- **Phase 1 (image + depth / 3D):** `reports/handoff_phase1.zip`
- **Phase 2 (computed metrics):** `reports/handoff_phase2_computed.zip`
- **Phase 3 (metadata‑reported):** `reports/handoff_phase3_metadata.zip`
- **Phase 4 (sensor‑required):** `reports/handoff_phase4_sensor.zip`

Each zip includes:
- Execution plan (CSV + MD)
- Model task list (where applicable)
- Labeling checklist (top 30 tags)
- README describing contents

## How to use this repo (recommended flow)
1) **Define / refine tags** in the registry.
2) **Run audits** to verify completeness and usability.
3) **Fill gaps** with batch generators (definitions, examples, scope, aliases, notes).
4) **Re‑audit** and ensure `./bin/tc doctor --prod` passes.
5) **Extractability planning** to decide which tags can be computed in each evidence phase.
6) **Hand off** phase bundles to modeling or data teams.

## Can students use this repo to operationalize tags?
Yes. The repo is designed so students can take a phase bundle and work on operationalizing tags into measurable signals. The extraction plans and checklists make this feasible without changing the registry itself.

## Region‑level tagging (important guidance)
Many tags are **local or regional** rather than global. This matters because interpretation changes if a tag describes:
- a **global property** (applies to the whole scene), or
- a **local property** (applies to specific regions, objects, or sub‑areas).

To avoid ambiguity, use extraction notes to clarify whether a tag is:
- **Global:** The property applies to the entire image/scene.
- **Regional:** The property appears in one or more sub‑regions; quantify area coverage.
- **Object‑level:** The property attaches to specific objects; count or detect instances.

Practical ways to represent locality for vision teams:
- **Region masks / segmentation** when precise area is needed.
- **Bounding boxes** for object‑level tags.
- **Area coverage** as a percent of image or percent of region (e.g., “biophilic stimuli cover ~20% of the image”).
- **Concentration descriptors** when distribution matters (e.g., “clustered on one wall” vs “distributed throughout”).

When a tag is ambiguous, make it explicit:
- Add a sentence to `extraction_notes_2d` / `extraction_notes_3d` describing **where** it applies.
- Include example positives with clear regional references.
- Specify acceptable proxies (e.g., “vegetation coverage” as a proxy for biophilic presence).

This is crucial for downstream models: a tag should not imply a single scalar if it actually encodes **spatial distribution**.

## Guidance for extraction readiness
- Respect evidence requirements; avoid inferring non‑visual tags from images.
- Apply abstain rules when evidence is insufficient.
- Validate each tag with a small labeled dataset before scaling.

## Notes
This repo is additive‑only; do not delete files. Archives are stored under `archive/`.
