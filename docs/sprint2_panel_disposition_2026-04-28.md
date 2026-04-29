# Sprint 2 Architectural Panel Disposition

**Convened:** 28 April 2026
**Panel:** Kaplan & Kaplan (preference matrix, restorative environments, Attention Restoration Theory), James Russell (circumplex of affect), Daniel Kahneman (cognitive load, fast/slow processing, perceived control), Roger Ulrich (stress recovery, threat appraisal), Wolfgang Spohn (Bayesian-network identifiability — retained from Sprint 1)
**Subject:** Architectural commitments governing the cognitive / affect / perception latents L01–L40, drawn from Parts I–IX of the Environment–Cognition Taxonomy V2.7
**Procedure:** Each panelist drafted independently from the same brief, in isolation from the others. This document synthesises the five critiques, ratifies the commitments that supersede the implicit defaults of Sprint 1, and preserves the disagreements that the four parallel JSON-authoring sub-agents must not silently flatten.

---

## 1. Substantive convergences

Five independent voices, recruited from cognitive psychology, affective science, and Bayesian epistemology, converged on four claims. The convergences are stronger than the Sprint 1 panel's because the domain — cognitive and affective response to the built environment — is more theoretically mature than the social-interaction territory Goffman, Hall, Kendon, and Hillier had to triangulate.

**The single time-scale assumption is wrong, and the registry must record temporal window explicitly.** Kahneman pressed this hardest: a perception of clutter (L28) is a snapshot judgement, made in fractions of a second by System 1 (Kahneman, 2011, ch. 4); a sense of soft fascination (L19) requires sustained engagement of System 2's defaults; a judgement of predictability (L08) requires longitudinal observation of the same environment across visits and is, strictly, not extractable from any single image. Russell agreed for affect: core affect (Russell, 2003) is a momentary state, but the appraisals that label it as "cosy" or "welcoming" require a longer integration window. Kaplan & Kaplan corroborated from the restoration literature: being-away and compatibility (L18, L20) are sustained-engagement constructs, not snapshot ones. Ulrich added the threat-appraisal case: contamination cues (L05) trigger a snapshot disgust response, but threat-monitoring (L01) is a sustained-vigilance construct that an extractor reading a single image will systematically underestimate. The four routes converge: temporal window is a registry-level property, not an implementation detail.

**The valence dimension is not derivable from the latent name alone, and the registry must record polarity.** Russell led the argument: the circumplex of affect (Russell, 1980) demonstrates that pleasure (valence) and activation (arousal) are independent axes, and that constructs like *arousal potential* (L23) are deliberately orthogonal to valence. A registry that treats every Likert scale as monotonically positive flattens the circumplex onto a single line and loses the distinction between *high-arousal-positive* (energising) and *high-arousal-negative* (alarming) environments. Kaplan & Kaplan agreed: restorativeness (L17) is signed positive; surveillance pressure (L04) is signed negative; valence potential (L24) is *bipolar* by construction. Ulrich pressed the same point from stress-recovery research: contamination risk (L05) and crowding pressure (L14) are negative-valence constructs whose Likert score should be interpreted *higher = more stressful*, while restorativeness (L17) and being-away (L18) are positive-valence constructs whose Likert score is *higher = more restorative*. The registry must record this asymmetry; otherwise the BN will combine signed and unsigned scores additively and produce nonsense.

**The 40 latents are extractable at strikingly different image-judgability tiers, and the V2.7 1-to-5 scale must map cleanly into Sprint 1's three-tier extractability schema.** All five panelists concurred on this point with little discussion. The V2.7 source assigns each latent an `Image_Judgability_1to5` score; the registry shape inherited from Sprint 1 uses a three-valued `extractability` block. Without an explicit translation rule the four parallel JSON-authoring agents will each invent their own mapping and the resulting registry will be incoherent. The panel ratifies a single deterministic table (see §3.iv).

**Spohn's 50%-overlap rule, ported from Sprint 1, will bite harder on this set than it did on the social-interaction set.** Spohn was emphatic: cognitive and affective latents share upstream observables far more densely than social-interaction latents do. Lighting, colour temperature, visual order, and material texture are upstream of dozens of L01–L40 constructs simultaneously. The panel predicts more pair violations than the {L43, L44} and {L42, L54} pairs Sprint 1 surfaced, and it flags four high-risk pairs (§3.vii) for the authoring agents to keep deliberately disjoint. Without explicit guidance, the parallel agents will inadvertently double-list `lighting_uniformity` or `visual_clutter_density` across overlapping triplets and the validator will reject the merged registry.

## 2. Substantive divergences (preserved disagreement)

The five panelists agreed on the convergences above but diverged sharply on three architectural questions. These disagreements are recorded without forcing resolution; they will become construct contests in the student handoff.

**Kaplan & Kaplan vs. Russell on the structure of L17 (Restorativeness, ART).** Kaplan & Kaplan's Attention Restoration Theory (Kaplan & Kaplan, 1989; Kaplan, 1995) treats restorativeness as a single integrated construct with four named components — being-away, fascination, extent, compatibility — that should be modelled as a coherent unit. Russell counters that restorativeness is a *region of the affective circumplex* (low-arousal-positive), not a discrete latent: encoding it as a separate ordinal scale double-counts variance already captured by valence and arousal. The disposition (§3.i) keeps L17 as a single ordinal latent per the V2.7 source, but adds a `bn_notes` flag that Sprint 3 may want to either (a) decompose L17 into its four ART components as a structured factor, or (b) re-encode L17 as a derived position in the Russell circumplex. The contest is preserved, not closed.

**Kahneman on the value type of L08 (Predictability/Stability).** Kahneman objected to ordinal Likert encoding of L08 on first principles: predictability is, by his account, a probability distribution over future states (Kahneman & Tversky, 1979), and compressing a distribution into five bins discards exactly the information the BN needs for downstream inference. Spohn agreed in principle but not in practice: continuous value types are not currently supported by the registry's CPT-based BN backend, and adding them is a Sprint 4 architectural commitment. The disposition (§3.iii) keeps L08 as `value_type: ordinal` for tractability, with an explicit `bn_notes` flag that Sprint 3 should evaluate continuous re-encoding once the BN identifiability check is in place.

**Spohn on the joint identifiability of the 63-node latent layer.** With Sprint 1's 23 latents plus Sprint 2's 40, the BN's latent layer reaches 63 nodes — more than twelve times its pre-Sprint-1 size. Spohn's view: this is no longer a small-network problem, and Sprint 1's `audit-extraction-plan` 50%-overlap check is necessary but not sufficient. A 63-node latent layer conditioned on a finite observable layer requires a *layer-level* identifiability test — formally, that the latent-layer Jacobian is full-rank over the observable-layer measurements (Goodman, 1974, on the identifiability of latent-class models). Kaplan & Kaplan, Russell, Kahneman, and Ulrich all deferred to Spohn on this; the disposition records the concern as an open Sprint 3 deliverable, ships Sprint 2 with the 50%-overlap check as the immediate guard, and flags identifiability formally in §3.viii.

**Cross-cultural variance for affective and aesthetic latents.** Russell, Kaplan & Kaplan, and Ulrich split on which of the affect-cluster latents merit a `high` cross-cultural-variance flag. The case for `high`: Markus & Kitayama (1991) demonstrate that independent vs. interdependent self-construals shift the meaning of constructs like welcome (L34), formality (L39), and prestige (L32); Henrich, Heine, and Norenzayan (2010) document the WEIRD-sample bias in nearly all affect research. The case for `medium` (or even `low`): Keltner & Haidt (2003) argue that awe (L36) is a cross-cultural universal with reliable elicitors; Ulrich (1991) shows stress-recovery responses to natural environments replicate across cultures studied to date. The disposition (§3.viii) sets `high` for the six latents the panel found most contested (L25, L32, L34, L36, L39, L40) and `medium` for the rest; the assignment is preserved as an explicit student contest because it rests on panel best judgement rather than empirical settlement.

| Panelist | Single recommendation |
|---|---|
| Kaplan & Kaplan | Add `notes.temporal_window` to the registry, with `sustained` required for L17–L20 (the ART cluster). |
| Russell | Add `notes.valence_polarity` to the registry; explicitly mark L23 and L24 `mixed` because they are bipolar by construction. |
| Kahneman | (a) `temporal_window: longitudinal` for L08; (b) flag L08 for continuous re-encoding in Sprint 3. |
| Ulrich | `interaction_mode: unfocused` for the safety-threat cluster L01–L05 (ambient threat appraisal is unfocused engagement); preserve `negative` valence flags for stress-relevant latents. |
| Spohn | Add a layer-level full-rank Jacobian check to `audit-extraction-plan` in Sprint 3; for Sprint 2, enforce the 50%-overlap rule and flag four predicted high-overlap pairs (§3.vii). |

These five recommendations are independently defensible and substantially complementary. The disposition adopts all five.

## 3. Disposition: ratified architectural decisions for L01–L40

The following nine decisions are *ratified*. The four parallel JSON-authoring sub-agents will treat them as fixed inputs. They supersede the implicit defaults of Sprint 1 wherever they conflict.

(i) **Two new schema fields are added to the registry shape.**

`notes.temporal_window`: enum `{snapshot, short_period, sustained, longitudinal, n/a}`. The time-scale over which the latent's meaning is well-defined. Default: `snapshot`. Required explicit values:
- L08 (Predictability/Stability) → `longitudinal`. The construct is a judgement about consistency across visits; it cannot be extracted from a single image without an explicit warning.
- L12 (Interruption Likelihood) → `short_period`. The judgement integrates over minutes of expected traffic, not over an instant.
- L19 (Soft Fascination) → `sustained`. Effortless attention capture is a property of sustained engagement, not of a saccade.
- L20 (Compatibility) → `sustained`. Fit between affordances and intended activity emerges only over the activity's full duration.

`notes.valence_polarity`: enum `{positive, negative, mixed, neutral, n/a}`. The signed direction of the construct on a hedonic axis. Default: `neutral`. Required values:
- `positive` for L17 (Restorativeness ART), L18 (Being-Away), L19 (Soft Fascination), L20 (Compatibility), L25 (Coziness), L34 (Welcome), L36 (Awe — Keltner & Haidt's positive-but-self-diminishing case), L40 (Playfulness).
- `negative` for L01 (Perceived Threat), L04 (Surveillance Pressure), L05 (Contamination/Disgust Risk), L14 (Crowding Pressure), L28 (Clutter Load).
- `mixed` for L23 (Arousal Potential — orthogonal to valence by Russell's circumplex) and L24 (Valence Potential — bipolar by construction).
- `neutral` for the remaining 25 latents.

These two fields extend the registry shape established in Sprint 1; they are documented in `docs/V2.6_to_registry_field_map.md` (which will be re-titled to cover V2.7 in Phase A).

(ii) **Domain and category assignments are uniform across L01–L40.**

`domain: cognitive_affect` for all 40 latents. `category: cognitive` (registry enum) for all 40. The `subdomain` field carries the finer structure per the table below.

| Subdomain | Latents |
|---|---|
| safety_threat | L01–L05 |
| control_autonomy | L06–L09 |
| privacy_attention | L10–L13 |
| crowding_density | L14–L16 |
| restoration | L17–L20 |
| aesthetic_affect | L21–L26 |
| cognitive_load | L27, L28 |
| wayfinding | L29–L31 |
| social_signal | L32–L36 |
| familiarity_novelty | L37–L40 |

(iii) **Value type is assigned by family.**

`latent_score` (binary, present/absent) for L05 (Contamination), L33 (Care/Maintenance), L34 (Welcome), L37 (Familiarity). The panel agreed that these four admit a clean present/absent reading and that ordinal compression adds noise without adding signal. Contamination, in particular, is a System-1 disgust trigger (Kahneman, 2011) that fires categorically rather than gradiently.

`ordinal` Likert [0,4] for the remaining 36. This matches the V2.7 indicator-item Likert 1–7 scales, compressed to 5 bins for CPT tractability per Spohn's parametric argument from Sprint 1. The compression discards information; the alternative — a 7-bin scale — produces $7^{|\text{pa}|}$-parameter CPTs that the available tagged corpus cannot estimate.

L08 is kept ordinal despite Kahneman's principled objection. The `bn_notes` field on L08 will record: *"Sprint 3: evaluate continuous re-encoding per Kahneman & Tversky (1979); current ordinal compression is provisional."*

(iv) **The V2.7 `Image_Judgability_1to5` score maps deterministically into the registry's `extractability` block.**

| `Image_Judgability_1to5` | `from_2d` | `from_3d_vr` | `monocular_3d_approx` | V2.7 Tier |
|---|---|---|---|---|
| 5 | yes | yes | yes | Tier 1 |
| 4 | partial | yes | partial | Tier 2 |
| 3 | partial | yes | no | Tier 2 |
| 2 | no | yes | no | Tier 3 |
| 1 | no | yes | no | Tier 3 |

The mapping is deterministic and authoring agents must apply it without negotiation. Panel logic: a judgability of 5 means a single 2D image suffices; 4 means partial extraction from 2D with VR fully sufficient; 3 means VR is needed for confident extraction but a 2D image yields a degraded signal; 2 and 1 mean only VR or richer multimodal stimuli are diagnostic.

(v) **`method_family` is assigned by subdomain.**

`vlm` (vision-language model with indicator-item prompts) for `safety_threat`, `social_signal`, `restoration`, `aesthetic_affect`, and `familiarity_novelty`. The panel reasoning: these subdomains require *holistic* judgements that integrate multiple visual properties simultaneously and that the affect literature has historically operationalised through Likert-scaled survey items (Russell, 1980; Kaplan & Kaplan, 1989). VLMs prompted with the V2.7 indicator items are the right substrate.

`composite` (segmentation + counting + spatial-graph features) for `privacy_attention`, `crowding_density`, `cognitive_load`. The panel reasoning: these subdomains decompose into countable observables — partition counts, occupancy density, distinct visual elements — and a composite extractor reading off segmentation outputs is more accurate than a holistic VLM judgement.

`geometry` for parts of `wayfinding`, specifically L29 (Legibility/Wayfinding Ease), which the panel agreed is best computed from isovist analysis when floor-plan or VR access is available. L30 and L31 within wayfinding remain `composite` (they involve sign legibility and route-marker counting, not isovist geometry).

(vi) **`bn.evidence_role: latent` and `bn.demand_state: optional` for all 40 latents.** All L01–L40 constructs are latent BN nodes (their values are inferred, not directly observed) and none is required to be present in every Atlas instance. This matches the Sprint 1 default for L41–L58.

(vii) **Spohn's 50%-overlap rule applies, with four predicted high-overlap pairs flagged for the authoring agents.** Authors must keep `bn.parent_tags` lists deliberately distinct on these pairs:

- **L01 (Perceived Threat) and L04 (Surveillance Pressure)** — both load on lighting and concealment observables. L01's parents should emphasise concealment geometry and lighting *gaps*; L04's should emphasise camera presence, open-plan exposure, and spotlight-style lighting *intensity*.
- **L17 (Restorativeness ART) and L18 (Being-Away)** — Kaplan & Kaplan name being-away as a *component* of restorativeness, so upstream-observable overlap is structurally guaranteed. Authors should keep L17's parents at the integrated ART level (nature presence, soft visual field, retreat affordance) and L18's at the *separation-from-demands* level (thresholds, spatial distance from work zones, view of non-work content).
- **L21 (Coherence/Order) and L29 (Legibility/Wayfinding Ease)** — both load on visual organisation. L21's parents should emphasise compositional regularity (alignment, repetition, colour harmony); L29's should emphasise navigability (sightlines to destinations, signage, isovist depth).
- **L23 (Arousal Potential) and L38 (Novelty)** — Berlyne's collative variables (Berlyne, 1971, ch. 1) are intentionally correlated, but the constructs are distinct: arousal potential is the *energising* property of a scene, novelty is the *unfamiliarity* property. Authors should keep L23's parents at the scene-energy level (saturation, contrast, visual complexity) and L38's at the corpus-comparison level (statistical rarity of features against a reference distribution).

The `audit-extraction-plan` validator will reject any merged registry state in which two of the above pairs share more than 50% of their `extraction.compute_from` references.

(viii) **Cross-cultural variance is set per panel best judgement, with the assignment preserved as a student contest.** `notes.cross_cultural_variance: high` for L25 (Coziness), L32 (Prestige Cues), L34 (Welcome), L36 (Awe), L39 (Formality), L40 (Playfulness). `medium` for the remaining 34 (the registry default). The `high` assignments record the panel's view that these six constructs are most strongly inflected by independent vs. interdependent self-construal (Markus & Kitayama, 1991) and by WEIRD-sample bias (Henrich et al., 2010); the assignment is preserved as a student contest in §5 because Keltner & Haidt (2003) provide a credible counter-argument for awe in particular.

(ix) **`interaction_mode` (Goffman's Sprint 1 field) is assigned by cluster.** The Sprint 1 panel ratified `interaction_mode` as a required field of `notes`; Sprint 2 inherits it.
- `unfocused` for the safety-threat cluster L01–L05. Threat appraisal, surveillance pressure, and contamination risk operate as *ambient* monitoring — Goffman's unfocused-engagement category (Goffman, 1963, ch. 4). Ulrich's recommendation.
- `focused` for the cognitive-load and wayfinding clusters L27–L31. Working-memory load, visual clutter, legibility, and signage interpretability all bear on tasks that the user is actively attending to.
- `mixed` for the remaining 30. Most cognitive/affect constructs apply across both focused and unfocused engagement (one can experience restorativeness while task-engaged or while idle).

## 4. Effect on phase plan

Phase A (field map) absorbs the two new schema fields `notes.temporal_window` and `notes.valence_polarity`; the field map document `docs/V2.6_to_registry_field_map.md` is re-titled to cover V2.7 and the two new field paths are added.

Phase B (per-latent deliberation) gains four new questions per latent — temporal window; valence polarity; method-family substrate (where the subdomain default is overridden); upstream-observable inventory in service of Spohn's 50%-overlap check, with explicit attention to the four high-risk pairs in §3.vii.

Phase C (parallel JSON authoring) is structured around the nine ratified decisions. Each of the four authoring sub-agents takes one quartile of the 40-latent set (10 latents each) and produces fully-populated JSON entries that already encode the decisions of §3. The decisions are *not negotiable* in Phase C; sub-agents that disagree must escalate to a panel re-convening, not silently override.

Phase D (validator gap-fill) inherits the Sprint 1 50%-overlap check unchanged. The Sprint 3 layer-level Jacobian identifiability check is *not* added in this sprint; it is logged as a Sprint 3 deliverable per Spohn's recommendation.

Phase E (extractor stubs) gains 40 new stubs cloned from the Sprint 1 patterns at `tagging_pipeline/extractors/latents/detect_L41.py` through `detect_L58.py`. Method-family assignments from §3.v drive the stub template selection: `vlm` stubs receive a different docstring scaffold from `composite` and `geometry` stubs.

The estimated sprint duration moves from the backlog's fifteen-to-twenty-day band to a tighter twelve-to-fifteen-day band, on the assumption that the four-way parallelisation in Phase C compresses the longest single-track work.

## 5. Construct contests preserved for the student handoff

The following four contests will be foregrounded in `LATENT_INTEGRATION_NOTES_2026-MM-DD.md` for the students to relitigate in their Sprint 3 deliberation:

1. **L17 as integrated construct vs. Russell-circumplex coordinate.** Kaplan & Kaplan's ART treats restorativeness as a single unit; Russell's circumplex would re-encode it as a low-arousal-positive position. The students should decide whether L17 should be (a) preserved as ordinal, (b) decomposed into the four ART components as a structured factor, or (c) re-encoded as a derived (valence, arousal) coordinate.

2. **L08 as ordinal vs. continuous.** Kahneman's argument that predictability is a probability distribution, not a five-bin scale, is theoretically clean but blocked by the registry's current CPT-based BN backend. The students should decide whether the eventual continuous re-encoding warrants Sprint 4 backend work.

3. **Cross-cultural-variance flag deployment for the affect cluster.** The panel set `high` for L25, L32, L34, L36, L39, L40 on best judgement. Students with cultural-anthropology background should audit this list, with particular attention to Keltner & Haidt's (2003) cross-cultural awe research as a counter-argument to the L36 `high` flag.

4. **Joint identifiability of the 63-node latent layer.** Spohn's identifiability concern is open. The students should consider whether the layer-level Jacobian check should be added to `audit-extraction-plan` in Sprint 3 and what the criteria for full-rank acceptance should be (Goodman, 1974, gives the formalism but not the threshold).

These four contests are the *first questions* the next cohort of students will see, not the last. The handoff is structured around them deliberately — to invert the usual posture in which students inherit a finished system and discover its flaws by experience, replacing it with a posture in which they inherit a *contested* system and adjudicate its flaws by deliberation. The same posture animated the Sprint 1 handoff and is preserved here as a methodological commitment.

---

## 6. References

Berlyne, D. E. (1971). *Aesthetics and psychobiology*. Appleton-Century-Crofts.

Goffman, E. (1963). *Behavior in public places: Notes on the social organization of gatherings*. Free Press.

Goodman, L. A. (1974). Exploratory latent structure analysis using both identifiable and unidentifiable models. *Biometrika*, *61*(2), 215–231.

Henrich, J., Heine, S. J., & Norenzayan, A. (2010). The weirdest people in the world? *Behavioral and Brain Sciences*, *33*(2–3), 61–135.

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, *47*(2), 263–291.

Kaplan, R., & Kaplan, S. (1989). *The experience of nature: A psychological perspective*. Cambridge University Press.

Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. *Journal of Environmental Psychology*, *15*(3), 169–182.

Keltner, D., & Haidt, J. (2003). Approaching awe, a moral, spiritual, and aesthetic emotion. *Cognition and Emotion*, *17*(2), 297–314.

Markus, H. R., & Kitayama, S. (1991). Culture and the self: Implications for cognition, emotion, and motivation. *Psychological Review*, *98*(2), 224–253.

Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, *39*(6), 1161–1178.

Russell, J. A. (2003). Core affect and the psychological construction of emotion. *Psychological Review*, *110*(1), 145–172.

Spohn, W. (2012). *The laws of belief: Ranking theory and its philosophical applications*. Oxford University Press.

Ulrich, R. S. (1984). View through a window may influence recovery from surgery. *Science*, *224*(4647), 420–421.

Ulrich, R. S., Simons, R. F., Losito, B. D., Fiorito, E., Miles, M. A., & Zelson, M. (1991). Stress recovery during exposure to natural and urban environments. *Journal of Environmental Psychology*, *11*(3), 201–230.

---

*End of disposition.*
