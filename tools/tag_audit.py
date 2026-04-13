#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path
import sys


def get(d, path, default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def truthy_text(x):
    return isinstance(x, str) and x.strip() != ""


def as_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return [str(a).strip() for a in x if str(a).strip()]
    if isinstance(x, str):
        s = x.strip()
        return [s] if s else []
    return [str(x).strip()]


def pick_def_short(sem):
    if truthy_text(sem.get("definition")):
        return sem.get("definition").strip()
    if truthy_text(sem.get("definition_short")):
        return sem.get("definition_short").strip()
    if truthy_text(sem.get("def")):
        return sem.get("def").strip()
    if truthy_text(sem.get("notes")):
        return sem.get("notes").strip()
    if truthy_text(sem.get("description")):
        return sem.get("description").strip()
    if truthy_text(sem.get("meaning")):
        return sem.get("meaning").strip()

    d = sem.get("definition")
    if isinstance(d, dict):
        for k in ("short", "summary", "text"):
            if truthy_text(d.get(k)):
                return d.get(k).strip()
    return ""


def pick_def_long(sem):
    if truthy_text(sem.get("definition_long")):
        return sem.get("definition_long").strip()
    d = sem.get("definition")
    if isinstance(d, dict):
        for k in ("long", "detailed", "full"):
            if truthy_text(d.get(k)):
                return d.get(k).strip()
    return ""


def pick_aliases(sem):
    for k in ("aliases", "alias", "synonyms", "aka"):
        if k in sem:
            return as_list(sem.get(k))
    return []


def has_examples(sem):
    ex = sem.get("examples")
    if isinstance(ex, dict):
        pos = as_list(ex.get("positive"))
        neg = as_list(ex.get("negative"))
        return len(pos) > 0 or len(neg) > 0
    if isinstance(ex, list):
        return len(as_list(ex)) > 0
    return False


def has_scope(sem):
    scope = sem.get("scope")
    if isinstance(scope, dict):
        inc = as_list(scope.get("includes"))
        exc = as_list(scope.get("excludes"))
        return len(inc) > 0 or len(exc) > 0
    inc = as_list(sem.get("scope_includes"))
    exc = as_list(sem.get("scope_excludes"))
    return len(inc) > 0 or len(exc) > 0


def has_extraction_notes(sem):
    extraction = sem.get("extraction")
    has_2d = False
    has_3d = False
    if isinstance(extraction, dict):
        has_2d = bool(extraction.get("from_2d_images")) or truthy_text(extraction.get("notes_2d"))
        has_3d = bool(extraction.get("from_3d_vr")) or truthy_text(extraction.get("notes_3d"))
    if truthy_text(sem.get("extraction_notes_2d")):
        has_2d = True
    if truthy_text(sem.get("extraction_notes_3d")):
        has_3d = True
    return has_2d, has_3d


def relation_count(sem):
    total = 0
    for k in ("related_tags", "inverse_of", "factor_associations"):
        v = sem.get(k)
        if isinstance(v, list):
            total += len([a for a in v if str(a).strip()])
        elif isinstance(v, dict):
            total += len(v.keys())
        elif truthy_text(v):
            total += 1
    return total


def priority(def_len, alias_ct):
    if def_len == 0:
        return "P0"
    if def_len < 40 or alias_ct == 0:
        return "P1"
    return "P2"


def main(registry_path, out_dir):
    reg = Path(registry_path)
    if not reg.exists():
        print(f"NO-GO: registry not found: {reg}", file=sys.stderr)
        return 2

    data = json.loads(reg.read_text(encoding="utf-8"))
    tags = data.get("tags") or data.get("registry") or data.get("items") or []
    if isinstance(tags, dict):
        tags = [{"tag_id": k, **(v if isinstance(v, dict) else {})} for k, v in tags.items()]

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    alias_count_dist = Counter()
    priority_counts = Counter()
    def_any = 0
    alias_any = 0

    for t in tags:
        tag_id = t.get("tag_id") or t.get("id") or t.get("name") or t.get("slug") or "UNKNOWN"
        canonical_name = t.get("canonical_name") or ""
        sem = t.get("semantics") if isinstance(t.get("semantics"), dict) else {}

        def_short = pick_def_short(sem)
        def_long = pick_def_long(sem)
        aliases = pick_aliases(sem)

        def_short_len = len(def_short) if truthy_text(def_short) else 0
        has_def_short = def_short_len > 0
        has_def_long = truthy_text(def_long)

        if has_def_short or has_def_long:
            def_any += 1
        if len(aliases) > 0:
            alias_any += 1

        alias_ct = len(aliases)
        alias_count_dist[alias_ct] += 1

        pr = priority(def_short_len or (len(def_long) if has_def_long else 0), alias_ct)
        priority_counts[pr] += 1

        ex = has_examples(sem)
        scope = has_scope(sem)
        has_2d, has_3d = has_extraction_notes(sem)
        rel_ct = relation_count(sem)

        rows.append({
            "tag_id": tag_id,
            "canonical_name": canonical_name,
            "has_definition_short": has_def_short,
            "definition_short_len": def_short_len,
            "has_definition_long": has_def_long,
            "alias_count": alias_ct,
            "has_examples": ex,
            "has_scope_includes_excludes": scope,
            "has_extraction_notes_2d": has_2d,
            "has_extraction_notes_3d": has_3d,
            "relation_count": rel_ct,
            "current_priority": pr,
        })

    rows.sort(key=lambda r: r["tag_id"])

    csv_path = out_dir / "tag_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(rows[0].keys()) if rows else []
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    hubs = sorted(rows, key=lambda r: (-r["relation_count"], r["tag_id"]))
    top_hubs = hubs[:50]

    top_hubs_path = out_dir / "top_hubs.csv"
    with top_hubs_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["tag_id", "canonical_name", "relation_count"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in top_hubs:
            w.writerow({
                "tag_id": r["tag_id"],
                "canonical_name": r["canonical_name"],
                "relation_count": r["relation_count"],
            })

    def lines_for_alias_dist(dist):
        buckets = [
            ("0", dist.get(0, 0)),
            ("1", dist.get(1, 0)),
            ("2-5", sum(dist.get(i, 0) for i in range(2, 6))),
            ("6+", sum(v for k, v in dist.items() if k >= 6)),
        ]
        return buckets

    summary = []
    summary.append("# Tag Audit Summary")
    summary.append("")
    summary.append(f"- Registry: `{reg}`")
    summary.append(f"- Total tags: **{len(rows)}**")
    summary.append(f"- Tags with any definition: **{def_any}**")
    summary.append(f"- Tags with any aliases: **{alias_any}**")
    summary.append("")
    summary.append("## Priority breakdown")
    for k in ("P0", "P1", "P2"):
        summary.append(f"- {k}: **{priority_counts.get(k, 0)}**")
    summary.append("")
    summary.append("## Alias count distribution")
    for label, count in lines_for_alias_dist(alias_count_dist):
        summary.append(f"- {label}: **{count}**")
    summary.append("")
    summary.append("## Top 50 hub tags by relation_count")
    for r in top_hubs:
        summary.append(f"- `{r['tag_id']}`: {r['relation_count']}")

    summary_path = out_dir / "tag_audit_summary.md"
    summary_path.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print(f"TOTAL {len(rows)}")
    print(f"HAS_ANY_DEFINITION {def_any}")
    print(f"HAS_ANY_ALIASES {alias_any}")
    print("TOP_HUBS")
    for r in hubs[:20]:
        print(r["tag_id"])

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: tag_audit.py <registry.json> <out_dir>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
