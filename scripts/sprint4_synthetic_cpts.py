#!/usr/bin/env python3
"""TRS Sprint 4 — Synthetic CPT generator.

═══════════════════════════════════════════════════════════════════════════
  SYNTHETIC — replace with empirical CPTs in Sprint 5+ once tagged data
  exists. The CPTs here are *literature-derived placeholders*; their only
  use is to bootstrap the Sprint 4 Jacobian-rank identifiability check
  and the κ ranking-function population. They must NOT be treated as
  empirical.
═══════════════════════════════════════════════════════════════════════════

For each `evidence_role: latent` tag in the registry, generate a plausible
CPT shaped P(L | parents):

  - For latents WITHOUT bn.parent_tags (most): generate a marginal P(L) with
    realistic distribution.
      * ordinal Likert [0..4]: discretised Gaussian centred on 2 with σ=1
      * binary (latent_score [0,1]): Beta(α=2, β=2) discretised at 0.5
      * categorical (e.g. F-formation arrangements): mild Dirichlet-ish bias
        toward `none` and the most common kinds.
  - For latents WITH bn.parent_tags: generate conditional structure with
    ~0.7 probability mass on parent-aligned states (parent low -> child low,
    parent high -> child high) for ordinal-vs-ordinal pairs; for binary
    children, parent at high -> P(child=1) ≈ 0.7.

Output: data/sprint4_synthetic_cpts.json mapping each canonical_name to a
CPT dict of the form:

    {
      "marginal": {"<state>": <prob>, ...},          # parent-free
      OR
      "conditional": {
        "parents": ["<canonical_name>", ...],
        "table": {"<parent_joint_state_str>": {"<state>": <prob>, ...}}
      }
    }

Usage:
    python3 scripts/sprint4_synthetic_cpts.py
    python3 scripts/sprint4_synthetic_cpts.py --json   # echo to stdout
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
OUT_DIR = REPO / "data"
OUT = OUT_DIR / "sprint4_synthetic_cpts.json"


def gaussian_likert_marginal(mean: float = 2.0, sigma: float = 1.0,
                             states: int = 5) -> dict[str, float]:
    """Discretise a Gaussian centred on `mean` over [0..states-1]."""
    raw = []
    for s in range(states):
        # Density at s
        z = (s - mean) / sigma
        raw.append(math.exp(-0.5 * z * z))
    total = sum(raw)
    return {str(s): raw[s] / total for s in range(states)}


def beta_binary_marginal(alpha: float = 2.0, beta: float = 2.0) -> dict[str, float]:
    """Marginal P over {0, 1} from Beta(α, β) mean = α/(α+β)."""
    p1 = alpha / (alpha + beta)
    return {"0": 1.0 - p1, "1": p1}


def categorical_marginal(states: list[str]) -> dict[str, float]:
    """Mild Dirichlet bias: `none` heavier (if present), rest evenly."""
    n = len(states)
    weights: list[float] = []
    for s in states:
        if s.lower() in ("none", "no", "absent"):
            weights.append(2.5)
        elif s.lower() in ("vis_a_vis", "side_by_side"):
            weights.append(1.5)
        else:
            weights.append(1.0)
    total = sum(weights)
    return {s: w / total for s, w in zip(states, weights)}


def get_value_states(tag: dict) -> list[str]:
    vt = tag.get("value_type", "ordinal")
    vr = tag.get("value_range") or [0, 4]
    if vt == "ordinal":
        if isinstance(vr, list) and len(vr) == 2:
            try:
                lo, hi = int(vr[0]), int(vr[1])
                return [str(s) for s in range(lo, hi + 1)]
            except Exception:
                pass
        return ["0", "1", "2", "3", "4"]
    if vt == "latent_score" or vt == "binary":
        return ["0", "1"]
    if vt == "categorical":
        if isinstance(vr, list) and vr and isinstance(vr[0], str):
            return list(vr)
        return ["0", "1", "2", "3", "4"]
    if vt == "continuous":
        # Discretise into 8 bins for the bound calc
        return [str(s) for s in range(8)]
    return ["0", "1", "2", "3", "4"]


def make_marginal(tag: dict) -> dict[str, float]:
    vt = tag.get("value_type", "ordinal")
    states = get_value_states(tag)
    if vt == "ordinal":
        return gaussian_likert_marginal(mean=(len(states) - 1) / 2.0,
                                        sigma=1.0, states=len(states))
    if vt == "latent_score" or vt == "binary":
        return beta_binary_marginal()
    if vt == "categorical":
        return categorical_marginal(states)
    if vt == "continuous":
        return gaussian_likert_marginal(mean=(len(states) - 1) / 2.0,
                                        sigma=2.0, states=len(states))
    return gaussian_likert_marginal()


def parent_joint_states(parent_states_lists: list[list[str]]) -> list[tuple[str, ...]]:
    """Cartesian product of parent state lists."""
    if not parent_states_lists:
        return [()]
    result: list[tuple[str, ...]] = [()]
    for ps in parent_states_lists:
        result = [r + (s,) for r in result for s in ps]
    return result


def make_conditional(tag: dict, parent_tags: list[dict]) -> dict:
    """Given a child tag and its parent tag dicts, build a conditional CPT.

    Heuristic for the synthetic generation:
      - Compute a parent_alignment_score = mean of (parent_state_index /
        (n_parent_states - 1)) across all parents (treats each parent as
        giving an "intensity" reading in [0, 1]).
      - For an ordinal child with K states, peak at index round(alignment * (K-1))
        with σ=1, then renormalise.
      - For a binary child, P(child=1) = 0.3 + 0.4 * alignment (so range
        [0.3, 0.7] giving the canonical ~0.7 high-mass when parents agree).
    """
    child_states = get_value_states(tag)
    child_vt = tag.get("value_type", "ordinal")
    parent_state_lists = [get_value_states(p) for p in parent_tags]
    parent_names = [p["canonical_name"] for p in parent_tags]
    table: dict[str, dict[str, float]] = {}
    for joint in parent_joint_states(parent_state_lists):
        # Compute alignment (intensity) from parent state indices
        alignments = []
        for parent_idx, state_str in enumerate(joint):
            states = parent_state_lists[parent_idx]
            try:
                idx = states.index(state_str)
                if len(states) > 1:
                    alignments.append(idx / (len(states) - 1))
                else:
                    alignments.append(0.5)
            except ValueError:
                alignments.append(0.5)
        alignment = sum(alignments) / len(alignments) if alignments else 0.5

        if child_vt == "ordinal":
            n = len(child_states)
            peak = alignment * (n - 1)
            raw = [math.exp(-0.5 * ((i - peak) / 1.0) ** 2) for i in range(n)]
            tot = sum(raw)
            cpt = {child_states[i]: raw[i] / tot for i in range(n)}
        elif child_vt in ("latent_score", "binary"):
            p1 = 0.3 + 0.4 * alignment
            cpt = {"0": 1.0 - p1, "1": p1}
        elif child_vt == "categorical":
            cpt = categorical_marginal(child_states)
        else:
            cpt = make_marginal(tag)

        # Joint key as comma-separated states
        key = ",".join(joint) if joint else "_"
        table[key] = cpt

    return {
        "parents": parent_names,
        "parent_states": parent_state_lists,
        "table": table,
    }


def build_cpts(reg: dict) -> dict:
    tags = reg["tags"]
    latents = {tid: t for tid, t in tags.items()
               if (t.get("bn") or {}).get("evidence_role") == "latent"
               and t.get("status") in ("active", "experimental")}

    cpts: dict[str, dict] = {}
    for cname, tag in latents.items():
        bn = tag.get("bn") or {}
        parent_names = bn.get("parent_tags") or []
        # Resolve parent tag dicts (only those that are also latents)
        parent_tags = [tags[pn] for pn in parent_names if pn in tags]

        if not parent_tags:
            cpts[cname] = {
                "value_type": tag.get("value_type"),
                "states": get_value_states(tag),
                "marginal": make_marginal(tag),
                "attribute_id": tag.get("attribute_id"),
            }
        else:
            cond = make_conditional(tag, parent_tags)
            cpts[cname] = {
                "value_type": tag.get("value_type"),
                "states": get_value_states(tag),
                "conditional": cond,
                "attribute_id": tag.get("attribute_id"),
            }
    return cpts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true",
                    help="Echo CPTs to stdout instead of writing to file")
    args = ap.parse_args()

    if not REGISTRY.exists():
        print(f"NO-GO: registry not found at {REGISTRY}", file=sys.stderr)
        return 2
    with REGISTRY.open() as f:
        reg = json.load(f)

    cpts = build_cpts(reg)
    out = {
        "_warning": (
            "SYNTHETIC — replace with empirical CPTs in Sprint 5+ once "
            "tagged data exists. The CPTs here are literature-derived "
            "placeholders for bootstrapping the Sprint-4 identifiability "
            "check and ranking-function κ population. They must NOT be "
            "used as empirical priors in production inference."
        ),
        "_generated": datetime.utcnow().isoformat() + "Z",
        "_generator": "scripts/sprint4_synthetic_cpts.py",
        "_registry": str(REGISTRY.relative_to(REPO)),
        "_count": len(cpts),
        "cpts": cpts,
    }

    if args.json:
        print(json.dumps(out, indent=2))
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {len(cpts)} synthetic CPTs to {OUT}")
    print("WARNING: SYNTHETIC. See _warning field. Replace in Sprint 5+.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
