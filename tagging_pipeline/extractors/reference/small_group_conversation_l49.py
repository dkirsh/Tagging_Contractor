"""L49 Small Group Conversation — composite family algorithmic skeleton.

Construct: Spatial support for a focused 3–6 person F-formation, standing or seated.
Method family: composite
Subdomain: conversation
Value type: categorical; value states: ['vis_a_vis', 'l_arrangement', 'side_by_side', 'semicircular', 'circular', 'none']

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect 3-6 person seating clusters via DBSCAN.
    Step 2: Fit F-formation per Kendon (semicircular/circular preferred for small groups).
    Step 3: Compute O-space centroid + radius via convex-hull of seat centroids.
    Step 4: Pick arrangement best supporting 3-6 person conversation.
    Step 5: Output categorical + FFormationResult.

Citations:
    Kendon, A. (1976). The F-formation system: The spatial organization of social encounters. *Man-Environment Systems*, *6*(6), 291–296. (Foundational F-formation article; pre-DOI era.)
    Kendon, A. (1990). *Conducting interaction: Patterns of behavior in focused encounters*. Cambridge University Press. (Definitive treatment of p-space and o-space; ch. 7 on F-formation arrangements; pp. 209–214 on the analytic priority of the o-space.)
    Hall, E. T. (1966). *The hidden dimension*. Doubleday. (Personal/social distance bands; ch. 10 on cross-cultural variance; the metric basis for distinguishing L49 conversational distance from L51 seminar distance.)
    Kendon, A. (1990). Conducting interaction. Cambridge.
    Goffman, E. (1981). Forms of talk. University of Pennsylvania Press.

Sprint 5 implementation notes:
    - Cluster size in [3, 6]; otherwise return 'none'.
    - O-space derived from Kendon convex-hull-around-orientations.
    - Validate against multi-party-conversation video datasets (e.g. AMI corpus).
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult, FFormationResult, DistanceAwareResult


class SmallGroupConversationExtractor(LatentExtractor):
    attribute_id = "L49"
    canonical_name = "social.small_group_conversation"
    method_family = "composite"
    value_states = ['vis_a_vis', 'l_arrangement', 'side_by_side', 'semicircular', 'circular', 'none']
    expected_upstream_observables = ['furniture.chair_cluster_count', 'furniture.round_table_present', 'furniture.chair_orientation', 'geometry.free_floor_pocket_radius', 'geometry.cluster_distance_estimate', 'scene.ambient_noise_proxy', 'geometry.o_space_centroid']

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
            f"Sprint 5: composite family detector for L49 "
            f"(social.small_group_conversation) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
