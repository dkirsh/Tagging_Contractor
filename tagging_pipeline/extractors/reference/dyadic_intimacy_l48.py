"""L48 Dyadic Intimacy — composite family algorithmic skeleton.

Construct: Two-person seating geometry whose distance and partial enclosure afford intimate dyadic talk.
Method family: composite
Subdomain: conversation
Value type: categorical; value states: ['vis_a_vis', 'l_arrangement', 'side_by_side', 'semicircular', 'circular', 'none']

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect 2-person seating clusters via DBSCAN.
    Step 2: For each pair, classify Kendon F-formation type (vis_a_vis preferred for dyads).
    Step 3: Compute interpersonal distance vs. Hall intimate/personal zones.
    Step 4: Pick best arrangement per pair; output categorical label.
    Step 5: Use FFormationResult + DistanceAwareResult fields (Hall zone).

Citations:
    Hall, E. T. (1966). *The hidden dimension*. Doubleday. (Definitive treatment of the four distance zones — intimate, personal, social, public — with cross-cultural variance documented in ch. 10; the load-bearing reference for L48's distance-zone-estimate requirement.)
    Kendon, A. (1990). *Conducting interaction: Patterns of behavior in focused encounters*. Cambridge University Press. (F-formation system; ch. 7 on the qualitative differences between vis-à-vis, L-arrangement, and side-by-side dyads; pp. 209–217 on dyadic interactional ecologies.)
    Goffman, E. (1971). *Relations in public: Microstudies of the public order*. Basic Books. (Withdrawal from the civil-inattention field as a precondition for intimate dyadic encounter; ch. 2 on the territorial preserves that booths and nooks instantiate.)
    Hall, E. T. (1966). The hidden dimension. Doubleday.
    Kendon, A. (1990). Conducting interaction. Cambridge.

Sprint 5 implementation notes:
    - Pair detection: cluster size == 2 in chair-centroid DBSCAN.
    - Distance estimate from depth + chair centroid distance.
    - Validate against Hall-Kendon dyadic-interaction imagery.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult, FFormationResult, DistanceAwareResult


class DyadicIntimacyExtractor(LatentExtractor):
    attribute_id = "L48"
    canonical_name = "social.dyadic_intimacy"
    method_family = "composite"
    value_states = ['vis_a_vis', 'l_arrangement', 'side_by_side', 'semicircular', 'circular', 'none']
    expected_upstream_observables = ['furniture.paired_seat_cluster', 'furniture.seat_separation_distance_estimate', 'furniture.intervening_small_artefact_present', 'enclosure.partial_screen_present', 'enclosure.alcove_or_corner_present', 'furniture.chair_back_height', 'geometry.dyad_midpoint_isovist']

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> FFormationResult:
        # Sprint 5: implement per algorithm sketch in module docstring.
        raise NotImplementedError(
            f"Sprint 5: composite family detector for L48 "
            f"(social.dyadic_intimacy) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
