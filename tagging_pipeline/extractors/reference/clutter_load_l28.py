"""L28 Clutter Load — composite-family Sprint-4 reference extractor.

Construct: Cognitive load imposed by visual clutter — object density,
disorder, occlusion (Sweller 1988 cognitive load theory; McMains & Kastner
2011 visual cortex clutter; Rosenholtz et al. 2007 measuring visual clutter).
Subdomain: cognitive_load.

Algorithm:

    Inputs: segments with object instances and per-class labels.

    1. object_instance_count: total distinct objects in segments.
    2. class_entropy_variance: variance across the per-class distribution
       (heterogeneity of object kinds; Rosenholtz feature-congestion proxy).
    3. cognitive_load = 0.5 * normalized_count + 0.5 * normalized_entropy
       Count normalised by 60 objects (saturates a typical "very cluttered"
       cluttered desk; McMains & Kastner suggest cortical interference
       saturates around N≈50-80).
       Entropy normalised by log2(N_classes_max) (uniform = max entropy).
    4. Likert bin to [0..4].

Citations:
    Sweller, J. (1988). Cognitive load during problem solving: Effects on
        learning. Cognitive Science, 12(2), 257-285.
    McMains, S., & Kastner, S. (2011). Interactions of top-down and
        bottom-up mechanisms in human visual cortex. Journal of
        Neuroscience, 31(2), 587-597.
    Rosenholtz, R., Li, Y., & Nakano, L. (2007). Measuring visual clutter.
        Journal of Vision, 7(2):17, 1-22.
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


COUNT_SATURATION = 60.0


class ClutterLoadExtractor(LatentExtractor):
    attribute_id = "L28"
    canonical_name = "cognitive.clutter_load"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "appearance.object_density",
        "appearance.edge_density",
        "geometry.occlusion_overlap_count",
        "appearance.feature_congestion",
        "appearance.color_variance_local",
    ]

    W_COUNT = 0.5
    W_ENTROPY = 0.5

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> ExtractorResult:
        if segments is None and image is None:
            return ExtractorResult(
                value=2, confidence=0.0,
                evidence=["L28 clutter-load: no segments/image; default 2."],
            )

        evidence: list[str] = []

        # ── Signal 1: total object count
        count_signal = 0.0
        total_count = 0
        try:
            class_counts: Counter = Counter()
            if segments:
                for cls, mask in segments.items():
                    instances = getattr(mask, "instance_count", None)
                    n = int(instances) if instances is not None else 1
                    class_counts[cls] += n
                    total_count += n
            count_signal = min(1.0, total_count / COUNT_SATURATION)
            evidence.append(
                f"total_object_count={total_count} across {len(class_counts)} classes "
                f"-> count_signal={count_signal:.3f} (saturated at {COUNT_SATURATION:.0f})"
            )
        except Exception as e:
            evidence.append(f"count fallback ({e}); 0")
            class_counts = Counter()

        # ── Signal 2: class entropy (heterogeneity)
        entropy_signal = 0.0
        try:
            if class_counts and total_count > 0:
                probs = [c / total_count for c in class_counts.values()]
                ent = -sum(p * math.log2(p) for p in probs if p > 0)
                # Maximum possible entropy = log2(N_classes)
                max_ent = math.log2(max(len(class_counts), 2))
                entropy_signal = ent / max_ent if max_ent > 0 else 0.0
                evidence.append(
                    f"class_entropy={ent:.3f}/{max_ent:.3f} "
                    f"-> entropy_signal={entropy_signal:.3f}"
                )
            else:
                evidence.append("no classes; entropy=0")
        except Exception as e:
            evidence.append(f"entropy fallback ({e}); 0")

        score = self.W_COUNT * count_signal + self.W_ENTROPY * entropy_signal
        if score >= 0.80: value = 4
        elif score >= 0.60: value = 3
        elif score >= 0.40: value = 2
        elif score >= 0.20: value = 1
        else: value = 0

        evidence.append(
            f"cognitive_load = {self.W_COUNT}*count({count_signal:.3f}) "
            f"+ {self.W_ENTROPY}*entropy({entropy_signal:.3f}) "
            f"= {score:.3f} -> Likert {value}"
        )
        evidence.append(
            "Sweller 1988 cognitive-load theory; McMains & Kastner 2011 V4 clutter; "
            "Rosenholtz et al. 2007 feature congestion."
        )

        signals_present = sum([
            1 if count_signal > 0 else 0,
            1 if entropy_signal > 0 else 0,
        ])
        confidence = 0.3 + 0.3 * signals_present
        return ExtractorResult(value=value, confidence=confidence, evidence=evidence)
