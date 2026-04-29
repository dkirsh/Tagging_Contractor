#!/usr/bin/env python3
"""Sprint 2 — merge L01–L40 cognitive/affect/perception latent entries into
registry_v0.2.8.json.

Idempotent. Loads 4 batch JSON files (10 entries each), validates basic shape,
backs up the registry, merges, and recomputes statistics. Designed to mirror
scripts/sprint1_merge_latents.py.

Usage:
    python3 scripts/sprint2_merge_latents.py --dry-run
    python3 scripts/sprint2_merge_latents.py
"""
from __future__ import annotations
import argparse, json, shutil, sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).parent.parent
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"
BATCHES = [
    REPO / "data/sprint2_latents_batch1.json",
    REPO / "data/sprint2_latents_batch2.json",
    REPO / "data/sprint2_latents_batch3.json",
    REPO / "data/sprint2_latents_batch4.json",
]
EXPECTED_KEYS = {
    "cognitive.perceived_threat","cognitive.escape_efficacy","cognitive.visibility_control",
    "cognitive.surveillance_pressure","cognitive.contamination_risk","cognitive.perceived_control",
    "cognitive.choice_richness","cognitive.predictability","cognitive.rule_tightness",
    "cognitive.visual_privacy","cognitive.acoustic_privacy","cognitive.interruption_likelihood",
    "cognitive.territorial_support","cognitive.crowding_pressure","cognitive.social_exposure",
    "cognitive.resource_scarcity","cognitive.restorativeness","cognitive.being_away",
    "cognitive.soft_fascination","cognitive.compatibility","cognitive.coherence_order",
    "cognitive.mystery","cognitive.arousal_potential","cognitive.valence_potential",
    "cognitive.coziness","cognitive.visual_comfort","cognitive.perceptual_fluency",
    "cognitive.clutter_load","cognitive.legibility","cognitive.landmark_clarity",
    "cognitive.decision_point_load","cognitive.prestige_signal","cognitive.care_signal",
    "cognitive.welcome","cognitive.placeness","cognitive.awe","cognitive.familiarity",
    "cognitive.novelty","cognitive.formality","cognitive.playfulness",
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    merged: dict[str, dict] = {}
    for bp in BATCHES:
        if not bp.exists():
            print(f"ERROR: missing batch {bp}", file=sys.stderr); return 1
        with bp.open() as f: data = json.load(f)
        for k, v in data.items():
            if k in merged:
                print(f"ERROR: duplicate key {k}", file=sys.stderr); return 1
            merged[k] = v
    print(f"Loaded {len(merged)} entries from 4 batches.")
    missing = EXPECTED_KEYS - set(merged.keys())
    extra = set(merged.keys()) - EXPECTED_KEYS
    if missing: print(f"ERROR: missing: {sorted(missing)}", file=sys.stderr); return 1
    if extra: print(f"WARNING: unexpected keys: {sorted(extra)}", file=sys.stderr)

    # Pre-merge spot validation (mirror Sprint 1 script)
    valid_cat = {"environmental","cognitive","physiological","preference","derived"}
    valid_vt = {"binary","ordinal","continuous","categorical","multilabel","region_map","latent_score"}
    valid_ex = {"yes","partial","no", None}
    valid_er = {"stimulus_antecedent","latent","outcome","moderator","derived_metric","marker"}
    valid_ds = {"required","optional","exploratory","not_applicable"}
    errors: list[str] = []
    for tid, t in merged.items():
        for f in ("canonical_name","category","value_type","status","domain"):
            if not t.get(f): errors.append(f"{tid}: missing {f}")
        if t.get("category") not in valid_cat: errors.append(f"{tid}: bad category {t.get('category')}")
        if t.get("value_type") not in valid_vt: errors.append(f"{tid}: bad value_type {t.get('value_type')}")
        extr = t.get("extractability") or {}
        for f in ("from_2d","from_3d_vr","monocular_3d_approx"):
            if extr.get(f) not in valid_ex: errors.append(f"{tid}: bad extractability.{f}={extr.get(f)}")
        bn = t.get("bn") or {}
        if bn.get("evidence_role") not in valid_er: errors.append(f"{tid}: bad bn.evidence_role")
        if bn.get("demand_state") not in valid_ds: errors.append(f"{tid}: bad bn.demand_state")
    if errors:
        print(f"PRE-MERGE VALIDATION FAILED ({len(errors)}):", file=sys.stderr)
        for e in errors[:20]: print(f"  {e}", file=sys.stderr)
        return 1
    print("Pre-merge validation passed.")

    # Load registry, back up, merge
    with REGISTRY.open() as f: reg = json.load(f)
    pre_count = len(reg.get("tags", {}))
    print(f"Registry currently has {pre_count} tags.")

    if not args.dry_run:
        backup = REGISTRY.with_suffix(f".json.pre_sprint2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        shutil.copyfile(REGISTRY, backup)
        print(f"Backed up to {backup.name}")

    overwrites = [k for k in merged if k in reg["tags"]]
    for k, v in merged.items(): reg["tags"][k] = v
    new_count = len(reg["tags"])
    print(f"After merge: {new_count} tags ({new_count - pre_count} added, {len(overwrites)} overwritten).")

    # Recompute stats
    by_role = {}; by_status = {}
    for t in reg["tags"].values():
        r = (t.get("bn") or {}).get("evidence_role","unknown"); by_role[r] = by_role.get(r,0)+1
        s = t.get("status","unknown"); by_status[s] = by_status.get(s,0)+1
    reg.setdefault("statistics", {})
    reg["statistics"]["by_bn_role"] = by_role
    reg["statistics"]["by_status"] = by_status
    reg["statistics"]["total_tags"] = new_count
    reg["generated_at_utc"] = datetime.now(timezone.utc).isoformat()

    if args.dry_run:
        print("DRY RUN — registry not written.")
        return 0
    with REGISTRY.open("w") as f: json.dump(reg, f, indent=2, sort_keys=True)
    print(f"Registry written. by_bn_role={by_role}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
