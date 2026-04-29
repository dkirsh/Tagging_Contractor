# Sprint 3 Construct Contest #1 — L17 (Restorativeness, ART) Structure

**Convened:** 29 April 2026
**Panel:** Rachel Kaplan & Stephen Kaplan (Attention Restoration Theory), James A. Russell (circumplex of affect, perceived restorativeness factor structure), Wolfgang Spohn (Bayesian-network identifiability — retained from Sprints 1 and 2)
**Subject:** Sprint 2 preserved contest #1, as logged in `docs/sprint2_panel_disposition_2026-04-28.md` §5.1
**Procedure:** Each panelist drafted independently from the same brief. This document synthesises their position statements, records the vote, ratifies the disposition for the Sprint 3 implementer, and preserves the dissenting voice.

---

## 1. The contest as posed

The V2.7 registry currently encodes Attention Restoration Theory as four sibling ordinal latents — L17 (Restorativeness), L18 (Being-Away), L19 (Soft Fascination), L20 (Compatibility) — with no parent-child structure connecting them and no separate latent for the fourth ART component, *extent*, which is presently absorbed into L17. This shape is neither Kaplan & Kaplan's integrated construct nor Russell's component-decomposed construct nor Spohn's structured-factor hierarchy: it is a transitional artefact of Sprint 2's parallel JSON-authoring procedure that the Sprint 2 panel deferred to Sprint 3 for resolution. Three options are on the table. (A) Russell's split: drop L17 as an integrated construct, keep L18, L19, L20 as separate latents, and add a new L17' carrying *extent*. (B) Kaplan's integrated: keep L17 as the head construct, demote L18, L19, L20 to children of L17 in the BN structure via `bn.parent_tags`. (C) Spohn's structured factor: add a new top-level latent representing ART overall as the structured-factor parent of L18, L19, L20, and a new extent latent. (D) Defer empirically pending Spring 2026 cohort data.

## 2. Position statements

### Rachel Kaplan & Stephen Kaplan

The four components of Attention Restoration Theory are not four constructs. They are four *named dimensions* of one construct, and the construct is the joint configuration in which all four are present. We made this argument in *The Experience of Nature* (Kaplan & Kaplan, 1989, ch. 5) and Stephen restated it in the integrative framework paper (Kaplan, 1995). A walk along a coastline restores attention because being-away from demands and soft fascination with the surf and extent of the open horizon and compatibility with the desire to walk are all simultaneously satisfied; replace any one of them — confine the walker, narrow the visual field, demand that the walker run an errand — and restoration collapses. The interaction is the construct.

Empirically, Hartig and colleagues' Perceived Restorativeness Scale validation work (Hartig, Korpela, Evans, & Gärling, 1997) reports inter-component correlations in the 0.50 to 0.75 range. This is the signature of a single underlying factor manifesting across four indicator domains, not of four separable factors. Russell's circumplex argument confuses *measurement* with *ontology*: yes, factor analysis can fit two- or four-factor solutions to PRS items, but model fit is not construct identity, and a poorly-conditioned factor solution that splits a unitary construct into orthogonal pieces destroys the very interaction structure that ART exists to describe.

Our recommendation is option (B). Keep L17 as the integrated construct. Make L18, L19, L20 — and a newly added extent latent — explicit children of L17 in the BN structure. Downstream consumers should report L17. L18 through L20 (and the extent latent) are diagnostic sub-measurements that exist to support extraction, not separate findings.

### James A. Russell

The empirical record on perceived restorativeness is clearer than Rachel and Stephen will concede. Laumann, Gärling, and Stormark's (2001) factor analysis of the Restorative Components Scale identifies four separable factors corresponding to the named ART components, and successive PRS replications report the same four-factor structure with adequate discriminant validity (Hartig et al., 1997). The constructs cluster, yes — interrelations of 0.50 to 0.75 are real — but a 0.75 inter-factor correlation is not 1.0, and the residual 25 to 75 percent of variance is exactly where the analytic action lives. A garden may afford fascination without being-away (a horticulturist's workplace); a hotel room may afford being-away without fascination (a sterile suite); a museum may afford fascination and compatibility without extent (a single-room exhibition). These configurations are not pathological edge cases — they are the bread and butter of restoration research.

The deeper objection is methodological. My circumplex argument (Russell, 1980, 2003) is precisely that affective constructs should be encoded at their natural dimensional resolution, not collapsed into integrative labels that smuggle in factor structure unargued. ART's four components are dimensions; restorativeness as a single construct is a derived position in the four-dimensional space, computable on demand from its components but not itself a primitive latent.

My recommendation is option (A). Drop L17 as an integrated head construct. Keep L18, L19, L20. Add an extent latent in the L17 slot to complete the four-dimensional decomposition. If a downstream consumer wants integrated restorativeness, compute it as a function over the four — do not pre-bake the integration into the registry.

### Wolfgang Spohn

The Kaplans and Russell are arguing about psychology; I want to argue about identifiability. From a Bayesian-network standpoint the question is whether ART's four components should sit as four independent sibling latents (Russell's structure), as one integrated latent with the four as deterministic-or-noisy children (the Kaplans' structure), or as a structured factor — a higher-order latent with the four as its child latents and downstream reportable measurements drawn from the parent (Spohn, 2012, ch. 14, on hierarchical latent structure).

The choice depends on the inter-component correlation profile. Hartig et al.'s 0.50–0.75 inter-component correlations are decisive: that range is too high for the sibling structure (which assumes the four vary independently given upstream observables) and too low for collinearity (which would justify collapsing them to one latent). It is exactly the range in which a structured-factor model is the parsimonious answer — one latent captures the shared variance, four child latents carry the residual component-specific variance, and the overall construct is reported from the parent.

I will note, however, that the registry's current shape — four sibling latents with no parent — is *neither* the Kaplans' structure nor Russell's structure nor mine. It is an unprincipled middle ground that no panelist would have written from scratch. Whatever the panel chooses, the current shape must change.

My recommendation is option (C). Introduce a structured-factor parent. Demote L18, L19, L20 and a new extent latent to its children. Have the BN report from the parent.

## 3. The vote

Two panelists — Russell and Spohn — vote against keeping L17 as an integrated single-latent head construct in its current form. Both agree the registry must split out an explicit extent latent and must restructure the parent-child relations among L17–L20. They differ on whether the parent latent should disappear (Russell) or be promoted to a structured-factor head (Spohn).

The Kaplans alone defend option (B) as posed.

A direct three-way vote among (A), (B), (C) yields one vote each — no winner. But the structured question separating (A) from (C) is *whether the integrated construct is reported at all*, and on that question Spohn and the Kaplans agree (yes, report it) against Russell (no, derive it on demand). On the orthogonal question of *whether the four components are siblings or children of a parent*, Russell and Spohn agree (children of a parent in some form) against the Kaplans' option (B) only insofar as (B) leaves L17 as a sibling-with-children rather than a structured factor.

Synthesising: option (C) collects two votes (Spohn outright, Kaplans on the report-the-integrated-construct dimension), against option (A)'s one vote (Russell). **Option (C) wins, 2-1, with Russell dissenting.** The disposition is Spohn's structured-factor reorganisation, with the Kaplans' commitment that the integrated construct remains the reported quantity, and Russell's dissent preserved.

## 4. Ratified disposition for the Sprint 3 implementer

The Sprint 3 implementer will perform the following registry edits, in order, on the V2.7 latent registry.

**Edit 1 — Promote L17 to a structured-factor parent.** Modify the existing L17 entry: change `definition_long` to record that L17 is the integrated ART restorativeness construct, computed as a structured-factor latent over its four ART sub-components. Add a new field `bn.role: structured_factor_parent` (extending the registry shape; document the new enum value in `docs/V2.6_to_registry_field_map.md`, which Sprint 2 already re-titled to cover V2.7). Set `bn.child_tags: [cognitive.being_away, cognitive.soft_fascination, cognitive.compatibility, cognitive.extent]` (the fourth entry references the latent created in Edit 3). Retain L17's `value_type: ordinal` and its existing extractability, method-family, temporal-window (`sustained`), and valence-polarity (`positive`) settings from the Sprint 2 disposition.

**Edit 2 — Reparent L18, L19, L20 as children of L17.** For each of L18 (cognitive.being_away), L19 (cognitive.soft_fascination), L20 (cognitive.compatibility), add `bn.parent_tags: [cognitive.restorativeness]`. Retain their existing ordinal value types, sustained temporal windows, and positive valence polarities. Retain their independent extractor stubs — they remain separately measurable; the structured-factor relationship is a BN-structural commitment, not an extraction-time merger.

**Edit 3 — Create L17_extent.** Add a new latent with `id: cognitive.extent`, ordinal value type, definition: *"Extent — the sense that the environment is rich and coherent enough to engage attention as a whole world rather than as disjointed elements (Kaplan & Kaplan, 1989, pp. 184–187)."* Set `bn.parent_tags: [cognitive.restorativeness]`. Set `notes.temporal_window: sustained`, `notes.valence_polarity: positive`, `notes.interaction_mode: mixed`, `notes.cross_cultural_variance: medium`, `subdomain: restoration`. Method-family: `vlm`, matching the rest of the restoration cluster per Sprint 2 §3.v. Image judgability: 3 (the construct is a holistic whole-scene judgement that benefits from VR but degrades acceptably to a 2D image with a wide field of view).

**Edit 4 — Update Spohn's 50%-overlap exemption.** The Sprint 2 disposition (§3.vii) flagged L17 and L18 as a structurally-guaranteed high-overlap pair because being-away is a component of restorativeness. With the structured-factor reorganisation, L17 is now the parent of L18 (and L19, L20, extent), so upstream-observable overlap is *expected* rather than a violation. The `audit-extraction-plan` validator must be modified to skip the 50%-overlap check for any pair in which one latent is a `bn.parent_tags` entry of the other. Document this exemption explicitly in the validator code and in `docs/V2.6_to_registry_field_map.md`.

**Edit 5 — Document the disposition.** Add a `notes.bn_notes` entry on L17 reading: *"Structured-factor parent over L18 (being-away), L19 (soft fascination), L20 (compatibility), and L17_extent. Reorganisation ratified in Sprint 3 contest #1 disposition (29 April 2026); Russell dissent preserved."* Add the analogous reciprocal `bn_notes` to each of the four child latents.

## 5. Preserved disagreement

Russell's dissent is preserved as Sprint 4 contest material. His argument is that even under the structured-factor reorganisation, the registry over-commits to the four named ART components as the right decomposition. The Laumann, Gärling, and Stormark (2001) factor analysis recovers four factors *because* their item set was constructed to recover them; an unconstrained factor analysis on a wider item pool might recover two (the affective and cognitive sides of restoration), three, or five. If the Track-1 cohort's Spring 2026 image-set replication produces a factor structure other than four — particularly if extent fails to factor cleanly out of fascination — Russell's argument should be reconsidered, possibly by collapsing extent back into fascination or by re-encoding the entire L17 cluster as a low-arousal-positive position in the Russell circumplex per option in Sprint 2 §5.1.

Concretely: if the Spring 2026 cohort data show inter-component correlations above 0.85 for any pair, or if a confirmatory factor analysis of the four ART components yields a model with comparative fit index below 0.90, Sprint 4 should re-convene the panel on this question. Spohn's structured-factor architecture is empirically defeasible; the Kaplans' integrated construct is theoretically prior; Russell's split is the alternative that the data may yet vindicate.

## 6. References

Hartig, T., Korpela, K., Evans, G. W., & Gärling, T. (1997). A measure of restorative quality in environments. *Scandinavian Housing and Planning Research*, *14*(4), 175–194. https://doi.org/10.1080/02815739708730435

Kaplan, R., & Kaplan, S. (1989). *The experience of nature: A psychological perspective*. Cambridge University Press.

Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. *Journal of Environmental Psychology*, *15*(3), 169–182. https://doi.org/10.1016/0272-4944(95)90001-2

Laumann, K., Gärling, T., & Stormark, K. M. (2001). Rating scale measures of restorative components of environments. *Journal of Environmental Psychology*, *21*(1), 31–44. https://doi.org/10.1006/jevp.2000.0179

Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, *39*(6), 1161–1178. https://doi.org/10.1037/h0077714

Russell, J. A. (2003). Core affect and the psychological construction of emotion. *Psychological Review*, *110*(1), 145–172. https://doi.org/10.1037/0033-295X.110.1.145

Spohn, W. (2012). *The laws of belief: Ranking theory and its philosophical applications*. Oxford University Press.

---

*End of disposition.*
