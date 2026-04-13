#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def is_empty(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip() == ""
    if isinstance(v, (list, dict, tuple, set)):
        return len(v) == 0
    return False


def as_list(v: Any) -> List[Any]:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    if isinstance(v, tuple):
        return list(v)
    if isinstance(v, str):
        s = v.strip()
        return [] if not s else [s]
    return [v]


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


def merge_aliases(tag_obj: Dict[str, Any]) -> List[str]:
    sem = tag_obj.get("semantics") if isinstance(tag_obj.get("semantics"), dict) else {}
    a1 = as_list(tag_obj.get("aliases"))
    a2 = as_list(sem.get("aliases"))
    out: List[str] = []
    seen = set()
    for x in a1 + a2:
        if not isinstance(x, str):
            continue
        s = x.strip()
        if not s:
            continue
        k = s.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(s)
    return out


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


def pick_def_long(sem: Dict[str, Any]) -> str:
    v = sem.get("definition_long")
    if isinstance(v, str) and v.strip():
        return v.strip()
    d = sem.get("definition")
    if isinstance(d, dict):
        for k in ("long", "detailed", "full"):
            v = d.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return ""


def examples_counts(sem: Dict[str, Any]) -> Tuple[int, int]:
    pos = []
    neg = []
    ex = sem.get("examples")
    if isinstance(ex, dict):
        pos = as_list(ex.get("positive"))
        neg = as_list(ex.get("negative"))
    else:
        pos = as_list(sem.get("examples_positive"))
        neg = as_list(sem.get("examples_negative"))
    pos_count = len([x for x in pos if not is_empty(x)])
    neg_count = len([x for x in neg if not is_empty(x)])
    return pos_count, neg_count


def scope_counts(sem: Dict[str, Any]) -> Tuple[int, int]:
    inc = []
    exc = []
    scope = sem.get("scope")
    if isinstance(scope, dict):
        inc = as_list(scope.get("includes"))
        exc = as_list(scope.get("excludes"))
    else:
        inc = as_list(sem.get("scope_includes"))
        exc = as_list(sem.get("scope_excludes"))
    inc_count = len([x for x in inc if not is_empty(x)])
    exc_count = len([x for x in exc if not is_empty(x)])
    return inc_count, exc_count


def extraction_notes(sem: Dict[str, Any]) -> Tuple[bool, bool]:
    extraction = sem.get("extraction")
    has_2d = False
    has_3d = False
    if isinstance(extraction, dict):
        has_2d = bool(extraction.get("from_2d_images")) or not is_empty(extraction.get("notes_2d"))
        has_3d = bool(extraction.get("from_3d_vr")) or not is_empty(extraction.get("notes_3d"))
    if not is_empty(sem.get("extraction_notes_2d")):
        has_2d = True
    if not is_empty(sem.get("extraction_notes_3d")):
        has_3d = True
    return has_2d, has_3d


def relation_count(sem: Dict[str, Any]) -> int:
    total = 0
    for k in ("related_tags", "inverse_of", "factor_associations"):
        v = sem.get(k)
        if isinstance(v, list):
            total += len([a for a in v if str(a).strip()])
        elif isinstance(v, dict):
            total += len(v.keys())
        elif isinstance(v, str) and v.strip():
            total += 1
    return total


def safe_backup(path: Path, archive_dir: Path) -> None:
    if path.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / f"{path.name}.bak_{ts}"
        dst.write_bytes(path.read_bytes())


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, Any]], archive_dir: Path) -> None:
    safe_backup(path, archive_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--registry", required=True)
    ap.add_argument("--out-csv", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    reg_path = Path(args.registry).resolve()
    if not reg_path.exists():
        print(f"NO-GO: registry not found: {reg_path}")
        return 2

    tags_map = load_registry(reg_path)
    rows: List[Dict[str, Any]] = []

    def_short_ct = 0
    def_long_ct = 0
    def_any_ct = 0
    alias_any_ct = 0
    ex_any_ct = 0
    scope_any_ct = 0
    notes_any_ct = 0

    for tid, tag_obj in tags_map.items():
        if not isinstance(tag_obj, dict):
            continue
        canonical_name = tag_obj.get("canonical_name") or tag_obj.get("canonicalName") or tag_obj.get("name") or ""
        sem = tag_obj.get("semantics") if isinstance(tag_obj.get("semantics"), dict) else {}

        def_short = pick_def_short(sem)
        def_long = pick_def_long(sem)
        has_def_short = not is_empty(def_short)
        has_def_long = not is_empty(def_long)
        if has_def_short:
            def_short_ct += 1
        if has_def_long:
            def_long_ct += 1
        if has_def_short or has_def_long:
            def_any_ct += 1

        aliases = merge_aliases(tag_obj)
        alias_count = len(aliases)
        if alias_count > 0:
            alias_any_ct += 1

        pos_count, neg_count = examples_counts(sem)
        has_examples = (pos_count + neg_count) > 0
        if has_examples:
            ex_any_ct += 1

        inc_count, exc_count = scope_counts(sem)
        has_scope = (inc_count + exc_count) > 0
        if has_scope:
            scope_any_ct += 1

        has_2d, has_3d = extraction_notes(sem)
        has_notes = has_2d or has_3d
        if has_notes:
            notes_any_ct += 1

        rows.append({
            "tag_id": tid,
            "canonical_name": canonical_name,
            "has_definition_short": has_def_short,
            "has_definition_long": has_def_long,
            "has_any_definition": has_def_short or has_def_long,
            "alias_count": alias_count,
            "examples_positive_count": pos_count,
            "examples_negative_count": neg_count,
            "has_any_examples": has_examples,
            "scope_includes_count": inc_count,
            "scope_excludes_count": exc_count,
            "has_any_scope": has_scope,
            "has_notes_2d": has_2d,
            "has_notes_3d": has_3d,
            "has_any_extraction_notes": has_notes,
            "relation_count": relation_count(sem),
        })

    rows.sort(key=lambda r: r["tag_id"])
    archive_dir = repo / "archive"
    out_csv = Path(args.out_csv).resolve()
    out_md = Path(args.out_md).resolve()

    fieldnames = list(rows[0].keys()) if rows else []
    write_csv(out_csv, fieldnames, rows, archive_dir)

    hubs = sorted(rows, key=lambda r: (-r["relation_count"], r["tag_id"]))
    top_hubs = hubs[:20]

    safe_backup(out_md, archive_dir)
    summary = []
    summary.append("# Tag Usability Audit Summary")
    summary.append("")
    summary.append(f"- Registry: `{reg_path}`")
    summary.append(f"- Total tags: **{len(rows)}**")
    summary.append(f"- Tags with any definition: **{def_any_ct}**")
    summary.append(f"- Tags with definition_short: **{def_short_ct}**")
    summary.append(f"- Tags with definition_long: **{def_long_ct}**")
    summary.append(f"- Tags with any aliases: **{alias_any_ct}**")
    summary.append(f"- Tags with any examples: **{ex_any_ct}**")
    summary.append(f"- Tags with any scope: **{scope_any_ct}**")
    summary.append(f"- Tags with any extraction notes: **{notes_any_ct}**")
    summary.append("")
    summary.append("## Top 20 hub tags by relation_count")
    for r in top_hubs:
        summary.append(f"- `{r['tag_id']}`: {r['relation_count']}")
    out_md.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print("OK: usability audit written")
    print(f"TOTAL {len(rows)}")
    print(f"HAS_ANY_DEFINITION {def_any_ct}")
    print(f"HAS_ANY_ALIASES {alias_any_ct}")
    print(f"HAS_ANY_EXAMPLES {ex_any_ct}")
    print(f"HAS_ANY_SCOPE {scope_any_ct}")
    print(f"HAS_ANY_EXTRACTION_NOTES {notes_any_ct}")
    print("TOP_HUBS")
    for r in top_hubs:
        print(r["tag_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
