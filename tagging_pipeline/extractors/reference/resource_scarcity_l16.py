"""L16 Resource Scarcity — composite family algorithmic skeleton.

Construct: Competition for seats/outlets/space.
Method family: composite
Subdomain: crowding_density
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Count high-demand resources visible (seats, outlets, restrooms, food).
    Step 2: Estimate occupancy / queue length per resource type.
    Step 3: Compute scarcity index = users / resources for each resource type.
    Step 4: Composite = max-scarcity across resource types (worst-case).
    Step 5: Bin to 0-4 Likert.

Citations:
    Barker, R. G. (1968). Ecological psychology: Concepts and methods for studying the environment of human behavior. Stanford University Press.
    Wicker, A. W. (1979). An introduction to ecological psychology. Brooks/Cole.
    Stokols, D. (1972). On the distinction between density and crowding: Some implications for future research. Psychological Review, 79(3), 275-277. https://doi.org/10.1037/h0032706
    Mullainathan, S., & Shafir, E. (2013). Scarcity: Why having too little means so much. Times Books.

Sprint 5 implementation notes:
    - Resource counting via fine-tuned object detector per category.
    - Occupancy estimation via person-to-resource assignment heuristic.
    - Validate against observed-vacancy datasets (e.g. cafe seating studies).
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class ResourceScarcityExtractor(LatentExtractor):
    attribute_id = "L16"
    canonical_name = "cognitive.resource_scarcity"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['scene.seat_to_occupant_ratio', 'furniture.outlet_count', 'furniture.outlet_to_seat_ratio', 'furniture.surface_area_per_occupant', 'scene.amenity_supply_count']

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
            f"Sprint 5: composite family detector for L16 "
            f"(cognitive.resource_scarcity) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
