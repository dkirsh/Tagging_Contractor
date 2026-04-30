# Sprint 4 — Contests #1 and #2 deferred to Sprint 5

*Filed: 2026-04-30 by Claude (Cowork session)*
*Status: **DEFERRED** — original contest material from Sprint 1 carries forward intact.*

Sprint 4 was scoped to resolve three deferred contests from Sprint 1 + Sprint 2. Of the three, only Contest #3 (top-level domain split) reached a panel vote within the Sprint 4 session budget. The other two carry forward to Sprint 5 with their original disposition material intact.

## Contest #1 — L42b Goffman split (deferred)

**Original contest** (Sprint 1 panel disposition §3 vii / Sprint 1 panel preserved disagreement): Goffman argued that `social.interactional_visibility` (L42) conflates two analytically distinct constructs — *opportunity to be seen* (exposure) and *quality of mutual visibility for civil inattention* (Goffman 1963, *Behavior in Public Places*, pp. 83–88). Sprint 1 retained L42 as a single tag with explicit scope notes flagging the unresolved distinction; L42b was logged as a Sprint-2 candidate which then slipped to Sprint 4.

**Sprint 4 disposition**: deferred to Sprint 5. The construct-validity case is sound, but the panel-vote work to ratify the split + the registry edit to create `social.civil_inattention_support` as L42b + the upstream-observable disambiguation between L42a and L42b was not within the Sprint 4 session budget (which prioritised the 46 algorithmic skeletons, 8 working detectors, synthetic CPTs, and Goodman 1974 Jacobian rank check).

**Sprint 5 follow-up**: dispatch a Goffman-voiced panel sub-agent to formalise the disposition; if it ratifies the split, add `cognitive.civil_inattention_support` (L42b) as a new latent with disjoint upstream observables (L42a focuses on `affordance.sightline_count`, `affordance.partition_height`; L42b focuses on `affordance.recess_count`, `affordance.partial_screen_density`).

## Contest #2 — L52 as F-formation variant (deferred)

**Original contest** (Sprint 1 panel disposition §3 viii): Kendon argued that L52 (`social.presentation_one_to_many`) is ontologically an F-formation variant — specifically a "semicircular arrangement of high asymmetry" in which one participant's transactional segment is privileged. Sprint 1 retained L52 as a separate construct because the V2.6 taxonomy treated it that way and rewriting the Image-Tagger tag IDs mid-cohort would break consumer contracts; the Kendon argument was logged as a Sprint-4 question.

**Sprint 4 disposition**: deferred to Sprint 5. The case for adding a `bn.f_formation_family` field linking L52 to {L44, L48, L49} is straightforward; the question is whether L52 should be additionally re-categorised in `notes.social_layer` (currently `social_organization` per Contest 3 disposition) given Kendon's interaction-order framing of presentation events.

**Sprint 5 follow-up**: dispatch a Kendon-voiced panel sub-agent. Likely outcome: hybrid — add `bn.f_formation_family: "asymmetric_semicircle"` to L52 and the corresponding family annotation to L44 (`circular`/`vis_a_vis`), L48 (`vis_a_vis`/`l_arrangement`), L49 (`semicircular`/`circular`). Preserves the Sprint-1 taxonomic commitment while honouring Kendon's structural point.

## Note on the Sprint 4 scope decision

The decision to defer Contests #1 and #2 reflects Sprint 4's actual deliverable balance: 46 algorithmic skeletons + 8 working detectors + synthetic-CPT generator + Goodman 1974 Jacobian rank check + ranking-function κ population + splat-augmentation scaffolds + Stage 5 doctor wrap. Contest 3 made it because its disposition was shorter (single registry edit + one new validated field) and because the social-layer distinction unlocks Sprint 5's planned extension to L01–L40.

The deferred contests do not block any downstream work. Sprint 1's original disposition for L42 (single tag, scope-note flagged) remains in the registry and is consistent. L52's social-organisation classification under Contest 3's social_layer disposition is consistent with both the Sprint-1 V2.6-traceability commitment and Kendon's Sprint-1 dissent (which acknowledged the V2.6 commitment as overriding).

---

*End of deferral document.*
