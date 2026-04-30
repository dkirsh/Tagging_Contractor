#!/usr/bin/env python3
"""Sprint 4 Contest 3 — apply notes.social_layer to all 18 social.* latents.

Per the disposition at docs/sprint4_contest3_top_level_domain_resolution.md
(Goffman/Bourdieu vs Spohn/Kahneman), the registry KEEPS domain="social" and
ADDS a new notes.social_layer field with enum {interaction_order,
social_organization, both}.

This script applies the per-latent assignment ratified by the panel.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

REPO = Path(__file__).parent.parent
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"

SOCIAL_LAYER = {
    "social.chance_encounter_potential":  "both",
    "social.interactional_visibility":    "interaction_order",
    "social.approach_invitation":          "interaction_order",
    "social.sociopetal_seating":           "interaction_order",
    "social.peripheral_participation":     "interaction_order",
    "social.hosting_script_clarity":       "social_organization",
    "social.queue_support":                "social_organization",
    "social.dyadic_intimacy":              "interaction_order",
    "social.small_group_conversation":     "interaction_order",
    "social.collaborative_work":           "both",
    "social.large_group_assembly":         "both",
    "social.presentation_one_to_many":     "social_organization",
    "social.shared_attention_anchor":      "interaction_order",
    "social.boundary_permeability":        "both",
    "social.group_territoriality":         "social_organization",
    "social.mingling":                     "interaction_order",
    "social.disengagement_ease":           "interaction_order",
    "social.interaction_diversity":        "both",
}

NOTE = ("Sprint 4 contest #3 disposition: hybrid (Goffman/Bourdieu vs "
        "Spohn/Kahneman). Registry keeps domain='social'; per-latent "
        "social_layer captures the analytical distinction between "
        "interaction-order (Goffman 1959/1963) and social-organisation "
        "(Goffman 1974, Bourdieu 1984) constructs. Sprint 5 extends to L01-L40.")


def main() -> int:
    with REGISTRY.open() as f: reg = json.load(f)
    tags = reg["tags"]
    applied = missing = 0
    for tid, layer in SOCIAL_LAYER.items():
        if tid not in tags:
            print(f"WARNING: {tid} not in registry", file=sys.stderr); missing += 1; continue
        notes = tags[tid].setdefault("notes", {})
        notes["social_layer"] = layer
        existing = notes.get("bn_notes") or ""
        if "Sprint 4 contest #3" not in existing:
            notes["bn_notes"] = (existing + (" | " if existing else "") + NOTE).strip()
        applied += 1
    with REGISTRY.open("w") as f: json.dump(reg, f, indent=2, sort_keys=True)
    print(f"Applied notes.social_layer to {applied} social.* latents ({missing} missing).")
    # Tally
    from collections import Counter
    print(f"Distribution: {dict(Counter(SOCIAL_LAYER.values()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
