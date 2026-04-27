# Backlog: Latent Variables L01–L40 — Cognitive / Affect / Perception Layer

*Filed: 2026-04-26 by Claude (Cowork session) on behalf of David Kirsh*
*Carrying topic: TOP-009 (Sprint 1, social-interaction latents L41–L58, completed Phases A–E on `track1/latents/L41-L58-claude-sprint1`)*
*Status: **DEFERRED — must not be forgotten**. Pending kickoff after Sprint 1 closes.*

---

## 1. What this document records

The Tagging_Contractor registry now contains the eighteen social-interaction latent variables L41–L58 from Part X of the Environment–Cognition Taxonomy V2.6. That is a single slice — Part X — of a larger taxonomy whose Parts I through IX comprise forty further latent variables covering cognitive, affective, and perceptual responses to the built environment. Those forty (L01 through L40) are not yet in the registry, are not yet documented, and are not yet visible to any downstream consumer of the Tagging_Contractor contracts. This document exists so that the absence is recorded, so that whoever opens the next Tagging_Contractor session — David, a future Claude session, an Image-Tagger student, an Article-Eater integrator — sees immediately that the latent layer is *not finished* and that the work to finish it is well-scoped and partially scaffolded.

## 2. Why this matters

The Bayesian network at the heart of the Knowledge Atlas inherits its latent structure from the registry. As of the close of Sprint 1, the BN's latent layer contains twenty-three nodes — five legacy plus the eighteen we just added. The original V2.6 taxonomy specifies *fifty-eight* latent constructs across Parts I–X; we are therefore at thirty-one percent coverage of the intended latent layer. Image-Tagger extractor stubs exist for the eighteen we shipped; they do not exist for L01–L40. Article-Eater HITL reviewers will, as a result, be unable to use the lower-numbered latents as ground truth, and any BN-track student who attempts inference against the full V2.6 belief network will discover that two-thirds of the latent nodes are missing. Shipping a partial latent layer and then forgetting to close it is a recurring failure mode in research infrastructure (Bowker & Star, 1999, on the politics of standards-in-the-making). This document is a guard against that failure.

## 3. What the next sprint inherits from Sprint 1

The Sprint 1 work was deliberately structured so that the lower-numbered latents could be added with substantially less labour than was required for the eighteen we shipped. Specifically, Sprint 2 inherits:

The five panel-added schema fields — `extractability.requires_floor_plan`, `extractability.configurational_measure`, `secondary_value_type`, `notes.interaction_mode`, `notes.cross_cultural_variance` — are now part of the registry shape. No further schema work is required for Sprint 2 unless a cognitive or affective construct demands a field that the social-interaction panel did not anticipate. (Two such demands are predictable: a `temporal_window` field for attention/memory latents whose meaning depends on the duration of observation, and a `valence_polarity` field for affect latents whose value is signed rather than unsigned. Neither is required at Sprint 2 commit; both are flagged here for the Sprint-2 architectural panel's first agenda.)

The semantic gate — `tc doctor --prod`, `tc audit-semantics`, `tc audit-extraction-plan` — is in place and will validate L01–L40 entries against the same constraints, including Spohn's 50% upstream-overlap rule. The rule's enforcement is mechanical; the only question is whether the L01–L40 set will produce more or fewer pair violations than L41–L58 did. (Likely *more*, because cognitive and perceptual latents tend to share upstream observables more densely — most affect constructs depend on lighting and colour observables, for example. This is a planning concern, not a blocker.)

The Phase plan (A through G, with A.5 panel and F.5 construct-validity vote) is fully reusable. The seven-phase scaffold, the three-pass per-latent deliberation procedure (Driver / Engineer / Blind-reader), the per-latent spec template at `docs/sprint1_latent_specs/_AGENT_BRIEFING.md`, and the merge / fix / validate scripts at `scripts/sprint1_merge_latents.py` and `scripts/sprint1_fix_validator_errors.py` can be cloned and adapted with minor edits.

The construct contests preserved for student deliberation in the Sprint 1 handoff (L41 Tier override; L42 split; L52 as F-formation variant; cross-cultural variance flag) provide a methodological model for Sprint 2's analogous contests, which the Sprint-2 panel will identify in its own §3.

## 4. What the next sprint must do that Sprint 1 did not

Three substantive items distinguish Sprint 2 from a mere copy-paste of Sprint 1.

First, **the panel composition must change**. The Sprint 1 panel — Goffman, Hall, Kendon, Hillier, Spohn — was selected because the constructs were social-interactional. The Sprint 2 panel for L01–L40 should be drawn from the cognitive, perceptual, and affect literatures: candidate voices include Kahneman (attention and intuition; *Thinking, Fast and Slow*, 2011), Treisman (feature integration; Treisman & Gelade, 1980), Gibson (ecological perception and affordance; *The Ecological Approach to Visual Perception*, 1979), Damasio (somatic-marker affect; *Descartes' Error*, 1994), Russell (circumplex of affect; Russell, 1980), Kaplan & Kaplan (preference and restorative environments; 1989), Ulrich (stress recovery; Ulrich et al., 1991), and Spohn (retained for the BN-structural critique). The exact set should be calibrated to which V2.6 Parts I–IX subdomains are present in the L01–L40 list — Phase A of Sprint 2 includes a survey pass to identify these subdomains and to nominate panel voices accordingly.

Second, **the BN identifiability concern grows worse**. With 23 latents now in place and 40 more to add, the latent layer will reach 63 nodes — more than twelve times its pre-Sprint-1 size. Even with Spohn's 50%-overlap rule enforced, the joint identifiability of 63 latents conditioned on a finite observable layer is non-trivial, and the EM convergence properties will not be self-evident. Sprint 2's Phase D may need to extend `audit-extraction-plan` with a *layer-level* identifiability check — a formal test that the latent-layer Jacobian is full-rank over the observable layer (Goodman, 1974, on the identifiability of latent class models; Koller & Friedman, 2009, ch. 19, on the EM convergence guarantees). This is a non-trivial extension and should be scoped in Sprint 2's planning, not deferred.

Third, **the cross-cultural variance flag will need recalibration**. The Hall-driven `cross_cultural_variance` field was set conservatively in Sprint 1 — five of the eighteen latents flagged `high`. For cognitive and perceptual constructs, the cross-cultural picture is more contested: feature-integration mechanisms appear to be relatively universal (Treisman & Gelade, 1980, with cross-cultural replications), but affective and aesthetic preferences are deeply culturally inflected (Henrich et al., 2010, on WEIRD samples; Markus & Kitayama, 1991, on independent vs. interdependent self-construals as it bears on social-affective response). Sprint 2's panel should include explicit deliberation on which L01–L40 latents merit `high` flags and which can defensibly be `medium` or `low`.

## 5. Estimated effort

Sprint 1 was planned at nine working days and ran to roughly eleven actual working days for Phases A through E (Phases F, F.5, G remain on the Sprint 1 backlog and would add another two to three days). Sprint 2 covers more than twice the number of latents (40 versus 18), but it inherits the infrastructure built in Sprint 1, so the per-latent labour will be lower. A defensible estimate is fifteen to twenty working days for the full Sprint 2 — plausibly compressible to twelve if the Phase B sub-agent procedure can be batched more aggressively now that the per-latent spec template is mature.

## 6. Triggers and prerequisites

Sprint 2 should not begin until the following are true:

Sprint 1 must be closed. Phases F (adversarial blind-read), F.5 (construct-validity panel vote), and G (handoff bundle, release v0.2.9-rc1, PR merge to `main`) must be complete, the v0.2.9 release must be tagged, and the eighteen L41–L58 entries must be live in the production registry consumed by Image-Tagger and Article-Eater. Without this closure, Sprint 2 risks branching from a moving Sprint 1 base and inheriting unresolved decisions.

The downstream consumers must have begun integration. At minimum, Image-Tagger students should have started populating one or two of the eighteen extractor stubs in `tagging_pipeline/extractors/latents/`. Sprint 2 will inherit any field-level lessons that integration surfaces (e.g., that `extraction.expected_upstream_observables` should have been a list of structured records rather than bare strings, or that the F-formation enum needs a `mixed` value).

The V2.6 taxonomy itself must be inspected. As of this writing I have not opened the V2.6 source workbook and read the L01–L40 rows. Sprint 2's first concrete action is therefore not panel deliberation but *taxonomic survey*: a one-day pass through the workbook's Parts I–IX to identify subdomains, subgroup the forty latents, draft the new domain controlled vocabulary, and nominate the panel composition.

## 7. First-day actions when this backlog is reactivated

When David or a future Claude session opens this document and begins Sprint 2, the first session's work should consist of, in order:

(i) **Confirm Sprint 1 closure.** `cd /Users/davidusa/REPOS/Tagging_Contractor && git log --oneline -5 main` should show the Sprint 1 merge commit. If not, reopen Sprint 1 first.

(ii) **Cut a new branch.** `git checkout -b track1/latents/L01-L40-claude-sprint2` from `main`.

(iii) **Read this document in full.** The architectural inheritances of §3 and the new requirements of §4 are not optional; Sprint 2's panel deliberation in particular must be aware that Sprint 1's panel results carry but do not exhaust the decisions to be made.

(iv) **Open the V2.6 source workbook.** Identify the L01–L40 rows. Cluster by subdomain. Draft a one-page Sprint 2 scope document at `docs/sprint2_scope_2026-MM-DD.md`.

(v) **Convene the Sprint 2 architectural panel.** Goffman/Hall/Kendon/Hillier are not the right voices for cognitive/perceptual constructs; assemble the panel per §4 above.

(vi) **Then begin Phase B** (per-latent deliberation), reusing the briefing template at `docs/sprint1_latent_specs/_AGENT_BRIEFING.md` with minor revisions to reflect the Sprint 2 panel's adopted commitments.

## 8. Files of inheritance

The following files in the Sprint 1 branch are the durable inheritance for Sprint 2:

| File | Role for Sprint 2 |
|---|---|
| `docs/sprint1_panel_disposition_2026-04-28.md` | Architectural commitments and preserved disagreements that carry forward |
| `docs/V2.6_to_registry_field_map.md` | Field-name map; extend in Sprint 2 with any new panel-added fields |
| `docs/sprint1_latent_specs/_AGENT_BRIEFING.md` | Per-latent spec template; clone with per-Sprint-2 edits |
| `scripts/sprint1_merge_latents.py` | Pattern for the merge step; clone as `sprint2_merge_latents.py` |
| `scripts/sprint1_fix_validator_errors.py` | Pattern for the post-merge fix step |
| `scripts/audit_extraction_plan.py` | Already enforces Spohn 50%-overlap on all latent tags including new ones |
| `scripts/audit_semantics_simple.py` | Already enforces semantic completeness on all latent tags |
| `scripts/doctor_prod.py` | The unified gate; works as-is for Sprint 2 with `--scope latent` |
| `bin/trs.py` | CLI dispatcher; already wired for the three production-gate verbs |
| `tagging_pipeline/extractors/latents/__init__.py` | Dispatch table to extend with L01–L40 stubs |
| `tagging_pipeline/extractors/latents/detect_L41.py` … `detect_L58.py` | Stubs to clone for L01–L40 with per-latent docstring contents |

## 9. References

Bowker, G. C., & Star, S. L. (1999). *Sorting things out: Classification and its consequences*. MIT Press.

Damasio, A. R. (1994). *Descartes' error: Emotion, reason, and the human brain*. Putnam.

Gibson, J. J. (1979). *The ecological approach to visual perception*. Houghton Mifflin.

Goodman, L. A. (1974). Exploratory latent structure analysis using both identifiable and unidentifiable models. *Biometrika*, *61*(2), 215–231.

Henrich, J., Heine, S. J., & Norenzayan, A. (2010). The weirdest people in the world? *Behavioral and Brain Sciences*, *33*(2–3), 61–135.

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Kaplan, R., & Kaplan, S. (1989). *The experience of nature: A psychological perspective*. Cambridge University Press.

Koller, D., & Friedman, N. (2009). *Probabilistic graphical models: Principles and techniques*. MIT Press.

Markus, H. R., & Kitayama, S. (1991). Culture and the self: Implications for cognition, emotion, and motivation. *Psychological Review*, *98*(2), 224–253.

Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, *39*(6), 1161–1178.

Treisman, A. M., & Gelade, G. (1980). A feature-integration theory of attention. *Cognitive Psychology*, *12*(1), 97–136.

Ulrich, R. S., Simons, R. F., Losito, B. D., Fiorito, E., Miles, M. A., & Zelson, M. (1991). Stress recovery during exposure to natural and urban environments. *Journal of Environmental Psychology*, *11*(3), 201–230.

---

*End of backlog document.*
