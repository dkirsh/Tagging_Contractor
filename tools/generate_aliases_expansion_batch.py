#!/usr/bin/env python3
from __future__ import annotations
import argparse
import datetime
import json
from pathlib import Path
from typing import Any, Dict, List


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


def candidate_aliases(tag_id: str, name: str) -> List[str]:
    prefix = prefix_of(tag_id)
    base = name
    base_lower = base.lower()
    last_seg = tag_id.split(".")[-1].replace("_", " ").replace("/", " / ").strip()
    last_lower = last_seg.lower()
    sans_paren = " ".join(part for part in base.replace(")", "").split("(")[0:1]).strip()

    cands: List[str] = []
    for v in (base, base_lower, last_seg, last_lower, sans_paren):
        if v:
            cands.append(v)

    if prefix in ("touch", "smell", "sound"):
        cands += [
            f"measured {base_lower}",
            f"{base_lower} measurement",
            f"{base_lower} metric",
            f"{base_lower} level",
            f"{base_lower} reading",
        ]
    elif prefix in ("affect", "psych", "cognitive"):
        cands += [
            f"perceived {base_lower}",
            f"{base_lower} feeling",
            f"{base_lower} response",
            f"sense of {base_lower}",
        ]
    elif prefix in ("cnfa", "complexity", "fluency", "science", "isovist") or tag_id.startswith("env.v") or tag_id.startswith("env.v2"):
        cands += [
            f"{base_lower} metric",
            f"{base_lower} measure",
            f"{base_lower} index",
            f"{base_lower} value",
            f"{base_lower} score",
        ]
    elif prefix == "style":
        cands += [
            f"{base_lower} style",
            f"{base_lower} design",
            f"{base_lower} aesthetic",
            f"{base_lower} look",
        ]
    elif prefix in ("component", "material", "materials", "mat"):
        cands += [
            f"{base_lower} material",
            f"{base_lower} finish",
            f"{base_lower} component",
            f"{base_lower} surface",
        ]
    elif prefix in ("color", "light", "lighting"):
        cands += [
            f"{base_lower} color",
            f"{base_lower} lighting",
            f"{base_lower} tone",
            f"{base_lower} hue",
        ]
    else:
        cands += [
            f"{base_lower} attribute",
            f"{base_lower} feature",
            f"{base_lower} characteristic",
        ]

    cands += [
        f"{base_lower} present",
        f"presence of {base_lower}",
        f"visible {base_lower}",
        f"dominant {base_lower}",
    ]

    out: List[str] = []
    seen = set()
    for c in cands:
        s = c.strip()
        if not s:
            continue
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--registry", required=True)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--target", type=int, default=6)
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
        existing = as_list(tag_obj.get("aliases")) + as_list(sem.get("aliases"))
        existing_norm = {s.strip().lower() for s in existing if s.strip()}

        if len(existing_norm) >= args.target:
            continue

        canonical_name = tag_obj.get("canonical_name") or tag_obj.get("canonicalName") or tag_obj.get("name") or ""
        name = normalize_name(tag_id, canonical_name)
        cands = candidate_aliases(tag_id, name)
        new_aliases: List[str] = []
        for cand in cands:
            if len(existing_norm) + len(new_aliases) >= args.target:
                break
            key = cand.strip().lower()
            if key in existing_norm:
                continue
            if key in {a.lower() for a in new_aliases}:
                continue
            new_aliases.append(cand)

        if not new_aliases:
            continue

        selected.append({
            "tag_id": tag_id,
            "aliases": new_aliases,
        })

        if len(selected) >= args.n:
            break

    if not selected:
        print("NO-GO: no tags require alias expansion")
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
