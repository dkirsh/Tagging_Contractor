"""L57 Disengagement Ease — composite family algorithmic skeleton.

Construct: Spatial-physical conditions facilitating face-saving departure from an encounter.
Method family: composite
Subdomain: encounter
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Compute exit accessibility: count of doors/openings + shortest path from each seat.
    Step 2: Detect alternative seating for graceful retreat.
    Step 3: Detect blocking obstacles between seat and exit.
    Step 4: Composite = 0.5*exit_accessibility + 0.3*alt_seat_count - 0.2*blockers.
    Step 5: Bin to 0-4 Likert.

Citations:
    Goffman, E. (1967). *Interaction ritual: Essays on face-to-face behavior* (pp. 41-45 on departure as ceremonial accomplishment). Doubleday.
    Goffman, E. (1963). *Behavior in public places: Notes on the social organization of gatherings* (pp. 100-107 on departure rituals and the spatial conditions that support them). Free Press.
    Schegloff, E. A., & Sacks, H. (1973). Opening up closings. *Semiotica*, *8*(4), 289-327. https://doi.org/10.1515/semi.1973.8.4.289
    Goffman, E. (1963). Behavior in public places. Free Press.
    Wolf, M. (1973). The defended neighborhood. Daedalus, 102(4), 31-44.

Sprint 5 implementation notes:
    - Exit detection per L02 sub-component.
    - Path-clearance via floor-segmentation obstacle check.
    - Validate against Goffman disengagement-strategy ethnographies.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class DisengagementEaseExtractor(LatentExtractor):
    attribute_id = "L57"
    canonical_name = "social.disengagement_ease"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['affordance.exit_count', 'affordance.alternate_destination_visibility', 'geometry.seating_dead_end_score', 'geometry.circulation_aisle_proximity']

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
            f"Sprint 5: composite family detector for L57 "
            f"(social.disengagement_ease) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
