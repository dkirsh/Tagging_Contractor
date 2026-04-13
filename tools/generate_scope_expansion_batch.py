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
        inc = [
            f"Measured sensor or lab data indicates {name}.",
            f"Instrumented readings support {name}.",
            f"Material or acoustic testing reports {name}.",
        ]
        exc = [
            f"Visual inference of {name} without sensor data.",
            f"Unverified claims of {name} without measurement.",
            f"Measured values contradict {name}.",
        ]
        return inc, exc

    if prefix in ("affect", "psych", "cognitive"):
        inc = [
            f"User reports describe the space as {name}.",
            f"Validated survey or rating data indicates {name}.",
            f"Consistent behavioral indicators align with {name}.",
        ]
        exc = [
            f"No user-reported evidence of {name}.",
            f"Opposite affective descriptors dominate the response.",
            f"Speculative inference of {name} from style alone.",
        ]
        return inc, exc

    if prefix in ("cnfa", "complexity", "fluency", "science", "isovist") or lower_id.startswith("env.v") or lower_id.startswith("env.v2"):
        inc = [
            f"Computed metric for the scene indicates {name}.",
            f"Measured data supports {name}.",
            f"Recorded values fall within the {name} range.",
        ]
        exc = [
            f"Metric not computed or recorded for {name}.",
            f"Inferred {name} without measurement.",
            f"Recorded values contradict {name}.",
        ]
        return inc, exc

    if prefix == "style":
        inc = [
            f"Overall design language clearly aligns with {name}.",
            f"Multiple elements consistently express {name}.",
            f"{name} is the dominant stylistic character.",
        ]
        exc = [
            f"Single accent suggests {name} but is not dominant.",
            f"Mixed style where {name} is not primary.",
            f"Opposing style cues override {name}.",
        ]
        return inc, exc

    if lower_id.startswith("arch.pattern"):
        inc = [
            f"Pattern is structurally present and repeated.",
            f"Spatial organization clearly follows {name}.",
            f"Design intent explicitly shows {name}.",
        ]
        exc = [
            f"Partial or incidental instance of {name}.",
            f"Feature does not influence spatial organization.",
            f"Ambiguous pattern without clear {name}.",
        ]
        return inc, exc

    if prefix in ("component", "material", "materials", "mat"):
        inc = [
            f"{name} is a primary material or component in the scene.",
            f"{name} appears in substantial, visible areas.",
            f"Specifications list {name} as a key material or component.",
        ]
        exc = [
            f"Minor accents of {name} only.",
            f"Ambiguous or mixed materials where {name} is uncertain.",
            f"Background detail without significant presence of {name}.",
        ]
        return inc, exc

    if prefix in ("color", "light", "lighting"):
        inc = [
            f"{name} is the dominant color or lighting attribute.",
            f"Specifications or measurements indicate {name}.",
            f"Consistent cues across the scene show {name}.",
        ]
        exc = [
            f"Weak or isolated hints of {name}.",
            f"Color or lighting varies such that {name} is not dominant.",
            f"Speculative inference of {name} without evidence.",
        ]
        return inc, exc

    inc = [
        f"Clear, primary presence of {name}.",
        f"Multiple consistent cues indicate {name}.",
        f"Dominant instance of {name}.",
    ]
    exc = [
        f"Ambiguous or incidental hints of {name}.",
        f"Inferred {name} without evidence.",
        f"Single minor accent of {name}.",
    ]
    return inc, exc


def append_until(existing: List[str], candidates: List[str], target: int) -> List[str]:
    out = list(existing)
    existing_lower = {s.strip().lower() for s in out}
    for item in candidates:
        if len(out) >= target:
            break
        s = item.strip()
        if not s:
            continue
        if s.lower() in existing_lower:
            continue
        out.append(s)
        existing_lower.add(s.lower())
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
        scope = sem.get("scope") if isinstance(sem.get("scope"), dict) else {}

        inc = as_list(sem.get("scope_includes")) or as_list(scope.get("includes"))
        exc = as_list(sem.get("scope_excludes")) or as_list(scope.get("excludes"))

        if len(inc) >= args.target and len(exc) >= args.target:
            continue

        canonical_name = tag_obj.get("canonical_name") or tag_obj.get("canonicalName") or tag_obj.get("name") or ""
        name = normalize_name(tag_id, canonical_name)
        cand_inc, cand_exc = templates(tag_id, name)
        new_inc = append_until(inc, cand_inc, args.target)
        new_exc = append_until(exc, cand_exc, args.target)

        selected.append({
            "tag_id": tag_id,
            "scope_includes": new_inc,
            "scope_excludes": new_exc,
        })

        if len(selected) >= args.n:
            break

    if not selected:
        print("NO-GO: no tags require scope expansion")
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
