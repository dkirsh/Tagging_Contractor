"""L38 Novelty — vlm-family Sprint-4 reference extractor.

Construct: Unexpectedness and distinctiveness — the encountered-information
dual of familiarity (Berlyne 1971 collative variables; Silvia 2005 interest
appraisal; Berlyne 1960 conflict-arousal). Subdomain: familiarity_novelty.

Algorithm (corpus-distance proxy via VLM):

    VLM is prompted with 5 distinctiveness/atypicality items contrasting
    the depicted scene against a corpus baseline:
      1. category-typicality (low value -> high novelty)
      2. unusual-fixture presence
      3. material-combination novelty
      4. layout schema-violation
      5. color/style distance from canonical exemplar

    novelty_score = mean of (1 - typicality) for typicality items and the
    direct distance score for atypicality items (see prompt list).
    Bin to Likert [0..4].

Citations:
    Berlyne, D. E. (1971). Aesthetics and psychobiology. Appleton-Century.
    Silvia, P. J. (2005). What is interesting? Exploring the appraisal
        structure of interest. Emotion, 5(1), 89-102.
    Berlyne, D. E. (1960). Conflict, arousal, and curiosity. McGraw-Hill.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


# Each prompt is annotated with a polarity sign:
#   +1 means "high VLM score -> high novelty" (atypicality items)
#   -1 means "high VLM score -> low novelty"  (typicality items, inverted)
NOVELTY_PROMPTS = [
    ("This scene is a typical, prototypical example of its category.", -1),
    ("There are unusual or unexpected fixtures or objects in this scene.", +1),
    ("The combination of materials is novel — unexpected pairings.", +1),
    ("The spatial layout violates the canonical schema for this kind of place.", +1),
    ("The colour and style depart noticeably from canonical exemplars in this category.", +1),
]


class NoveltyExtractor(LatentExtractor):
    attribute_id = "L38"
    canonical_name = "cognitive.novelty"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "objects.unusual_fixture_class_presence",
        "material.novel_combination_score",
        "layout.graph_distance_from_centroid",
        "style.corpus_distance_score",
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
                evidence=["L38 novelty: image unavailable; default 2."],
            )
        if vlm_client is None:
            return ExtractorResult(
                value=2, confidence=0.0,
                evidence=["L38 novelty: VLM client unavailable; default 2 "
                          "(Sprint-4 contract — VLM injected at runtime)."],
            )

        contributions: list[float] = []
        evidence: list[str] = []
        for prompt, polarity in NOVELTY_PROMPTS:
            try:
                s = float(vlm_client.score(image, prompt))
                contribution = s if polarity == +1 else (1.0 - s)
                contributions.append(contribution)
                evidence.append(
                    f"  '{prompt[:55]}...' -> raw={s:.2f}, "
                    f"contribution={contribution:.2f} (polarity {polarity:+d})"
                )
            except Exception as e:
                contributions.append(0.5)
                evidence.append(f"  '{prompt[:55]}...' -> 0.50 (VLM error: {e})")

        novelty_score = sum(contributions) / len(contributions) if contributions else 0.5
        if novelty_score >= 0.80: value = 4
        elif novelty_score >= 0.60: value = 3
        elif novelty_score >= 0.40: value = 2
        elif novelty_score >= 0.20: value = 1
        else: value = 0

        # Confidence: extremity of mean (decisive) and number of items
        confidence = min(0.9, 0.4 + abs(novelty_score - 0.5) * 1.5)

        evidence.insert(
            0,
            f"L38 novelty corpus-distance proxy: mean_contribution={novelty_score:.3f} "
            f"-> Likert {value}"
        )
        evidence.append(
            "Berlyne 1971 collative variables; Silvia 2005 interest appraisal."
        )
        return ExtractorResult(value=value, confidence=confidence, evidence=evidence)
