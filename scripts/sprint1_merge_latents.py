#!/usr/bin/env python3
"""Sprint 1 — merge L41–L58 latent tag entries into registry_v0.2.8.json.

Idempotent: re-running on a registry that already contains the social.* tags
will overwrite their values cleanly without creating duplicates.

Usage:
    python3 scripts/sprint1_merge_latents.py
    python3 scripts/sprint1_merge_latents.py --dry-run

Exit codes:
    0 = merge successful (or dry-run produced no errors)
    1 = merge failed (file errors, JSON errors, or schema-shape errors)
"""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).parent.parent
REGISTRY = REPO_ROOT / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"
BATCHES = [
    REPO_ROOT / "data/sprint1_latents_batch1.json",
    REPO_ROOT / "data/sprint1_latents_batch2.json",
    REPO_ROOT / "data/sprint1_latents_batch3.json",
]
EXPECTED_KEYS = {
    f"social.{name}" for name in [
        "chance_encounter_potential", "interactional_visibility",
        "approach_invitation", "sociopetal_seating", "peripheral_participation",
        "hosting_script_clarity", "queue_support", "dyadic_intimacy",
        "small_group_conversation", "collaborative_work", "large_group_assembly",
        "presentation_one_to_many", "shared_attention_anchor",
        "boundary_permeability", "group_territoriality", "mingling",
        "disengagement_ease", "interaction_diversity",
    ]
}


def load_batches() -> dict[str, dict]:
    """Load and merge the three batch JSON files. Verify all 18 keys present."""
    merged: dict[str, dict] = {}
    for batch_path in BATCHES:
        if not batch_path.exists():
            print(f"ERROR: batch file missing: {batch_path}", file=sys.stderr)
            sys.exit(1)
        with batch_path.open() as f:
            data = json.load(f)
        for k, v in data.items():
            if k in merged:
                print(f"ERROR: duplicate key {k} across batch files", file=sys.stderr)
                sys.exit(1)
            merged[k] = v
    missing = EXPECTED_KEYS - set(merged.keys())
    extra = set(merged.keys()) - EXPECTED_KEYS
    if missing:
        print(f"ERROR: missing expected keys: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)
    if extra:
        print(f"WARNING: unexpected keys: {sorted(extra)}", file=sys.stderr)
    return merged


def validate_minimum_shape(tag_id: str, tag: dict, errors: list) -> None:
    """Spot-check the minimum schema shape before merging."""
    REQUIRED = ["canonical_name", "category", "value_type", "status", "domain"]
    for f in REQUIRED:
        if f not in tag or tag[f] is None:
            errors.append(f"{tag_id}: missing required field {f}")
    # category must be in registry enum
    valid_cat = {"environmental", "cognitive", "physiological", "preference", "derived"}
    if tag.get("category") not in valid_cat:
        errors.append(f"{tag_id}: invalid category {tag.get('category')!r}")
    # value_type must be in registry enum
    valid_vt = {"binary", "ordinal", "continuous", "categorical", "multilabel", "region_map", "latent_score"}
    if tag.get("value_type") not in valid_vt:
        errors.append(f"{tag_id}: invalid value_type {tag.get('value_type')!r}")
    # extractability must use enum values
    valid_ex = {"yes", "partial", "no", None}
    extr = tag.get("extractability", {})
    for f in ["from_2d", "from_3d_vr", "monocular_3d_approx"]:
        if extr.get(f) not in valid_ex:
            errors.append(f"{tag_id}: invalid extractability.{f} = {extr.get(f)!r}")
    # bn.evidence_role and bn.demand_state
    bn = tag.get("bn", {})
    valid_er = {"stimulus_antecedent", "latent", "outcome", "moderator", "derived_metric", "marker"}
    if bn.get("evidence_role") not in valid_er:
        errors.append(f"{tag_id}: invalid bn.evidence_role = {bn.get('evidence_role')!r}")
    valid_ds = {"required", "optional", "exploratory", "not_applicable"}
    if bn.get("demand_state") not in valid_ds:
        errors.append(f"{tag_id}: invalid bn.demand_state = {bn.get('demand_state')!r}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="Validate and merge in memory; do not write")
    args = p.parse_args()

    print(f"Loading three batch files...")
    batches = load_batches()
    print(f"Loaded {len(batches)} new tag entries.")

    # Pre-merge spot validation
    errors: list[str] = []
    for tag_id, tag in batches.items():
        validate_minimum_shape(tag_id, tag, errors)
    if errors:
        print(f"PRE-MERGE VALIDATION FAILED ({len(errors)} errors):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"Pre-merge validation passed.")

    # Load registry
    if not REGISTRY.exists():
        print(f"ERROR: registry not found: {REGISTRY}", file=sys.stderr)
        return 1
    with REGISTRY.open() as f:
        registry = json.load(f)
    pre_count = len(registry.get("tags", {}))
    print(f"Registry currently contains {pre_count} tags.")

    # Backup
    if not args.dry_run:
        backup = REGISTRY.with_suffix(f".json.pre_sprint1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        shutil.copyfile(REGISTRY, backup)
        print(f"Registry backed up to {backup.name}")

    # Merge
    overwrites = []
    for tag_id, tag in batches.items():
        if tag_id in registry["tags"]:
            overwrites.append(tag_id)
        registry["tags"][tag_id] = tag

    # Update statistics
    new_count = len(registry["tags"])
    print(f"After merge: {new_count} tags ({new_count - pre_count} added, {len(overwrites)} overwritten).")
    if overwrites:
        print(f"Overwrote: {overwrites}")

    # Recompute statistics block
    stats = registry.setdefault("statistics", {})
    by_role = {}
    by_status = {}
    for t in registry["tags"].values():
        r = t.get("bn", {}).get("evidence_role", "unknown")
        by_role[r] = by_role.get(r, 0) + 1
        s = t.get("status", "unknown")
        by_status[s] = by_status.get(s, 0) + 1
    stats["by_bn_role"] = by_role
    stats["by_status"] = by_status
    stats["total_tags"] = new_count

    # Update generated_at
    registry["generated_at_utc"] = datetime.now(timezone.utc).isoformat()

    if args.dry_run:
        print("DRY RUN — registry not written.")
        return 0

    # Write
    with REGISTRY.open("w") as f:
        json.dump(registry, f, indent=2, sort_keys=True)
    print(f"Registry written: {REGISTRY}")
    print(f"Statistics: by_bn_role={by_role}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
