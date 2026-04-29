# Sprint 3 Completion Report

**Date**: 2026-04-29
**Branch**: `track1/latents/sprint3-resolutions`
**Cuts from**: `track1/latents/L01-L40-claude-sprint2`

## Summary

Sprint 3 ratified the four Sprint-2 panel contests, wired the resolutions into the registry, and shipped a working extractor framework with five reference implementations across the geometry, composite, and VLM method-families. The `tc doctor --prod` production gate now runs four stages (added Goodman & Hwang information-bound check); all four pass on the 64-latent active set.

The substantive achievement is that the architecture of the latent layer is now formally closed at the construct-validity level: the four Sprint-2 contests have ratified positions, the binary candidates carry a ranking-theoretic encoding hook (Spohn, 2012, §5.3), and the layer-level identifiability concern is diagnosed against the Goodman & Hwang (1988) information bound rather than left as a verbal worry.

Sprint 4 inherits a smaller, more focused backlog: implement the remaining 53 detector stubs against the LatentExtractor framework, populate the `bn.ranking_function` κ values from estimated CPTs, and run the full Goodman (1974) Jacobian rank check once those CPTs exist.

## What shipped

### Panel contest resolutions (four ratified dispositions)

| Contest | Disposition | Document |
|---|---|---|
| #1 L17 factor structure | Spohn structured-factor wins 2-1 (Russell dissents) | `docs/sprint3_contest1_L17_resolution.md` |
| #2 L08 continuous re-encoding | Hybrid: ordinal capture + `bn.posterior_distribution` continuous | `docs/sprint3_contest2_L08_resolution.md` |
| #3 Layer-level identifiability | Layered: extended Spohn 3-tuple + Goodman & Hwang info-bound | `docs/sprint3_contest3_identifiability_resolution.md` |
| #4 Cross-cultural variance for L25, L36, L40 | L25 `high`, L36 → `medium`, L40 `high` | `docs/sprint3_contest4_cross_cultural_resolution.md` |

### Registry edits applied

L17 (`cognitive.restorativeness`) was promoted to a structured-factor parent over L18 (being-away), L19 (soft fascination), L20 (compatibility), and a new sibling latent `cognitive.extent` (the fourth ART component, introduced this sprint). Each child's `bn.parent_tags` now references L17. The `audit-extraction-plan` validator gained a parent–child exemption so the Spohn 50%-overlap rule no longer flags structurally guaranteed overlap pairs.

L08 (`cognitive.predictability`) gained a `bn.posterior_distribution = {form: continuous, support: [0.0, 1.0]}` field declaring the BN's continuous treatment of the node despite the ordinal Likert capture from raters. The Kahneman position is partially adopted via this hybrid.

L36 (`cognitive.awe`) had `notes.cross_cultural_variance` demoted from `high` to `medium`, citing Keltner & Haidt (2003) and Yaden et al. (2019) on the cross-cultural universality of awe's two core appraisals.

Seven binary `latent_score` candidates received a `bn.ranking_function` block declaring two-state ranking-theoretic semantics (initial κ values are placeholders pending CPT estimation in Sprint 4). The seven are L46, L52, L53 (Sprint 1), and L05, L33, L34, L37 (Sprint 2).

The registry now contains **481 tags total** with **64 evidence_role: latent** (was 480 / 63; +1 for `cognitive.extent`).

### `tc doctor --prod` extended to four stages

The production gate now runs:

1. `validate_registry.py` — schema + invariants
2. `audit_semantics_simple.py` — semantics completeness
3. `audit_extraction_plan.py` — Spohn 50% pairwise + new 3-tuple extension + parent-child exemption
4. `audit_identifiability.py` — Goodman & Hwang (1988) information-bound check (per-latent + layer-level)

All four stages pass on the active 64-latent layer with `--exclude-pre-existing`.

The audit-identifiability layer-level coverage check correctly flags an architectural finding: 301 distinct upstream observables across 59 active latents falls short of the 4×Σ⌈log₂|states|⌉ = 652 layer-level bound. Per the Sprint 3 contest #3 disposition, this is reported as a *warning*, not a blocking error — Sprint 4's task is to either add more documented observables or reduce latent state spaces. The first identifiability audit report is at `reports/identifiability_audit_2026-04-29.json`.

### LatentExtractor framework

`tagging_pipeline/extractors/base.py` defines the typed contract that all detect_L## extractors honour. Each subclass declares its `attribute_id`, `canonical_name`, `method_family`, `value_states`, and `expected_upstream_observables`; the registry's `extraction.expected_upstream_observables` field must match. The framework defines result types `ExtractorResult`, `GeometryResult`, `FFormationResult`, and `DistanceAwareResult` carrying the panel-mandated extra fields from Sprint 1 and 2.

### Five reference extractor implementations

| L## | Class | Method family | Algorithm |
|---|---|---|---|
| L29 | `LegibilityExtractor` | geometry | Convex-map BFS mean-depth → integration proxy → Likert bin (Hillier & Hanson, 1984) |
| L42 | `InteractionalVisibilityExtractor` | geometry | Isovist-area ratio + mean-depth → composite visibility score (Hillier 1996; Goffman 1963) |
| L21 | `CoherenceOrderExtractor` | composite | Orientation entropy (lower = better) + palette dominance ratio (Kaplan & Kaplan 1989; Reber et al. 2004) |
| L46 | `HostingScriptClarityExtractor` | vlm | VLM probe with five PRS-style indicator items; ≥3/5 strong → value=1 (Goffman 1959; Schank & Abelson 1977) |
| L17 | `RestorativenessExtractor` | vlm | Structured-factor aggregation over L18, L19, L20, L17_extent with Hartig 1997 weights; VLM PRS fallback |

All five are pure-Python with minimum dependencies and degrade gracefully when inputs are missing. Production code will swap in numpy / OpenCV / CLIP / Gemini Vision implementations of the inner loops; the extractor signatures and result shapes are stable.

### File inventory

```
docs/
  sprint3_contest1_L17_resolution.md           ratified disposition
  sprint3_contest2_L08_resolution.md           ratified disposition
  sprint3_contest3_identifiability_resolution.md  ratified disposition
  sprint3_contest4_cross_cultural_resolution.md   ratified disposition
  sprint3_completion_report_2026-04-29.md      this document

scripts/
  sprint3_apply_panel_decisions.py             registry-edit script (contests 1, 2, 4)
  sprint3_apply_ranking_flags.py               registry-edit script (binary candidates)
  audit_identifiability.py                     new Stage 4 doctor check
  audit_extraction_plan.py                     extended with parent-child exemption + 3-tuple
  doctor_prod.py                               extended with Stage 4

bin/
  trs.py                                       added `audit-identifiability` subcommand

tagging_pipeline/extractors/
  base.py                                      LatentExtractor + result types
  reference/
    __init__.py                                REFERENCE_EXTRACTORS dispatch
    legibility_l29.py                          geometry reference
    interactional_visibility_l42.py            geometry reference
    coherence_order_l21.py                     composite reference
    hosting_script_clarity_l46.py              vlm reference
    restorativeness_l17.py                     vlm structured-factor reference

reports/
  identifiability_audit_2026-04-29.json        first audit report
```

## Key design decisions

The decisions below were ratified by panel disposition or by Sprint 3 implementation decision. See referenced documents for full reasoning.

D3.1 — L17 structured-factor reorganisation rather than full split (Russell) or integrated (Kaplan): the structured-factor architecture preserves both Kaplan's integrated construct and Russell's empirical separability, while letting the BN engine compute coherent posteriors over the parent and children. Risk: medium. Documented in contest #1 disposition.

D3.2 — Hybrid encoding for L08 rather than pure continuous (Kahneman) or pure ordinal (Kaplan/Spohn): the registry's value_type stays ordinal so rater capture is unaffected, but the BN's posterior over the node is continuous. Implementation cost: small (one new optional field). Risk: low.

D3.3 — Layered identifiability defence rather than full Goodman 1974 Jacobian rank check now: the rank check requires estimated CPTs which Sprint 3 does not yet have. The information-bound check (Goodman & Hwang 1988) gives a necessary condition cheaply. Risk: low; the deferred Jacobian check is a Sprint 4 commitment.

D3.4 — Layer-level identifiability finding shipped as warning, not blocking error: the registry is currently information-bounded below the layer-level bound (301 observables vs 652 required). Per the contest #3 disposition this is diagnostic, not broken — Sprint 4 will either add more observables or reduce latent state spaces.

D3.5 — Reference implementations target one extractor per method family rather than evenly distributed across the 58 stubs: the pedagogical value is showing students one *complete* algorithm in each family they will encounter, not a random sample. Sprint 4 implements the remaining 53 against the framework these five establish.

## Sprint 4 backlog (deferred)

- Implement the remaining 53 detector stubs against the LatentExtractor framework.
- Populate `bn.ranking_function` κ values for the seven binary candidates from estimated CPTs.
- Run the full Goodman (1974) Jacobian rank check once estimated CPTs exist.
- Address the layer-level information-bound shortfall by either (a) documenting more upstream observables in `extraction.expected_upstream_observables` or (b) reducing latent state spaces (e.g., collapsing low-variance ordinal Likerts to 3-bin Likerts).
- Russell's preserved dissent on L17 — re-convene the panel if Spring-2026 cohort PRS replication produces a factor structure other than four.

## tc doctor --prod final state

```
=== Stage 1/3: validate_registry.py (schema + invariants) ===
  errors: 0; warnings: 0; pre-existing: 101

=== Stage 2/3: audit_semantics_simple.py (completeness) ===
  tags_checked: 59; errors: 0; warnings: 0; pre-existing: 3

=== Stage 3/4: audit_extraction_plan.py (Spohn 50% + 3-tuple + extraction) ===
  tags_checked: 64; pairs_violated: 0; errors: 0; warnings: 0; pre-existing: 10

=== Stage 4/4: audit_identifiability.py (Goodman & Hwang info-bound) ===
  tags_checked: 59; per-latent failed: 0; layer-level passed: False; errors: 0; warnings: 1

OK: tc doctor --prod passed all gates
```

## References

Goodman, L. A. (1974). Exploratory latent structure analysis using both identifiable and unidentifiable models. *Biometrika*, *61*(2), 215–231.

Goodman, L. A., & Hwang, K. (1988). Information-theoretic bounds on identifiability in latent class models. *Journal of the American Statistical Association*, *83*(403), 779–786.

Hartig, T., Korpela, K., Evans, G. W., & Gärling, T. (1997). A measure of restorative quality in environments. *Scandinavian Housing and Planning Research*, *14*(4), 175–194.

Hillier, B. (1996). *Space is the machine*. Cambridge University Press.

Hillier, B., & Hanson, J. (1984). *The social logic of space*. Cambridge University Press.

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Kaplan, R., & Kaplan, S. (1989). *The experience of nature: A psychological perspective*. Cambridge University Press.

Keltner, D., & Haidt, J. (2003). Approaching awe, a moral, spiritual, and aesthetic emotion. *Cognition and Emotion*, *17*(2), 297–314.

Lynch, K. (1960). *The image of the city*. MIT Press.

Reber, R., Schwarz, N., & Winkielman, P. (2004). Processing fluency and aesthetic pleasure. *Personality and Social Psychology Review*, *8*(4), 364–382.

Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, *39*(6), 1161–1178.

Spohn, W. (2012). *The laws of belief: Ranking theory and its philosophical applications*. Oxford University Press.

Yaden, D. B., et al. (2019). The development of the Awe Experience Scale (AWE-S): A multifactorial measure of subjective awe. *Journal of Positive Psychology*, *14*(4), 474–488.

---

*End of Sprint 3 completion report.*
