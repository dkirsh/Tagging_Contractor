"""L33 Care Signal — vlm-family Sprint-4 reference extractor.

Construct: Binary inference that the place is actively maintained and
someone is in charge of it (Wilson & Kelling 1982 broken-windows;
Sampson & Raudenbush 1999 collective efficacy & physical disorder).
Subdomain: social_signal. Value type: latent_score (binary).

Algorithm (inverse-disorder logic):

    VLM probes 5 visible-disorder cues:
      1. broken windows / missing fixtures
      2. visible graffiti or unauthorised marks
      3. ground-level dirt, litter, dust
      4. peeling paint / surface degradation
      5. abandoned objects / unmaintained debris

    Each item returns a probability in [0, 1] that the cue is *present*
    (i.e., that disorder is visible). Care signal is the inverse:
      care_signal = 1 if (n_strong_disorder_cues == 0) else 0
    A single strong disorder cue suffices to fail care; this matches the
    Wilson-Kelling escalation logic where a single broken window licenses
    further degradation.

Citations:
    Wilson, J. Q., & Kelling, G. L. (1982). Broken windows: The police and
        neighborhood safety. Atlantic Monthly, 249(3), 29-38.
    Sampson, R. J., & Raudenbush, S. W. (1999). Systematic social
        observation of public spaces: A new look at disorder in urban
        neighborhoods. AJS, 105(3), 603-651.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


DISORDER_PROMPTS = [
    "There are broken windows or missing/damaged fixtures visible.",
    "There is visible graffiti or unauthorised markings.",
    "There is ground-level dirt, litter, dust, or grime.",
    "There is peeling paint or visible surface degradation.",
    "There are abandoned or unmaintained objects/debris in the scene.",
]


class CareSignalExtractor(LatentExtractor):
    attribute_id = "L33"
    canonical_name = "cognitive.care_signal"
    method_family = "vlm"
    value_states = [0, 1]
    expected_upstream_observables = [
        "disorder.litter_pixels",
        "disorder.graffiti_presence",
        "disorder.broken_fixture_count",
        "disorder.dust_or_grime_score",
        "order.stored_items_alignment_score",
        "material.fixture_intactness_score",
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
                value=0, confidence=0.0,
                evidence=["L33 care-signal: image unavailable; default 0."],
            )
        if vlm_client is None:
            return ExtractorResult(
                value=0, confidence=0.0,
                evidence=["L33 care-signal: VLM client unavailable; default 0 "
                          "(Sprint-4 contract — VLM injected at runtime)."],
            )

        disorder_scores: list[float] = []
        evidence: list[str] = []
        for prompt in DISORDER_PROMPTS:
            try:
                s = float(vlm_client.score(image, prompt))
                disorder_scores.append(s)
                evidence.append(f"  disorder '{prompt[:50]}...' -> {s:.2f}")
            except Exception as e:
                disorder_scores.append(0.5)
                evidence.append(f"  disorder '{prompt[:50]}...' -> 0.50 (VLM error: {e})")

        n_strong = sum(1 for s in disorder_scores if s > 0.5)
        value = 1 if n_strong == 0 else 0
        # Confidence: higher when scores are extreme (decisive), lower when scores cluster around 0.5
        mean_dist = sum(abs(s - 0.5) for s in disorder_scores) / len(disorder_scores) if disorder_scores else 0.0
        confidence = min(0.95, 0.3 + 1.4 * mean_dist)

        evidence.insert(
            0,
            f"L33 care-signal (inverse-disorder): {n_strong}/5 disorder cues strong; "
            f"value={value} (1=cared-for, 0=neglected)"
        )
        evidence.append(
            "Wilson & Kelling 1982 broken-windows; Sampson & Raudenbush 1999 "
            "collective efficacy & physical disorder."
        )
        return ExtractorResult(value=value, confidence=confidence, evidence=evidence)
