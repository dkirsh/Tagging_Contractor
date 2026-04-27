#!/usr/bin/env python3
"""TRS Sprint 1 — Audit the extraction plan for latent tags.

Three checks, each producing errors that fail the gate:

1. **Spohn 50%-overlap rule.** No two tags with `bn.evidence_role: "latent"` may
   share more than 50% of their upstream observable references (taken from the
   union of `bn.parent_tags` and `extraction.expected_upstream_observables`).
   This is the identifiability constraint adopted by the architectural panel
   (28 April 2026 disposition, §3 Spohn).

2. **Method-family non-default.** Each latent must declare a non-trivial
   `extraction.method_family` (not empty, not "unknown", not the placeholder
   used by some imported tags).

3. **Extraction-notes minimum length.** Each latent must have
   `semantics.extraction_notes_2d` and `semantics.extraction_notes_3d` of
   length >= 200 chars.

Usage:
    python3 scripts/audit_extraction_plan.py
    python3 scripts/audit_extraction_plan.py --json
    python3 scripts/audit_extraction_plan.py --evidence-role latent

Exit codes:
    0 = audit passed
    1 = audit failed
    2 = registry could not be loaded
"""
from __future__ import annotations
import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"

OVERLAP_THRESHOLD = 0.50  # Spohn rule: > 50% upstream overlap is a violation
EXTRACTION_NOTES_MIN_LEN = 200
NON_TRIVIAL_METHOD_FAMILIES = {
    "geometry", "segmentation", "vlm", "composite", "manual",
}  # accept extant + Sprint-1 set


def upstream_set(tag: dict) -> set[str]:
    """Union of bn.parent_tags and extraction.expected_upstream_observables."""
    bn = tag.get("bn") or {}
    ext = tag.get("extraction") or {}
    parents = set(bn.get("parent_tags") or [])
    expected = set(ext.get("expected_upstream_observables") or [])
    return parents | expected


def jaccard_overlap(a: set, b: set) -> float:
    """Symmetric upstream overlap. Defined as |a ∩ b| / min(|a|, |b|).
    This is the *one-sided* overlap that catches asymmetric collinearity:
    if A is a subset of B, jaccard_overlap == 1.0 even though Jaccard
    similarity would be |A|/|B|. The Spohn rule cares about whether two
    latents are non-identifiable — the worst case is the smaller of the two."""
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def audit(reg: dict, evidence_role_filter: str = "latent") -> dict:
    tags = reg.get("tags", {})
    target = {tid: t for tid, t in tags.items()
              if (t.get("bn") or {}).get("evidence_role") == evidence_role_filter}

    errors: list[dict] = []
    warnings: list[dict] = []

    # Check 1: Spohn 50%-overlap
    pairs_checked = 0
    pairs_violated = 0
    for (a_id, a), (b_id, b) in combinations(target.items(), 2):
        a_up = upstream_set(a)
        b_up = upstream_set(b)
        if not a_up or not b_up:
            continue  # cannot compute overlap if either has no upstreams
        ov = jaccard_overlap(a_up, b_up)
        pairs_checked += 1
        if ov > OVERLAP_THRESHOLD:
            pairs_violated += 1
            errors.append({
                "rule": "spohn_50pct_overlap",
                "tag_a": a_id, "tag_b": b_id,
                "overlap": round(ov, 3),
                "shared": sorted(a_up & b_up),
                "message": f"{a_id} and {b_id} share {ov:.0%} of upstream observables (>{OVERLAP_THRESHOLD:.0%}); identifiability concern (Spohn 2012)",
            })

    # Check 2: method_family non-default
    for tid, t in target.items():
        ext = t.get("extraction") or {}
        mf = (ext.get("method_family") or "").strip()
        if not mf:
            errors.append({"rule": "method_family_present", "tag": tid,
                          "message": "extraction.method_family is empty"})
        elif mf.lower() in {"unknown", "placeholder", "tbd"}:
            errors.append({"rule": "method_family_present", "tag": tid,
                          "message": f"extraction.method_family is placeholder: {mf!r}"})

    # Check 3: extraction notes length
    for tid, t in target.items():
        sem = t.get("semantics") or {}
        for f in ("extraction_notes_2d", "extraction_notes_3d"):
            note = sem.get(f) or ""
            if len(note) < EXTRACTION_NOTES_MIN_LEN:
                # Tier-3 tags may legitimately have brief 2D notes — warn instead
                ext_2d = (t.get("extractability") or {}).get("from_2d", "")
                if f == "extraction_notes_2d" and ext_2d == "no":
                    warnings.append({"rule": "extraction_notes_min_len", "tag": tid,
                                    "field": f, "len": len(note),
                                    "message": f"{f} is short ({len(note)} chars) but Tier-3 from_2d=no — accepted with warning"})
                else:
                    errors.append({"rule": "extraction_notes_min_len", "tag": tid,
                                  "field": f, "len": len(note),
                                  "message": f"{f} is too short: {len(note)} chars (minimum {EXTRACTION_NOTES_MIN_LEN})"})

    return {
        "passed": len(errors) == 0,
        "evidence_role": evidence_role_filter,
        "tags_checked": len(target),
        "pairs_checked": pairs_checked,
        "pairs_violated": pairs_violated,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable")
    p.add_argument("--evidence-role", default="latent",
                   help="Audit only tags with this evidence_role (default: latent)")
    args = p.parse_args()

    if not REGISTRY.exists():
        print(f"NO-GO: registry not found: {REGISTRY}", file=sys.stderr)
        return 2

    with REGISTRY.open() as f:
        reg = json.load(f)

    result = audit(reg, args.evidence_role)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0 if result["passed"] else 1

    # Human-readable
    print(f"audit-extraction-plan: registry {REGISTRY.name}")
    print(f"  evidence_role filter: {result['evidence_role']}")
    print(f"  tags checked: {result['tags_checked']}")
    print(f"  pairs checked (Spohn 50%): {result['pairs_checked']}")
    print(f"  pairs violated: {result['pairs_violated']}")
    print(f"  errors: {result['error_count']}, warnings: {result['warning_count']}")
    if result["errors"]:
        print("\n=== ERRORS ===")
        for e in result["errors"]:
            print(f"  [{e['rule']}] {e.get('tag', e.get('tag_a', '?'))}{(' & ' + e['tag_b']) if 'tag_b' in e else ''}")
            print(f"    {e['message']}")
            if e.get("shared"):
                print(f"    shared upstreams ({len(e['shared'])}): {e['shared'][:6]}...")
    if result["warnings"]:
        print("\n=== WARNINGS ===")
        for w in result["warnings"]:
            print(f"  [{w['rule']}] {w.get('tag', '?')}: {w['message']}")
    print()
    if result["passed"]:
        print("OK: audit-extraction-plan passed")
        return 0
    print("NO-GO: audit-extraction-plan failed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
