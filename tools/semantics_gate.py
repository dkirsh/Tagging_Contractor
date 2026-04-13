#!/usr/bin/env python3
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple


def run_audit() -> int:
    res = subprocess.run(["./bin/tc", "audit-semantics"], text=True)
    return res.returncode


def parse_counts(md_path: Path) -> Tuple[Dict[str, int], Dict[str, int]]:
    overall: Dict[str, int] = {}
    relation: Dict[str, int] = {}
    section = ""

    if not md_path.exists():
        raise FileNotFoundError(f"Missing summary: {md_path}")

    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Buckets (overall)"):
            section = "overall"
            continue
        if line.startswith("## Buckets (relation-linked"):
            section = "relation"
            continue
        m = re.match(r"^-\s*(P[0-9])[^:]*:\s*(\d+)\s*$", line)
        if not m or not section:
            continue
        bucket, count = m.group(1), int(m.group(2))
        if section == "overall":
            overall[bucket] = count
        elif section == "relation":
            relation[bucket] = count

    return overall, relation


def main() -> int:
    audit_rc = run_audit()
    if audit_rc != 0:
        print("NO-GO: audit-semantics failed", file=sys.stderr)
        return 2

    md_path = Path("reports/tag_semantics_completeness_summary.md")
    try:
        overall, relation = parse_counts(md_path)
    except Exception as exc:
        print(f"NO-GO: failed to parse summary: {exc}", file=sys.stderr)
        return 2

    overall_p0 = overall.get("P0", -1)
    rel_p0 = relation.get("P0", -1)
    rel_p2 = relation.get("P2", -1)

    if overall_p0 == 0 and rel_p0 == 0 and rel_p2 == 95:
        print("OK: semantics gate passed")
        return 0

    print("NO-GO: semantics gate failed", file=sys.stderr)
    print(f"  Overall P0: {overall_p0}", file=sys.stderr)
    print(f"  Relation-linked P0: {rel_p0}", file=sys.stderr)
    print(f"  Relation-linked P2: {rel_p2}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
