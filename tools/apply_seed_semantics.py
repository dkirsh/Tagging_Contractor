#!/usr/bin/env python3
"""
Apply seed semantics JSONL entries to the Tagging_Contractor registry (additive, defensive).

What it does
- Loads a registry JSON (auto-detected unless --registry is provided)
- For each JSONL row (one object per line), finds the matching tag by tag_id
- Adds/merges semantic fields under tag["semantics"] (and merges aliases to top-level aliases if present)
- Does NOT delete anything.
- Will not overwrite non-empty existing values unless --force is passed.
- Writes an archive copy of the original registry under ./archive/ before saving.

Expected JSONL schema (per line):
{
  "tag_id": "...",
  "definition_short": "...",
  "definition_long": "...",
  "aliases": [...],
  "examples_positive": [...],
  "examples_negative": [...],
  "scope_includes": [...],
  "scope_excludes": [...],
  "extraction_notes_2d": "...",
  "extraction_notes_3d": "..."
}

Usage examples
  python3 tools/apply_seed_semantics.py --repo-root . --jsonl seed/tag_semantics_top20.jsonl
  python3 tools/apply_seed_semantics.py --registry registry_v0.2.8.json --jsonl seed/tag_semantics_top20.jsonl

Return codes
  0 success
  2 input error (missing file, parse failure)
  3 registry structure unexpected
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _is_empty(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and v.strip() == "":
        return True
    if isinstance(v, (list, dict)) and len(v) == 0:
        return True
    return False


def _dedupe_preserve(seq: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for x in seq:
        if x is None:
            continue
        s = str(x).strip()
        if not s:
            continue
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def _parse_version_from_name(name: str) -> Tuple[int, ...]:
    m = re.search(r"v(\d+(?:\.\d+)*)", name)
    if not m:
        return tuple()
    return tuple(int(p) for p in m.group(1).split("."))


def _find_registry(repo_root: Path) -> Optional[Path]:
    patterns = [
        "registry_v*.json",
        "registry*.json",
        "registry/*.json",
        "data/registry*.json",
        "data/*.json",
    ]
    candidates: List[Path] = []
    for pat in patterns:
        candidates.extend(repo_root.glob(pat))

    candidates = [p for p in candidates if p.is_file() and p.suffix.lower() == ".json"]
    if not candidates:
        return None

    def score(p: Path) -> Tuple[int, Tuple[int, ...], float]:
        name = p.name
        is_registry = 1 if "registry" in name else 0
        v = _parse_version_from_name(name)
        mtime = p.stat().st_mtime
        return (is_registry, v, mtime)

    candidates.sort(key=score, reverse=True)
    return candidates[0]


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path: Path, obj: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")


def _iter_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _get_tag_id(tag_obj: Dict[str, Any]) -> Optional[str]:
    for k in ("tag_id", "tagId", "id"):
        v = tag_obj.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def _get_or_create_semantics(tag_obj: Dict[str, Any]) -> Dict[str, Any]:
    sem = tag_obj.get("semantics")
    if isinstance(sem, dict):
        return sem
    sem = {}
    tag_obj["semantics"] = sem
    return sem


def _merge_field(target: Dict[str, Any], key: str, value: Any, *, force: bool) -> bool:
    if force:
        target[key] = value
        return True
    if key not in target or _is_empty(target.get(key)):
        target[key] = value
        return True
    return False


def _merge_aliases(tag_obj: Dict[str, Any], sem: Dict[str, Any], new_aliases: List[str], *, force: bool) -> bool:
    changed = False

    existing_sem = sem.get("aliases", [])
    if not isinstance(existing_sem, list):
        existing_sem = []
    merged_sem = _dedupe_preserve(list(existing_sem) + list(new_aliases))
    if force or merged_sem != existing_sem:
        sem["aliases"] = merged_sem
        changed = True

    existing_top = tag_obj.get("aliases", None)
    if existing_top is None:
        tag_obj["aliases"] = merged_sem
        changed = True
    elif isinstance(existing_top, list):
        merged_top = _dedupe_preserve(list(existing_top) + list(new_aliases))
        if force or merged_top != existing_top:
            tag_obj["aliases"] = merged_top
            changed = True

    return changed


def apply_seed(registry_obj: Any, seed_rows: List[Dict[str, Any]], *, force: bool) -> Tuple[int, int, List[str]]:
    tags = None
    if isinstance(registry_obj, dict):
        if isinstance(registry_obj.get("tags"), (list, dict)):
            tags = registry_obj["tags"]
        elif isinstance(registry_obj.get("registry"), dict) and isinstance(registry_obj["registry"].get("tags"), list):
            tags = registry_obj["registry"]["tags"]
    elif isinstance(registry_obj, list):
        tags = registry_obj

    if not isinstance(tags, (list, dict)):
        raise RuntimeError("Could not find tags list/map in registry JSON (expected dict['tags'], dict['registry']['tags'], or list).")

    index: Dict[str, Dict[str, Any]] = {}
    if isinstance(tags, dict):
        for tid, t in tags.items():
            if isinstance(t, dict) and tid:
                index[tid] = t
    else:
        for t in tags:
            if not isinstance(t, dict):
                continue
            tid = _get_tag_id(t)
            if tid:
                index[tid] = t

    updated = 0
    missing: List[str] = []

    for row in seed_rows:
        tag_id = row.get("tag_id")
        if not isinstance(tag_id, str) or not tag_id.strip():
            continue
        tag_id = tag_id.strip()

        tag = index.get(tag_id)
        if tag is None:
            missing.append(tag_id)
            continue

        sem = _get_or_create_semantics(tag)
        changed = False

        ds = row.get("definition_short")
        dl = row.get("definition_long")
        if isinstance(ds, str):
            changed |= _merge_field(sem, "definition_short", ds, force=force)
        if isinstance(dl, str):
            changed |= _merge_field(sem, "definition_long", dl, force=force)
            changed |= _merge_field(sem, "definition", dl, force=False)

        for k in ("examples_positive","examples_negative","scope_includes","scope_excludes"):
            v = row.get(k)
            if isinstance(v, list):
                changed |= _merge_field(sem, k, v, force=force)

        for k in ("extraction_notes_2d","extraction_notes_3d"):
            v = row.get(k)
            if isinstance(v, str):
                changed |= _merge_field(sem, k, v, force=force)

        aliases = row.get("aliases", [])
        if isinstance(aliases, list):
            changed |= _merge_aliases(tag, sem, aliases, force=force)

        if changed:
            updated += 1

    return updated, len(missing), missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".", help="Repo root to search for registry (default: .)")
    ap.add_argument("--registry", default="", help="Path to registry JSON (if omitted, auto-detect)")
    ap.add_argument("--jsonl", required=True, help="Seed semantics JSONL file")
    ap.add_argument("--force", action="store_true", help="Overwrite non-empty existing fields")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    jsonl_path = Path(args.jsonl).expanduser().resolve()
    if not jsonl_path.exists():
        print(f"ERROR: JSONL not found: {jsonl_path}")
        return 2

    registry_path = Path(args.registry).expanduser().resolve() if args.registry else _find_registry(repo_root)
    if not registry_path or not registry_path.exists():
        print("ERROR: Could not auto-detect registry JSON. Pass --registry <path>.")
        return 2

    reg = _load_json(registry_path)
    rows = _iter_jsonl(jsonl_path)

    archive_dir = repo_root / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = archive_dir / f"{registry_path.name}.pre_seed_{ts}.json"
    shutil.copy2(registry_path, archive_path)

    updated, missing_n, missing_ids = apply_seed(reg, rows, force=args.force)
    _save_json(registry_path, reg)

    print("OK: Seed semantics applied.")
    print(f"Registry: {registry_path}")
    print(f"Archived original: {archive_path}")
    print(f"Updated tags: {updated}")
    print(f"Missing tag_ids from registry: {missing_n}")
    if missing_ids:
        for tid in missing_ids[:25]:
            print(f"  - {tid}")
        if len(missing_ids) > 25:
            print(f"  ... ({len(missing_ids)-25} more)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
