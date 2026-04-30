"""L03 Visibility Control — vlm family algorithmic skeleton.

Construct: Visibility Control — ability to monitor environment without being monitored.
Method family: vlm
Subdomain: safety_threat
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Estimate observer's visible isovist area (depth + image frustum back-projection).
    Step 2: Identify partial-occluder count (planters, screens, half-walls) via segmentation.
    Step 3: VLM probe: 'I can see who is around me without being seen'.
    Step 4: Composite = 0.4*isovist_area_norm + 0.3*occluder_density + 0.3*VLM.
    Step 5: Bin to 0-4 (Appleton prospect-refuge balance).

Citations:
    Appleton, J. (1975). The experience of landscape. Wiley.
    Hildebrand, G. (1999). Origins of architectural pleasure. University of California Press.
    Stamps, A. E. (2005). Visual permeability, locomotive permeability, safety, and enclosure. Environment and Behavior, 37(5), 587–619. https://doi.org/10.1177/0013916505276741

Sprint 5 implementation notes:
    - Isovist computation requires depth; Sprint 5 should use ZoeDepth or DPT for monocular depth.
    - Occluder count needs panoptic segmentation (e.g. Mask2Former).
    - Validate against Appleton prospect-refuge expert ratings.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class VisibilityControlExtractor(LatentExtractor):
    attribute_id = "L03"
    canonical_name = "cognitive.visibility_control"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['affordance.vantage_point', 'scene.sightline_extent', 'affordance.partition_height', 'affordance.mirror_presence', 'scene.openness_index']

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
            f"Sprint 5: vlm family detector for L03 "
            f"(cognitive.visibility_control) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
