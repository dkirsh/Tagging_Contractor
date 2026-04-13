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


def classify_evidence(tag_id: str, sem: Dict[str, Any]) -> Tuple[str, List[str]]:
    prefix = namespace_of(tag_id)
    lower_id = tag_id.lower()

    sensor_prefix = {"touch", "smell", "sound"}
    computed_prefix = {"cnfa", "complexity", "fluency", "science", "isovist"}
    metadata_prefix = {"affect", "psych", "cognitive", "provenance", "tag"}

    allowed = set()

    if prefix in sensor_prefix:
        allowed.add("sensor")
    if prefix in computed_prefix or lower_id.startswith("env.v") or lower_id.startswith("env.v2"):
        allowed.add("computed")
    if prefix in metadata_prefix:
        allowed.add("metadata")
    if "rating" in lower_id or "survey" in lower_id or "request" in lower_id:
        allowed.add("metadata")

    notes_2d = sem.get("extraction_notes_2d", "") if isinstance(sem.get("extraction_notes_2d"), str) else ""
    notes_3d = sem.get("extraction_notes_3d", "") if isinstance(sem.get("extraction_notes_3d"), str) else ""
    notes = f"{notes_2d} {notes_3d}".strip()

    if notes:
        if has_keywords(notes, ["not inferable", "requires", "measurement", "measured", "sensor", "lab", "tactile", "haptic", "acoustic", "olfactory"]):
            allowed.add("sensor")
        if has_keywords(notes, ["computed", "calculated", "metric", "index", "measure", "value", "score"]):
            allowed.add("computed")
        if has_keywords(notes, ["reported", "survey", "user", "feedback", "annotator", "human", "policy", "request", "source", "evidence"]):
            allowed.add("metadata")
        if has_keywords(notes, ["3d", "geometry", "spatial", "depth"]):
            allowed.add("image_3d")
        if has_keywords(notes, ["2d", "imagery", "visual cues", "image"]):
            allowed.add("image_2d")

    if not allowed:
        allowed.add("image_2d")

    # primary evidence_type priority
    if "sensor" in allowed:
        evidence = "sensor"
    elif "computed" in allowed:
        evidence = "computed"
    elif "metadata" in allowed:
        evidence = "metadata"
    elif "image_3d" in allowed:
        evidence = "image_3d"
    else:
        evidence = "image_2d"

    return evidence, sorted(allowed)


def model_families(tag_id: str, evidence: str) -> List[str]:
    prefix = namespace_of(tag_id)
    lower_id = tag_id.lower()
    families = set()

    if evidence == "sensor":
        if prefix == "sound":
            families.add("audio_analysis")
        elif prefix == "smell":
            families.add("olfactory_sensing")
        elif prefix == "touch":
            families.add("tactile_sensing")
        else:
            families.add("sensor_generic")
        return sorted(families)

    if evidence == "metadata":
        families.update(["user_reports", "survey_data", "annotation_review"])
        return sorted(families)

    if evidence == "computed":
        families.add("metric_computation")
        if "isovist" in lower_id or "depth" in lower_id or "spatial" in lower_id or "layout" in lower_id:
            families.add("spatial_metrics")
        if "light" in lower_id or "luminance" in lower_id or "illum" in lower_id or "cct" in lower_id or "cri" in lower_id:
            families.add("photometric_metrics")
        return sorted(families)

    if evidence == "image_3d":
        families.update(["depth_estimation", "layout_estimation", "multi_view_geometry"])
        return sorted(families)

    # image_2d
    if prefix in ("component", "obj"):
        families.add("object_detection")
    if prefix in ("material", "materials", "mat"):
        families.add("material_classification")
    if prefix == "texture":
        families.add("texture_classification")
    if prefix == "color":
        families.add("color_estimation")
    if prefix in ("light", "lighting"):
        families.add("lighting_estimation")
    if prefix == "style":
        families.add("style_classification")
    if prefix == "spatial" or lower_id.startswith("arch.pattern"):
        families.add("layout_estimation")
    if "signage" in lower_id or "text" in lower_id:
        families.add("ocr_text")
    if not families:
        families.add("scene_classification")

    return sorted(families)


def phase_for_evidence(evidence: str) -> str:
    if evidence == "image_2d":
        return "phase_0_image_2d"
    if evidence == "image_3d":
        return "phase_1_image_3d"
    if evidence == "computed":
        return "phase_2_computed"
    if evidence == "metadata":
        return "phase_3_metadata"
    if evidence == "sensor":
        return "phase_4_sensor"
    return "phase_unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--registry", required=True)
    ap.add_argument("--audit", default="reports/tag_usability_audit.csv")
    ap.add_argument("--out-evidence-csv", required=True)
    ap.add_argument("--out-model-csv", required=True)
    ap.add_argument("--out-roadmap-csv", required=True)
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

    evidence_rows: List[Dict[str, Any]] = []
    model_rows: List[Dict[str, Any]] = []
    roadmap_rows: List[Dict[str, Any]] = []

    for tid, tag_obj in tags_map.items():
        if not isinstance(tag_obj, dict):
            continue
        canonical_name = tag_obj.get("canonical_name") or tag_obj.get("canonicalName") or tag_obj.get("name") or ""
        sem = tag_obj.get("semantics") if isinstance(tag_obj.get("semantics"), dict) else {}
        evidence, allowed = classify_evidence(tid, sem)
        families = model_families(tid, evidence)
        arow = audit_map.get(tid, {})
        relation_count = arow.get("relation_count") or 0

        evidence_rows.append({
            "tag_id": tid,
            "canonical_name": canonical_name,
            "namespace": namespace_of(tid),
            "evidence_type": evidence,
            "allowed_inputs": ";".join(allowed),
            "relation_count": relation_count,
        })

        model_rows.append({
            "tag_id": tid,
            "evidence_type": evidence,
            "model_families": ";".join(families),
        })

        roadmap_rows.append({
            "tag_id": tid,
            "phase": phase_for_evidence(evidence),
            "evidence_type": evidence,
            "allowed_inputs": ";".join(allowed),
            "model_families": ";".join(families),
            "relation_count": relation_count,
        })

    evidence_rows.sort(key=lambda r: (r["namespace"], r["tag_id"]))
    model_rows.sort(key=lambda r: (r["evidence_type"], r["tag_id"]))
    roadmap_rows.sort(key=lambda r: (r["phase"], r["tag_id"]))

    archive_dir = repo / "archive"
    out_evidence = Path(args.out_evidence_csv).resolve()
    out_model = Path(args.out_model_csv).resolve()
    out_roadmap = Path(args.out_roadmap_csv).resolve()
    out_md = Path(args.out_md).resolve()

    safe_backup(out_evidence, archive_dir)
    out_evidence.parent.mkdir(parents=True, exist_ok=True)
    with out_evidence.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["tag_id","canonical_name","namespace","evidence_type","allowed_inputs","relation_count"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(evidence_rows)

    safe_backup(out_model, archive_dir)
    out_model.parent.mkdir(parents=True, exist_ok=True)
    with out_model.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["tag_id","evidence_type","model_families"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(model_rows)

    safe_backup(out_roadmap, archive_dir)
    out_roadmap.parent.mkdir(parents=True, exist_ok=True)
    with out_roadmap.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["tag_id","phase","evidence_type","allowed_inputs","model_families","relation_count"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(roadmap_rows)

    # summary
    evidence_counts: Dict[str, int] = {}
    phase_counts: Dict[str, int] = {}
    for r in roadmap_rows:
        evidence_counts[r["evidence_type"]] = evidence_counts.get(r["evidence_type"], 0) + 1
        phase_counts[r["phase"]] = phase_counts.get(r["phase"], 0) + 1

    def rel_int(v: Any) -> int:
        try:
            return int(v)
        except Exception:
            return 0

    top_phase: Dict[str, List[Dict[str, Any]]] = {}
    for phase in phase_counts.keys():
        items = [r for r in roadmap_rows if r["phase"] == phase]
        items.sort(key=lambda r: (-rel_int(r["relation_count"]), r["tag_id"]))
        top_phase[phase] = items[:10]

    safe_backup(out_md, archive_dir)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    summary = []
    summary.append("# Tag Extraction Plan Summary")
    summary.append("")
    summary.append(f"- Registry: `{reg_path}`")
    if audit_path.exists():
        summary.append(f"- Audit: `{audit_path}`")
    summary.append(f"- Total tags: **{len(roadmap_rows)}**")
    summary.append("")
    summary.append("## Evidence type counts")
    for k in sorted(evidence_counts.keys()):
        summary.append(f"- {k}: **{evidence_counts[k]}**")
    summary.append("")
    summary.append("## Phase counts")
    for k in sorted(phase_counts.keys()):
        summary.append(f"- {k}: **{phase_counts[k]}**")
    summary.append("")
    summary.append("## Top tags by phase (relation_count)")
    for phase in sorted(top_phase.keys()):
        summary.append(f"### {phase}")
        for r in top_phase[phase]:
            summary.append(f"- `{r['tag_id']}`: {r['relation_count']}")
        summary.append("")
    out_md.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print("OK: extraction plan written")
    print(f"TOTAL {len(roadmap_rows)}")
    print("EVIDENCE_COUNTS")
    for k in sorted(evidence_counts.keys()):
        print(f"{k} {evidence_counts[k]}")
    print("PHASE_COUNTS")
    for k in sorted(phase_counts.keys()):
        print(f"{k} {phase_counts[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
