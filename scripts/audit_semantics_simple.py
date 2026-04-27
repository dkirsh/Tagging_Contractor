#!/usr/bin/env python3
"""TRS Sprint 1 — Simple semantics-completeness audit for latent tags.

A lightweight alternative to the full tools/semantics_gate.py pipeline that
operates directly on the registry JSON and reports completeness for the
panel-required fields. Intended to be wrapped by `tc audit-semantics`.

Required semantic fields for any active latent tag (per panel disposition):
  - definition_short (>= 30 chars)
  - definition_long (>= 200 chars)
  - aliases (>= 3)
  - examples_positive (>= 6)
  - examples_negative (>= 4)
  - scope_includes (>= 3)
  - scope_excludes (>= 3)

Plus the panel-added fields on the tag root or notes:
  - notes.interaction_mode (focused/unfocused/mixed)
  - notes.cross_cultural_variance (low/medium/high)
  - notes.l_number (e.g., "L44")

Plus literature:
  - literature.key_refs (>= 1)

Usage:
    python3 scripts/audit_semantics_simple.py
    python3 scripts/audit_semantics_simple.py --json
    python3 scripts/audit_semantics_simple.py --evidence-role latent

Exit codes:
    0 = audit passed
    1 = audit failed
    2 = registry could not be loaded
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"

VALID_INTERACTION_MODE = {"focused", "unfocused", "mixed"}
VALID_CROSS_CULTURAL = {"low", "medium", "high"}


def length(x) -> int:
    """Length-or-zero for None-or-empty handling."""
    if x is None:
        return 0
    return len(x)


def audit(reg: dict, evidence_role_filter: str = "latent") -> dict:
    tags = reg.get("tags", {})
    target = {tid: t for tid, t in tags.items()
              if (t.get("bn") or {}).get("evidence_role") == evidence_role_filter
              and t.get("status") in ("active", "experimental")}

    errors: list[dict] = []
    warnings: list[dict] = []

    for tid, t in target.items():
        sem = t.get("semantics") or {}
        notes = t.get("notes") or {}
        lit = t.get("literature") or {}

        def err(field, msg):
            errors.append({"tag": tid, "field": field, "message": msg})

        def warn(field, msg):
            warnings.append({"tag": tid, "field": field, "message": msg})

        # definition_short
        ds = sem.get("definition_short") or ""
        if len(ds) < 30:
            err("semantics.definition_short", f"too short ({len(ds)} chars, minimum 30)")
        # definition_long
        dl = sem.get("definition_long") or ""
        if len(dl) < 200:
            err("semantics.definition_long", f"too short ({len(dl)} chars, minimum 200)")
        # aliases
        if length(sem.get("aliases")) < 3:
            err("semantics.aliases", f"too few aliases ({length(sem.get('aliases'))}, minimum 3)")
        # examples
        if length(sem.get("examples_positive")) < 6:
            err("semantics.examples_positive", f"too few ({length(sem.get('examples_positive'))}, minimum 6)")
        if length(sem.get("examples_negative")) < 4:
            err("semantics.examples_negative", f"too few ({length(sem.get('examples_negative'))}, minimum 4)")
        # scope
        if length(sem.get("scope_includes")) < 3:
            err("semantics.scope_includes", f"too few ({length(sem.get('scope_includes'))}, minimum 3)")
        if length(sem.get("scope_excludes")) < 3:
            err("semantics.scope_excludes", f"too few ({length(sem.get('scope_excludes'))}, minimum 3)")
        # panel-added required
        im = notes.get("interaction_mode")
        if im not in VALID_INTERACTION_MODE:
            err("notes.interaction_mode", f"invalid or missing: {im!r}")
        ccv = notes.get("cross_cultural_variance")
        if ccv not in VALID_CROSS_CULTURAL:
            err("notes.cross_cultural_variance", f"invalid or missing: {ccv!r}")
        if not notes.get("l_number"):
            warn("notes.l_number", "missing L-number for traceability")
        # literature
        if length(lit.get("key_refs")) < 1:
            err("literature.key_refs", "no APA citations recorded (minimum 1)")

    return {
        "passed": len(errors) == 0,
        "evidence_role": evidence_role_filter,
        "tags_checked": len(target),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--json", action="store_true")
    p.add_argument("--evidence-role", default="latent")
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

    print(f"audit-semantics: registry {REGISTRY.name}")
    print(f"  evidence_role filter: {result['evidence_role']}")
    print(f"  tags checked: {result['tags_checked']}")
    print(f"  errors: {result['error_count']}, warnings: {result['warning_count']}")
    for e in result["errors"][:30]:
        print(f"  [ERROR] {e['tag']}: {e['field']}: {e['message']}")
    if len(result["errors"]) > 30:
        print(f"  ... and {len(result['errors']) - 30} more errors")
    for w in result["warnings"][:10]:
        print(f"  [WARN]  {w['tag']}: {w['field']}: {w['message']}")
    print()
    if result["passed"]:
        print("OK: audit-semantics passed")
        return 0
    print("NO-GO: audit-semantics failed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
