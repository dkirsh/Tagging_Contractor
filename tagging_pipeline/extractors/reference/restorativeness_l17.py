"""L17 Restorativeness (ART) — vlm-family reference extractor.

Construct: integrated Attention Restoration Theory restorativeness (Kaplan &
Kaplan, 1989; Hartig et al., 1997 PRS). Sprint 3 contest #1 disposition:
L17 is now a structured-factor parent over L18 (being-away), L19 (soft
fascination), L20 (compatibility), and L17_extent.

The Sprint 3 reference implementation aggregates over the four child
extractors when available, falling back to a direct VLM PRS-style probe
when child results are not provided.

Aggregation when children are present:
    L17.value = round(weighted_mean(L18, L19, L20, L17_extent))
    weights from Hartig et al. (1997) factor loadings:
        being_away: 0.25, soft_fascination: 0.30,
        compatibility: 0.20, extent: 0.25

Direct VLM probe (fallback): use a single Hartig PRS aggregate item.

The implementation honours the Sprint 3 structured-factor commitment: it
defers to children when they have been computed, only invokes the VLM
when child results are absent.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


PRS_ITEMS = [
    "Spending time here gives me a break from my day-to-day routine.",
    "There is much to explore and discover here.",
    "There is a sense of coherence in this place.",
    "I would have a chance to do things I like here.",
]

CHILD_WEIGHTS = {
    "L18": 0.25,  # being_away
    "L19": 0.30,  # soft_fascination
    "L20": 0.20,  # compatibility
    "L17_extent": 0.25,
}


class RestorativenessExtractor(LatentExtractor):
    attribute_id = "L17"
    canonical_name = "cognitive.restorativeness"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "scene.calm_visual_field_indicator",
        "lighting.daylight_present",
        "scene.greenery_presence",
        "scene.retreat_nook_present",
    ]

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
        child_results: Optional[dict] = None,
    ) -> ExtractorResult:
        # Path 1: child results present (preferred per Sprint 3 contest #1)
        if child_results:
            weighted_sum = 0.0
            weight_total = 0.0
            evidence_parts = []
            for cid, w in CHILD_WEIGHTS.items():
                if cid in child_results:
                    cv = child_results[cid].get("value", None)
                    if cv is not None:
                        weighted_sum += cv * w
                        weight_total += w
                        evidence_parts.append(f"  {cid}: value={cv} weight={w}")
            if weight_total > 0:
                weighted = weighted_sum / weight_total
                value = round(max(0, min(4, weighted)))
                confidence = 0.85
                evidence = ["L17 structured-factor aggregation (Sprint 3 contest #1):"]
                evidence.extend(evidence_parts)
                evidence.append(f"  weighted_mean={weighted:.3f} -> Likert {value}")
                evidence.append("Hartig et al. 1997 PRS factor loadings")
                return ExtractorResult(value=value, confidence=confidence, evidence=evidence)

        # Path 2: VLM PRS direct probe
        if vlm_client is None or image is None:
            return ExtractorResult(
                value=2, confidence=0.0,
                evidence=["L17 requires either child_results (preferred) or "
                         "(image + vlm_client) for direct PRS probe"]
            )
        scores = []
        evidence = []
        for prompt in PRS_ITEMS:
            try:
                s = vlm_client.score(image, prompt)
                scores.append(s)
                evidence.append(f"  PRS '{prompt[:60]}...' -> {s:.2f}")
            except Exception as e:
                scores.append(0.5)
                evidence.append(f"  PRS item failed: {e}")
        agg = sum(scores) / len(scores) if scores else 0.5
        # Map to 0..4
        value = round(agg * 4)
        confidence = min(0.7, agg)
        evidence.insert(0, f"L17 direct PRS probe (no children): aggregate={agg:.3f}")
        evidence.append("Kaplan & Kaplan 1989; Hartig et al. 1997")
        return ExtractorResult(value=value, confidence=confidence, evidence=evidence)
