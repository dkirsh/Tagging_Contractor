#!/usr/bin/env python3
"""TRS Sprint 4 — Populate ranking-function κ values from synthetic CPTs.

For the 7 binary `latent_score` candidates:

    L05 — cognitive.contamination_risk
    L33 — cognitive.care_signal
    L34 — cognitive.welcome
    L37 — cognitive.familiarity
    L46 — social.hosting_script_clarity
    L52 — social.presentation_one_to_many
    L53 — social.shared_attention_anchor

Compute κ_0 and κ_1 from the synthetic CPT marginals via the standard
ranking-function instantiation (Spohn 2012, §5.3):

    κ_state = floor(-log_2(P(L = state)))

This converts a probability-mass function into a Spohn ranking function
where κ assigns natural-number disbelief values to each state. Lower κ
indicates higher belief (zero κ = the most plausible state). The
floor/log2 form chosen here is one of several admissible Spohn-conjugate
forms; it is well-defined whenever P > 0 (we clamp very small probs to
2^{-32} as a safety to avoid infinite κ).

The script updates each tag's `bn.ranking_function.kappa_default` accordingly,
adds an inline note in `bn_notes` documenting that the κ values are derived
from synthetic CPTs and will be re-derived from real CPTs in Sprint 5+.

Usage:
    python3 scripts/sprint4_populate_kappa.py            # dry-run preview
    python3 scripts/sprint4_populate_kappa.py --apply    # write registry

Exit codes: 0 success, 1 failure, 2 missing input.
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"
SYNTHETIC_CPTS = REPO / "data/sprint4_synthetic_cpts.json"

# The 7 binary latent_score candidates per Sprint-4 spec
BINARY_LATENTS = [
    "cognitive.contamination_risk",   # L05
    "cognitive.care_signal",          # L33
    "cognitive.welcome",              # L34
    "cognitive.familiarity",          # L37
    "social.hosting_script_clarity",  # L46
    "social.presentation_one_to_many",  # L52
    "social.shared_attention_anchor", # L53
]

KAPPA_NOTE_SPRINT4 = (
    "κ values populated by scripts/sprint4_populate_kappa.py from "
    "data/sprint4_synthetic_cpts.json (Spohn 2012 §5.3 instantiation: "
    "κ_state = floor(-log_2 P(state))). Synthetic CPT-derived; will be "
    "re-derived from empirical CPTs in Sprint 5+ once tagged data exists."
)
PROB_FLOOR = 2 ** -32


def kappa_from_prob(p: float) -> int:
    """Spohn 2012 §5.3 instantiation: κ = floor(-log_2(p))."""
    p = max(p, PROB_FLOOR)
    return int(math.floor(-math.log2(p)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Write changes back to the registry. Without "
                         "this flag, the script prints a dry-run preview.")
    ap.add_argument("--registry", type=Path, default=REGISTRY,
                    help="Registry path (default: v0.2.8 latest).")
    args = ap.parse_args()

    if not args.registry.exists():
        print(f"NO-GO: registry not found at {args.registry}", file=sys.stderr)
        return 2
    if not SYNTHETIC_CPTS.exists():
        print(f"NO-GO: synthetic CPTs not found at {SYNTHETIC_CPTS}; "
              f"run scripts/sprint4_synthetic_cpts.py first.", file=sys.stderr)
        return 2

    with args.registry.open() as f:
        reg = json.load(f)
    with SYNTHETIC_CPTS.open() as f:
        cpt_doc = json.load(f)
    cpts = cpt_doc.get("cpts", {})

    tags = reg.get("tags", {})
    updates: list[dict] = []
    missing: list[str] = []

    for cname in BINARY_LATENTS:
        tag = tags.get(cname)
        if tag is None:
            missing.append(cname)
            continue
        cpt = cpts.get(cname)
        if cpt is None:
            missing.append(f"{cname} (no CPT)")
            continue
        marginal = cpt.get("marginal")
        if marginal is None:
            # Conditional CPT — collapse to marginal under uniform parent prior
            cond = cpt.get("conditional", {})
            table = cond.get("table", {})
            states = cpt.get("states", ["0", "1"])
            sums = {s: 0.0 for s in states}
            n = len(table) or 1
            for joint, child_cpt in table.items():
                for s, p in child_cpt.items():
                    sums[s] = sums.get(s, 0.0) + p / n
            marginal = sums

        p0 = float(marginal.get("0", 0.5))
        p1 = float(marginal.get("1", 0.5))
        # Renormalise to handle floating drift
        total = p0 + p1
        if total <= 0:
            p0, p1 = 0.5, 0.5
        else:
            p0, p1 = p0 / total, p1 / total

        k0 = kappa_from_prob(p0)
        k1 = kappa_from_prob(p1)
        updates.append({
            "canonical_name": cname,
            "attribute_id": tag.get("attribute_id"),
            "marginal": {"0": p0, "1": p1},
            "kappa": {"0": k0, "1": k1},
        })

        if args.apply:
            bn = tag.setdefault("bn", {})
            rf = bn.setdefault("ranking_function", {})
            rf["fallback_value_type"] = rf.get("fallback_value_type", "latent_score")
            rf["form"] = rf.get("form", "two_state")
            rf["states"] = rf.get("states", [0, 1])
            rf["kappa_default"] = {"0": k0, "1": k1}
            rf["note"] = KAPPA_NOTE_SPRINT4
            # Append an inline bn_notes note documenting source
            notes = tag.setdefault("notes", {})
            existing = notes.get("bn_notes", "") or ""
            sprint4_marker = "[Sprint 4 κ-populate]"
            if sprint4_marker not in existing:
                notes["bn_notes"] = (
                    (existing + " " if existing else "")
                    + f"{sprint4_marker} {KAPPA_NOTE_SPRINT4}"
                )

    print(f"Sprint-4 ranking-function κ population — {len(updates)} of "
          f"{len(BINARY_LATENTS)} binary latents processed:")
    print()
    for u in updates:
        print(f"  {u['attribute_id']} {u['canonical_name']}:")
        print(f"     marginal: P(0)={u['marginal']['0']:.4f}, "
              f"P(1)={u['marginal']['1']:.4f}")
        print(f"     kappa:    κ(0)={u['kappa']['0']}, κ(1)={u['kappa']['1']}")

    if missing:
        print()
        print(f"WARNING: {len(missing)} binary latent(s) not processed:")
        for m in missing:
            print(f"  - {m}")

    if args.apply:
        # Write back atomically
        backup = args.registry.with_suffix(
            f".pre_sprint4_kappa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with backup.open("w") as f:
            json.dump(reg, f, indent=2, sort_keys=False)
        with args.registry.open("w") as f:
            json.dump(reg, f, indent=2, sort_keys=False)
        print()
        print(f"Wrote registry updates to {args.registry}")
        print(f"Backup at {backup}")
    else:
        print()
        print("Dry-run only. Pass --apply to persist changes.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
