#!/usr/bin/env python3
"""Fix Sprint 2 validator errors:
1. Move bn.parent_tags -> extraction.expected_upstream_observables (forward refs).
2. Remove alias collisions with existing tags.
3. Validate inverse_of strings against the tag set; null out invalid ones.
4. Ensure top-level definition is set.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

REPO = Path(__file__).parent.parent
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"
COGNITIVE_KEYS = {
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
    with REGISTRY.open() as f: reg = json.load(f)
    tags = reg["tags"]

    # Build sets
    all_tag_ids = set(tags.keys())
    # Build alias-owner map (excluding cognitive.* entries which we'll fix)
    alias_owners: dict[str, str] = {}
    for tid, t in tags.items():
        if tid in COGNITIVE_KEYS: continue
        sem = t.get("semantics") or {}
        for a in sem.get("aliases") or []:
            alias_owners.setdefault(str(a).lower().strip(), tid)

    fixed_parents = 0
    fixed_aliases = 0
    fixed_inverses = 0
    fixed_defs = 0
    for tid in COGNITIVE_KEYS:
        tag = tags.get(tid)
        if tag is None: continue

        # 1. Move bn.parent_tags -> extraction.expected_upstream_observables
        bn = tag.setdefault("bn", {})
        parents = bn.get("parent_tags") or []
        if parents:
            ext = tag.setdefault("extraction", {})
            existing = ext.get("expected_upstream_observables") or []
            ext["expected_upstream_observables"] = list(dict.fromkeys(existing + parents))
            bn["parent_tags"] = []
            fixed_parents += 1

        # 2. Remove alias collisions
        sem = tag.setdefault("semantics", {})
        aliases = sem.get("aliases") or []
        cleaned = []
        for a in aliases:
            key = str(a).lower().strip()
            owner = alias_owners.get(key)
            if owner and owner != tid:
                fixed_aliases += 1
                continue  # drop colliding alias
            cleaned.append(a)
        # Also dedupe within this tag
        seen = set(); deduped = []
        for a in cleaned:
            k = str(a).lower().strip()
            if k in seen: continue
            seen.add(k); deduped.append(a)
        sem["aliases"] = deduped
        # Mirror to top-level aliases (Sprint 1 convention)
        tag["aliases"] = deduped

        # 3. Validate inverse_of
        inv = sem.get("inverse_of")
        if inv and inv not in all_tag_ids:
            sem["inverse_of"] = None
            fixed_inverses += 1
        # Also some entries may have a top-level `inverse_of` field
        if "inverse_of" in tag and tag.get("inverse_of") and tag["inverse_of"] not in all_tag_ids:
            tag["inverse_of"] = None

        # 4. Ensure top-level definition
        if not tag.get("definition"):
            tag["definition"] = sem.get("definition_short")
            if tag["definition"]: fixed_defs += 1

    # Recompute stats
    by_role = {}; by_status = {}
    for t in tags.values():
        r = (t.get("bn") or {}).get("evidence_role","unknown"); by_role[r] = by_role.get(r,0)+1
        s = t.get("status","unknown"); by_status[s] = by_status.get(s,0)+1
    reg.setdefault("statistics", {})
    reg["statistics"]["by_bn_role"] = by_role
    reg["statistics"]["by_status"] = by_status
    reg["statistics"]["total_tags"] = len(tags)

    with REGISTRY.open("w") as f: json.dump(reg, f, indent=2, sort_keys=True)
    print(f"Moved bn.parent_tags -> expected_upstream_observables on {fixed_parents} latents.")
    print(f"Removed {fixed_aliases} colliding aliases.")
    print(f"Nulled {fixed_inverses} invalid inverse_of references.")
    print(f"Populated top-level definition on {fixed_defs} latents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
