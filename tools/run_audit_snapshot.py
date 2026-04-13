#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import datetime
import subprocess
from pathlib import Path
from typing import Dict, Tuple


def run(cmd, repo_root: Path) -> None:
    res = subprocess.run(cmd, cwd=repo_root)
    if res.returncode != 0:
        raise SystemExit(res.returncode)


def parse_semantics_summary(path: Path) -> Dict[str, Dict[str, int]]:
    overall = {}
    relation = {}
    section = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Buckets (overall)"):
            section = "overall"
            continue
        if line.startswith("## Buckets (relation-linked"):
            section = "relation"
            continue
        if line.startswith("- P") and ":" in line:
            parts = line.split(":", 1)
            key = parts[0].split()[1]
            try:
                val = int(parts[1].strip())
            except Exception:
                continue
            if section == "overall":
                overall[key] = val
            elif section == "relation":
                relation[key] = val
    return {"overall": overall, "relation": relation}


def usability_counts(path: Path) -> Dict[str, int]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    total = len(rows)
    def_long = sum(1 for r in rows if r.get("has_definition_long", "").lower() == "true")
    alias_ge8 = sum(1 for r in rows if int(r.get("alias_count", 0)) >= 8)
    pos_ge3 = sum(1 for r in rows if int(r.get("examples_positive_count", 0)) >= 3)
    neg_ge3 = sum(1 for r in rows if int(r.get("examples_negative_count", 0)) >= 3)
    inc_ge3 = sum(1 for r in rows if int(r.get("scope_includes_count", 0)) >= 3)
    exc_ge3 = sum(1 for r in rows if int(r.get("scope_excludes_count", 0)) >= 3)
    notes_2d = sum(1 for r in rows if r.get("has_notes_2d", "").lower() == "true")
    notes_3d = sum(1 for r in rows if r.get("has_notes_3d", "").lower() == "true")
    return {
        "total": total,
        "def_long": def_long,
        "alias_ge8": alias_ge8,
        "pos_ge3": pos_ge3,
        "neg_ge3": neg_ge3,
        "inc_ge3": inc_ge3,
        "exc_ge3": exc_ge3,
        "notes_2d": notes_2d,
        "notes_3d": notes_3d,
    }


def extraction_phase_counts(path: Path) -> Dict[str, int]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    counts: Dict[str, int] = {}
    for r in rows:
        ph = r.get("phase", "unknown")
        counts[ph] = counts.get(ph, 0) + 1
    return counts


def safe_backup(path: Path, archive_dir: Path) -> None:
    if path.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / f"{path.name}.bak_{ts}"
        dst.write_bytes(path.read_bytes())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--out-dir", default="reports/snapshots")
    ap.add_argument("--update-dashboard", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = repo / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # run audits
    run(["./bin/tc", "audit-semantics"], repo)
    run(["./bin/tc", "audit-usability"], repo)
    run(["./bin/tc", "audit-usability-backlog"], repo)
    run(["./bin/tc", "audit-extraction-plan"], repo)

    sem_summary = repo / "reports/tag_semantics_completeness_summary.md"
    usability_csv = repo / "reports/tag_usability_audit.csv"
    roadmap_csv = repo / "reports/tag_extraction_roadmap.csv"

    sem = parse_semantics_summary(sem_summary)
    usability = usability_counts(usability_csv)
    phases = extraction_phase_counts(roadmap_csv)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_path = out_dir / f"audit_snapshot_{ts}.md"

    lines = []
    lines.append(f"# Audit Snapshot {ts}")
    lines.append("")
    lines.append("## Semantics completeness (overall)")
    for k in ("P0", "P1", "P2"):
        lines.append(f"- {k}: {sem['overall'].get(k, 'n/a')}")
    lines.append("")
    lines.append("## Semantics completeness (relation-linked)")
    for k in ("P0", "P1", "P2"):
        lines.append(f"- {k}: {sem['relation'].get(k, 'n/a')}")
    lines.append("")
    lines.append("## Usability targets")
    lines.append(f"- Total tags: {usability['total']}")
    lines.append(f"- Definition long: {usability['def_long']}/{usability['total']}")
    lines.append(f"- Aliases >=8: {usability['alias_ge8']}/{usability['total']}")
    lines.append(f"- Examples pos>=3: {usability['pos_ge3']}/{usability['total']}")
    lines.append(f"- Examples neg>=3: {usability['neg_ge3']}/{usability['total']}")
    lines.append(f"- Scope includes>=3: {usability['inc_ge3']}/{usability['total']}")
    lines.append(f"- Scope excludes>=3: {usability['exc_ge3']}/{usability['total']}")
    lines.append(f"- Extraction notes 2D: {usability['notes_2d']}/{usability['total']}")
    lines.append(f"- Extraction notes 3D: {usability['notes_3d']}/{usability['total']}")
    lines.append("")
    lines.append("## Extraction phases")
    for k in sorted(phases.keys()):
        lines.append(f"- {k}: {phases[k]}")

    snapshot_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if args.update_dashboard:
        dashboard = repo / "reports/status_dashboard.md"
        archive_dir = repo / "archive"
        safe_backup(dashboard, archive_dir)
        dashboard_lines = [
            "# Status Dashboard",
            "",
            f"Last updated: {ts}",
            "",
            "## Semantics completeness (overall)",
            f"- P0: {sem['overall'].get('P0','n/a')}",
            f"- P1: {sem['overall'].get('P1','n/a')}",
            f"- P2: {sem['overall'].get('P2','n/a')}",
            "",
            "## Usability targets",
            f"- Definition long: {usability['def_long']}/{usability['total']}",
            f"- Aliases >=8: {usability['alias_ge8']}/{usability['total']}",
            f"- Examples pos>=3: {usability['pos_ge3']}/{usability['total']}",
            f"- Examples neg>=3: {usability['neg_ge3']}/{usability['total']}",
            f"- Scope includes>=3: {usability['inc_ge3']}/{usability['total']}",
            f"- Scope excludes>=3: {usability['exc_ge3']}/{usability['total']}",
            f"- Extraction notes 2D: {usability['notes_2d']}/{usability['total']}",
            f"- Extraction notes 3D: {usability['notes_3d']}/{usability['total']}",
            "",
            "## Extraction phases",
        ]
        for k in sorted(phases.keys()):
            dashboard_lines.append(f"- {k}: {phases[k]}")
        dashboard_lines.append("")
        dashboard_lines.append("## Handoff bundles")
        dashboard_lines.append("- reports/handoff_phase0.zip")
        dashboard_lines.append("- reports/handoff_phase1.zip")
        dashboard_lines.append("- reports/handoff_phase2_computed.zip")
        dashboard_lines.append("- reports/handoff_phase3_metadata.zip")
        dashboard_lines.append("- reports/handoff_phase4_sensor.zip")
        dashboard.write_text("\n".join(dashboard_lines) + "\n", encoding="utf-8")

    print(f"OK: wrote snapshot {snapshot_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
