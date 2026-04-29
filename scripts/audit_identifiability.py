#!/usr/bin/env python3
"""TRS Sprint 3 — Layer-level identifiability audit (Goodman & Hwang, 1988).

Implements the information-bound check option (C) from Sprint 3 contest #3:

  Per-latent rule:    |compute_from(L)|  >=  ceil(log2(|states(L)|))
  Layer-level rule:   |union of compute_from across all latents|
                       >=  4 * sum(ceil(log2(|states(L)|)))

The rules are *necessary* but not sufficient conditions for identifiability
in the Goodman & Hwang (1988) sense; they decouple from CPT estimation, which
is appropriate for Sprint 3 (CPTs are not yet estimated). Sprint 4 will add
the full Goodman (1974) Jacobian rank check once estimated CPTs exist.

For categorical / latent_score latents, |states| is the size of the value
range. For ordinal Likert [0,4], |states| = 5. For binary, |states| = 2.
For continuous (post-Sprint-3 hybrid encoding of L08), we use |states| = 8
(a discretisation guard) for the bound calculation.

Usage:
    python3 scripts/audit_identifiability.py
    python3 scripts/audit_identifiability.py --json
    python3 scripts/audit_identifiability.py --evidence-role latent

Exit codes: 0 pass, 1 fail, 2 registry error.
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"
REPORTS_DIR = REPO / "reports"

LAYER_COVERAGE_FACTOR = 4  # union of compute_from must be >= 4 * sum(log2|states|)


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


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.add_argument("--evidence-role", default="latent")
    p.add_argument("--save-report", action="store_true",
                   help="Save full report to reports/identifiability_audit_{date}.json")
    args = p.parse_args()

    if not REGISTRY.exists():
        print(f"NO-GO: registry not found", file=sys.stderr); return 2
    with REGISTRY.open() as f: reg = json.load(f)
    result = audit(reg, args.evidence_role)

    if args.save_report:
        REPORTS_DIR.mkdir(exist_ok=True)
        out = REPORTS_DIR / f"identifiability_audit_{datetime.now().strftime('%Y-%m-%d')}.json"
        with out.open("w") as f: json.dump(result, f, indent=2)
        print(f"Report saved to {out}")

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
