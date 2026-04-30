"""L34 Welcome — vlm family algorithmic skeleton.

Construct: Binary sense that 'people like me' belong here and would be received hospitably.
Method family: vlm
Subdomain: social_signal
Value type: latent_score; value states: [0, 1]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect welcoming cues (greeter desk, signage 'WELCOME', open posture).
    Step 2: Compute warmth signals (warm light, soft seating, plants).
    Step 3: VLM probe: 'Someone like me is welcome here' (5 inclusion items).
    Step 4: Binary: 1 if (>=3 of 5 VLM items > 0.5) OR (greeter detected); else 0.
    Step 5: Confidence = mean VLM score.

Citations:
    Tuan, Y.-F. (1977). *Space and place: The perspective of experience*. University of Minnesota Press.
    Smith, J. L. (1976). The early decoration of inclusive design. In *Designing for the disabled*. RIBA Publications.
    Goffman, E. (1971). *Relations in public: Microstudies of the public order*. Basic Books.
    Goffman, E. (1963). Behavior in public places. Free Press.
    Cheryan, S., et al. (2009). Ambient belonging. Journal of Personality and Social Psychology, 97(6), 1045-1060.

Sprint 5 implementation notes:
    - Greeter detection via person-detection + foreground-position heuristic.
    - Use Cheryan ambient-belonging items in the VLM probe.
    - Validate against Cheryan 2009 belonging ratings.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class WelcomeExtractor(LatentExtractor):
    attribute_id = "L34"
    canonical_name = "cognitive.welcome"
    method_family = "vlm"
    value_states = [0, 1]
    expected_upstream_observables = ['furniture.seating_variety_score', 'signage.tone_sentiment', 'accessibility.ramp_or_lift_visible', 'accessibility.accessible_seating_present', 'barrier.security_or_turnstile_present', 'objects.threshold_undefended']

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
            f"Sprint 5: vlm family detector for L34 "
            f"(cognitive.welcome) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
