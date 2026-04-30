"""L45 Peripheral Participation — composite family algorithmic skeleton.

Construct: Affordance for adjacent-but-not-incorporated presence: watching, listening, lingering on edges.
Method family: composite
Subdomain: peripheral_engagement
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect peripheral-zone seating (edges, alcoves, low-occupancy positions).
    Step 2: Compute sightline from peripheral seat to central activity.
    Step 3: Detect physical barrier permeability (low walls, glass).
    Step 4: Composite = 0.4*peripheral_seats + 0.4*sightline_to_centre + 0.2*permeability.
    Step 5: Bin to 0-4 Likert (Lave-Wenger LPP gradient).

Citations:
    Whyte, W. H. (1980). The social life of small urban spaces. Conservation Foundation.
    Lave, J., & Wenger, E. (1991). Situated learning: Legitimate peripheral participation. Cambridge University Press. https://doi.org/10.1017/CBO9780511815355
    Goffman, E. (1963). Behavior in public places: Notes on the social organization of gatherings. Free Press.

Sprint 5 implementation notes:
    - Peripheral classification: distance from layout centroid > 0.6 * room half-diagonal.
    - Sightline check: ray-casting from seat to centre activity region.
    - Validate against Lave-Wenger LPP qualitative case-study sites.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class PeripheralParticipationExtractor(LatentExtractor):
    attribute_id = "L45"
    canonical_name = "social.peripheral_participation"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['affordance.perch_count', 'affordance.edge_seating_orientation', 'affordance.sightline_to_flow', 'affordance.rail_balcony_presence']

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
            f"Sprint 5: composite family detector for L45 "
            f"(social.peripheral_participation) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
