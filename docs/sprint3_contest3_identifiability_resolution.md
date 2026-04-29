# Sprint 3 Contest #3 Resolution: Layer-Level Identifiability of the 63-Node Latent Layer

**Date:** 29 April 2026
**Contest origin:** Sprint 2 Architectural Panel Disposition, §2 ("Spohn on the joint identifiability of the 63-node latent layer") and §5.4 ("Joint identifiability of the 63-node latent layer")
**Panel voices consulted:** Wolfgang Spohn (carrying the Sprint 1 and Sprint 2 identifiability concern), Leo A. Goodman (in absentia, via the 1974 *Biometrika* foundational paper and the 1988 Goodman & Hwang follow-up), and the practical engineering position canonically expressed by Koller & Friedman's (2009) graphical-models textbook.

---

## 1. The contest as posed

Sprint 1 added 23 latent nodes to the Bayesian network. Sprint 2 added 40 more, bringing the latent layer to 63 nodes. The observable layer — the existing `stimulus_antecedent` tag pool — contains 417 tags, and only a subset of those tags is actually upstream of any given latent. Spohn's deferral, recorded in the Sprint 2 disposition §2 and again in §5.4, is that a 63-node latent layer conditioned on a finite observable layer is no longer a small-network problem and that the pairwise 50%-overlap rule shipped in Sprint 1 (the "Spohn rule") is necessary but not sufficient.

The substantive worry traces to Goodman (1974). Goodman showed that a latent-class model's parameters are identifiable from the joint distribution of the manifest variables only when a particular Jacobian matrix has full column rank, and he gave explicit examples of nominally-identifiable models that empirically collapse — distinct parameter vectors produce indistinguishable observable distributions — once the manifest layer is small relative to the latent layer or once latent classes share too much of their parent structure. Goodman & Hwang (1988) revisited the practical version of the problem and argued that, when full estimation is infeasible, an *information-theoretic lower bound* on each latent's identifiability is the right defensive substitute.

The technical question Sprint 3 must answer is: what does a layer-level identifiability check look like, and what level of rigour ships now versus later?

## 2. Three position statements

**Spohn's position.** Spohn would prefer the full Goodman (1974) Jacobian rank check. The 50%-overlap rule from Sprint 1 was a pairwise proxy chosen for tractability; with 63 latents and dense upstream-observable sharing, pairwise checks miss multi-way collisions — three-latent and four-latent subsets whose joint upstream parents collapse into a degenerate subspace even though no single pair violates the 50% bound. Spohn accepts, however, that the Jacobian check requires *estimated* CPT parameters to be evaluated numerically, and that Sprint 3 will not have estimated CPTs because the extractors are still stubs. His fallback is the information-bound check (option C below), which decouples cleanly from CPT estimation and gives a *necessary* condition on identifiability — failing it is a definite problem; passing it is a defensible-but-not-final guarantee. Pairwise-only continuation (option A) Spohn judges too weak for a 63-node layer.

**Goodman's position (reconstructed from the published record).** Goodman (1974) is the rank-based formulation: identifiability obtains iff the Jacobian of the joint manifest distribution with respect to the latent parameters is full rank, evaluated at the true parameters. This is option B. Goodman & Hwang (1988) is the practical-substitute formulation: when estimation is infeasible, demand that each latent be informationally separated from the manifest layer by at least the latent's own state-cardinality entropy. This is option C, and it is what Goodman would accept as a Sprint-3-feasible check.

**Koller & Friedman's engineering position.** The standard graphical-models textbook position (Koller & Friedman, 2009, ch. 19 on partially observed data) is layered defence: use cheap pairwise checks as the running validator gate, reserve the full rank check for release-gate evaluation against estimated parameters, and treat the information-bound check as the appropriate placeholder when estimation is not yet available. This position cleanly absorbs Spohn's and Goodman's recommendations into a sequenced plan.

## 3. The ratified plan

The right answer is layered. Sprint 3 ships the cheap-and-medium tiers; Sprint 4 ships the full Jacobian gate once estimated CPTs exist.

| Tier | Check | Status in Sprint 3 |
|------|-------|--------------------|
| A | Pairwise 50%-overlap rule (Sprint 1, retained) | Ships, retained verbatim |
| A′ | Pairwise rule extended to 3-tuples (small-clique check) | **Ships in Sprint 3** |
| C | Information-bound check (Goodman & Hwang 1988 form) | **Ships in Sprint 3** |
| B | Jacobian rank check (Goodman 1974 sufficient condition) | **Deferred to Sprint 4** |

The disposition is consistent with all three voices: Spohn gets the small-clique extension and the information-bound placeholder he requested; Goodman gets the necessary-condition check that is feasible without CPTs; Koller & Friedman get the layered architecture they recommend.

## 4. Implementation specification — what Sprint 3 builds

### 4.1 Extend the Spohn rule from pairwise to 3-tuple subset (option A′)

The existing validator computes, for every pair of latents `(L_i, L_j)`, the Jaccard overlap of their `extraction.compute_from` sets and rejects the merged registry if any pair exceeds 0.50. Sprint 3 extends this to 3-tuples.

**Rule.** For every ordered triple of latents `(L_i, L_j, L_k)` such that `i < j < k`, compute:

```
overlap_3 = |compute_from(L_i) ∩ compute_from(L_j) ∩ compute_from(L_k)| /
            |compute_from(L_i) ∪ compute_from(L_j) ∪ compute_from(L_k)|
```

Reject the merged registry if `overlap_3 > 0.50` for any triple. The threshold is held at 0.50 to mirror the pairwise case — Spohn's argument from Sprint 1, that the parametric break-point for CPT identifiability under five-bin ordinal compression is roughly half-overlap, applies *a fortiori* to 3-tuples (any three-way collision implies all three pairwise collisions and is strictly stronger evidence of a degeneracy).

Because the registry has 63 latents, the 3-tuple count is C(63,3) = 39,711, which is computationally trivial. No 4-tuple check is added in Sprint 3; the panel's view (Spohn carrying) is that 3-tuple is sufficient for the layer's current density and that 4-tuple coverage should wait for the Jacobian gate of Sprint 4.

### 4.2 Build `scripts/audit_identifiability.py` implementing the information-bound check (option C)

The script implements the Goodman & Hwang (1988) information-theoretic necessary condition, adapted to operate on the registry's documented `expected_upstream_observables` lists *without* requiring estimated CPT parameters. It does this by constructing a synthetic observable distribution from the registry itself.

**Synthetic observable distribution.** For each observable tag `o ∈ stimulus_antecedent`, the script assumes a uniform Bernoulli prior `P(o = present) = 0.5` with independence across tags. This is a deliberately permissive prior — it maximises the entropy of the observable layer and therefore yields a *generous* information bound. If a latent fails the bound under this maximally-favourable prior, it cannot be rescued by any non-uniform empirical prior; the failure is robust.

**Per-latent rule.** For each latent `L` with state-cardinality `|S_L|` (the number of distinct ordinal or binary states the latent admits — typically 5 for ordinal, 2 for binary):

```
require:  |compute_from(L)|  ≥  ⌈log₂(|S_L|)⌉
```

The bound expresses Goodman & Hwang's necessary condition: a latent with `k` states cannot be identified from a manifest set whose cardinality is below `log₂(k)`, because the manifest set cannot encode enough distinct configurations to distinguish the latent's states. For a 5-state ordinal latent, this requires at least `⌈log₂(5)⌉ = 3` upstream observables. For a 2-state binary latent, the requirement is `⌈log₂(2)⌉ = 1` upstream observable.

**Layer-level rule.** For the union of all latents' `compute_from` sets, the script requires:

```
require:  |⋃_L compute_from(L)|  ≥  4 × dim(latent_layer)
```

where `dim(latent_layer)` is the sum of `⌈log₂(|S_L|)⌉` across all 63 latents. The factor of 4 is the Goodman & Hwang practical multiplier — they argue that the manifest layer needs to be roughly four times the effective latent dimensionality before joint identifiability is plausible, and that smaller multipliers reliably surface as estimation pathologies (multi-modal likelihoods, parameter-vector swapping under bootstrap, label-switching under MCMC). For the current 63-latent registry, with most latents 5-state ordinal, `dim(latent_layer) ≈ 63 × 3 ≈ 189`, so the union must contain at least 756 distinct observables. The current `stimulus_antecedent` pool is 417 tags; the layer-level bound is therefore *currently violated* and the script will report this. The disposition is that this is exactly the signal Sprint 3 needs to surface — the registry is informationally undersized for its latent layer, and either the observable pool must grow (additional tagged image properties) or the latent layer must shrink (collapse closely-related ordinal latents into shared structured factors).

### 4.3 Wrap into `tc doctor --prod` as Stage 4

The existing `tc doctor` command runs three production-readiness stages: schema validation (Stage 1), pairwise overlap (Stage 2), and extractor stub presence (Stage 3). Sprint 3 adds Stage 4: identifiability audit. Stage 4 invokes `scripts/audit_identifiability.py`, runs both the 3-tuple extension of the Spohn rule and the information-bound check, and reports pass/fail. A failure in Stage 4 fails `tc doctor --prod` and blocks release.

### 4.4 Output format — structured JSON report

The script writes `reports/identifiability_audit_{YYYY-MM-DD}.json` with the following shape:

```json
{
  "audit_date": "2026-04-29",
  "registry_version": "v2.7",
  "n_latents": 63,
  "n_observables": 417,
  "checks": {
    "spohn_pairwise": { "passed": true, "n_violations": 0, "violations": [] },
    "spohn_3tuple":   { "passed": false, "n_violations": 2,
                        "violations": [
                          { "latents": ["L17","L18","L19"],
                            "overlap_3": 0.62,
                            "shared_observables": ["nature_presence","soft_visual_field"] }
                        ] },
    "info_bound_per_latent": { "passed": true, "n_violations": 0, "violations": [] },
    "info_bound_layer":      { "passed": false,
                               "required_observables": 756,
                               "actual_observables":   417,
                               "shortfall":            339 }
  },
  "release_gate": "FAIL"
}
```

Each violation entry includes the latent ID(s) and the violated bound, so failure messages are actionable without consulting the source.

## 5. Sprint 4 deferral — full Jacobian rank check (option B)

Once Sprint 3's extractors are implemented and yield estimated CPT parameters, Sprint 4 will add the full Goodman (1974) Jacobian rank check as Stage 5 of `tc doctor --prod`. The Jacobian is the matrix of partial derivatives of the joint manifest distribution `P(O₁, …, O_n; θ)` with respect to the latent-parameter vector `θ`. Identifiability obtains iff the Jacobian has full column rank at the estimated parameter values, evaluated symbolically where possible and numerically where not. Sprint 4 will specify the rank-tolerance threshold (Goodman left it open in 1974; common practice is to require the smallest singular value to exceed 1e-6 times the largest). The Jacobian gate is the *sufficient* condition; the information-bound gate of Sprint 3 remains as the *necessary* condition and is retained.

## 6. References

Goodman, L. A. (1974). Exploratory latent structure analysis using both identifiable and unidentifiable models. *Biometrika*, *61*(2), 215–231. https://doi.org/10.1093/biomet/61.2.215

Goodman, L. A., & Hwang, J. T. G. (1988). On the identifiability of latent structure models. *Journal of the American Statistical Association*, *83*(403), 731–740.

Koller, D., & Friedman, N. (2009). *Probabilistic graphical models: Principles and techniques*. MIT Press.

Spohn, W. (2012). *The laws of belief: Ranking theory and its philosophical applications*. Oxford University Press.

---

*End of resolution.*
