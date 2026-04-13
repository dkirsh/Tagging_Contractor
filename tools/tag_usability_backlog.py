#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import datetime
import statistics
from pathlib import Path
from typing import Any, Dict, List


def safe_backup(path: Path, archive_dir: Path) -> None:
    if path.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / f"{path.name}.bak_{ts}"
        dst.write_bytes(path.read_bytes())


def parse_int(v: Any, default: int = 0) -> int:
    try:
        return int(float(str(v)))
    except Exception:
        return default


def read_audit(path: Path) -> List[Dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return [row for row in r]


def priority_score(row: Dict[str, Any]) -> Dict[str, Any]:
    has_long = str(row.get("has_definition_long", "")).strip().lower() == "true"
    alias_count = parse_int(row.get("alias_count", 0))
    pos = parse_int(row.get("examples_positive_count", 0))
    neg = parse_int(row.get("examples_negative_count", 0))
    inc = parse_int(row.get("scope_includes_count", 0))
    exc = parse_int(row.get("scope_excludes_count", 0))
    has_notes = str(row.get("has_any_extraction_notes", "")).strip().lower() == "true"

    missing = []
    if not has_long:
        missing.append("def_long")
    if alias_count < 6:
        missing.append(f"aliases<6({alias_count})")
    if pos < 2:
        missing.append(f"pos_examples<2({pos})")
    if neg < 2:
        missing.append(f"neg_examples<2({neg})")
    if inc < 2:
        missing.append(f"scope_includes<2({inc})")
    if exc < 2:
        missing.append(f"scope_excludes<2({exc})")
    if not has_notes:
        missing.append("extraction_notes")

    score = 0
    score += 100 if not has_long else 0
    score += max(0, 6 - alias_count) * 10
    score += max(0, 2 - pos) * 5
    score += max(0, 2 - neg) * 5
    score += max(0, 2 - inc) * 3
    score += max(0, 2 - exc) * 3
    score += 2 if not has_notes else 0

    return {"score": score, "missing": ";".join(missing)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--audit", default="reports/tag_usability_audit.csv")
    ap.add_argument("--out-csv", default="reports/tag_usability_backlog.csv")
    ap.add_argument("--out-md", default="reports/tag_usability_backlog_summary.md")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    audit_path = Path(args.audit)
    if not audit_path.is_absolute():
        audit_path = repo / audit_path
    if not audit_path.exists():
        print(f"NO-GO: audit CSV not found: {audit_path}")
        return 2

    rows = read_audit(audit_path)

    backlog: List[Dict[str, Any]] = []
    alias_counts = []
    rel_counts = []
    missing_long = 0
    for row in rows:
        alias_count = parse_int(row.get("alias_count", 0))
        relation_count = parse_int(row.get("relation_count", 0))
        alias_counts.append(alias_count)
        rel_counts.append(relation_count)
        if str(row.get("has_definition_long", "")).strip().lower() != "true":
            missing_long += 1

        pr = priority_score(row)
        backlog.append({
            "tag_id": row.get("tag_id", ""),
            "canonical_name": row.get("canonical_name", ""),
            "relation_count": relation_count,
            "has_definition_long": row.get("has_definition_long", ""),
            "alias_count": alias_count,
            "examples_positive_count": parse_int(row.get("examples_positive_count", 0)),
            "examples_negative_count": parse_int(row.get("examples_negative_count", 0)),
            "scope_includes_count": parse_int(row.get("scope_includes_count", 0)),
            "scope_excludes_count": parse_int(row.get("scope_excludes_count", 0)),
            "has_any_extraction_notes": row.get("has_any_extraction_notes", ""),
            "priority_score": pr["score"],
            "priority_reasons": pr["missing"],
        })

    backlog.sort(key=lambda r: (-r["priority_score"], -r["relation_count"], r["tag_id"]))
    for i, row in enumerate(backlog, start=1):
        row["rank"] = i

    archive_dir = repo / "archive"
    out_csv = Path(args.out_csv)
    if not out_csv.is_absolute():
        out_csv = repo / out_csv
    out_md = Path(args.out_md)
    if not out_md.is_absolute():
        out_md = repo / out_md

    safe_backup(out_csv, archive_dir)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "tag_id",
        "canonical_name",
        "relation_count",
        "has_definition_long",
        "alias_count",
        "examples_positive_count",
        "examples_negative_count",
        "scope_includes_count",
        "scope_excludes_count",
        "has_any_extraction_notes",
        "priority_score",
        "priority_reasons",
    ]
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in backlog:
            w.writerow({k: row.get(k, "") for k in fieldnames})

    safe_backup(out_md, archive_dir)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    summary = []
    summary.append("# Tag Usability Backlog Summary")
    summary.append("")
    summary.append(f"- Audit: `{audit_path}`")
    summary.append(f"- Total tags: **{len(rows)}**")
    summary.append(f"- Tags missing definition_long: **{missing_long}**")
    if alias_counts:
        summary.append(f"- Alias count min/median/max: **{min(alias_counts)} / {statistics.median(alias_counts)} / {max(alias_counts)}**")
    if rel_counts:
        summary.append(f"- Relation count min/median/max: **{min(rel_counts)} / {statistics.median(rel_counts)} / {max(rel_counts)}**")
    summary.append("")
    summary.append("## Top 20 backlog tags")
    for row in backlog[:20]:
        summary.append(
            f"- `{row['tag_id']}` score={row['priority_score']} rel={row['relation_count']} missing={row['priority_reasons']}"
        )
    out_md.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print("OK: usability backlog written")
    print(f"TOTAL {len(rows)}")
    print(f"MISSING_DEF_LONG {missing_long}")
    print("TOP_BACKLOG")
    for row in backlog[:20]:
        print(row.get("tag_id", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
