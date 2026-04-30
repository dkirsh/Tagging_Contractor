"""L22 Mystery — vlm family algorithmic skeleton.

Construct: Promise of further information beyond the visible vantage — invitation to explore.
Method family: vlm
Subdomain: aesthetic_affect
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect occluded/curving paths and obscured regions (sightline depth + blockage).
    Step 2: Compute information-gain heuristic: edges leading out of frame, partial-glimpse fraction.
    Step 3: VLM probe: 'I would learn more by walking further into this scene' (Kaplan items).
    Step 4: Composite = 0.5*(path_curvature + partial_glimpse) + 0.5*VLM.
    Step 5: Bin to 0-4 Likert.

Citations:
    Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
    Berlyne, D. E. (1971). Aesthetics and psychobiology. Appleton-Century-Crofts.
    Kaplan, S. (1987). Aesthetics, affect, and cognition: Environmental preference from an evolutionary perspective. Environment and Behavior, 19(1), 3-32. https://doi.org/10.1177/0013916587191001
    Stamps, A. E. (2004). Mystery, complexity, legibility, and coherence: A meta-analysis. Journal of Environmental Psychology, 24(1), 1-16.
    Herzog, T. R., & Bryce, A. G. (2007). Mystery and preference in within-forest settings. Environment and Behavior, 39(6), 779-796.

Sprint 5 implementation notes:
    - Path-curvature from skeletonization of segmentation 'path' class.
    - Use VLM with the Kaplan-Stamps 4 mystery items.
    - Validate against Stamps 2004 meta-analytic mystery ratings.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class MysteryExtractor(LatentExtractor):
    attribute_id = "L22"
    canonical_name = "cognitive.mystery"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['geometry.partial_occlusion_score', 'affordance.curving_path_present', 'affordance.deflected_sightline_count', 'appearance.luminance_gradient_into_depth', 'geometry.foreground_partial_screen']

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> ExtractorResult:
        # Sprint 5: implement per algorithm sketch in module docstring.
        raise NotImplementedError(
            f"Sprint 5: vlm family detector for L22 "
            f"(cognitive.mystery) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
