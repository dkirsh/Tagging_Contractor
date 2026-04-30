"""L36 Awe — vlm family algorithmic skeleton.

Construct: Vastness and need for cognitive accommodation — the architectural cathedral effect.
Method family: vlm
Subdomain: social_signal
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Compute scale (apparent ceiling height; vertical extent in pixels normalised by depth).
    Step 2: Detect awe cues (vista, mountain, cathedral, vast sky, monumental architecture).
    Step 3: VLM probe: 'I feel a sense of awe / vastness here' (Keltner-Haidt awe items).
    Step 4: Composite = 0.4*vertical_scale + 0.3*vista_count + 0.3*VLM.
    Step 5: Bin to 0-4 Likert.

Citations:
    Vartanian, O., Navarrete, G., Chatterjee, A., Fich, L. B., Leder, H., Modrono, C., Nadal, M., Rostrup, N., & Skov, M. (2015). Architectural design and the brain: Effects of ceiling height and perceived enclosure on beauty judgments and approach-avoidance decisions. *Journal of Environmental Psychology*, *41*, 10-18. https://doi.org/10.1016/j.jenvp.2014.11.006
    Keltner, D., & Haidt, J. (2003). Approaching awe, a moral, spiritual, and aesthetic emotion. *Cognition and Emotion*, *17*(2), 297-314. https://doi.org/10.1080/02699930302297
    Bermudez, J., Krizaj, D., Lipschitz, D. L., Bueler, C. E., Rogowska, J., Yurgelun-Todd, D., & Nakamura, Y. (2017). Externally-induced meditative states: An exploratory fMRI study of architects' responses to contemplative architecture. *Frontiers of Architectural Research*, *6*(2), 123-136. https://doi.org/10.1016/j.foar.2017.02.002
    Shiota, M. N., Keltner, D., & Mossman, A. (2007). The nature of awe. Cognition and Emotion, 21(5), 944-963.

Sprint 5 implementation notes:
    - Ceiling height via depth-camera or DPT depth.
    - Vista classifier: Places365 'cathedral_indoor', 'mountain', 'sky' subset.
    - Validate against Shiota-Keltner awe-state ratings.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class AweExtractor(LatentExtractor):
    attribute_id = "L36"
    canonical_name = "cognitive.awe"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['geometry.ceiling_height_proxy', 'geometry.vertical_aspect_ratio', 'geometry.proportional_canon_score', 'light.above_eye_level_illumination', 'compositional.vista_terminus_present']

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
            f"Sprint 5: vlm family detector for L36 "
            f"(cognitive.awe) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
