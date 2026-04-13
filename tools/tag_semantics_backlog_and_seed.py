import json, re, datetime
from pathlib import Path
from collections import Counter

def nowstamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def find_latest_core_registry():
    core_root = Path("core/trs-core")
    if not core_root.exists():
        raise SystemExit("NO-GO: missing core/trs-core (run from repo root?)")

    vers = []
    for p in core_root.iterdir():
        if p.is_dir() and re.match(r"^v\d+\.\d+\.\d+$", p.name):
            vers.append(p.name)

    if not vers:
        raise SystemExit("NO-GO: no core/trs-core/vX.Y.Z found")

    def key(v): return tuple(map(int, v[1:].split(".")))
    vers.sort(key=key)
    core_ver = vers[-1]

    reg = core_root / core_ver / "registry" / f"registry_{core_ver}.json"
    if not reg.exists():
        raise SystemExit(f"NO-GO: missing {reg}")
    return core_ver, reg

def _as_str(x):
    if x is None:
        return ""
    if isinstance(x, str):
        return x.strip()
    return str(x).strip()

def _as_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return [str(a).strip() for a in x if str(a).strip()]
    if isinstance(x, str):
        s = x.strip()
        return [s] if s else []
    return [str(x).strip()]

def _get_semantics(tag_obj: dict) -> dict:
    sem = tag_obj.get("semantics")
    return sem if isinstance(sem, dict) else {}

def _pick_definition(sem: dict) -> str:
    # tolerate schema variance
    for k in ("definition", "def", "notes", "description", "meaning"):
        if k in sem and _as_str(sem.get(k)):
            return _as_str(sem.get(k))
    return ""

def _pick_aliases(sem: dict) -> list:
    for k in ("aliases", "alias", "synonyms", "aka"):
        v = sem.get(k)
        if v is not None:
            return _as_list(v)
    return []

def semantics_priority(def_len: int, alias_ct: int) -> str:
    # Simple triage:
    # P0: no definition
    # P1: definition tiny OR no aliases
    # P2: otherwise
    if def_len == 0:
        return "P0"
    if def_len < 40 or alias_ct == 0:
        return "P1"
    return "P2"

def main():
    core_ver, reg_path = find_latest_core_registry()
    d = json.loads(reg_path.read_text(encoding="utf-8"))
    tags = d.get("tags", {})
    if not isinstance(tags, dict):
        raise SystemExit("NO-GO: registry JSON missing 'tags' dict")

    stamp = nowstamp()
    out_dir = Path("_archive/sprints") / f"S1_semantics_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load enrichment (seed if missing)
    enrich_path = Path("enrichment") / "tag_specs_v0.1.json"
    if enrich_path.exists():
        enrich = json.loads(enrich_path.read_text(encoding="utf-8"))
        if not isinstance(enrich, dict) or "tags" not in enrich:
            enrich = {"schema_version": "tag_specs_v0.1", "generated_from": {}, "tags": {}}
    else:
        enrich = {"schema_version": "tag_specs_v0.1", "generated_from": {}, "tags": {}}

    # provenance
    enrich["generated_from"] = {"core_version": core_ver, "registry_path": str(reg_path)}

    # Ensure every tag has an enrichment entry (in case S1 is run before S0)
    seeded = 0
    for tid in tags.keys():
        if tid not in enrich["tags"]:
            enrich["tags"][tid] = {
                "semantics_snapshot": {"aliases": [], "definition": ""},
                "compute": {
                    "modality": "UNASSIGNED",
                    "bucket_hint": "UNSET",
                    "signals": [],
                    "extractors": [],
                    "dependencies": [],
                    "qc": [],
                    "cost_hint": "UNSET"
                },
                "evidence": {"refs": [], "rationale": ""},
                "status": {"needs_semantics": True, "needs_compute": True, "needs_evidence": True}
            }
            seeded += 1

    # Add a richer semantics work area (purely in enrichment)
    for tid, spec in enrich["tags"].items():
        if "semantics_enriched" not in spec:
            spec["semantics_enriched"] = {
                "definition": "",
                "aliases": [],
                "scope_includes": [],
                "scope_excludes": [],
                "examples_positive": [],
                "examples_negative": [],
                "disambiguation": "",
                "notes": ""
            }

    # Audit + compute backlog rows
    counts = Counter()
    priority_counts = Counter()
    key_usage_sem = Counter()

    rows = []
    for tid, tag_obj in tags.items():
        tag_obj = tag_obj if isinstance(tag_obj, dict) else {}
        sem = _get_semantics(tag_obj)

        # track keys seen in semantics for schema reconnaissance
        for k in sem.keys():
            key_usage_sem[k] += 1

        core_def = _pick_definition(sem)
        core_aliases = _pick_aliases(sem)

        core_def_len = len(core_def.strip())
        core_alias_ct = len(core_aliases)

        pr = semantics_priority(core_def_len, core_alias_ct)
        priority_counts[pr] += 1

        # update snapshot in enrichment (non-destructive: overwrite snapshot with current core view)
        spec = enrich["tags"].get(tid, {})
        spec.setdefault("semantics_snapshot", {})
        spec["semantics_snapshot"]["definition"] = core_def
        spec["semantics_snapshot"]["aliases"] = core_aliases

        # needs_semantics: based on core snapshot (not enriched), since the point is to know where core is thin
        needs_sem = (core_def_len == 0) or (core_def_len < 40) or (core_alias_ct == 0)
        spec.setdefault("status", {})
        spec["status"]["needs_semantics"] = bool(needs_sem)

        # count buckets by current compute hint (if present)
        bucket_hint = (spec.get("compute", {}) or {}).get("bucket_hint", "UNSET")
        counts[f"bucket:{bucket_hint}"] += 1

        rows.append({
            "tag_id": tid,
            "priority": pr,
            "core_definition_len": core_def_len,
            "core_alias_count": core_alias_ct,
            "needs_semantics": "YES" if needs_sem else "NO",
            "bucket_hint": bucket_hint,
            "enriched_definition_len": len(_as_str(spec.get("semantics_enriched", {}).get("definition"))),
            "enriched_alias_count": len(_as_list(spec.get("semantics_enriched", {}).get("aliases"))),
        })

    # write enrichment (additive structure + refreshed snapshot + needs_semantics flag)
    enrich_path.write_text(json.dumps(enrich, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # backlog CSV
    csv_path = out_dir / f"semantics_backlog_{core_ver}.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("tag_id,priority,needs_semantics,core_definition_len,core_alias_count,bucket_hint,enriched_definition_len,enriched_alias_count\n")
        for r in sorted(rows, key=lambda x: (x["priority"], x["core_definition_len"], x["core_alias_count"], x["tag_id"])):
            f.write(f'{r["tag_id"]},{r["priority"]},{r["needs_semantics"]},{r["core_definition_len"]},{r["core_alias_count"]},{r["bucket_hint"]},{r["enriched_definition_len"]},{r["enriched_alias_count"]}\n')

    # report.md
    need_ct = sum(1 for r in rows if r["needs_semantics"] == "YES")
    total = len(rows)

    report = []
    report.append(f"# Sprint S1 Semantics Audit ({stamp})")
    report.append("")
    report.append(f"- Registry: `{reg_path}`")
    report.append(f"- Core version: `{core_ver}`")
    report.append(f"- Tags audited: **{total}**")
    report.append(f"- Tags needing semantics work (definition too short/missing or aliases missing): **{need_ct}**")
    report.append(f"- Enrichment updated: `{enrich_path}`")
    report.append(f"- Backlog CSV: `{csv_path}`")
    report.append("")
    report.append("## Priority breakdown")
    for k in ["P0","P1","P2"]:
        report.append(f"- {k}: **{priority_counts.get(k,0)}**")
    report.append("")
    report.append("## Semantics schema reconnaissance (top 25 keys under tag.semantics)")
    for k, c in key_usage_sem.most_common(25):
        report.append(f"- `{k}`: {c}")
    report.append("")
    report.append("## Notes on interpretation")
    report.append("- P0 = no definition in core semantics (highest priority).")
    report.append("- P1 = definition exists but is short (<40 chars) OR aliases list empty.")
    report.append("- P2 = definition present and non-trivial AND aliases present.")
    report.append("- This sprint does NOT change the core registry; it only refreshes a snapshot and seeds a richer semantics workspace in enrichment.")
    (out_dir / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    # ledger append
    ledger = Path("_archive/sprints/_ledger/SPRINT_LEDGER.md")
    if not ledger.exists():
        ledger.write_text("# Sprint Ledger\n\n", encoding="utf-8")
    with ledger.open("a", encoding="utf-8") as f:
        f.write(f"## S1 Semantics {stamp}\n")
        f.write(f"- Registry: `{reg_path}`\n")
        f.write(f"- Core: `{core_ver}`\n")
        f.write(f"- Tags: {total}\n")
        f.write(f"- Needs semantics: {need_ct}\n")
        f.write(f"- Priority: {dict(priority_counts)}\n")
        f.write(f"- Outputs: `{out_dir}`\n\n")

    print("OK: S1 semantics audit complete")
    print(f"Report:  {out_dir/'report.md'}")
    print(f"CSV:     {csv_path}")
    print(f"Enrich:  {enrich_path}")
    print(f"Ledger:  {ledger}")
    print(f"Seeded enrichment entries (if any were missing): {seeded}")

    print("\n---- REPORT (first 80 lines) ----")
    txt = (out_dir / "report.md").read_text(encoding="utf-8")
    for i, line in enumerate(txt.splitlines(), start=1):
        if i > 80:
            break
        print(line)

if __name__ == "__main__":
    main()
