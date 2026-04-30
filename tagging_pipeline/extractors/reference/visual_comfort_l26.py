"""L26 Visual Comfort — vlm family algorithmic skeleton.

Construct: Low-glare, low-strain optical environment with comfortable contrast and brightness.
Method family: vlm
Subdomain: aesthetic_affect
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Compute glare/contrast issues from luminance histogram (top-1% vs median).
    Step 2: Compute Unified Glare Rating (UGR) proxy from light-source detection + luminance.
    Step 3: VLM probe: 'The lighting in this scene is comfortable to look at' (visual-comfort items).
    Step 4: Composite = 0.4*(1 - glare_index) + 0.3*(1 - UGR_norm) + 0.3*VLM.
    Step 5: Bin to 0-4 Likert.

Citations:
    Boyce, P. R. (2014). Human factors in lighting (3rd ed.). CRC Press. https://doi.org/10.1201/b16707
    CIE. (1995). CIE 117-1995: Discomfort glare in interior lighting. International Commission on Illumination.
    Wienold, J., & Christoffersen, J. (2006). Evaluation methods and development of a new glare prediction model for daylight environments with the use of CCD cameras. Energy and Buildings, 38(7), 743-757. https://doi.org/10.1016/j.enbuild.2006.03.017
    CIE Publication 117-1995. Discomfort Glare in Interior Lighting.

Sprint 5 implementation notes:
    - Convert image to log-luminance; compute glare index per Boyce 2014.
    - UGR proxy: detect bright light sources via thresholding + position weighting.
    - Validate against CIE 117 lab-rated glare scenes.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class VisualComfortExtractor(LatentExtractor):
    attribute_id = "L26"
    canonical_name = "cognitive.visual_comfort"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['appearance.specular_highlight_extent', 'appearance.luminance_ratio_max_min', 'appearance.glare_source_present', 'appearance.contrast_distribution', 'appearance.daylight_window_treatment']

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
            f"Sprint 5: vlm family detector for L26 "
            f"(cognitive.visual_comfort) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
