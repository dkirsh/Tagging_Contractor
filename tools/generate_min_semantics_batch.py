#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, datetime
from pathlib import Path
from typing import Any, Dict, List


def safe_backup(path: Path, archive_dir: Path) -> None:
    if path.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / f"{path.name}.bak_{ts}"
        dst.write_bytes(path.read_bytes())


def parse_int(v: Any, default: int = 0) -> int:
    try:
        return int(float(str(v)))
    except Exception:
        return default


def normalize_name(tag_id: str, canonical_name: str) -> str:
    name = canonical_name.strip() if canonical_name else ""
    if not name:
        name = tag_id.split(".")[-1]
    name = name.replace("_", " ").replace("/", " / ")
    name = " ".join(name.split())
    return name


def prefix_of(tag_id: str) -> str:
    return tag_id.split(".", 1)[0] if "." in tag_id else tag_id


def definition_short(tag_id: str, name: str) -> str:
    prefix = prefix_of(tag_id)
    if prefix == "touch":
        return f"Measured tactile property: {name} as reported by material or haptic data rather than visual appearance."
    if prefix == "affect":
        return f"Perceived affective response described as {name} in the observer's experience of the environment."
    if prefix == "env":
        return f"Observable environmental attribute where {name} is present."
    if prefix == "form":
        return f"Formal or shape attribute characterized by {name}."
    if prefix == "mat":
        return f"Material attribute characterized by {name}."
    if prefix == "color":
        return f"Color attribute characterized by {name}."
    if prefix in ("light", "lighting"):
        return f"Lighting attribute characterized by {name}."
    if prefix == "obj":
        return f"Object or fixture attribute characterized by {name}."
    return f"Tag indicating presence of {name} in the scene or data."


def build_aliases(tag_id: str, name: str) -> List[str]:
    prefix = prefix_of(tag_id)
    id_phrase = normalize_name(tag_id, "")
    raw: List[str] = []
    if name:
        raw += [name, name.lower(), f"{name} present", f"presence of {name}"]
    if id_phrase and id_phrase.lower() != name.lower():
        raw += [id_phrase, id_phrase.lower()]
    if prefix == "touch":
        raw += [f"tactile {name}", f"haptic {name}", f"measured {name}"]
    elif prefix == "affect":
        raw += [f"{name} feeling", f"feels {name}", f"sense of {name}"]
    else:
        raw += [f"visible {name}", f"{name} attribute"]

    out: List[str] = []
    seen = set()
    for a in raw:
        s = a.strip()
        if not s:
            continue
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(s)

    if len(out) < 3:
        extras = [f"{name} characteristic", f"{name} feature", f"characterized by {name}"]
        for a in extras:
            key = a.lower()
            if key not in seen and len(out) < 3:
                out.append(a)
                seen.add(key)

    return out[:6]


def examples(tag_id: str, name: str) -> Dict[str, List[str]]:
    prefix = prefix_of(tag_id)
    if prefix == "touch":
        pos = [f"Material sample with measured {name}.", f"Haptic data indicates {name}."]
        neg = [f"No tactile measurements indicate {name}.", f"{name} is only inferred visually."]
    elif prefix == "affect":
        pos = [f"Viewer reports the space as {name}.", f"User feedback describes a {name} feeling."]
        neg = [f"Viewer does not describe the space as {name}.", f"Feedback indicates the space is not {name}."]
    else:
        pos = [f"Scene clearly shows {name}.", f"{name} is a dominant visible attribute."]
        neg = [f"Scene does not show {name}.", f"{name} is not visibly present."]
    return {"pos": pos[:2], "neg": neg[:2]}


def scopes(tag_id: str, name: str) -> Dict[str, List[str]]:
    prefix = prefix_of(tag_id)
    if prefix == "touch":
        inc = [f"Measured tactile data reporting {name}.", f"Material specs listing {name}."]
        exc = [f"Visual guesses of {name} without tactile data.", f"Unverified descriptions of {name}."]
    elif prefix == "affect":
        inc = [f"Explicit user reports of {name}.", f"Consistent cues linked to described {name} response."]
        exc = ["Speculative emotional inference without evidence.", "Opposite affective descriptors."]
    else:
        inc = [f"Clear, primary presence of {name}.", f"Dominant visible instance of {name}."]
        exc = [f"Ambiguous or incidental hints of {name}.", f"Inferred {name} without visual evidence."]
    return {"inc": inc[:4], "exc": exc[:4]}


def extraction_notes(tag_id: str, name: str) -> Dict[str, str]:
    prefix = prefix_of(tag_id)
    if prefix == "touch":
        notes_2d = "Not inferable from 2D imagery; requires material or tactile measurements."
        notes_3d = "3D geometry alone is insufficient; use physical measurements or material data."
    elif prefix == "affect":
        notes_2d = "Use only when affect is explicitly reported or strongly evidenced; avoid projecting emotion."
        notes_3d = "Prefer user feedback or validated behavioral data; geometry alone is insufficient."
    else:
        notes_2d = f"From 2D imagery, rely on clear visual cues of {name}; avoid inference."
        notes_3d = f"From 3D or scene data, use geometry, material, or lighting cues for {name}; avoid speculation."
    return {"2d": notes_2d, "3d": notes_3d}


def select_rows(rows: List[Dict[str, Any]], n: int, prefixes: List[str]) -> List[Dict[str, Any]]:
    def bucket_rank(b: str) -> int:
        return {"P0": 0, "P1": 1, "P2": 2}.get(b or "", 3)

    def matches_prefix(tag_id: str) -> bool:
        if not prefixes:
            return True
        for p in prefixes:
            if tag_id.startswith(p):
                return True
            if not p.endswith(".") and tag_id.startswith(p + "."):
                return True
        return False

    filtered = [r for r in rows if matches_prefix(r.get("tag_id", ""))]
    filtered.sort(key=lambda r: (
        bucket_rank(r.get("bucket", "")),
        parse_int(r.get("completeness_score", 0)),
        r.get("tag_id", ""),
    ))
    return filtered[:n]


def read_completeness(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return [row for row in r]


def build_payload(row: Dict[str, Any]) -> Dict[str, Any]:
    tag_id = row.get("tag_id", "").strip()
    canonical_name = row.get("canonical_name", "").strip()
    name = normalize_name(tag_id, canonical_name)
    payload: Dict[str, Any] = {
        "tag_id": tag_id,
        "definition_short": definition_short(tag_id, name),
        "aliases": build_aliases(tag_id, name),
        "examples_positive": examples(tag_id, name)["pos"],
        "examples_negative": examples(tag_id, name)["neg"],
        "scope_includes": scopes(tag_id, name)["inc"],
        "scope_excludes": scopes(tag_id, name)["exc"],
        "extraction_notes_2d": extraction_notes(tag_id, name)["2d"],
        "extraction_notes_3d": extraction_notes(tag_id, name)["3d"],
    }
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--completeness", default="reports/tag_semantics_completeness.csv")
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--prefix", default="")
    ap.add_argument("--out", default="seed/tag_semantics_min_batch_01.jsonl")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    completeness = Path(args.completeness)
    if not completeness.is_absolute():
        completeness = repo / completeness
    if not completeness.exists():
        print(f"ERROR: completeness CSV not found: {completeness}")
        return 2

    out = Path(args.out)
    if not out.is_absolute():
        out = repo / out
    out.parent.mkdir(parents=True, exist_ok=True)

    prefixes = [p.strip() for p in args.prefix.split(",") if p.strip()] if args.prefix else []

    rows = read_completeness(completeness)
    selected = select_rows(rows, args.n, prefixes)

    archive_dir = repo / "archive"
    safe_backup(out, archive_dir)
    with out.open("w", encoding="utf-8") as f:
        for row in selected:
            payload = build_payload(row)
            f.write(json.dumps(payload, ensure_ascii=True) + "\n")

    print(f"OK: wrote {len(selected)} tags to {out}")
    for row in selected:
        print(row.get("tag_id", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
