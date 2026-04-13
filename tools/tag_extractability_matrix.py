#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import datetime
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def safe_backup(path: Path, archive_dir: Path) -> None:
    if path.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / f"{path.name}.bak_{ts}"
        dst.write_bytes(path.read_bytes())


def get_tag_id(tag_obj: Dict[str, Any], fallback: Optional[str] = None) -> Optional[str]:
    for k in ("tag_id", "tagId", "id"):
        v = tag_obj.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return fallback


def load_registry(reg_path: Path) -> Dict[str, Dict[str, Any]]:
    obj = json.loads(reg_path.read_text(encoding="utf-8"))
    tags_map: Dict[str, Dict[str, Any]] = {}

    container = obj
    if isinstance(obj, dict) and isinstance(obj.get("registry"), dict):
        container = obj["registry"]

    tags = container.get("tags") if isinstance(container, dict) else None

    if isinstance(tags, dict):
        for tid, t in tags.items():
            if isinstance(t, dict):
                tags_map[str(tid)] = t
    elif isinstance(tags, list):
        for t in tags:
            if isinstance(t, dict):
                tid = get_tag_id(t)
                if tid:
                    tags_map[tid] = t
    elif isinstance(obj, dict) and isinstance(obj.get("tags"), dict):
        for tid, t in obj["tags"].items():
            if isinstance(t, dict):
                tags_map[str(tid)] = t
    elif isinstance(obj, list):
        for t in obj:
            if isinstance(t, dict):
                tid = get_tag_id(t)
                if tid:
                    tags_map[tid] = t
    else:
        raise RuntimeError("Unsupported registry shape: cannot find tags map/list")

    return tags_map


def read_audit(audit_path: Path) -> Dict[str, Dict[str, Any]]:
    if not audit_path.exists():
        return {}
    with audit_path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        rows = {}
        for row in r:
            tid = row.get("tag_id") or row.get("tagId") or row.get("id")
            if tid:
                rows[str(tid)] = row
        return rows


def namespace_of(tag_id: str) -> str:
    return tag_id.split(".", 1)[0] if "." in tag_id else tag_id


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def has_keywords(text: str, keywords: List[str]) -> bool:
    t = normalize_text(text)
    return any(k in t for k in keywords)


def classify_extractability(tag_id: str, sem: Dict[str, Any]) -> Tuple[str, List[str]]:
    prefix = namespace_of(tag_id)
    lower_id = tag_id.lower()
    sources = set()

    sensor_prefix = {"touch", "smell", "sound"}
    computed_prefix = {"cnfa", "complexity", "fluency", "science", "isovist"}
    metadata_prefix = {"affect", "psych", "cognitive", "provenance", "tag"}

    if prefix in sensor_prefix:
        sources.add("sensor_required")
    if prefix in computed_prefix or lower_id.startswith("env.v") or lower_id.startswith("env.v2"):
        sources.add("computed_metric")
    if prefix in metadata_prefix:
        sources.add("metadata_reported")
    if "rating" in lower_id or "survey" in lower_id or "request" in lower_id:
        sources.add("metadata_reported")

    notes_2d = sem.get("extraction_notes_2d", "") if isinstance(sem.get("extraction_notes_2d"), str) else ""
    notes_3d = sem.get("extraction_notes_3d", "") if isinstance(sem.get("extraction_notes_3d"), str) else ""
    notes = f"{notes_2d} {notes_3d}".strip()

    if notes:
        if has_keywords(notes, ["not inferable", "requires", "measurement", "measured", "sensor", "lab", "tactile", "haptic", "acoustic", "olfactory"]):
            sources.add("sensor_required")
        if has_keywords(notes, ["computed", "calculated", "metric", "index", "measure", "value", "score"]):
            sources.add("computed_metric")
        if has_keywords(notes, ["reported", "survey", "user", "feedback", "annotator", "human", "policy", "request", "source", "evidence"]):
            sources.add("metadata_reported")
        if has_keywords(notes, ["3d", "geometry", "spatial", "depth"]):
            sources.add("visual_3d")
        if has_keywords(notes, ["2d", "imagery", "visual cues", "image"]):
            sources.add("visual_2d")

    if not sources:
        sources.add("visual_2d")

    if len(sources) == 1:
        return next(iter(sources)), sorted(sources)

    if "sensor_required" in sources:
        primary = "mixed_sensor"
    elif "computed_metric" in sources:
        primary = "mixed_computed"
    elif "metadata_reported" in sources:
        primary = "mixed_metadata"
    else:
        primary = "mixed_visual"

    return primary, sorted(sources)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--registry", required=True)
    ap.add_argument("--audit", default="reports/tag_usability_audit.csv")
    ap.add_argument("--out-csv", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    reg_path = Path(args.registry).resolve()
    if not reg_path.exists():
        print(f"NO-GO: registry not found: {reg_path}")
        return 2

    audit_path = Path(args.audit)
    if not audit_path.is_absolute():
        audit_path = repo / audit_path

    tags_map = load_registry(reg_path)
    audit_map = read_audit(audit_path)

    rows: List[Dict[str, Any]] = []
    for tid, tag_obj in tags_map.items():
        if not isinstance(tag_obj, dict):
            continue
        canonical_name = tag_obj.get("canonical_name") or tag_obj.get("canonicalName") or tag_obj.get("name") or ""
        sem = tag_obj.get("semantics") if isinstance(tag_obj.get("semantics"), dict) else {}
        cls, sources = classify_extractability(tid, sem)
        arow = audit_map.get(tid, {})
        relation_count = arow.get("relation_count") or 0
        rows.append({
            "tag_id": tid,
            "canonical_name": canonical_name,
            "namespace": namespace_of(tid),
            "extractability_class": cls,
            "sources": ";".join(sources),
            "relation_count": relation_count,
        })

    rows.sort(key=lambda r: (r["namespace"], r["tag_id"]))

    out_csv = Path(args.out_csv).resolve()
    out_md = Path(args.out_md).resolve()
    archive_dir = repo / "archive"

    safe_backup(out_csv, archive_dir)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["tag_id", "canonical_name", "namespace", "extractability_class", "sources", "relation_count"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # summary
    class_counts: Dict[str, int] = {}
    ns_counts: Dict[str, int] = {}
    for r in rows:
        class_counts[r["extractability_class"]] = class_counts.get(r["extractability_class"], 0) + 1
        ns_counts[r["namespace"]] = ns_counts.get(r["namespace"], 0) + 1

    non_visual = [
        r for r in rows
        if r["extractability_class"].startswith("mixed_")
        or r["extractability_class"] in ("sensor_required", "computed_metric", "metadata_reported")
    ]

    def rel_int(v: Any) -> int:
        try:
            return int(v)
        except Exception:
            return 0

    non_visual.sort(key=lambda r: (-rel_int(r["relation_count"]), r["tag_id"]))
    top_non_visual = non_visual[:20]

    safe_backup(out_md, archive_dir)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    summary = []
    summary.append("# Tag Extractability Matrix Summary")
    summary.append("")
    summary.append(f"- Registry: `{reg_path}`")
    if audit_path.exists():
        summary.append(f"- Audit: `{audit_path}`")
    summary.append(f"- Total tags: **{len(rows)}**")
    summary.append("")
    summary.append("## Extractability class counts")
    for k in sorted(class_counts.keys()):
        summary.append(f"- {k}: **{class_counts[k]}**")
    summary.append("")
    summary.append("## Namespace counts (top 12)")
    for ns, count in sorted(ns_counts.items(), key=lambda x: (-x[1], x[0]))[:12]:
        summary.append(f"- {ns}: **{count}**")
    summary.append("")
    summary.append("## Top 20 non-visual or mixed tags by relation_count")
    for r in top_non_visual:
        summary.append(f"- `{r['tag_id']}`: {r['relation_count']} ({r['extractability_class']})")
    out_md.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print("OK: extractability matrix written")
    print(f"TOTAL {len(rows)}")
    print("CLASS_COUNTS")
    for k in sorted(class_counts.keys()):
        print(f"{k} {class_counts[k]}")
    print("TOP_NON_VISUAL")
    for r in top_non_visual:
        print(r["tag_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
