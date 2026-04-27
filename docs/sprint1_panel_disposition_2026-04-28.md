# Sprint 1 Architectural Panel Disposition

**Convened:** 28 April 2026
**Panel:** Goffman (interaction order), Hall (proxemics), Kendon (F-formation system), Hillier (space syntax), Spohn (ranking-theoretic / Bayesian-network role)
**Subject:** §2 architectural commitments of `SPRINT1_LATENT_INTEGRATION_PLAN.md` for L41–L58 (social-interaction latents)
**Procedure:** Each panelist drafted independently from the same brief, in isolation from the others. This document synthesises their critiques, records preserved disagreement, and ratifies the revised commitments that supersede §2 of the planning document.

---

## 1. Substantive convergences

Five independent voices converged, more strongly than I anticipated, on three claims.

**The ordinal-Likert default is wrong for at least a subset of the latents, and probably for most.** The panel converged from four directions: Goffman noted that several latents (L42, L43, L54, L57) have *optima* rather than monotonic intensities — a maximally-visible reading room is a failed library, because civil inattention (Goffman, 1963, pp. 83–88) requires the very arrangement that *permits* mutual sight while *forbidding* its full exercise. Kendon noted that the F-formation latents (L44, L48, L49, L52) are constitutively *categorical* (vis-à-vis, L-arrangement, side-by-side, semicircular, circular) and that pressing them into a 0–4 ordinal flattens the analytic distinction the F-formation tradition has insisted upon for fifty years. Hillier noted that the configurational latents (L41, L42, L54) have natural real-valued substrates in the topological measures of space syntax — integration, depth, isovist area — and that ordinal compression discards exactly the gradient that does the explanatory work in the natural-movement theorem (Hillier, 1996). Spohn, finally, gave the parametric argument: a 5-state CPT per latent commits the network to roughly $5^{|\text{pa}|}$ free parameters per latent's conditional table, which with even modest fan-in (three parents) means 125 parameters per latent and 2,250 across the eighteen — far more than the available tagged corpus can estimate. All four routes converge on the same disposition: ordinal Likert as a global default is indefensible.

**Several latents, as named, are configurational properties that cannot in principle be extracted from a single still image.** Hillier was the loudest voice here but not the only one. L41 (Chance-Encounter Potential) is the space-syntax construct par excellence: co-presence is a function of natural movement, and natural movement is a function of integration in the axial map of the *whole* spatial system, which is invisible in a photograph of one room. Hillier asks for L41's demotion from V2.6 Tier 2 to Tier 3, treating it "as the registry's position on the whole question." L42 (Interactional Visibility), L54 (Boundary Permeability), and L56 (Mingling Affordance) are all configurational at their core, with image-extractable proxies whose validity depends on the global configuration the image cannot show. Kendon and Goffman corroborated the general worry from their own traditions: Tier 1 → 2D presumes that an image of an empty room contains evidence about *gatherings*, when what it contains is evidence about *affordances for* gatherings — a different ontological category (*Frame Analysis*, Goffman, 1974, pp. 1–11).

**The 18 latents are framed as if culturally invariant, and they are not.** Hall pressed this hardest. Sociopetal/sociofugal arrangements vary cross-culturally in well-documented ways (Hall, 1966, ch. 10): North European and North American sociopetal seating favours face-to-face at personal-far distance; Mediterranean and Latin American arrangements tolerate closer angles and shorter distances; Japanese arrangements often substitute side-by-side around a shared focus. A sociopetal score trained on Western interiors will misread a Japanese tea room as sociofugal. The territorial constructs (L55) carry analogous cultural variance. Goffman registered the same point in different idiom: the cue language for L46 (hosting/service script) treats furniture as a proxy for role-bound performance, but service performances are deliberately desk-less in many cultural traditions.

## 2. Substantive divergences (preserved disagreement)

Each panelist, asked for one concrete recommendation, produced a *different* recommendation. They are mostly complementary, not contradictory, but they disagree on what the most important addition to the registry is. These disagreements are recorded here without forcing resolution.

| Panelist | Single recommendation |
|---|---|
| Goffman | Add a mandatory `interaction_mode` attribute to every latent with values `{focused, unfocused, mixed}`; require cue language and value-type to be justified against this mode. |
| Hall | Add a required `distance_zone_estimate` field to every extractor output for L42, L43, L44, L48, L49, L50, L51, L56, encoded against the Hall (1966) zones, with explicit Western-calibration warning. |
| Kendon | (a) Add `extraction_notes_2d.f_formation_geometry` sub-field with implied o-space centroid, radius, and predominant arrangement enum. (b) For L44, L48, L49, L52, replace ordinal Likert with categorical `value_type` keyed to the F-formation arrangement enum. |
| Hillier | Add `extractability.requires_floor_plan: bool` and `extractability.configurational_measure` enum {integration, depth, connectivity, isovist_area, none}. Set `requires_floor_plan: true` for L41, L42, L51, L54, L56, L58. Demote L41 from Tier 2 to Tier 3. |
| Spohn | Hard constraint: no two latents in L41–L58 may share more than 50% of their `compute_from` upstream observables. Pairs that violate must merge, re-specify, or defer. |

These five recommendations are independently defensible and substantially complementary. The disposition below adopts the union of those that can be implemented within Sprint 1 budget and defers the rest with explicit notes.

## 3. Disposition: revisions to §2 architectural commitments

The following revisions supersede §2 of `SPRINT1_LATENT_INTEGRATION_PLAN.md`. The revised plan will be re-versioned to v1.1.

**Adopted in full.**

(i) *Hillier's floor-plan and configurational-measure fields.* Add `extractability.requires_floor_plan: bool` (default false) and `extractability.configurational_measure: enum {integration, depth, connectivity, isovist_area, none}` (default `none`) to the registry schema as part of Sprint 1. Set `requires_floor_plan: true` for L41, L42, L51, L54, L56, L58. The schema extension is small; the alternative — silently representing un-extractable latents as if they were extractable — is the registry's most serious epistemic risk.

(ii) *Demotion of L41 from V2.6 Tier 2 to Tier 3.* Adopt Hillier's recommendation. Document the override of V2.6 in `notes.extraction_notes` with the citation to Hillier (1996, ch. 4) on the natural-movement theorem. This will be the first construct contest the students see in the handoff document.

(iii) *Spohn's 50% upstream-overlap constraint.* Adopt as a Phase D validator check: `audit-extraction-plan` will reject any registry state in which two `evidence_role: latent` tags share more than half of their `extraction.compute_from` references. Initial expected violations: {L43, L44} on chair-orientation observables; {L42, L54} on visibility observables. These pairs will be either re-specified to disjoint upstream sets or merged before PR.

(iv) *Goffman's `interaction_mode` attribute.* Add as a required field of `notes` (not the schema's `bn` block, since it carries no BN role) with values `{focused, unfocused, mixed}`. Each latent's cue language and value-type choice must cite this mode in its `extraction_notes_2d`. This is small overhead and prevents the Likert default from flattening the focused/unfocused distinction.

(v) *Hall's cross-cultural-variance flag.* Add `notes.cross_cultural_variance: enum {low, medium, high}` with default `medium` and explicit `high` for L43, L44, L48, L49, L55. Document the Western-calibration warning in `extraction_notes_2d` for each `high`-flagged latent. The flag is minimal in cost and signals to downstream model trainers that these extractor outputs should be treated as culturally indexed.

(vi) *Kendon's F-formation categorical type for L44, L48, L49.* Replace `value_type: ordinal` with `value_type: categorical` and define a `value_range` enum `{vis_a_vis, l_arrangement, side_by_side, semicircular, circular, none}`. Retain a *separate* `secondary_value_type: ordinal` field (a small schema extension) carrying the Likert "strength of affordance" judgment. This separates the *kind* of arrangement implied by the geometry from the *strength* with which the setting affords it — the distinction Kendon (1990, ch. 7) has insisted upon. Note: L52 (One-to-Many Presentation) is left as ordinal in this sprint, despite Kendon's argument that it is an F-formation variant — see preserved disagreement (3).

**Adopted with modification.**

(vii) *Splitting L42 (Interactional Visibility).* Goffman's argument that "interactional visibility" conflates exposure with civil-inattention support is correct in principle but a registry-level split would inflate the L41–L58 count and create renumbering dependencies. Compromise: retain L42 as a single tag, but explicitly document in `definition_long` and `scope_excludes` that L42 measures *opportunity to be seen*, not *quality of mutual visibility for civil inattention*; flag the latter as an explicit candidate for a future L42b in the Sprint 2 backlog.

(viii) *Hall's distance-zone estimate.* Add to the *extractor contract* documentation in Phase E (not as a registry field) for L42, L43, L44, L48, L49, L50, L51, L56. Each stub's docstring will require the eventual implementation to emit a `distance_zone_estimate` alongside its primary value. This is the right place for the requirement: it binds the implementer in Sprint 2 without inflating the registry schema.

(ix) *Kendon's F-formation geometry sub-field.* Add to the *extractor contract* for L44, L48, L49, L52, requiring the eventual implementation to emit `(o_space_centroid_xy, o_space_radius_px, predominant_arrangement)`. As above, this lives in the extractor stub docstring rather than in the registry schema, because it is a runtime output specification, not a tag-level meaning claim.

**Deferred to Sprint 2 (with explicit handoff note).**

(x) *Spohn's ranking-theoretic recoding for L46, L52, L53.* The registry does not currently support ranking-function value types, only probabilistic CPTs. Adding ranking-theoretic primitives is too large for Sprint 1. For L46, L52, L53, mark `value_type: latent_score` (binary) as originally proposed; add `notes.bn_notes` with the explicit recommendation that Sprint 2 evaluate ranking-theoretic encoding (Spohn, 2012, §5.3) once the BN integration sprint begins.

(xi) *Goffman's `interaction_order` vs `social_organization` top-level domain split.* Rejected for Sprint 1; "social" remains the single top-level domain. The split is conceptually defensible but would require renaming and re-keying the existing `social.<construct>` IDs across all consumer contracts. Logged as a Sprint 4 architectural question.

(xii) *Kendon's argument that L52 is an F-formation variant rather than ontologically distinct.* Rejected for Sprint 1: the V2.6 taxonomy has been shipped to students with L52 as a separate construct, and preserving the registry's traceability to that source matters more than the ontological purity of the F-formation tradition. Logged as a construct contest in the student handoff.

## 4. Effect on Phase plan

Phase A (field map) absorbs the new schema fields: `extractability.requires_floor_plan`, `extractability.configurational_measure`, `secondary_value_type`, `notes.interaction_mode`, `notes.cross_cultural_variance`. These are five new field paths to document.

Phase B (per-latent deliberation) gains five new questions per latent — focused/unfocused/mixed; cross-cultural variance bin; F-formation arrangement (where applicable); configurational-measure substrate (where applicable); upstream-observable inventory (in service of Spohn's 50% rule).

Phase D (validator gap-fill) gains the upstream-overlap check in `audit-extraction-plan`.

Phase E (extractor stubs) gains the docstring-level requirements for distance-zone and F-formation-geometry outputs.

The added scope is real but contained. The estimated sprint duration moves from 9 working days to 10–11.

## 5. Construct contests for the student handoff

The following four contests will be foregrounded in `LATENT_INTEGRATION_NOTES_2026-05-04.md` for the students to relitigate in Week 5:

1. *L41 demotion to Tier 3.* Hillier's argument is that L41 is the flagship configurational construct; the V2.6 taxonomy disagreed. The students should decide whether they accept the demotion or whether the project's commitment to image-only extraction warrants restoring it to Tier 2 with a documented limitation.

2. *L42 split.* Goffman's argument that exposure and civil-inattention support are distinct constructs deserves a student vote. The compromise (one tag, two scope notes) may not survive scrutiny.

3. *L52 as F-formation variant.* Kendon's ontological argument may matter to BN structure even if it does not matter to V2.6 traceability. Students should consider whether L52 should be folded into the L48/L49/L44 cluster.

4. *Cross-cultural variance flag deployment.* Hall's `high` flag is set for five latents on the panel's judgment. Students with relevant cultural-anthropology background should audit this list.

These four contests are the *first questions* the students will see, not the last. The handoff is structured around them deliberately — to invert the usual posture in which students inherit a finished system and discover its flaws by experience, replacing it with a posture in which they inherit a *contested* system and adjudicate its flaws by deliberation.

---

## 6. References

Goffman, E. (1959). *The presentation of self in everyday life*. Doubleday.

Goffman, E. (1963). *Behavior in public places: Notes on the social organization of gatherings*. Free Press.

Goffman, E. (1967). *Interaction ritual: Essays on face-to-face behavior*. Doubleday.

Goffman, E. (1971). *Relations in public: Microstudies of the public order*. Basic Books.

Goffman, E. (1974). *Frame analysis: An essay on the organization of experience*. Harvard University Press.

Goodman, L. A. (1974). Exploratory latent structure analysis using both identifiable and unidentifiable models. *Biometrika*, *61*(2), 215–231.

Hall, E. T. (1959). *The silent language*. Doubleday.

Hall, E. T. (1966). *The hidden dimension*. Doubleday.

Hillier, B. (1996). *Space is the machine: A configurational theory of architecture*. Cambridge University Press.

Hillier, B., & Hanson, J. (1984). *The social logic of space*. Cambridge University Press.

Kendon, A. (1976). The F-formation system: The spatial organization of social encounters. *Man-Environment Systems*, *6*(6), 291–296.

Kendon, A. (1990). *Conducting interaction: Patterns of behavior in focused encounters*. Cambridge University Press.

Spohn, W. (2012). *The laws of belief: Ranking theory and its philosophical applications*. Oxford University Press.

---

*End of disposition.*
