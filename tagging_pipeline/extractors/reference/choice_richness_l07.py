"""L07 Choice Richness — composite family algorithmic skeleton.

Construct: Choice Richness — availability of distinct zones/options.
Method family: composite
Subdomain: control_autonomy
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Count distinct affordances per region (seat types, surfaces, route options).
    Step 2: Compute Shannon-diversity of affordance categories.
    Step 3: Compute decision-point fanout from circulation graph (Hillier).
    Step 4: Composite = 0.5*shannon + 0.3*decision_fanout + 0.2*affordance_count.
    Step 5: Bin to 0-4 Likert (Iyengar choice-richness gradient).

Citations:
    Barker, R. G. (1968). Ecological psychology: Concepts and methods for studying the environment of human behavior. Stanford University Press.
    Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
    Deci, E. L., & Ryan, R. M. (1985). Intrinsic motivation and self-determination in human behavior. Plenum.
    Iyengar, S. S., & Lepper, M. R. (2000). When choice is demotivating. Journal of Personality and Social Psychology, 79(6), 995-1006.
    Heft, H. (2010). Affordances and the perception of landscape. In Innovative approaches to researching landscape and health (pp. 9-32).

Sprint 5 implementation notes:
    - Affordance taxonomy from Heft 2010; map detected objects to categories.
    - Shannon diversity via standard scipy.stats.entropy.
    - Validate against Iyengar choice-richness paradigm ratings.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class ChoiceRichnessExtractor(LatentExtractor):
    attribute_id = "L07"
    canonical_name = "cognitive.choice_richness"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['affordance.zone_count', 'furniture.seating_type_variety', 'lighting.zone_count', 'scene.niche_diversity', 'scene.activity_setting_count']

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
            f"Sprint 5: composite family detector for L07 "
            f"(cognitive.choice_richness) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
