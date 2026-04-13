#!/usr/bin/env python3
from __future__ import annotations
import argparse
import datetime
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def safe_backup(path: Path, archive_dir: Path) -> None:
    if path.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / f"{path.name}.bak_{ts}"
        dst.write_bytes(path.read_bytes())


def get_tag_id(tag_obj: Dict[str, Any], fallback: str = "") -> str:
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


def normalize_name(tag_id: str, canonical_name: str) -> str:
    name = canonical_name.strip() if canonical_name else ""
    if not name:
        name = tag_id.split(".")[-1]
    name = name.replace("_", " ").replace("/", " / ")
    return " ".join(name.split())


def prefix_of(tag_id: str) -> str:
    return tag_id.split(".", 1)[0] if "." in tag_id else tag_id


def sentence_count(text: str) -> int:
    if not text or not text.strip():
        return 0
    parts = re.split(r"[.!?]+", text)
    return sum(1 for p in parts if p.strip())


def templates(tag_id: str, name: str) -> Dict[str, List[str]]:
    prefix = prefix_of(tag_id)
    lower_id = tag_id.lower()

    if prefix in ("touch", "smell", "sound"):
        return {
            "2d": [
                "Not inferable from 2D imagery.",
                "Requires sensor, material, or lab measurements.",
            ],
            "3d": [
                "3D geometry is insufficient without measurements.",
                "Use measured or reported data to assign this tag.",
            ],
        }

    if prefix in ("affect", "psych", "cognitive"):
        return {
            "2d": [
                "Use only when explicitly reported or supported by validated data.",
                "Avoid projecting affect from style cues alone.",
            ],
            "3d": [
                "Prefer user feedback or validated behavioral data.",
                "Geometry alone is insufficient for this tag.",
            ],
        }

    if prefix in ("cnfa", "complexity", "fluency", "science", "isovist") or lower_id.startswith("env.v") or lower_id.startswith("env.v2"):
        return {
            "2d": [
                "Assign only when the metric is computed from imagery or measurements.",
                "Do not infer the value without calculation.",
            ],
            "3d": [
                "Assign only when computed from 3D or spatial data.",
                "Do not guess this metric from appearance.",
            ],
        }

    return {
        "2d": [
            f"From 2D imagery, rely on clear visual cues for {name}.",
            "Avoid inference when cues are weak or ambiguous.",
        ],
        "3d": [
            f"From 3D or scene data, use geometry/material cues for {name}.",
            "Avoid speculation without supporting evidence.",
        ],
    }


def extend_note(existing: str, sentences: List[str], target: int) -> str:
    base = existing.strip()
    count = sentence_count(base)
    out = base
    for s in sentences:
        if count >= target:
            break
        if not out:
            out = s
        else:
            out = out.rstrip()
            if not out.endswith((".", "!", "?")):
                out += "."
            out += " " + s
        count += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--registry", required=True)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--target", type=int, default=2)
    ap.add_argument("--prefix", default="")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    reg_path = Path(args.registry).resolve()
    if not reg_path.exists():
        print(f"NO-GO: registry not found: {reg_path}")
        return 2

    tags_map = load_registry(reg_path)
    prefixes = [p.strip() for p in args.prefix.split(",") if p.strip()] if args.prefix else []

    selected: List[Dict[str, Any]] = []
    for tag_id, tag_obj in tags_map.items():
        if prefixes:
            ok = False
            for p in prefixes:
                if tag_id.startswith(p) or tag_id.startswith(p + "."):
                    ok = True
                    break
            if not ok:
                continue

        sem = tag_obj.get("semantics") if isinstance(tag_obj.get("semantics"), dict) else {}
        notes_2d = sem.get("extraction_notes_2d") if isinstance(sem.get("extraction_notes_2d"), str) else ""
        notes_3d = sem.get("extraction_notes_3d") if isinstance(sem.get("extraction_notes_3d"), str) else ""

        if sentence_count(notes_2d) >= args.target and sentence_count(notes_3d) >= args.target:
            continue

        canonical_name = tag_obj.get("canonical_name") or tag_obj.get("canonicalName") or tag_obj.get("name") or ""
        name = normalize_name(tag_id, canonical_name)
        tmpl = templates(tag_id, name)

        new_2d = extend_note(notes_2d, tmpl["2d"], args.target)
        new_3d = extend_note(notes_3d, tmpl["3d"], args.target)

        selected.append({
            "tag_id": tag_id,
            "extraction_notes_2d": new_2d,
            "extraction_notes_3d": new_3d,
        })

        if len(selected) >= args.n:
            break

    if not selected:
        print("NO-GO: no tags require extraction notes expansion")
        return 2

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = repo / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)

    archive_dir = repo / "archive"
    safe_backup(out_path, archive_dir)
    with out_path.open("w", encoding="utf-8") as f:
        for row in selected:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")

    print(f"OK: wrote {len(selected)} tags to {out_path}")
    for row in selected:
        print(row.get("tag_id", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
