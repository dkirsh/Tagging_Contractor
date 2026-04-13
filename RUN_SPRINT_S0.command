#!/usr/bin/env bash
set -euo pipefail

# Run from the folder where this .command file lives (assumed repo root)
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "== RUN_SPRINT_S0 =="
echo "Repo: $ROOT"
echo

# Create folders (additive only)
mkdir -p tools enrichment _archive/sprints _archive/sprints/_ledger

# Write Sprint-0 tool (idempotent: overwrites the tool file, but never deletes outputs)
cat > tools/tag_audit_and_seed_enrichment.py <<'PY'
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

VISION_HINTS = [
    "material","texture","lighting","glare","shadow","window","vegetation","plant","people","crowd",
    "furniture","artwork","signage","pattern","symmetry","depth","prospect","refuge","clutter",
    "ceiling","floor","wall","glass","wood","stone","fabric"
]
NOT_2D_HINTS = [
    "acoustic","smell","scent","temperature","humidity","air quality","co2","reverb","thermal","odor","noise"
]

def bucket_for(tag_id: str, sem: dict):
    blob = (tag_id.lower() + " " + json.dumps(sem, ensure_ascii=False).lower())
    if any(h in blob for h in NOT_2D_HINTS):
        return "NOT_2D"
    if any(h in blob for h in VISION_HINTS):
        return "VISION_HEAVY"
    return "RULE_OR_DERIVED"

def main():
    core_ver, reg_path = find_latest_core_registry()
    d = json.loads(reg_path.read_text(encoding="utf-8"))
    tags = d.get("tags", {})
    if not isinstance(tags, dict):
        raise SystemExit("NO-GO: registry JSON missing 'tags' dict")

    stamp = nowstamp()
    out_dir = Path("_archive/sprints") / f"S0_audit_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load or init enrichment file
    enrich_path = Path("enrichment") / "tag_specs_v0.1.json"
    if enrich_path.exists():
        enrich = json.loads(enrich_path.read_text(encoding="utf-8"))
        if not isinstance(enrich, dict) or "tags" not in enrich:
            enrich = {"schema_version": "tag_specs_v0.1", "generated_from": {}, "tags": {}}
    else:
        enrich = {"schema_version": "tag_specs_v0.1", "generated_from": {}, "tags": {}}

    enrich["generated_from"] = {"core_version": core_ver, "registry_path": str(reg_path)}

    key_usage = Counter()
    bucket_counts = Counter()

    # Seed enrichment entries for every tag_id (never touches registry)
    for tid, tag in tags.items():
        if not isinstance(tag, dict):
            continue

        for k in tag.keys():
            key_usage[k] += 1

        sem = tag.get("semantics") if isinstance(tag.get("semantics"), dict) else {}
        b = bucket_for(tid, sem)
        bucket_counts[b] += 1

        if tid not in enrich["tags"]:
            enrich["tags"][tid] = {
                "semantics_snapshot": {
                    "aliases": sem.get("aliases", []),
                    "definition": sem.get("definition", sem.get("notes", "")),
                },
                "compute": {
                    "modality": "UNASSIGNED",   # later: vision_2d | derived | not_computable | vision_3d | text_only
                    "bucket_hint": b,
                    "signals": [],
                    "extractors": [],
                    "dependencies": [],
                    "qc": [],
                    "cost_hint": "UNSET"
                },
                "evidence": {
                    "refs": [],
                    "rationale": ""
                },
                "status": {
                    "needs_semantics": False,
                    "needs_compute": True,
                    "needs_evidence": True
                }
            }

    enrich_path.write_text(json.dumps(enrich, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # CSV backlog
    csv_path = out_dir / f"tag_audit_{core_ver}.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("tag_id,bucket_hint,enrichment_modality,signals_count,extractors_count,refs_count\n")
        for tid, spec in sorted(enrich["tags"].items()):
            c = spec.get("compute", {})
            e = spec.get("evidence", {})
            f.write(f"{tid},{c.get('bucket_hint','')},{c.get('modality','')},{len(c.get('signals',[]))},{len(c.get('extractors',[]))},{len(e.get('refs',[]))}\n")

    # Human report
    report_lines = []
    report_lines.append(f"# Sprint S0 Audit ({stamp})")
    report_lines.append("")
    report_lines.append(f"- Registry: `{reg_path}`")
    report_lines.append(f"- Core version: `{core_ver}`")
    report_lines.append(f"- Tag count: **{len(tags)}**")
    report_lines.append("")
    report_lines.append("## Heuristic buckets (starting point)")
    for k in ["VISION_HEAVY","RULE_OR_DERIVED","NOT_2D"]:
        report_lines.append(f"- {k}: **{bucket_counts.get(k,0)}**")
    report_lines.append("")
    report_lines.append("## Top-level keys present in registry (top 25)")
    for k, c in key_usage.most_common(25):
        report_lines.append(f"- `{k}`: {c}")
    report_lines.append("")
    report_lines.append("## Outputs")
    report_lines.append(f"- CSV backlog: `{csv_path}`")
    report_lines.append(f"- Enrichment file (seeded): `{enrich_path}`")

    (out_dir / "report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    # Append to sprint ledger
    ledger = Path("_archive/sprints/_ledger/SPRINT_LEDGER.md")
    if not ledger.exists():
        ledger.write_text("# Sprint Ledger\n\n", encoding="utf-8")
    with ledger.open("a", encoding="utf-8") as f:
        f.write(f"## S0 Audit {stamp}\n")
        f.write(f"- Registry: `{reg_path}`\n")
        f.write(f"- Core: `{core_ver}`\n")
        f.write(f"- Tags: {len(tags)}\n")
        f.write(f"- Buckets: {dict(bucket_counts)}\n")
        f.write(f"- Outputs: `{out_dir}`\n\n")

    print("OK: S0 audit complete")
    print(f"Report: {out_dir/'report.md'}")
    print(f"CSV:    {csv_path}")
    print(f"Enrich: {enrich_path}")
    print(f"Ledger: {ledger}")

    # Also print the first chunk of the report for convenience
    print("\n---- REPORT (first 80 lines) ----")
    txt = (out_dir / "report.md").read_text(encoding="utf-8")
    for i, line in enumerate(txt.splitlines(), start=1):
        if i > 80:
            break
        print(line)

if __name__ == "__main__":
    main()
PY

echo "Running S0 audit..."
python3 tools/tag_audit_and_seed_enrichment.py

echo
echo "DONE."
echo "Outputs live under: _archive/sprints/S0_audit_<timestamp>/"
echo "Ledger: _archive/sprints/_ledger/SPRINT_LEDGER.md"
echo "Enrichment: enrichment/tag_specs_v0.1.json"
echo
echo "You can close this Terminal window."
