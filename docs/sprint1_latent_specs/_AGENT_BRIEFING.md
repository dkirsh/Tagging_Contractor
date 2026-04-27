# Phase B Sub-Agent Briefing — Per-Latent Spec Authoring

*This document is read by every Phase B sub-agent before authoring a per-latent spec. It contains the procedural and substantive constraints established by the architectural panel of 28 April 2026. Spec authors who deviate from these constraints must justify the deviation in writing within their spec's `## Engineer pass — deviations from briefing` section.*

---

## 1. The procedure you will follow

You are authoring a single per-latent specification for one of L41–L58 (the social-interaction latents from Environment–Cognition Taxonomy V2.6). Your output is a single Markdown file at `docs/sprint1_latent_specs/L##.md` (where ## is the L-number you have been assigned).

You will execute three internal passes, in sequence, with explicit context resets between them. The procedure substitutes for what would otherwise be three independent expert sub-agents, and it preserves the procedural discipline of a Driver/Engineer/Blind-reader trio at the cost of full role-independence.

**Pass 1 — Driver pass (semantics).** Acting as the Driver:
- Write the `definition_short` (≤ 90 chars) and `definition_long` (≥ 200 chars) for this latent.
- Write `aliases` (≥ 3), `examples_positive` (≥ 6), `examples_negative` (≥ 4).
- Write `scope_includes` (≥ 3) and `scope_excludes` (≥ 3).
- Write `factor_associations` (the V2.6 indicator structure, if known) and `related_tags` (≥ 2 sibling tags from L41–L58).
- Cite at least one primary literature reference inline in `definition_long` using APA in-text format.

**Pass 2 — Engineer pass (extractability, method, BN role).** Acting as the Engineer:
- Verify the panel-mandated values for `value_type`, `extractability`, `bn`, and the five new fields. If your assigned latent's V2.6 cues conflict with the panel constraints, document the conflict in a `## Engineer pass — deviations from briefing` section.
- Write `extraction_notes_2d` (≥ 200 chars) and `extraction_notes_3d` (≥ 200 chars). Critical rule: replace V2.6 cue language ("warm lighting", "open thresholds") with available-upstream-observable language ("upstream tag `lighting.warmth_index`", "upstream tag `affordance.threshold_count`"). If you do not know whether an upstream observable exists, write what you would expect it to be called — Phase D will reconcile.
- Populate `bn.parent_tags` with the upstream observable tag IDs your extraction depends on. This is the field on which the Spohn 50%-overlap rule operates.
- For L46, L52, L53, write a `bn_notes` paragraph flagging the Sprint-2 ranking-theoretic recoding recommendation.
- For L41 specifically, document the V2.6 Tier 2 → Tier 3 override in `extraction_notes` with an inline citation to Hillier (1996, ch. 4) on the natural-movement theorem.

**Pass 3 — Blind-reader pass (construct validity check).** Acting as the Blind-reader:
- Forget — explicitly, in writing — your own `definition_short` and `definition_long`. State at the top of the section: *"Working only from the examples I wrote in Pass 1, can I reverse-engineer the construct?"*
- Read your own `examples_positive` and `examples_negative` only. Write what construct you infer.
- Compare your inferred construct to your Pass 1 definition. If they diverge in any meaningful way, revise the **examples** (not the definition) until a re-blind-read recovers the definition. Document each iteration in the spec's `## Blind-reader pass — iteration log` section.

You are explicitly NOT to attempt to reconcile away genuine construct ambiguity. If after three blind-read iterations the examples still under-specify the construct, mark the spec with `status: "proposed"` rather than `status: "active"` and document the unresolved ambiguity in `notes.validation_notes`.

---

## 2. Required spec file structure

Your output file MUST follow this exact structure (use the headings verbatim so Phase C can parse it):

```markdown
# L## — <V2.6 Name> (<canonical_name>)

*Authored by Claude Phase-B sub-agent, 2026-04-28*
*V2.6 Tier: <N>; final Tier: <N> (justify if overridden)*
*Subdomain: <subdomain>*
*Interaction mode: <focused/unfocused/mixed>*
*Cross-cultural variance: <low/medium/high>*

## Driver pass — semantics

### definition_short
<≤ 90 chars>

### definition_long
<≥ 200 chars, with inline APA citation>

### aliases
- <alias 1>
- <alias 2>
- <alias 3>
- (more if relevant)

### examples_positive (≥ 6)
1. <example 1, ≥ 1 sentence describing a recognisable scene>
2. ...

### examples_negative (≥ 4)
1. <example 1, a scene that LOOKS like the construct but isn't>
2. ...

### scope_includes (≥ 3)
- <boundary case included>

### scope_excludes (≥ 3)
- <boundary case excluded>

### factor_associations
- <factor ID or description from V2.6 Latent_Indicators sheet>

### related_tags (≥ 2 siblings from L41–L58)
- <related tag canonical_name>

### inverse_of
<canonical_name of opposing construct, or "null">

## Engineer pass — extractability, method, BN

### value_type assignment
<value_type per panel: ordinal | categorical | latent_score>
<value_range>
<unit>
<secondary_value_type if categorical: ordinal/likert_0_4>

### extractability
- from_2d: <"yes" | "partial" | "no">
- from_3d_vr: <...>
- monocular_3d_approx: <...>
- requires_floor_plan: <true | false>
- configurational_measure: <integration | depth | connectivity | isovist_area | none>
- region_support: <true | false>

### extraction
- compute_from: <string description of input substrate>
- method_family: <geometry | composite | vlm>
- primary_extractors: []  (Sprint 2 will populate)
- recipe_id: null

### extraction_notes_2d
<≥ 200 chars, in available-upstream-observable language not raw V2.6 cue language>

### extraction_notes_3d
<≥ 200 chars>

### bn
- evidence_role: latent
- demand_state: optional
- consumable: true
- parent_tags: [<list of upstream observable tag IDs; Spohn 50% overlap rule applies here>]
- child_tags: []

### bn_notes
<required for L46, L52, L53; optional otherwise. For ranking-theoretic flag, see briefing.>

## Engineer pass — deviations from briefing
<empty if no deviations; else one paragraph per deviation>

## Blind-reader pass — iteration log

### Iteration 1
**Inferred construct from examples alone**: <what you guessed without looking at the definition>
**Comparison to Pass 1 definition**: <converged | minor wording divergence | major divergence>
**Action taken**: <none | revised examples | revised scope_includes/excludes>

### Iteration 2 (if needed)
...

### Final convergence status
<converged | unresolved — mark spec status: "proposed">

## Literature

### key_refs (≥ 1 with full APA, DOI where available)
1. <APA citation>

### search_terms (≥ 5)
- <term>

## Notes

### interaction_mode
<focused | unfocused | mixed>

### cross_cultural_variance
<low | medium | high>

### extraction_notes
<free form; document any V2.6 Tier override here>

### validation_notes
<populated by Phase F.5; leave as "Pending Phase F.5 panel vote">

### l_number
L##
```

---

## 3. Substantive constraints from the panel

Read `docs/sprint1_panel_disposition_2026-04-28.md` in full before writing. The most consequential constraints:

- **L44, L48, L49** receive `value_type: categorical` with enum `[vis_a_vis, l_arrangement, side_by_side, semicircular, circular, none]`, plus `secondary_value_type: ordinal` carrying the affordance-strength Likert. Do NOT default these to ordinal Likert.
- **L46, L52, L53** receive `value_type: latent_score` (binary). Add Sprint-2 ranking-theoretic flag in `bn_notes`.
- **L41, L42, L51, L54, L56, L58** receive `requires_floor_plan: true`. L41 is additionally Tier-overridden to Tier 3.
- **L43, L44, L48, L49, L55** receive `cross_cultural_variance: high` with explicit Western-calibration warning in `extraction_notes_2d`.
- **L42** is NOT split in this sprint despite Goffman's argument. Document the exposure-vs-civil-inattention distinction in `scope_excludes`.

---

## 4. Required reading before you start

1. `docs/V2.6_to_registry_field_map.md` — for field paths and registry conventions
2. `docs/sprint1_panel_disposition_2026-04-28.md` — for panel reasoning behind constraints
3. The exemplar tags `affect.cozy` and `affordance.isovist_area` in `core/trs-core/v0.2.8/registry/registry_v0.2.8.json` — for tone, length, and structural conventions

---

*End of briefing.*
