"""L18 Being Away — vlm family algorithmic skeleton.

Construct: Psychological distance from demands.
Method family: vlm
Subdomain: restoration
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Classify scene as 'natural / quiet / non-routine' vs. 'urban / familiar' (Places365 head).
    Step 2: Detect work-related artefacts (computers, files, signage) -> being-away inverse.
    Step 3: VLM probe with Hartig PRS Being-Away items (6 items).
    Step 4: Composite = 0.3*place_class + 0.3*(1 - work_artefact_density) + 0.4*VLM.
    Step 5: Bin to 0-4 Likert.

Citations:
    Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
    Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. Journal of Environmental Psychology, 15(3), 169-182. https://doi.org/10.1016/0272-4944(95)90001-2
    Hartig, T., Korpela, K., Evans, G. W., & Garling, T. (1997). A measure of restorative quality in environments. Scandinavian Housing and Planning Research, 14(4), 175-194. https://doi.org/10.1080/02815739708730435
    Hartig, T., Mang, M., & Evans, G. W. (1991). Restorative effects of natural environment experiences. Environment and Behavior, 23(1), 3-26.

Sprint 5 implementation notes:
    - Reuse the L17 RestorativenessExtractor scaffolding with PRS subscale weighting.
    - Use Places365-CNN scene category for the natural/urban dichotomy.
    - Validate against Hartig PRS-26 Being-Away subscale on benchmark images.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class BeingAwayExtractor(LatentExtractor):
    attribute_id = "L18"
    canonical_name = "cognitive.being_away"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['scene.threshold_present', 'geometry.separation_from_workspace', 'scene.natural_view_present', 'scene.demand_artefact_absent']

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
            f"Sprint 5: vlm family detector for L18 "
            f"(cognitive.being_away) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
