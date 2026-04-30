"""L20 Compatibility — vlm family algorithmic skeleton.

Construct: Fit between space affordances and intended activity.
Method family: vlm
Subdomain: restoration
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Infer the user's likely activity goal (work, rest, social) from contextual prompt.
    Step 2: Detect setting affordances (chairs, desks, beds, queues).
    Step 3: VLM probe: 'This place is suitable for what I want to do' (PRS Compatibility).
    Step 4: Composite = 0.3*affordance_match + 0.7*VLM (compatibility is goal-relative).
    Step 5: Bin to 0-4 Likert.

Citations:
    Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
    Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. Journal of Environmental Psychology, 15(3), 169-182. https://doi.org/10.1016/0272-4944(95)90001-2
    Hartig, T., Korpela, K., Evans, G. W., & Garling, T. (1997). A measure of restorative quality in environments. Scandinavian Housing and Planning Research, 14(4), 175-194. https://doi.org/10.1080/02815739708730435

Sprint 5 implementation notes:
    - Activity-goal inference may require a separate user-context input; default to 'general visit'.
    - VLM probe is dominant since compatibility is goal-relative.
    - Validate against Hartig PRS-26 Compatibility subscale.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class CompatibilityExtractor(LatentExtractor):
    attribute_id = "L20"
    canonical_name = "cognitive.compatibility"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['furniture.task_relevant_equipment_present', 'ergonomics.posture_support_index', 'geometry.layout_task_alignment', 'scene.intended_activity_inferred', 'scene.task_obstruction_absent']

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
            f"Sprint 5: vlm family detector for L20 "
            f"(cognitive.compatibility) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
