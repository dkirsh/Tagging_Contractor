"""L19 Soft Fascination — vlm family algorithmic skeleton.

Construct: Effortless attention capture (non-demanding).
Method family: vlm
Subdomain: restoration
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Compute fractal dimension of natural texture (clouds, foliage, water) via box-counting.
    Step 2: Detect biophilic features (Browning patterns 1-14): water, plants, fire, animals.
    Step 3: VLM probe: 'This scene gently holds my attention without effort' (PRS items).
    Step 4: Composite = 0.4*fractal_score + 0.3*biophilic_count + 0.3*VLM.
    Step 5: Bin to 0-4 Likert.

Citations:
    Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
    Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. Journal of Environmental Psychology, 15(3), 169-182. https://doi.org/10.1016/0272-4944(95)90001-2
    Berman, M. G., Jonides, J., & Kaplan, S. (2008). The cognitive benefits of interacting with nature. Psychological Science, 19(12), 1207-1212. https://doi.org/10.1111/j.1467-9280.2008.02225.x
    Taylor, R. P. (2006). Reduction of physiological stress using fractal art and architecture. Leonardo, 39(3), 245-251.
    Browning, W. D., Ryan, C. O., & Clancy, J. O. (2014). 14 Patterns of Biophilic Design. Terrapin Bright Green.

Sprint 5 implementation notes:
    - Fractal dimension via skimage; D ~ 1.3-1.5 = peak fascination per Taylor.
    - Biophilic-feature classifier: fine-tune CLIP with the 14 Browning patterns.
    - Validate against PRS Fascination subscale + Taylor fractal preference data.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class SoftFascinationExtractor(LatentExtractor):
    attribute_id = "L19"
    canonical_name = "cognitive.soft_fascination"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['scene.water_feature_present', 'scene.gentle_motion_indicator', 'texture.fractal_pattern_strength', 'scene.natural_pattern_density', 'scene.gentle_complexity_index']

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
            f"Sprint 5: vlm family detector for L19 "
            f"(cognitive.soft_fascination) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
