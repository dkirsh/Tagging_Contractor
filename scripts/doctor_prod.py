#!/usr/bin/env python3
"""TRS Sprint 1 — `tc doctor --prod` unified production gate.

Runs the three semantic gates in sequence and emits a unified pass/fail:

    1. validate_registry.py        (schema + invariants)
    2. audit_semantics_simple.py   (semantics completeness for latent tags)
    3. audit_extraction_plan.py    (Spohn 50% overlap + method family + notes)

A `--scope` argument restricts the strict gates (2, 3) to a subset of tags.
The default scope is `social.*` (the Sprint 1 latent layer); `all` runs against
every active latent in the registry.

A `--exclude-pre-existing` flag treats validate_registry.py errors that
predate Sprint 1 as warnings rather than failures. The criterion is whether
the failing tag id starts with `social.` or is one of the canonical Sprint 1
canonical names; everything else is treated as pre-existing.

Usage:
    python3 scripts/doctor_prod.py --prod
    python3 scripts/doctor_prod.py --prod --json
    python3 scripts/doctor_prod.py --prod --scope all
    python3 scripts/doctor_prod.py --prod --exclude-pre-existing

Exit codes:
    0 = production gate passed
    1 = production gate failed
    2 = registry could not be loaded
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY_DIR = REPO / "core/trs-core/v0.2.8/registry/"
SCRIPTS = REPO / "scripts"


def run_validate(registry_dir: Path, exclude_pre_existing: bool) -> dict:
    """Wrap scripts/validate_registry.py."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_registry.py"), str(registry_dir), "--json"],
        capture_output=True, text=True,
    )
    if not proc.stdout.strip():
        return {"passed": False, "error_count": 1, "errors": [
            {"tag_id": "<system>", "field": "<validate_registry>", "message": proc.stderr or "empty stdout"}
        ], "warnings": []}
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"passed": False, "error_count": 1, "errors": [
            {"tag_id": "<system>", "field": "<validate_registry>", "message": f"non-JSON stdout: {proc.stdout[:200]}"}
        ], "warnings": []}

    if exclude_pre_existing:
        my = [e for e in out["errors"] if e["tag_id"].startswith("social.")]
        pre = [e for e in out["errors"] if not e["tag_id"].startswith("social.")]
        out["errors"] = my
        out["error_count"] = len(my)
        out["pre_existing_count"] = len(pre)
        out["passed"] = len(my) == 0
    return out


def run_script(script_name: str, args: list[str]) -> dict:
    """Wrap any of our --json-emitting scripts."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script_name), "--json"] + args,
        capture_output=True, text=True,
    )
    if not proc.stdout.strip():
        return {"passed": False, "error_count": 1, "errors": [
            {"tag": "<system>", "message": proc.stderr or "empty stdout"}
        ]}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"passed": False, "error_count": 1, "errors": [
            {"tag": "<system>", "message": f"non-JSON stdout: {proc.stdout[:200]}"}
        ]}


def main() -> int:
    p = argparse.ArgumentParser(description="Production gate for the TRS registry.")
    p.add_argument("--prod", action="store_true", required=False,
                   help="Run the production gate (currently the only mode).")
    p.add_argument("--json", action="store_true",
                   help="Emit JSON instead of human-readable.")
    p.add_argument("--scope", default="latent",
                   help="evidence_role to scope semantic+extraction audits to (default: latent)")
    p.add_argument("--exclude-pre-existing", action="store_true",
                   help="Treat validate_registry.py errors on non-Sprint-1 tags as warnings.")
    args = p.parse_args()

    results: dict[str, dict] = {}
    overall_pass = True

    print("=== Stage 1/3: validate_registry.py (schema + invariants) ===")
    results["validate"] = run_validate(REGISTRY_DIR, args.exclude_pre_existing)
    print(f"  errors: {results['validate'].get('error_count', '?')}; "
          f"warnings: {results['validate'].get('warning_count', '?')}; "
          f"pre-existing: {results['validate'].get('pre_existing_count', 0)}")
    if not results["validate"].get("passed"):
        overall_pass = False
    print()

    print("=== Stage 2/3: audit_semantics_simple.py (completeness) ===")
    results["semantics"] = run_script("audit_semantics_simple.py",
                                      ["--evidence-role", args.scope])
    if args.exclude_pre_existing:
        sem_my = [e for e in results["semantics"].get("errors", []) if e.get("tag", "").startswith("social.")]
        sem_pre = [e for e in results["semantics"].get("errors", []) if not e.get("tag", "").startswith("social.")]
        results["semantics"]["errors"] = sem_my
        results["semantics"]["error_count"] = len(sem_my)
        results["semantics"]["pre_existing_count"] = len(sem_pre)
        results["semantics"]["passed"] = len(sem_my) == 0
    print(f"  tags_checked: {results['semantics'].get('tags_checked', '?')}; "
          f"errors: {results['semantics'].get('error_count', '?')}; "
          f"warnings: {results['semantics'].get('warning_count', '?')}; "
          f"pre-existing: {results['semantics'].get('pre_existing_count', 0)}")
    if not results["semantics"].get("passed"):
        overall_pass = False
    print()

    print("=== Stage 3/3: audit_extraction_plan.py (Spohn 50% + extraction) ===")
    results["extraction"] = run_script("audit_extraction_plan.py",
                                       ["--evidence-role", args.scope])
    if args.exclude_pre_existing:
        # Errors here have either 'tag' or 'tag_a'/'tag_b'
        def is_mine(e):
            t = e.get("tag") or e.get("tag_a", "")
            return t.startswith("social.")
        ext_my = [e for e in results["extraction"].get("errors", []) if is_mine(e)]
        ext_pre = [e for e in results["extraction"].get("errors", []) if not is_mine(e)]
        results["extraction"]["errors"] = ext_my
        results["extraction"]["error_count"] = len(ext_my)
        results["extraction"]["pre_existing_count"] = len(ext_pre)
        results["extraction"]["passed"] = len(ext_my) == 0
    print(f"  tags_checked: {results['extraction'].get('tags_checked', '?')}; "
          f"pairs_violated: {results['extraction'].get('pairs_violated', '?')}; "
          f"errors: {results['extraction'].get('error_count', '?')}; "
          f"warnings: {results['extraction'].get('warning_count', '?')}; "
          f"pre-existing: {results['extraction'].get('pre_existing_count', 0)}")
    if not results["extraction"].get("passed"):
        overall_pass = False
    print()

    if args.json:
        print(json.dumps({"overall_passed": overall_pass, "stages": results}, indent=2))
    else:
        if overall_pass:
            print("OK: tc doctor --prod passed all three gates")
        else:
            print("NO-GO: tc doctor --prod failed", file=sys.stderr)
            print("Per-stage details above; rerun individual stage scripts for full output.", file=sys.stderr)

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
