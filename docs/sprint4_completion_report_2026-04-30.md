# Sprint 4 Completion Report

**Date**: 2026-04-30
**Branch**: `track1/latents/sprint4-detectors`
**Cuts from**: `track1/latents/sprint3-resolutions`

## Summary

Sprint 4 closed the bulk of the detector-implementation backlog deferred from Sprint 3. The latent-extractor framework now has working reference implementations for thirteen of the fifty-nine latents — one per Sprint-2 subdomain plus the five from Sprint 3 — and algorithmic skeletons for the remaining forty-six. The synthetic-CPT machinery is in place, the full Goodman 1974 Jacobian rank identifiability check runs as a doctor stage 5 (warning-only), and the seven binary candidates have ranking-function κ values populated from the synthetic CPTs. One of the three deferred contests (top-level domain split) was resolved; the other two carry forward to Sprint 5 with explicit deferral documents.

The substantive achievement is that the latent layer now has *machinery* sufficient for a Spring 2026 cohort to populate without further architectural work. Cohort students inherit thirteen working detectors as exemplars of each method-family pattern, forty-six skeletons whose `extract()` methods they fill in, a typed result contract that downstream BN ingestion honours, and a five-stage `tc doctor --prod` gate that validates schema, semantics, extraction plan, identifiability bound, and Jacobian rank.

## What shipped

### Eight new working reference detectors (one per Sprint-2 subdomain)

| L## | Class | Family | Subdomain | Citation |
|---|---|---|---|---|
| L01 | PerceivedThreatExtractor | composite | safety_threat | Stamps 2014 prospect-refuge |
| L06 | PerceivedControlExtractor | composite | control_autonomy | Bandura 1977 + Karasek 1979 + Veitch & Gifford 1996 |
| L10 | VisualPrivacyExtractor | geometry | privacy_attention | Altman 1975 + Pedersen 1997 |
| L14 | CrowdingPressureExtractor | composite | crowding_density | Stokols 1972 + Hall 1966 + Evans 1979 |
| L25 | CozinessExtractor | vlm | aesthetic_affect | Kaplan & Kaplan 1989 + Wiking 2017 |
| L28 | ClutterLoadExtractor | composite | cognitive_load | Sweller 1988 + McMains & Kastner 2011 + Rosenholtz 2007 |
| L33 | CareSignalExtractor | vlm | social_signal | Wilson & Kelling 1982 + Sampson & Raudenbush 1999 |
| L38 | NoveltyExtractor | vlm | familiarity_novelty | Berlyne 1971 + Silvia 2005 |

`REFERENCE_EXTRACTORS` dict now has thirteen entries (5 Sprint-3 + 8 Sprint-4); `len() == 13` confirmed.

### Forty-six algorithmic skeletons

The remaining detectors are scaffolded as `LatentExtractor` subclasses with typed signatures, registry-aligned class attributes, four-to-six-line algorithm sketches in module docstrings, deduplicated APA citations, and `NotImplementedError("Sprint 5: ...")` raises in `extract()`. Method-family breakdown: composite=24, vlm=20, geometry=2.

`SKELETON_EXTRACTORS` dict maintains zero overlap with `REFERENCE_EXTRACTORS` so the doctor can report coverage (working vs scaffolded).

### Synthetic CPT generator

`scripts/sprint4_synthetic_cpts.py` produces `data/sprint4_synthetic_cpts.json` with 59 latent CPTs (55 marginal, 4 conditional for L17 children). Top-level `_warning` flags the file as SYNTHETIC for replacement with empirical CPTs once the Spring-2026 cohort ships its tagged 500-image set.

### Goodman 1974 Jacobian rank identifiability check

`scripts/audit_identifiability.py` extended with `goodman_1974_jacobian_rank_check()` and `--jacobian` flag. Engine: numpy/scipy when available, pure-Python power-iteration SVD fallback for portability. Sprint-4 run on the synthetic CPTs: 200 pairs checked, 0 rank-deficient. Treated as warning-only per the Sprint-3 contest #3 disposition. Report written to `reports/jacobian_audit_2026-04-30.json`.

### Ranking-function κ population

`scripts/sprint4_populate_kappa.py` derived κ_0 and κ_1 from synthetic-CPT marginals for the seven binary latent_score candidates (L05, L33, L34, L37, L46, L52, L53) per Spohn (2012) §5.3: κ_state = floor(-log_2 P(state)). With synthetic 0.5/0.5 marginals every κ defaults to 1; Sprint 5's empirical CPTs will produce informative asymmetric values.

### Splat-augmentation scaffolds

`scripts/track3/splat_to_hdri.py` (213 lines, ~1) and `scripts/track3/splat_to_materials.py` (268 lines) ship as scaffolds with full CLI, file I/O, library organisation, and stub-mode behaviour for zero-dependency smoke testing. Sprint 5 implementer fills in the SH-coefficient extraction and PBR-channel separation. Companion update: `t3_task1.html` Phase 2.5 added with the splat-scanning sub-phase, capture protocol, and Polycam / Luma / Scaniverse alternatives.

### Contest 3 — top-level domain split (Goffman/Bourdieu vs Spohn/Kahneman)

Hybrid disposition adopted: registry KEEPS `domain: "social"`, ADDS `notes.social_layer` field with enum `{interaction_order, social_organization, both}`. Per-latent assignment ratified by panel and applied via `scripts/sprint4_apply_contest3_social_layer.py`. Distribution: 9 interaction_order, 4 social_organization, 5 both. Full disposition at `docs/sprint4_contest3_top_level_domain_resolution.md`.

### Stage 5 doctor wrap

`tc doctor --prod` now runs five stages. Stage 5 is the Jacobian rank check, warning-only. Final state: all five stages pass with 0 errors on the active 64-latent layer; one warning carried over from Sprint 3 (layer-level info-bound) and Stage 5's per-pair report.

## What's deferred to Sprint 5

| Item | Why deferred | Sprint 5 work estimate |
|---|---|---|
| Contest #1 — L42b Goffman split | Session budget (panel vote not run) | Half-day: dispatch Goffman panel, ratify, register L42b |
| Contest #2 — L52 Kendon F-formation flag | Session budget | Half-day: dispatch Kendon panel, ratify, add `bn.f_formation_family` |
| 46 working detector implementations | Cohort Track 1 task | Whole-quarter cohort effort |
| Real (empirical) CPTs from cohort data | Awaits Spring 2026 cohort tagged data | Two days once data arrives |
| Real κ values from empirical CPTs | Awaits empirical CPTs | Hours once CPTs arrive |
| Layer-level info-bound shortfall (301 vs 652) | Sprint 3 architectural finding | One day to add upstream-observable annotations OR collapse low-variance Likerts |
| `notes.social_layer` extension to L01–L40 | Per Contest 3 disposition follow-up | Two hours of cataloguing |

## Final tc doctor state

```
=== Stage 1/5: validate_registry.py (schema + invariants) ===
  errors: 0; warnings: 0; pre-existing: 101

=== Stage 2/5: audit_semantics_simple.py (completeness) ===
  tags_checked: 59; errors: 0; warnings: 0; pre-existing: 3

=== Stage 3/5: audit_extraction_plan.py (Spohn 50% + 3-tuple + extraction) ===
  tags_checked: 64; pairs_violated: 0; errors: 0; warnings: 0; pre-existing: 10

=== Stage 4/5: audit_identifiability.py (Goodman & Hwang info-bound) ===
  tags_checked: 59; per-latent failed: 0; layer-level passed: False; errors: 0; warnings: 1

=== Stage 5/5: audit_identifiability.py --jacobian (Goodman 1974 rank) ===
  pairs_checked: 200; pairs_deficient: 0; engine: numpy/scipy; warning-only: True

OK: tc doctor --prod passed all five gates (Stage 5 Jacobian is warning-only)
```

## References

Bandura, A. (1977). Self-efficacy: Toward a unifying theory of behavioral change. *Psychological Review*, *84*(2), 191–215.

Bourdieu, P. (1984). *Distinction: A social critique of the judgement of taste*. Harvard University Press.

Goffman, E. (1959). *The presentation of self in everyday life*. Doubleday.

Goffman, E. (1963). *Behavior in public places*. Free Press.

Goffman, E. (1974). *Frame analysis: An essay on the organization of experience*. Harvard University Press.

Goodman, L. A. (1974). Exploratory latent structure analysis. *Biometrika*, *61*(2), 215–231.

Kerbl, B., Kopanas, G., Leimkühler, T., & Drettakis, G. (2023). 3D Gaussian Splatting for real-time radiance field rendering. *ACM Transactions on Graphics (SIGGRAPH)*, *42*(4).

Spohn, W. (2012). *The laws of belief: Ranking theory and its philosophical applications*. Oxford University Press.

Stamps, A. E. (2014). Some findings on prospect and refuge theory: I. *Perceptual and Motor Skills*, *119*(1), 290–311.

Wilson, J. Q., & Kelling, G. L. (1982). Broken windows. *Atlantic Monthly*, March, 29–38.

---

*End of Sprint 4 completion report.*
