#!/usr/bin/env python3
from __future__ import annotations
import argparse
import datetime
import csv
import json
from pathlib import Path
from typing import Any, Dict, List


def safe_backup(path: Path, archive_dir: Path) -> None:
    if path.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / f"{path.name}.bak_{ts}"
        dst.write_bytes(path.read_bytes())


def is_empty(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip() == ""
    if isinstance(v, (list, dict, tuple, set)):
        return len(v) == 0
    return False


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


def pick_def_short(sem: Dict[str, Any]) -> str:
    for key in ("definition_short", "definition", "def", "notes", "description", "meaning"):
        v = sem.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    d = sem.get("definition")
    if isinstance(d, dict):
        for k in ("short", "summary", "text"):
            v = d.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return ""


def has_def_long(sem: Dict[str, Any]) -> bool:
    v = sem.get("definition_long")
    if isinstance(v, str) and v.strip():
        return True
    d = sem.get("definition")
    if isinstance(d, dict):
        for k in ("long", "detailed", "full"):
            v = d.get(k)
            if isinstance(v, str) and v.strip():
                return True
    return False


def normalize_name(tag_id: str, canonical_name: str) -> str:
    name = canonical_name.strip() if canonical_name else ""
    if not name:
        name = tag_id.split(".")[-1]
    name = name.replace("_", " ").replace("/", " / ")
    return " ".join(name.split())


def prefix_of(tag_id: str) -> str:
    return tag_id.split(".", 1)[0] if "." in tag_id else tag_id


def long_definition(tag_id: str, name: str, def_short: str) -> str:
    base = def_short.strip()
    if base.endswith("."):
        base = base[:-1]
    if not base:
        base = f"{name} is the target attribute"

    prefix = prefix_of(tag_id)
    lower_id = tag_id.lower()

    if prefix in ("touch", "smell", "sound"):
        return (
            f"{base}. This tag should only be used when measurement, sensing, or metadata supports {name}, "
            "not from visual inference. For 2D/3D imagery alone, do not assign without corroborating data."
        )
    if prefix in ("cnfa", "complexity", "fluency", "science", "isovist", "env") or lower_id.startswith("env.v") or lower_id.startswith("env.v2"):
        return (
            f"{base}. This is a computed or measured metric from environmental, spatial, or visual data; "
            "use only when the metric is calculated for the scene. Do not guess the value from appearance."
        )
    if prefix in ("affect", "psych", "cognitive"):
        return (
            f"{base}. Use when observer reports or validated instruments indicate this affective/cognitive response. "
            "Avoid projecting the response from style cues alone."
        )
    if prefix in ("style",):
        return (
            f"{base}. Apply when the overall design language aligns clearly with {name}. "
            "Do not assign based on a single object or minor accent."
        )
    if lower_id.startswith("arch.pattern"):
        return (
            f"{base}. Use when the architectural pattern is explicitly present and structurally significant. "
            "Avoid use for incidental or partial instances."
        )
    if prefix in ("component", "material", "materials", "mat"):
        return (
            f"{base}. Use when this component or material is clearly visible or specified and is a primary feature. "
            "Do not tag for negligible or ambiguous presence."
        )
    if prefix in ("color", "light", "lighting"):
        return (
            f"{base}. Apply when the color/lighting attribute is dominant or explicitly specified. "
            "Avoid assigning from weak or ambiguous cues."
        )

    return (
        f"{base}. Use when this attribute is clearly present and salient in the scene or data. "
        "Do not infer without evidence."
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--backlog", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    backlog_path = Path(args.backlog)
    if not backlog_path.is_absolute():
        backlog_path = repo / backlog_path
    if not backlog_path.exists():
        print(f"NO-GO: backlog CSV not found: {backlog_path}")
        return 2

    reg_path = Path(args.registry).resolve()
    if not reg_path.exists():
        print(f"NO-GO: registry not found: {reg_path}")
        return 2

    tags_map = load_registry(reg_path)

    rows: List[Dict[str, str]] = []
    with backlog_path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        rows = [row for row in r]
        if not rows:
            print("NO-GO: backlog CSV empty")
            return 2

    selected: List[Dict[str, str]] = []
    for row in rows:
        if len(selected) >= args.n:
            break
        if str(row.get("has_definition_long", "")).strip().lower() == "true":
            continue
        selected.append(row)

    if not selected:
        print("NO-GO: no eligible tags found in backlog (check CSV integrity)", flush=True)
        return 2

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = repo / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)

    archive_dir = repo / "archive"
    safe_backup(out_path, archive_dir)
    with out_path.open("w", encoding="utf-8") as f:
        for row in selected:
            tag_id = row.get("tag_id", "")
            tag_obj = tags_map.get(tag_id, {})
            sem = tag_obj.get("semantics") if isinstance(tag_obj.get("semantics"), dict) else {}
            if has_def_long(sem):
                continue
            canonical_name = tag_obj.get("canonical_name") or tag_obj.get("canonicalName") or tag_obj.get("name") or ""
            name = normalize_name(tag_id, canonical_name)
            def_short = pick_def_short(sem)
            payload = {
                "tag_id": tag_id,
                "definition_long": long_definition(tag_id, name, def_short),
            }
            f.write(json.dumps(payload, ensure_ascii=True) + "\n")

    print(f"OK: wrote {len(selected)} tags to {out_path}")
    for row in selected:
        print(row.get("tag_id", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
