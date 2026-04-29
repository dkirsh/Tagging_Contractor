#!/usr/bin/env python3
"""Sprint 3 — add bn.ranking_function flag to the 7 binary latent_score candidates.

Per the Sprint 3 disposition deferred from Sprint 1 (Spohn) and Sprint 2 panel:
binary latents may be re-encoded under a ranking-theoretic representation
(Spohn, 2012, §5.3) where κ: {0,1} → ℕ records the disbelief in negation rather
than a probability. This is parametrically more parsimonious than a 5-state
Likert CPT and composes cleanly under the chain rule for conditional ranks.

Sprint 3 does not switch the *value_type* — that would require a registry-engine
change. It adds a structured `bn.ranking_function` block that downstream
inference engines can consult; the Likert encoding is retained as the fallback
representation.

Affected latents (7 binary candidates):
  Sprint 1: cognitive.hosting_script_clarity (L46),
            cognitive.presentation_one_to_many (L52),
            cognitive.shared_attention_anchor (L53)  — wait, these are social.* not cognitive.*
  Re-checking Sprint 1: social.hosting_script_clarity, social.presentation_one_to_many,
                       social.shared_attention_anchor
  Sprint 2: cognitive.contamination_risk (L05),
            cognitive.care_signal (L33),
            cognitive.welcome (L34),
            cognitive.familiarity (L37)
"""
from __future__ import annotations
import json, sys
from pathlib import Path

REPO = Path(__file__).parent.parent
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"

BINARY_CANDIDATES = [
    "social.hosting_script_clarity",        # L46 (Sprint 1)
    "social.presentation_one_to_many",      # L52 (Sprint 1)
    "social.shared_attention_anchor",       # L53 (Sprint 1)
    "cognitive.contamination_risk",          # L05 (Sprint 2)
    "cognitive.care_signal",                 # L33 (Sprint 2)
    "cognitive.welcome",                     # L34 (Sprint 2)
    "cognitive.familiarity",                 # L37 (Sprint 2)
]

RANKING_NOTE = (
    "Sprint 3 ranking-theoretic flag: this latent is a binary candidate for "
    "ranking-function encoding (Spohn, 2012, §5.3). The downstream BN engine "
    "may consult bn.ranking_function as an alternative to the binary CPT. "
    "Fallback: Likert encoding via the existing latent_score value_type."
)


def main() -> int:
    with REGISTRY.open() as f: reg = json.load(f)
    tags = reg["tags"]

    flagged = 0
    missing = []
    for tid in BINARY_CANDIDATES:
        if tid not in tags:
            missing.append(tid)
            continue
        t = tags[tid]
        t.setdefault("bn", {})
        # Add structured ranking_function block; default kappa values are placeholders
        # (Sprint 4 will populate real values from estimated CPTs)
        t["bn"]["ranking_function"] = {
            "form": "two_state",
            "states": [0, 1],
            "kappa_default": {"0": 0, "1": 0},  # placeholder; real κ values set in Sprint 4
            "fallback_value_type": t.get("value_type", "latent_score"),
            "note": ("Two-state ranking function κ: {0,1} → ℕ where κ(¬state) records "
                    "disbelief in the alternative state. Initialized to (0, 0) — "
                    "Sprint 4 will populate from estimated CPTs.")
        }
        notes = t.setdefault("notes", {})
        existing = notes.get("bn_notes") or ""
        if "Sprint 3 ranking-theoretic flag" not in existing:
            notes["bn_notes"] = (existing + (" | " if existing else "") + RANKING_NOTE).strip()
        flagged += 1

    if missing:
        print(f"WARNING: {len(missing)} binary candidates missing from registry: {missing}", file=sys.stderr)

    with REGISTRY.open("w") as f: json.dump(reg, f, indent=2, sort_keys=True)
    print(f"Ranking-theoretic flag added to {flagged} binary candidates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
