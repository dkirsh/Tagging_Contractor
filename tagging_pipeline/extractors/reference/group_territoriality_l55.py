"""L55 Group Territoriality — composite family algorithmic skeleton.

Construct: Ease with which a group of two or more can claim a shared spot as theirs.
Method family: composite
Subdomain: territory
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect group territorial markers (jackets on chairs, claimed table objects).
    Step 2: Detect spatial enclosure of group (booth, alcove, chair circle).
    Step 3: Compute marker density per group footprint.
    Step 4: Composite = 0.5*marker_density + 0.5*enclosure_score.
    Step 5: Bin to 0-4 Likert (Lyman-Scott group territory).

Citations:
    Altman, I. (1975). *The environment and social behavior: Privacy, personal space, territory, crowding*. Brooks/Cole. (See ch. 6 on the primary/secondary/public territory distinction.)
    Goffman, E. (1971). *Relations in public: Microstudies of the public order*. Basic Books. (See ch. 2, 'The territories of the self,' for the marker mechanism and stalls/turns/possessional territories.)
    Hall, E. T. (1966). *The hidden dimension*. Doubleday. (See ch. 10 on cross-cultural variation in territorial markers.)
    Lyman, S. M., & Scott, M. B. (1967). Territoriality: A neglected sociological dimension. Social Problems, 15(2), 236-249.
    Brown, B. B. (1987). Territoriality. In Handbook of environmental psychology (Vol. 1, pp. 505-531).

Sprint 5 implementation notes:
    - Marker detection: fine-tune detector on jacket-on-chair, drinks-on-table.
    - Enclosure scoring via geometry (booth detection).
    - Validate against Lyman-Scott territoriality coding scheme.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class GroupTerritorialityExtractor(LatentExtractor):
    attribute_id = "L55"
    canonical_name = "social.group_territoriality"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['affordance.furniture_class_map', 'affordance.surface_inventory', 'affordance.bounding_count', 'affordance.circulation_distance_px', 'affordance.marker_presence', 'affordance.spot_enclosure_isovist']

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
            f"Sprint 5: composite family detector for L55 "
            f"(social.group_territoriality) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
