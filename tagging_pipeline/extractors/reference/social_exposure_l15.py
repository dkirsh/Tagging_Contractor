"""L15 Social Exposure — composite family algorithmic skeleton.

Construct: Feeling on display.
Method family: composite
Subdomain: crowding_density
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Compute observer's exposure: 360deg sightline depth + isovist openness.
    Step 2: Count visible bystanders/passers-by (person detector).
    Step 3: Detect occluding refuge elements (planters, half-walls).
    Step 4: Composite = 0.4*isovist_openness + 0.4*bystander_count - 0.2*refuge_count.
    Step 5: Bin to 0-4 Likert (Appleton inverse-refuge axis).

Citations:
    Goffman, E. (1963). Behavior in public places: Notes on the social organization of gatherings. Free Press.
    Goffman, E. (1959). The presentation of self in everyday life. Anchor Books.
    Hall, E. T. (1966). The hidden dimension. Doubleday.
    Appleton, J. (1975). The experience of landscape. Wiley.
    Goffman, E. (1963). Behavior in public places. Free Press.

Sprint 5 implementation notes:
    - Isovist computation requires depth + 360deg image (or panoramic).
    - Person detection via Mask R-CNN COCO.
    - Validate against Goffman/Appleton exposure ratings.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class SocialExposureExtractor(LatentExtractor):
    attribute_id = "L15"
    canonical_name = "cognitive.social_exposure"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['geometry.seat_centrality', 'geometry.visibility_isovist_at_seat', 'lighting.key_light_intensity_at_seat', 'scene.surrounding_observer_count', 'geometry.seat_back_to_wall_or_open']

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
            f"Sprint 5: composite family detector for L15 "
            f"(cognitive.social_exposure) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
