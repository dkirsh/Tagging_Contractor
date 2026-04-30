"""L25 Coziness — vlm-family Sprint-4 reference extractor.

Construct: Inviting softness, warmth, and enclosure that supports lingering
(Kaplan & Kaplan 1989 preference matrix; Wiking 2017 hygge ethnography;
Linnet 2011 Danish hygge sociology). Subdomain: aesthetic_affect.

Algorithm:

    VLM probes 5 hygge-style indicator items (Wiking 2017, condensed for
    PRS-style elicitation). Aggregate: ≥3/5 strong (>0.5) -> high (Likert 4),
    2/5 -> moderate-high (3), 1/5 -> moderate (2), else low.

    Coziness is treated as a 5-point Likert (per registry value_range [0,4]).
    The vlm aggregation rule maps n_strong to a fine-grained Likert rather
    than a binary because the registry value_type is `ordinal`, not
    `latent_score` (cf. L46 which is binary).

Citations:
    Kaplan, R., & Kaplan, S. (1989). The experience of nature: A
        psychological perspective. Cambridge University Press.
    Wiking, M. (2017). The little book of hygge: The Danish way to live
        well. Penguin.
    Linnet, J. T. (2011). Money can't buy me hygge. Social Analysis,
        55(2), 21-44.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


HYGGE_PROMPTS = [
    "The lighting is warm and low — pools of warm light rather than bright overhead.",
    "There are soft textiles visible — throws, cushions, rugs, drapes.",
    "The space feels enclosed and intimate, not large or exposed.",
    "The scale of the seating area is intimate — close conversation distance.",
    "Materials are organic — wood, wool, ceramic, candle, plant — rather than steel and glass.",
]


class CozinessExtractor(LatentExtractor):
    attribute_id = "L25"
    canonical_name = "cognitive.coziness"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "appearance.textile_presence",
        "appearance.warm_lighting_index",
        "geometry.partial_enclosure_score",
        "appearance.soft_seating_present",
        "appearance.localised_warm_light_pools",
    ]

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> ExtractorResult:
        if image is None:
            return ExtractorResult(
                value=2, confidence=0.0,
                evidence=["L25 coziness: image unavailable; default 2."],
            )
        if vlm_client is None:
            return ExtractorResult(
                value=2,
                confidence=0.0,
                evidence=["L25 coziness: VLM client unavailable; default 2 "
                          "(Sprint-4 contract — VLM injected at runtime)."],
            )

        scores: list[float] = []
        evidence: list[str] = []
        for prompt in HYGGE_PROMPTS:
            try:
                s = float(vlm_client.score(image, prompt))
                scores.append(s)
                evidence.append(f"  '{prompt[:55]}...' -> {s:.2f}")
            except Exception as e:
                scores.append(0.5)
                evidence.append(f"  '{prompt[:55]}...' -> 0.50 (VLM error: {e})")

        n_strong = sum(1 for s in scores if s > 0.5)
        # Map n_strong (0..5) to Likert (0..4) with hygge gradient
        # 5 of 5 -> 4 (high coziness), 4 -> 4, 3 -> 3, 2 -> 2, 1 -> 1, 0 -> 0
        if n_strong >= 4: value = 4
        elif n_strong == 3: value = 3
        elif n_strong == 2: value = 2
        elif n_strong == 1: value = 1
        else: value = 0
        confidence = sum(scores) / len(scores) if scores else 0.0

        evidence.insert(
            0,
            f"L25 VLM hygge-aggregate: {n_strong}/5 indicators strong; value={value}"
        )
        evidence.append(
            "Kaplan & Kaplan 1989 preference matrix; Wiking 2017 hygge; Linnet 2011."
        )
        return ExtractorResult(value=value, confidence=confidence, evidence=evidence)
