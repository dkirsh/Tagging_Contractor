"""L43 Approach Invitation — composite family algorithmic skeleton.

Construct: Degree to which entry geometry and seating frontage invite a stranger to initiate contact.
Method family: composite
Subdomain: encounter
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect open seating with frontal exposure (no rear barrier).
    Step 2: Compute eye-level signage warmth (welcoming vs. forbidding text).
    Step 3: Detect approach-blocking elements (gates, locked doors, 'staff only').
    Step 4: Composite = 0.4*seating_openness + 0.3*signage_warmth - 0.3*blockers.
    Step 5: Bin to 0-4 Likert (Whyte sittable-edges gradient).

Citations:
    Whyte, W. H. (1980). The social life of small urban spaces. The Conservation Foundation.
    Goffman, E. (1963). Behavior in public places: Notes on the social organization of gatherings. Free Press.
    Goffman, E. (1971). Relations in public: Microstudies of the public order. Basic Books.
    Gehl, J. (2010). Cities for people. Island Press.

Sprint 5 implementation notes:
    - Seating detection via Mask R-CNN COCO + custom 'bench' class.
    - OCR signage classification (welcoming/forbidding) via CLIP zero-shot.
    - Validate against Whyte-Gehl plaza-sitting observational data.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult, DistanceAwareResult


class ApproachInvitationExtractor(LatentExtractor):
    attribute_id = "L43"
    canonical_name = "social.approach_invitation"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['affordance.threshold_count', 'affordance.entry_to_first_seat_distance_m', 'affordance.host_barrier_present', 'affordance.sittable_edge_length_m', 'affordance.edge_orientation_to_circulation', 'affordance.barrier_count_at_approach_axis']

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> DistanceAwareResult:
        # Sprint 5: implement per algorithm sketch in module docstring.
        raise NotImplementedError(
            f"Sprint 5: composite family detector for L43 "
            f"(social.approach_invitation) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
