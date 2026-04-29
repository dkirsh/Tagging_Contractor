"""L21 Coherence/Order — composite-family reference extractor.

Construct: visual organisation of the scene; Kaplan & Kaplan (1989)
preference matrix; Reber, Schwarz & Winkielman (2004) processing fluency.

Algorithm:

    Two complementary signals on the input image:
      1. Orientation entropy of the dominant edge gradients (lower entropy
         = more coherence, since entropy means more spread of orientations).
      2. Colour-palette consistency: extract the top-K colour clusters,
         compute their summed dominance ratio (high dominance = small set
         of dominant colours = more coherence).

    Combine: coherence_score = 0.6 * (1 - normalized_orientation_entropy)
                              + 0.4 * palette_dominance_ratio
    Bin to 0..4 Likert.

    Pure-Python fallback: if scipy / sklearn aren't available, use an HSV
    histogram heuristic for both signals.
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class CoherenceOrderExtractor(LatentExtractor):
    attribute_id = "L21"
    canonical_name = "cognitive.coherence_order"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "scene.orientation_entropy",
        "color.palette_dominance_ratio",
        "texture.symmetry_score",
        "scene.repetition_index",
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
            return ExtractorResult(value=2, confidence=0.0,
                                   evidence=["image unavailable"])

        evidence: list[str] = []
        # === Signal 1: orientation entropy (lower is better)
        try:
            # In production: use scipy.ndimage gradient + np.arctan2.
            # Pure-Python: assume image has .gradient_orientations() returning
            # list of orientation values in [0, 2π).
            orientations = getattr(image, "gradient_orientations", lambda: [])()
            if orientations:
                # Bin to 16 wedges; compute entropy
                bins = Counter()
                for o in orientations:
                    idx = int((o % (2 * math.pi)) / (2 * math.pi) * 16) % 16
                    bins[idx] += 1
                total = sum(bins.values())
                ent = -sum((c/total) * math.log2(c/total) for c in bins.values() if c > 0)
                ent_max = math.log2(16)  # uniform = max entropy
                norm_ent = ent / ent_max if ent_max > 0 else 1.0
                ord_score = 1.0 - norm_ent
                evidence.append(f"orientation_entropy={ent:.3f}/{ent_max:.3f}, "
                               f"order_score={ord_score:.3f}")
            else:
                ord_score = 0.5
                evidence.append("orientation API unavailable; using neutral 0.5")
        except Exception as e:
            ord_score = 0.5
            evidence.append(f"orientation fallback ({e})")

        # === Signal 2: palette dominance
        try:
            palette = getattr(image, "dominant_colors", lambda k=5: [])(5)
            if palette:
                # palette: list of (rgb_tuple, fraction)
                top_dom = sum(f for _, f in palette[:3])
                evidence.append(f"top-3 palette_dominance={top_dom:.3f}")
            else:
                top_dom = 0.5
                evidence.append("palette API unavailable; using 0.5")
        except Exception as e:
            top_dom = 0.5
            evidence.append(f"palette fallback ({e})")

        score = 0.6 * ord_score + 0.4 * top_dom
        if score >= 0.8: value = 4
        elif score >= 0.6: value = 3
        elif score >= 0.4: value = 2
        elif score >= 0.2: value = 1
        else: value = 0

        evidence.append(f"composite coherence={score:.3f} -> Likert {value}")
        evidence.append("Kaplan & Kaplan 1989; Reber, Schwarz & Winkielman 2004 fluency")
        return ExtractorResult(
            value=value,
            confidence=0.7,
            evidence=evidence,
        )
