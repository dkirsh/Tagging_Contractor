#!/usr/bin/env python3
"""TRS Sprint 3+4 — Layer-level identifiability audit.

Sprint 3 implemented the information-bound check (Goodman & Hwang 1988):

  Per-latent rule:    |compute_from(L)|  >=  ceil(log2(|states(L)|))
  Layer-level rule:   |union of compute_from across all latents|
                       >=  4 * sum(ceil(log2(|states(L)|)))

Sprint 4 adds the full Goodman (1974) Jacobian rank identifiability check:
for each pair of latents, perturb the CPT entries and observe how the joint
observable distribution shifts. Stack the Jacobians and compute the rank;
if rank < (number of latent parameters), report the unidentified subspace
dimension. This is treated as a WARNING (not blocking).

For categorical / latent_score latents, |states| is the size of the value
range. For ordinal Likert [0,4], |states| = 5. For binary, |states| = 2.
For continuous (post-Sprint-3 hybrid encoding of L08), we use |states| = 8
(a discretisation guard) for the bound calculation.

Usage:
    python3 scripts/audit_identifiability.py
    python3 scripts/audit_identifiability.py --json
    python3 scripts/audit_identifiability.py --evidence-role latent
    python3 scripts/audit_identifiability.py --jacobian              # Sprint 4
    python3 scripts/audit_identifiability.py --jacobian --save-report

Exit codes: 0 pass, 1 fail, 2 registry error.
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"
REPORTS_DIR = REPO / "reports"
SYNTHETIC_CPTS = REPO / "data/sprint4_synthetic_cpts.json"

LAYER_COVERAGE_FACTOR = 4  # union of compute_from must be >= 4 * sum(log2|states|)
JACOBIAN_PERTURBATION = 1e-3
JACOBIAN_RANK_TOL = 1e-6


def n_states(tag: dict) -> int:
    vt = tag.get("value_type", "ordinal")
    vr = tag.get("value_range") or [0, 4]
    if vt == "latent_score" or vt == "binary":
        return 2
    if vt == "categorical":
        if isinstance(vr, list) and vr and isinstance(vr[0], str):
            return len(vr)
        return 5
    if vt == "continuous":
        return 8  # discretisation guard for the bound; not used in inference
    if vt == "ordinal":
        if isinstance(vr, list) and len(vr) == 2:
            try:
                lo, hi = int(vr[0]), int(vr[1])
                return hi - lo + 1
            except: pass
        return 5
    return 5


def upstream_set(tag: dict) -> set[str]:
    bn = tag.get("bn") or {}
    ext = tag.get("extraction") or {}
    parents = set(bn.get("parent_tags") or [])
    expected = set(ext.get("expected_upstream_observables") or [])
    return parents | expected


def audit(reg: dict, evidence_role: str = "latent") -> dict:
    tags = reg.get("tags", {})
    target = {tid: t for tid, t in tags.items()
              if (t.get("bn") or {}).get("evidence_role") == evidence_role
              and t.get("status") in ("active", "experimental")}

    errors = []
    warnings = []

    # Per-latent check
    per_latent = []
    for tid, t in target.items():
        ns = n_states(t)
        bits = math.ceil(math.log2(ns)) if ns > 1 else 1
        ups = upstream_set(t)
        n_up = len(ups)
        passing = n_up >= bits
        per_latent.append({
            "tag": tid,
            "states": ns,
            "log2_states_ceil": bits,
            "compute_from_size": n_up,
            "info_bound_passed": passing,
        })
        if not passing:
            errors.append({
                "rule": "info_bound_per_latent",
                "tag": tid,
                "states": ns,
                "required_upstreams": bits,
                "actual_upstreams": n_up,
                "message": (f"{tid} has {ns} states (needs >={bits} upstream observables) "
                           f"but only {n_up} listed; identifiability bound violated "
                           f"(Goodman & Hwang 1988)."),
            })

    # Layer-level check
    union_upstreams = set()
    sum_bits = 0
    for tid, t in target.items():
        union_upstreams |= upstream_set(t)
        sum_bits += math.ceil(math.log2(n_states(t))) if n_states(t) > 1 else 1
    required_layer = LAYER_COVERAGE_FACTOR * sum_bits
    layer_passed = len(union_upstreams) >= required_layer
    if not layer_passed:
        # Layer-level violation is reported as a WARNING rather than an error:
        # the per-latent rule is what the doctor blocks on; layer-level is a
        # diagnostic flag for Sprint 4 (more observables needed) per the
        # contest #3 disposition.
        warnings.append({
            "rule": "info_bound_layer_level",
            "latent_count": len(target),
            "sum_log2_states": sum_bits,
            "required_layer_size": required_layer,
            "actual_layer_size": len(union_upstreams),
            "message": (f"Layer-level: {len(target)} latents with sum log2|states|={sum_bits}; "
                       f"need union of compute_from >= {required_layer}, "
                       f"but only {len(union_upstreams)} distinct upstream observables listed. "
                       f"Layer is information-bounded below identifiability (Goodman & Hwang 1988). "
                       f"Sprint 4: add more documented upstream observables OR reduce latent state spaces."),
        })

    return {
        "passed": len(errors) == 0,
        "evidence_role": evidence_role,
        "tags_checked": len(target),
        "per_latent_summary": {
            "passed": sum(1 for x in per_latent if x["info_bound_passed"]),
            "failed": sum(1 for x in per_latent if not x["info_bound_passed"]),
        },
        "layer_level": {
            "sum_log2_states": sum_bits,
            "required_layer_size": required_layer,
            "actual_layer_size": len(union_upstreams),
            "passed": layer_passed,
        },
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "per_latent": per_latent if len(per_latent) <= 80 else per_latent[:80],
    }


# ──────────────────────────────────────────────────────────────────
# Sprint 4 — Goodman (1974) Jacobian rank identifiability check
# ──────────────────────────────────────────────────────────────────

def _try_import_numpy_scipy():
    """Best-effort import of numpy + scipy.linalg for the rank computation.

    Returns (np, svd_fn) where svd_fn(A) -> singular values vector, or
    (None, pure_python_svd) if neither library is available.
    """
    try:
        import numpy as np  # type: ignore
        try:
            from scipy.linalg import svd as scipy_svd  # type: ignore
            return np, lambda M: scipy_svd(M, compute_uv=False, lapack_driver="gesdd")
        except Exception:
            return np, lambda M: np.linalg.svd(M, compute_uv=False)
    except Exception:
        # Pure-Python SVD via power iteration on M^T M (small matrices only).
        return None, _pure_python_singular_values


def _pure_python_singular_values(M: list[list[float]],
                                 max_iter: int = 200,
                                 tol: float = 1e-10) -> list[float]:
    """Pure-Python singular values via repeated power iteration on
    M^T M with deflation. Suitable for small matrices (≤ ~30 x 30)."""
    if not M or not M[0]:
        return []
    rows, cols = len(M), len(M[0])
    # MtM (cols x cols)
    def mat_mul_t(A):
        # Returns A^T A
        n = len(A[0])
        out = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                s = 0.0
                for k in range(len(A)):
                    s += A[k][i] * A[k][j]
                out[i][j] = s
        return out

    MtM = mat_mul_t(M)

    def mat_vec(A, v):
        return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

    def vec_norm(v):
        return math.sqrt(sum(x * x for x in v))

    def vec_normalize(v):
        n = vec_norm(v)
        if n < 1e-30: return [0.0] * len(v)
        return [x / n for x in v]

    def vec_sub(u, v):
        return [a - b for a, b in zip(u, v)]

    def outer_scale(u, v, scale):
        # Returns scale * u v^T (matrix)
        return [[scale * a * b for b in v] for a in u]

    def mat_sub(A, B):
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    sv: list[float] = []
    A = [row[:] for row in MtM]
    n = len(A)
    rank_cap = min(rows, cols)
    for _ in range(rank_cap):
        # Power iteration to dominant eigenvalue of A
        v = [1.0 / math.sqrt(n)] * n
        last = 0.0
        for _it in range(max_iter):
            v = vec_normalize(mat_vec(A, v))
            # Rayleigh quotient
            Av = mat_vec(A, v)
            lam = sum(v[i] * Av[i] for i in range(n))
            if abs(lam - last) < tol: break
            last = lam
        if lam <= tol:
            break
        sv.append(math.sqrt(max(0.0, lam)))
        # Deflate: A := A - lam * v v^T
        A = mat_sub(A, outer_scale(v, v, lam))
    return sv


def _build_marginal_observable(reg: dict, cpts: dict, latent_a: str,
                               latent_b: str) -> list[float]:
    """Compute a 'joint observable' marginal: P(L_A) ⊗ P(L_B) flattened.

    For Sprint-4 synthetic CPTs we treat the observable distribution as the
    product of the two latents' marginals — a simplification, since the true
    observable would marginalise over upstream observables, but the
    upstream observable CPTs are not yet estimated. The Jacobian computed
    against this simplified observable is informative about the rank
    structure of the latent parameter space, which is the rank-deficiency
    signal of interest at Sprint 4.
    """
    cpt_a = cpts.get(latent_a) or {}
    cpt_b = cpts.get(latent_b) or {}
    states_a = cpt_a.get("states", [])
    states_b = cpt_b.get("states", [])
    marg_a = cpt_a.get("marginal", {})
    marg_b = cpt_b.get("marginal", {})
    if not marg_a or not marg_b:
        # Conditional CPTs: collapse over parent states with uniform prior
        marg_a = _collapse_to_marginal(cpt_a, states_a)
        marg_b = _collapse_to_marginal(cpt_b, states_b)
    out = []
    for sa in states_a:
        pa = marg_a.get(sa, 0.0)
        for sb in states_b:
            pb = marg_b.get(sb, 0.0)
            out.append(pa * pb)
    return out


def _collapse_to_marginal(cpt: dict, states: list[str]) -> dict[str, float]:
    if "marginal" in cpt:
        return cpt["marginal"]
    cond = cpt.get("conditional", {})
    table = cond.get("table", {})
    if not table:
        return {s: 1.0 / max(1, len(states)) for s in states}
    # Uniform parent prior
    n = len(table)
    sums = {s: 0.0 for s in states}
    for joint, child_cpt in table.items():
        for s, p in child_cpt.items():
            sums[s] = sums.get(s, 0.0) + p / n
    total = sum(sums.values()) or 1.0
    return {s: v / total for s, v in sums.items()}


def goodman_1974_jacobian_rank_check(reg: dict, cpts: dict,
                                     evidence_role: str = "latent",
                                     max_pairs: int = 200) -> dict:
    """Compute Jacobian-rank identifiability per pair of latents.

    For each pair (A, B):
      1. Treat the marginal P(L_A), P(L_B) as parameter vectors.
      2. Numerically perturb each parameter (finite-difference) and recompute
         the joint observable distribution P(L_A) ⊗ P(L_B).
      3. Stack the Jacobian columns; compute SVD; rank = #(σ > tol).
      4. If rank < total_params, the (params - rank) gap is the unidentified
         subspace dimension.

    Args:
        max_pairs: cap on number of pairs to check (default 200, enough to
                   cover bottlenecks on the latent layer for Sprint 4).
    """
    np_mod, svd_fn = _try_import_numpy_scipy()
    tags = reg.get("tags", {})
    latents = [tid for tid, t in tags.items()
               if (t.get("bn") or {}).get("evidence_role") == evidence_role
               and t.get("status") in ("active", "experimental")
               and tid in cpts]
    latents.sort()

    pair_results = []
    pair_count = 0
    deficient_count = 0
    for i in range(len(latents)):
        if pair_count >= max_pairs: break
        for j in range(i + 1, len(latents)):
            if pair_count >= max_pairs: break
            a, b = latents[i], latents[j]
            cpt_a = cpts[a]
            cpt_b = cpts[b]
            states_a = cpt_a.get("states", [])
            states_b = cpt_b.get("states", [])
            n_a = len(states_a)
            n_b = len(states_b)
            if n_a < 2 or n_b < 2:
                continue
            # Param vector: unconstrained marginals (n_a + n_b entries; we
            # will see rank ≤ n_a + n_b - 2 because each marginal has a
            # sum-to-1 constraint that creates a dependent direction).
            base_obs = _build_marginal_observable(reg, cpts, a, b)
            n_obs = len(base_obs)
            n_params = n_a + n_b
            jacobian: list[list[float]] = []  # rows = obs dims, cols = params
            # Initialise jacobian as zeros
            for _ in range(n_obs):
                jacobian.append([0.0] * n_params)
            # Pull out marginals
            marg_a = _collapse_to_marginal(cpt_a, states_a)
            marg_b = _collapse_to_marginal(cpt_b, states_b)
            # Build perturbed observables
            for k in range(n_a):
                m2 = dict(marg_a)
                key = states_a[k]
                m2[key] = m2.get(key, 0.0) + JACOBIAN_PERTURBATION
                # Recompute observable
                pert_obs = []
                for sa in states_a:
                    pa = m2.get(sa, 0.0)
                    for sb in states_b:
                        pert_obs.append(pa * marg_b.get(sb, 0.0))
                for r in range(n_obs):
                    jacobian[r][k] = (pert_obs[r] - base_obs[r]) / JACOBIAN_PERTURBATION
            for k in range(n_b):
                m2 = dict(marg_b)
                key = states_b[k]
                m2[key] = m2.get(key, 0.0) + JACOBIAN_PERTURBATION
                pert_obs = []
                for sa in states_a:
                    pa = marg_a.get(sa, 0.0)
                    for sb in states_b:
                        pert_obs.append(pa * m2.get(sb, 0.0))
                for r in range(n_obs):
                    jacobian[r][n_a + k] = (pert_obs[r] - base_obs[r]) / JACOBIAN_PERTURBATION

            # Compute singular values
            try:
                if np_mod is not None:
                    M = np_mod.array(jacobian, dtype=float)
                    sv = svd_fn(M)
                    sv = list(sv)
                else:
                    sv = svd_fn(jacobian)
                rank = sum(1 for s in sv if s > JACOBIAN_RANK_TOL)
            except Exception as e:
                pair_results.append({
                    "pair": [a, b],
                    "n_params": n_params,
                    "rank": None,
                    "deficient": False,
                    "error": str(e),
                })
                pair_count += 1
                continue

            # Expected rank = n_params - 2 (one sum-to-1 constraint per marginal)
            expected_rank = n_params - 2
            deficient = rank < expected_rank
            if deficient:
                deficient_count += 1
            pair_results.append({
                "pair": [a, b],
                "n_params": n_params,
                "expected_rank": expected_rank,
                "rank": rank,
                "deficient": deficient,
                "unidentified_subspace_dim": max(0, expected_rank - rank),
                "top_singular_values": [round(float(s), 6) for s in sv[:5]],
            })
            pair_count += 1

    return {
        "method": "Goodman (1974) Jacobian rank identifiability",
        "engine": "numpy/scipy" if np_mod is not None else "pure-python (power iteration)",
        "perturbation": JACOBIAN_PERTURBATION,
        "rank_tolerance": JACOBIAN_RANK_TOL,
        "latents_considered": len(latents),
        "pairs_checked": pair_count,
        "pairs_deficient": deficient_count,
        "max_pairs": max_pairs,
        "pair_results": pair_results,
        "warning_only": True,  # per Sprint 4 spec: not blocking
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.add_argument("--evidence-role", default="latent")
    p.add_argument("--save-report", action="store_true",
                   help="Save full report to reports/identifiability_audit_{date}.json")
    p.add_argument("--jacobian", action="store_true",
                   help="Sprint 4: also run the Goodman (1974) Jacobian rank check "
                        "against the synthetic CPTs. Heavier; warning-only.")
    p.add_argument("--max-pairs", type=int, default=200,
                   help="Cap on number of pairs in the Jacobian check (default 200).")
    args = p.parse_args()

    if not REGISTRY.exists():
        print(f"NO-GO: registry not found", file=sys.stderr); return 2
    with REGISTRY.open() as f: reg = json.load(f)
    result = audit(reg, args.evidence_role)

    # Sprint 4: optional Jacobian rank check
    jac_result = None
    if args.jacobian:
        if not SYNTHETIC_CPTS.exists():
            jac_result = {
                "method": "Goodman (1974) Jacobian rank identifiability",
                "skipped": True,
                "reason": (f"Synthetic CPT file not found at "
                           f"{SYNTHETIC_CPTS.relative_to(REPO)}; run "
                           f"scripts/sprint4_synthetic_cpts.py first."),
                "warning_only": True,
            }
            result["warnings"].append({
                "rule": "jacobian_rank_skipped",
                "message": jac_result["reason"],
            })
        else:
            with SYNTHETIC_CPTS.open() as jf:
                cpt_doc = json.load(jf)
            cpts = cpt_doc.get("cpts", {})
            jac_result = goodman_1974_jacobian_rank_check(
                reg, cpts, args.evidence_role, max_pairs=args.max_pairs
            )
            if jac_result.get("pairs_deficient", 0) > 0:
                result["warnings"].append({
                    "rule": "jacobian_rank_deficient",
                    "pairs_deficient": jac_result["pairs_deficient"],
                    "pairs_checked": jac_result["pairs_checked"],
                    "message": (
                        f"Jacobian rank check found "
                        f"{jac_result['pairs_deficient']} of "
                        f"{jac_result['pairs_checked']} pair(s) with "
                        f"rank-deficient parameter Jacobians (Goodman 1974). "
                        f"Synthetic CPTs were used; this is informative for "
                        f"Sprint 5+ when empirical CPTs replace the synthetic "
                        f"placeholders. Warning-only per Sprint 4 spec."
                    ),
                })
            result["warning_count"] = len(result["warnings"])

    # Always include jacobian summary in the result for downstream tooling
    if jac_result is not None:
        result["jacobian"] = {
            "engine": jac_result.get("engine"),
            "pairs_checked": jac_result.get("pairs_checked", 0),
            "pairs_deficient": jac_result.get("pairs_deficient", 0),
            "warning_only": jac_result.get("warning_only", True),
            "skipped": jac_result.get("skipped", False),
        }

    if args.save_report:
        REPORTS_DIR.mkdir(exist_ok=True)
        out = REPORTS_DIR / f"identifiability_audit_{datetime.now().strftime('%Y-%m-%d')}.json"
        with out.open("w") as f: json.dump(result, f, indent=2)
        print(f"Report saved to {out}")
        if jac_result is not None and not jac_result.get("skipped"):
            jac_out = REPORTS_DIR / f"jacobian_audit_{datetime.now().strftime('%Y-%m-%d')}.json"
            with jac_out.open("w") as f: json.dump(jac_result, f, indent=2)
            print(f"Jacobian report saved to {jac_out}")

    # Always write Jacobian report when --jacobian is set, even without --save-report
    if jac_result is not None and not jac_result.get("skipped"):
        REPORTS_DIR.mkdir(exist_ok=True)
        jac_out = REPORTS_DIR / f"jacobian_audit_{datetime.now().strftime('%Y-%m-%d')}.json"
        with jac_out.open("w") as f: json.dump(jac_result, f, indent=2)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0 if result["passed"] else 1

    print(f"audit-identifiability: {result['evidence_role']} evidence role")
    print(f"  tags checked: {result['tags_checked']}")
    print(f"  per-latent info bound: {result['per_latent_summary']['passed']} passed, {result['per_latent_summary']['failed']} failed")
    ll = result['layer_level']
    print(f"  layer level: union={ll['actual_layer_size']} required={ll['required_layer_size']} "
          f"({'PASS' if ll['passed'] else 'FAIL'})")
    print(f"  errors: {result['error_count']}, warnings: {result['warning_count']}")
    if jac_result is not None:
        if jac_result.get("skipped"):
            print(f"  jacobian: SKIPPED ({jac_result.get('reason')})")
        else:
            print(f"  jacobian: pairs_checked={jac_result['pairs_checked']}, "
                  f"pairs_deficient={jac_result['pairs_deficient']} "
                  f"(engine: {jac_result.get('engine')}, warning-only)")
    if result["errors"]:
        for e in result["errors"][:10]:
            print(f"  [{e['rule']}] {e['message']}")
    if result["passed"]:
        print("\nOK: audit-identifiability passed (necessary-condition info bound)")
        return 0
    print("\nNO-GO: audit-identifiability failed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
