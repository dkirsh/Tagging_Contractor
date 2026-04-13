#!/usr/bin/env python3
from __future__ import annotations
import argparse
import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def safe_backup(path: Path, archive_dir: Path) -> None:
    if path.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / f"{path.name}.bak_{ts}"
        dst.write_bytes(path.read_bytes())


def as_list(v: Any) -> List[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    if isinstance(v, str):
        s = v.strip()
        return [s] if s else []
    return [str(v)]


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


def templates(tag_id: str, name: str) -> Tuple[List[str], List[str]]:
    prefix = prefix_of(tag_id)
    lower_id = tag_id.lower()

    if prefix in ("touch", "smell", "sound"):
        pos = [
            f"Measured data indicates {name}.",
            f"Sensor readings confirm {name}.",
            f"Lab testing supports {name}.",
        ]
        neg = [
            f"No measurement indicates {name}.",
            f"Recorded data does not support {name}.",
            f"Measurements contradict {name}.",
        ]
        return pos, neg

    if prefix in ("affect", "psych", "cognitive"):
        pos = [
            f"User reports describe the space as {name}.",
            f"Survey ratings indicate {name}.",
            f"Validated feedback shows {name}.",
        ]
        neg = [
            f"User reports do not describe the space as {name}.",
            f"Survey ratings indicate not {name}.",
            f"Feedback contradicts {name}.",
        ]
        return pos, neg

    if prefix in ("cnfa", "complexity", "fluency", "science", "isovist") or lower_id.startswith("env.v") or lower_id.startswith("env.v2"):
        pos = [
            f"Computed metric indicates {name}.",
            f"Measured values fall within {name}.",
            f"Calculated outputs support {name}.",
        ]
        neg = [
            f"Metric not computed for {name}.",
            f"Measured values do not indicate {name}.",
            f"Calculated outputs contradict {name}.",
        ]
        return pos, neg

    if prefix == "style":
        pos = [
            f"Overall design reads as {name}.",
            f"Multiple elements consistently express {name}.",
            f"The dominant style is {name}.",
        ]
        neg = [
            f"Overall design does not read as {name}.",
            f"Style cues are mixed; {name} is not dominant.",
            f"Isolated accents are not enough for {name}.",
        ]
        return pos, neg

    if lower_id.startswith("arch.pattern"):
        pos = [
            f"The pattern {name} is clearly present.",
            f"Spatial organization follows {name}.",
            f"{name} is a dominant architectural feature.",
        ]
        neg = [
            f"The pattern {name} is not present.",
            f"Spatial organization does not follow {name}.",
            f"Only incidental hints of {name} appear.",
        ]
        return pos, neg

    if prefix in ("component", "material", "materials", "mat"):
        pos = [
            f"{name} is a primary material or component.",
            f"{name} is clearly visible in the scene.",
            f"{name} is specified in the materials list.",
        ]
        neg = [
            f"{name} is not present.",
            f"{name} is only a minor accent at most.",
            f"Materials list does not include {name}.",
        ]
        return pos, neg

    if prefix in ("color", "light", "lighting"):
        pos = [
            f"{name} is the dominant color or lighting attribute.",
            f"{name} is clearly visible or specified.",
            f"Consistent cues show {name}.",
        ]
        neg = [
            f"{name} is not visually present.",
            f"{name} is not the dominant attribute.",
            f"Only weak cues suggest {name}.",
        ]
        return pos, neg

    pos = [
        f"Clear evidence of {name} is present.",
        f"{name} is a dominant attribute.",
        f"Multiple cues indicate {name}.",
    ]
    neg = [
        f"No clear evidence of {name} is present.",
        f"{name} is not a dominant attribute.",
        f"Only weak cues suggest {name}.",
    ]
    return pos, neg


def dedupe_preserve(items: List[str]) -> List[str]:
    out = []
    seen = set()
    for s in items:
        key = s.strip().lower()
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(s.strip())
    return out


def append_until(existing: List[str], candidates: List[str], target: int) -> List[str]:
    out = dedupe_preserve(existing)
    for item in candidates:
        if len(out) >= target:
            break
        if item.strip().lower() in {s.lower() for s in out}:
            continue
        out.append(item.strip())
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--registry", required=True)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--target", type=int, default=3)
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
        ex = sem.get("examples") if isinstance(sem.get("examples"), dict) else {}
        pos = as_list(sem.get("examples_positive")) or as_list(ex.get("positive"))
        neg = as_list(sem.get("examples_negative")) or as_list(ex.get("negative"))

        if len(pos) >= args.target and len(neg) >= args.target:
            continue

        canonical_name = tag_obj.get("canonical_name") or tag_obj.get("canonicalName") or tag_obj.get("name") or ""
        name = normalize_name(tag_id, canonical_name)
        cand_pos, cand_neg = templates(tag_id, name)
        new_pos = append_until(pos, cand_pos, args.target)
        new_neg = append_until(neg, cand_neg, args.target)

        selected.append({
            "tag_id": tag_id,
            "examples_positive": new_pos,
            "examples_negative": new_neg,
        })

        if len(selected) >= args.n:
            break

    if not selected:
        print("NO-GO: no tags require example expansion")
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
