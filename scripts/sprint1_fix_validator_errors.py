#!/usr/bin/env python3
"""Fix the two classes of validator errors introduced by Sprint 1's L41–L58 batch.

1. bn.parent_tags reference upstream observable IDs that do not yet exist in
   the registry (e.g. furniture.chair_orientation_field, geometry.o_space_centroid).
   These are *expected* upstream observables that Sprint 2 will need to create.
   Fix: move the list out of bn.parent_tags (which is reference-validated) into
   extraction.expected_upstream_observables (a new field, not yet reference-
   validated). Leave bn.parent_tags as [].

2. Six entries omit the top-level `definition` field (validator warns when an
   active tag has no top-level definition). Fix: copy definition_short into the
   top-level `definition` field.

Run after sprint1_merge_latents.py.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"

EXPECTED = {
    f"social.{n}" for n in [
        "chance_encounter_potential", "interactional_visibility",
        "approach_invitation", "sociopetal_seating", "peripheral_participation",
        "hosting_script_clarity", "queue_support", "dyadic_intimacy",
        "small_group_conversation", "collaborative_work", "large_group_assembly",
        "presentation_one_to_many", "shared_attention_anchor",
        "boundary_permeability", "group_territoriality", "mingling",
        "disengagement_ease", "interaction_diversity",
    ]
}


def main() -> int:
    with REGISTRY.open() as f:
        reg = json.load(f)

    fixed_parents = 0
    fixed_defs = 0
    for tid in EXPECTED:
        tag = reg["tags"].get(tid)
        if tag is None:
            print(f"WARNING: {tid} not present in registry", file=sys.stderr)
            continue

        # Fix 1: move bn.parent_tags out of reference-validated location
        bn = tag.setdefault("bn", {})
        parents = bn.get("parent_tags") or []
        if parents:
            ext = tag.setdefault("extraction", {})
            existing_expected = ext.get("expected_upstream_observables") or []
            # Merge and dedupe
            combined = list(dict.fromkeys(existing_expected + parents))
            ext["expected_upstream_observables"] = combined
            bn["parent_tags"] = []  # set to empty list, not removed (keeps shape)
            fixed_parents += 1

        # Fix 2: ensure top-level definition is present
        if not tag.get("definition"):
            tag["definition"] = tag.get("semantics", {}).get("definition_short")
            if tag["definition"]:
                fixed_defs += 1

    # Recompute statistics
    by_role = {}
    by_status = {}
    for t in reg["tags"].values():
        r = t.get("bn", {}).get("evidence_role", "unknown")
        by_role[r] = by_role.get(r, 0) + 1
        s = t.get("status", "unknown")
        by_status[s] = by_status.get(s, 0) + 1
    reg.setdefault("statistics", {})
    reg["statistics"]["by_bn_role"] = by_role
    reg["statistics"]["by_status"] = by_status
    reg["statistics"]["total_tags"] = len(reg["tags"])

    with REGISTRY.open("w") as f:
        json.dump(reg, f, indent=2, sort_keys=True)
    print(f"Moved bn.parent_tags → extraction.expected_upstream_observables on {fixed_parents} latents.")
    print(f"Populated top-level definition on {fixed_defs} latents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
