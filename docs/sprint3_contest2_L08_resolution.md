# Sprint 3 Contest #2 Resolution: L08 (Predictability/Stability) Value-Type Encoding

**Convened:** 29 April 2026
**Panel:** Daniel Kahneman (judgment under uncertainty, fast/slow processing), Wolfgang Spohn (Bayesian-network identifiability and parameter estimation, retained from Sprints 1 and 2), Kaplan & Kaplan (perceptual-judgment tradition, Attention Restoration Theory, restorative-environments rating practice)
**Subject:** Sprint 2 preserved contest #2 — whether L08 (Predictability/Stability) should be re-encoded from `value_type: ordinal` (Likert 0–4) to `value_type: continuous` per Kahneman's panel position (Sprint 2 disposition §3.iii, §5.2).
**Procedure:** Each panel voice produced an independent position statement from the same brief, voted between three options, and ratified the disposition that follows.

---

## 1. The contest as posed

Sprint 2 ratified `value_type: ordinal` (Likert [0, 4]) for L08 (Predictability/Stability) as the conservative default for the 36 ordinal latents in the cognitive-affect cluster (Sprint 2 §3.iii). Kahneman registered a preserved objection on first principles: predictability is, by his account, a probability distribution over future states (Kahneman & Tversky, 1979), and compressing a distribution into five Likert bins discards exactly the information the downstream Bayesian inference engine will need when computing posteriors over fine-grained predictability levels. Spohn agreed in principle but counselled deferral pending clarification of whether the BN backend supports continuous CPTs. The Sprint 2 disposition recorded the disagreement and flagged Sprint 3 for resolution: *"evaluate continuous re-encoding per Kahneman & Tversky (1979); current ordinal compression is provisional"* (Sprint 2 §3.iii, on `bn_notes`).

The Sprint 3 panel was asked to choose among three options:

(A) **Adopt continuous** — change L08 to `value_type: continuous`, `value_range: [0.0, 1.0]`, `unit: "probability"`. Update the `audit-semantics` validator to accept `continuous` for latent tags. Document the engine assumption in `bn_notes`.

(B) **Reject continuous, keep ordinal** — close the deferral. Document why ordinal won (Kaplan rater-resolution argument; Spohn parameter-estimation argument).

(C) **Hybrid** — keep `value_type: ordinal` for human-rater capture, but add a new field `bn.posterior_distribution` declaring that the BN node's posterior is computed as a continuous distribution conditioned on the ordinal observation. Conceptually cleaner; requires registry-schema work.

## 2. Position statements

### 2.1 Daniel Kahneman — vote: (C) Hybrid (first preference); (A) Continuous (second preference)

The substantive psychology is settled: human predictability judgments are probabilistic (Kahneman & Tversky, 1979; Kahneman, 2011, ch. 14). When a person judges a setting "predictable," the underlying mental representation is not a five-point ordinal; it is a degree of belief over future-state distributions, anchored by representativeness heuristics and adjusted by what Kahneman & Tversky called *judgment by similarity to a stereotype*. The ordinal Likert encoding is a *measurement* compromise — what raters can produce reliably under instrument constraints — but it is not the *construct*. Encoding the Likert as the construct's value type, without registering that the construct itself is continuous, hardcodes the measurement compromise into the BN's inference layer and propagates it forward.

The full continuous re-encoding (Option A) is the theoretically clean choice and would be my first preference if the BN engine supported it without registry-schema disruption. But Spohn's Sprint 2 caveat — that continuous CPTs are not currently supported — makes (A) costly to ship now. Option (C) is the right *near-term* move: it preserves the ordinal capture from human raters (acknowledging Kaplan's measurement-instrument point) while explicitly registering that the BN's posterior over L08 is computed continuously. This separates measurement from construct, which is exactly the discipline the registry needs. I would describe (B) as a defensible engineering position but a weak epistemological one: it fuses the rater's instrument with the latent's nature, and the Sprint 2 disposition itself flagged this as provisional. Closing the deferral by accepting the provisional encoding as final is regress, not progress.

If forced to choose between only (A) and (B), I vote (A): the engine assumption should be documented and the schema work should follow, not the construct definition bend to the engine's current capability.

### 2.2 Wolfgang Spohn — vote: (C) Hybrid (first preference); (B) Reject (second preference)

The decision turns on engine capability and parameter-estimation cost, and the panel should be honest about both. A continuous CPT for L08 raises two distinct estimation problems. First, a Gaussian-conditional or Beta-conditional density requires more parameters per parent configuration than a discrete CPT — specifically, two parameters per configuration for Gaussian (mean, variance), or two for Beta (α, β), versus four free probabilities for a 5-bin discrete CPT. The naive count favours continuous, but the *effective* count is worse because student-rater data is sparse and continuous densities require smoothness assumptions that Likert data does not satisfy. Second, the BN engine I had in mind for Sprints 1–2 was discrete-only (CPT-based); if the registry's downstream engine is now confirmed to support hybrid Bayesian networks (e.g., conditional Gaussian models in the Lauritzen tradition; Lauritzen, 1992), the calculus changes.

Option (C) handles both concerns cleanly. The ordinal encoding remains the rater-facing capture, which respects Kaplan's measurement-resolution argument. The `bn.posterior_distribution` field declares — at the registry level — that the BN node will be inferred continuously, which protects against ordinal flattening at inference time. Crucially, this field does not commit Sprint 3 to actually implementing continuous inference; it commits the registry to *recording* the construct's continuous nature, so that when the engine catches up, the migration is one-line, not a registry-wide refactor.

I would vote (B) only if I were confident the engine will never support continuous nodes — and I am not. Hybrid Bayesian networks are mature technology (Koller & Friedman, 2009, ch. 14) and the project's Sprint 4 backlog explicitly considers them. (A) is theoretically clean but premature: changing `value_type` to `continuous` without engine support produces a registry that the validator will pass and the BN will fail to ingest.

### 2.3 Kaplan & Kaplan — vote: (B) Reject continuous (first preference); (C) Hybrid (second preference)

The Attention Restoration Theory tradition has used 7-point and 9-point Likert scales for forty years (Kaplan & Kaplan, 1989; Hartig et al., 1997) for one reason: that is the rater-resolution band human judges can produce reliably on subjective constructs like restorativeness, predictability, and compatibility. Demanding *continuous* output from a human rater of subjective predictability is a category error. Humans do not have sub-Likert resolution on these constructs — between "fairly predictable" and "very predictable" there is no operationalisable interval that a rater can mark on a continuous slider with reliability above chance. The literature on visual analogue scales versus Likert in subjective rating (e.g., Krosnick & Presser, 2010) confirms that the gain from continuous instruments on subjective constructs is small to negative, and the cost in inter-rater reliability is real.

The registry should match the rating instrument's resolution, not the construct's idealised mathematical structure. Kahneman's argument is correct *about the construct in the world*, but the registry encodes what the rater produces, which is ordinal. Recording ordinal as the value type is therefore not an epistemic compromise; it is an honest specification of the data's nature. The bn_notes can flag the construct-vs-instrument distinction without changing `value_type`.

Option (C) is acceptable as a fallback because it does not contaminate the rater-facing field; it adds a separate declaration about the BN's inferential treatment, which is downstream. But (C) introduces schema-extension cost and a new field that future authors will need to populate consistently across the cluster — not just L08. If the panel accepts (C) for L08, it should expect the question to recur for L17 (Restorativeness ART), L23 (Arousal Potential), and L24 (Valence Potential), and should be prepared to write the field for the entire cognitive-affect cluster. (A) is unacceptable: it conflates construct with instrument and asks raters to produce data they cannot reliably produce.

## 3. The vote

| Voice | First preference | Second preference |
|---|---|---|
| Kahneman | (C) Hybrid | (A) Continuous |
| Spohn | (C) Hybrid | (B) Reject |
| Kaplan & Kaplan | (B) Reject | (C) Hybrid |

**First-preference tally:** (C) — 2 votes; (B) — 1 vote; (A) — 0 votes.

**Second-preference tally:** (C) — 1 vote; (A) — 1 vote; (B) — 1 vote.

**Borda count** (2 points first, 1 point second): (C) — 5 points; (B) — 3 points; (A) — 1 point.

**Winner: Option (C) Hybrid**, by 2-of-3 first preferences and a clear Borda margin. The hybrid disposition is the unique option preferred or accepted by every panel voice — it is the Condorcet winner against both (A) and (B) in pairwise comparison.

## 4. Ratified disposition: precise registry edit specification

The following edits are ratified for Sprint 3 implementation and supersede the Sprint 2 §3.iii disposition for L08 specifically.

**(i) L08 entry edits.** In the L08 registry JSON entry:
- Retain `value_type: ordinal`.
- Retain `value_range: [0, 4]`.
- Retain `unit: "likert_bin"`.
- Add new field `bn.posterior_distribution` with the following sub-structure:
  ```json
  "bn": {
    ...,
    "posterior_distribution": {
      "form": "continuous",
      "support": [0.0, 1.0],
      "support_unit": "probability",
      "rationale": "Predictability is a probability distribution over future states (Kahneman & Tversky, 1979; Kahneman, 2011 ch. 14). Ordinal Likert is the rater-facing instrument; the BN node is inferred continuously.",
      "engine_requirement": "hybrid_bayesian_network_with_continuous_nodes",
      "engine_status": "Sprint 4 deliverable; registry records the requirement, not its current support."
    }
  }
  ```
- Update `bn_notes` to read: *"Sprint 3 contest #2 ratified hybrid encoding (29 April 2026): ordinal capture, continuous posterior. See `docs/sprint3_contest2_L08_resolution.md`. Sprint 4 must verify BN engine supports `posterior_distribution.form: continuous` before activating; until then, the BN treats L08 as ordinal at inference time and records the discrepancy in audit logs."*

**(ii) Schema extension.** Extend the registry schema to permit the optional `bn.posterior_distribution` block on any latent. The block's schema:
- `form`: enum `{discrete, continuous, ordinal_with_continuous_posterior}`.
- `support`: array of two numbers (continuous) or array of allowed discrete values.
- `support_unit`: free-text string.
- `rationale`: free-text string, required when `form` differs from the parent latent's `value_type`.
- `engine_requirement`: free-text string naming the BN-engine capability assumed.
- `engine_status`: free-text string describing current support.

**(iii) Validator extension.** The `audit-semantics` validator gains one rule: if `bn.posterior_distribution.form` differs from the latent's `value_type`, the `rationale` field is required and non-empty. No other validation is added in Sprint 3; engine-capability checking is deferred to the Sprint 4 BN-integration sprint.

**(iv) Cluster review trigger.** Per Kaplan & Kaplan's caveat, the question of whether to add `bn.posterior_distribution` to L17, L23, L24, and the broader aesthetic-affect cluster is logged as a Sprint 3 follow-up item. The L08 ratification establishes the *pattern*; cluster-wide deployment is a separate decision.

**(v) Documentation.** The Sprint 2 §5.2 contest is closed. The new schema field is added to `docs/V2.7_to_registry_field_map.md` (the Sprint 2-renamed field map document).

## 5. Preserved disagreement

Three threads of disagreement are preserved rather than forced to closure.

**Kaplan & Kaplan's instrument-purism objection to (C).** Kaplan & Kaplan accepted (C) as a fallback but registered concern that adding `bn.posterior_distribution` will create downstream pressure to populate the field for the entire cognitive-affect cluster, and that the registry's authors will not consistently distinguish constructs that *genuinely* have continuous structure (predictability, arousal potential) from constructs that are *intrinsically* categorical at the human-judgment level (welcome, prestige cues). The Sprint 3 follow-up review (§4.iv) is the agreed mechanism for this concern, but the worry is recorded.

**Kahneman's reservation that (C) is a half-measure.** Kahneman accepted (C) over (A) only because the engine timeline forced the compromise. He registered for the record that the *correct* long-term encoding is (A), and that Sprint 4's BN-integration sprint should re-examine whether `value_type: continuous` directly is preferable to `bn.posterior_distribution: {form: continuous}` once engine support is in place. The hybrid encoding may be a transitional architecture rather than a permanent one.

**Spohn's identifiability worry.** Spohn observed that adding continuous posterior nodes to a 63-node latent layer (Sprint 2 §3.viii) compounds the identifiability problem flagged in Sprint 2: a hybrid network's identifiability conditions are stricter than a discrete network's, and the layer-level Jacobian check Spohn requested for Sprint 3 must be performed against the hybrid topology, not the discrete one. The Sprint 3 identifiability deliverable inherits this constraint.

These three disagreements are the *first questions* the next cohort will see when the L08 hybrid encoding reaches the BN-integration sprint, in keeping with the methodological commitment of Sprints 1 and 2 to inherit a contested system rather than a finished one.

---

## 6. References

Hartig, T., Korpela, K., Evans, G. W., & Gärling, T. (1997). A measure of restorative quality in environments. *Scandinavian Housing and Planning Research*, *14*(4), 175–194.

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, *47*(2), 263–291.

Kaplan, R., & Kaplan, S. (1989). *The experience of nature: A psychological perspective*. Cambridge University Press.

Koller, D., & Friedman, N. (2009). *Probabilistic graphical models: Principles and techniques*. MIT Press.

Krosnick, J. A., & Presser, S. (2010). Question and questionnaire design. In P. V. Marsden & J. D. Wright (Eds.), *Handbook of survey research* (2nd ed., pp. 263–313). Emerald.

Lauritzen, S. L. (1992). Propagation of probabilities, means, and variances in mixed graphical association models. *Journal of the American Statistical Association*, *87*(420), 1098–1108.

Spohn, W. (2012). *The laws of belief: Ranking theory and its philosophical applications*. Oxford University Press.

---

*End of resolution.*
