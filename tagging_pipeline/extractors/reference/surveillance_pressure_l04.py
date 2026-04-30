"""L04 Surveillance Pressure — vlm family algorithmic skeleton.

Construct: Surveillance Pressure — feeling watched/judged.
Method family: vlm
Subdomain: safety_threat
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect cameras, mirrors, supervisor desks, one-way windows (object detector).
    Step 2: Compute eye-line density (face/figure detections oriented at observer).
    Step 3: VLM probe: 'I feel I am being watched here' (5 items).
    Step 4: Composite = 0.3*camera_density + 0.3*eyeline_density + 0.4*VLM.
    Step 5: Bin to 0-4 (Foucault panopticon gradient).

Citations:
    Foucault, M. (1977). Discipline and punish: The birth of the prison (A. Sheridan, Trans.). Pantheon Books.
    Zajonc, R. B. (1965). Social facilitation. Science, 149(3681), 269–274. https://doi.org/10.1126/science.149.3681.269
    Ulrich, R. S. (1991). Effects of interior design on wellness: Theory and recent scientific research. Journal of Health Care Interior Design, 3, 97–109.
    Foucault, M. (1977). Discipline and punish. Pantheon.
    Hatuka, T., & Toch, E. (2017). Being visible in public space. Urban Studies, 54(4), 984-998.

Sprint 5 implementation notes:
    - Use OpenMMDetection 'security_camera' class or fine-tune YOLOv8 on CCTV imagery.
    - Face detection via RetinaFace; orientation via 6DRepNet head-pose.
    - Cross-validate against Hatuka-Toch surveillance scale.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class SurveillancePressureExtractor(LatentExtractor):
    attribute_id = "L04"
    canonical_name = "cognitive.surveillance_pressure"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['object.camera_presence', 'scene.openplan_exposure', 'lighting.spotlight_pattern', 'scene.gaze_lines', 'scene.elevated_platform_focus']

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
            f"Sprint 5: vlm family detector for L04 "
            f"(cognitive.surveillance_pressure) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
