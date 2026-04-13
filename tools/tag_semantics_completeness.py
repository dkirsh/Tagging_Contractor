#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, os, sys, datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

def is_empty(v: Any) -> bool:
    if v is None: return True
    if isinstance(v, str): return v.strip() == ""
    if isinstance(v, (list, dict, tuple, set)): return len(v) == 0
    return False

def as_list(v: Any) -> List[Any]:
    if v is None: return []
    if isinstance(v, list): return v
    if isinstance(v, tuple): return list(v)
    if isinstance(v, str):
        s = v.strip()
        return [] if not s else [s]
    return [v]

def get_tag_id(tag_obj: Dict[str, Any], fallback: Optional[str]=None) -> Optional[str]:
    for k in ("tag_id", "tagId", "id"):
        v = tag_obj.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return fallback

def find_registry(repo_root: Path) -> Optional[Path]:
    # Try common patterns; pick newest mtime
    cands: List[Path] = []
    for pat in ("**/registry_v*.json", "**/*registry*.json"):
        cands += [p for p in repo_root.glob(pat) if p.is_file()]
    if not cands:
        return None
    cands.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return cands[0]

def load_registry(reg_path: Path) -> Tuple[Dict[str, Any], Dict[str, Dict[str, Any]]]:
    obj = json.loads(reg_path.read_text(encoding="utf-8"))
    tags_map: Dict[str, Dict[str, Any]] = {}

    # Supports:
    # 1) {"tags": {tag_id: tag_obj, ...}}
    # 2) {"tags": [tag_obj, ...]}
    # 3) {"registry": {"tags": ...}}
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
                if tid: tags_map[tid] = t
    elif isinstance(obj, dict) and isinstance(obj.get("tags"), dict):
        for tid, t in obj["tags"].items():
            if isinstance(t, dict):
                tags_map[str(tid)] = t
    elif isinstance(obj, list):
        for t in obj:
            if isinstance(t, dict):
                tid = get_tag_id(t)
                if tid: tags_map[tid] = t
    else:
        raise RuntimeError("Unsupported registry shape: cannot find tags map/list")

    return obj, tags_map

def merge_aliases(tag_obj: Dict[str, Any]) -> List[str]:
    sem = tag_obj.get("semantics") if isinstance(tag_obj.get("semantics"), dict) else {}
    a1 = as_list(tag_obj.get("aliases"))
    a2 = as_list(sem.get("aliases"))
    out: List[str] = []
    seen = set()
    for x in a1 + a2:
        if not isinstance(x, str): continue
        s = x.strip()
        if not s: continue
        k = s.lower()
        if k in seen: continue
        seen.add(k)
        out.append(s)
    return out

def score_counts(count: int, thresh: int, points: int) -> int:
    if thresh <= 0: return 0
    frac = min(max(count, 0) / float(thresh), 1.0)
    return int(round(points * frac))

def compute_completeness(tag_obj: Dict[str, Any]) -> Dict[str, Any]:
    sem = tag_obj.get("semantics") if isinstance(tag_obj.get("semantics"), dict) else {}

    def_short = sem.get("definition_short")
    def_long  = sem.get("definition_long") or sem.get("definition")
    has_def_short = not is_empty(def_short)
    has_def_long  = not is_empty(def_long)

    aliases = merge_aliases(tag_obj)
    alias_count = len(aliases)

    pos = as_list(sem.get("examples_positive"))
    neg = as_list(sem.get("examples_negative"))
    pos_count = len([x for x in pos if not is_empty(x)])
    neg_count = len([x for x in neg if not is_empty(x)])

    inc = as_list(sem.get("scope_includes"))
    exc = as_list(sem.get("scope_excludes"))
    inc_count = len([x for x in inc if not is_empty(x)])
    exc_count = len([x for x in exc if not is_empty(x)])

    notes_2d = sem.get("extraction_notes_2d")
    notes_3d = sem.get("extraction_notes_3d")
    has_2d = not is_empty(notes_2d)
    has_3d = not is_empty(notes_3d)

    # scoring
    score = 0
    score += 15 if has_def_short else 0
    score += 15 if has_def_long else 0
    score += score_counts(alias_count, 6, 15)
    score += score_counts(pos_count, 2, 10)
    score += score_counts(neg_count, 2, 10)
    score += score_counts(inc_count, 3, 8)   # 8+7 = 15
    score += score_counts(exc_count, 3, 7)
    score += 10 if has_2d else 0
    score += 10 if has_3d else 0

    bucket = "P2" if score >= 70 else ("P1" if score >= 40 else "P0")

    missing: List[str] = []
    if not has_def_short: missing.append("def_short")
    if not has_def_long:  missing.append("def_long")
    if alias_count < 6:   missing.append(f"aliases<{6}({alias_count})")
    if pos_count < 2:     missing.append(f"pos_examples<{2}({pos_count})")
    if neg_count < 2:     missing.append(f"neg_examples<{2}({neg_count})")
    if inc_count < 3:     missing.append(f"scope_includes<{3}({inc_count})")
    if exc_count < 3:     missing.append(f"scope_excludes<{3}({exc_count})")
    if not has_2d:        missing.append("notes_2d")
    if not has_3d:        missing.append("notes_3d")

    return {
        "has_def_short": has_def_short,
        "has_def_long": has_def_long,
        "alias_count": alias_count,
        "pos_examples_count": pos_count,
        "neg_examples_count": neg_count,
        "scope_includes_count": inc_count,
        "scope_excludes_count": exc_count,
        "has_notes_2d": has_2d,
        "has_notes_3d": has_3d,
        "completeness_score": score,
        "bucket": bucket,
        "missing_fields": ";".join(missing),
    }

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

def safe_backup(path: Path, archive_dir: Path):
    if path.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / f"{path.name}.bak_{ts}"
        dst.write_bytes(path.read_bytes())

def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, Any]], archive_dir: Path):
    safe_backup(path, archive_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--registry", default="")
    ap.add_argument("--audit", default="")
    ap.add_argument("--out-csv", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-next25", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    reg_path = Path(args.registry).resolve() if args.registry else find_registry(repo)
    if not reg_path or not reg_path.exists():
        print("ERROR: registry not found; pass --registry", file=sys.stderr)
        return 2

    audit_path = Path(args.audit).resolve() if args.audit else Path("")
    audit_map = read_audit(audit_path) if str(audit_path) else {}

    _, tags_map = load_registry(reg_path)
    rows: List[Dict[str, Any]] = []

    for tid, tag_obj in tags_map.items():
        if not isinstance(tag_obj, dict):
            continue
        canonical_name = tag_obj.get("canonical_name") or tag_obj.get("canonicalName") or tag_obj.get("name") or ""
        c = compute_completeness(tag_obj)
        row = {"tag_id": tid, "canonical_name": canonical_name}
        row.update(c)

        # bring in relation_count if present
        arow = audit_map.get(tid, {})
        rc = arow.get("relation_count") or arow.get("relationCount") or arow.get("relations") or ""
        ac = arow.get("alias_count") or arow.get("aliasCount") or arow.get("aliases") or ""
        row["relation_count"] = rc
        row["audit_alias_count"] = ac
        rows.append(row)

    archive_dir = repo / "archive"
    out_csv = Path(args.out_csv).resolve()
    out_md = Path(args.out_md).resolve()
    out_next25 = Path(args.out_next25).resolve()

    fieldnames = [
        "tag_id","canonical_name",
        "relation_count","audit_alias_count",
        "completeness_score","bucket","missing_fields",
        "has_def_short","has_def_long",
        "alias_count",
        "pos_examples_count","neg_examples_count",
        "scope_includes_count","scope_excludes_count",
        "has_notes_2d","has_notes_3d",
    ]
    write_csv(out_csv, fieldnames, rows, archive_dir)

    # summary counts
    def bucket_counts(filter_fn=None):
        bc = {"P0":0,"P1":0,"P2":0}
        for r in rows:
            if filter_fn and not filter_fn(r): 
                continue
            b = r.get("bucket","P0")
            if b in bc: bc[b]+=1
        return bc

    # relation-linked filter if audit available
    def is_relation_linked(r):
        try:
            return int(str(r.get("relation_count","0") or "0")) > 0
        except:
            return False

    overall = bucket_counts()
    rel = bucket_counts(is_relation_linked) if audit_map else {"P0":"n/a","P1":"n/a","P2":"n/a"}

    # Next25 weakest relation-linked tags (if audit present)
    next25_rows: List[Dict[str, Any]] = []
    if audit_map:
        rel_rows = [r for r in rows if is_relation_linked(r)]
        def rc_int(r):
            try: return int(str(r.get("relation_count","0") or "0"))
            except: return 0
        rel_rows.sort(key=lambda r: (int(r.get("completeness_score",0)), -rc_int(r), r.get("tag_id","")))
        for i, r in enumerate(rel_rows[:25], start=1):
            next25_rows.append({
                "rank": i,
                "tag_id": r.get("tag_id",""),
                "canonical_name": r.get("canonical_name",""),
                "relation_count": r.get("relation_count",""),
                "completeness_score": r.get("completeness_score",""),
                "bucket": r.get("bucket",""),
                "missing_fields": r.get("missing_fields",""),
            })
        write_csv(out_next25,
                  ["rank","tag_id","canonical_name","relation_count","completeness_score","bucket","missing_fields"],
                  next25_rows, archive_dir)
    else:
        safe_backup(out_next25, archive_dir)
        out_next25.write_text("No audit CSV provided; cannot compute relation-linked Next25.\n", encoding="utf-8")

    # write md summary
    safe_backup(out_md, archive_dir)
    md = []
    md.append("# Tag semantics completeness summary\n")
    md.append(f"- Registry: `{reg_path}`\n")
    if audit_map:
        md.append(f"- Audit: `{audit_path}`\n")
    md.append("\n## Buckets (overall)\n")
    md.append(f"- P0 (<40): {overall['P0']}\n- P1 (40–69): {overall['P1']}\n- P2 (>=70): {overall['P2']}\n")
    md.append("\n## Buckets (relation-linked; relation_count>0)\n")
    md.append(f"- P0: {rel['P0']}\n- P1: {rel['P1']}\n- P2: {rel['P2']}\n")
    md.append("\n## Outputs\n")
    md.append(f"- `{out_csv}`\n- `{out_md}`\n- `{out_next25}`\n")
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("".join(md), encoding="utf-8")

    print("OK: completeness reports written")
    print("Overall buckets:", overall)
    print("Relation-linked buckets:", rel)
    if next25_rows:
        print("Next25 (relation-linked) written:", out_next25)
        print("Top 10 Next25:")
        for r in next25_rows[:10]:
            print(f" {r['rank']:>2}. {r['tag_id']} score={r['completeness_score']} missing={r['missing_fields']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
