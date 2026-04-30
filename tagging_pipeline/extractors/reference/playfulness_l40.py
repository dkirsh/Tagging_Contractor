"""L40 Playfulness — vlm family algorithmic skeleton.

Construct: Ludic, informal tone — invitation to non-serious engagement.
Method family: vlm
Subdomain: familiarity_novelty
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect playful cues (bright colours, curved lines, toys, games, child-scale furniture).
    Step 2: Compute hue-variance and curvature density.
    Step 3: VLM probe: 'This space invites play / non-serious activity' (Sutton-Smith items).
    Step 4: Composite = 0.3*cue_density + 0.2*hue_variance + 0.5*VLM.
    Step 5: Bin to 0-4 Likert.

Citations:
    Bateson, G. (1955). A theory of play and fantasy. *Psychiatric Research Reports*, *2*, 39-51. (Reprinted in *Steps to an Ecology of Mind*, 1972, Chandler Publishing.)
    Bekoff, M. (2014). The significance of ethological studies: Playing and peeing. In M. Bekoff, *Why dogs hump and bees get depressed: The fascinating science of animal intelligence, emotions, friendship, and conservation* (pp. 121-140). New World Library.
    Sutton-Smith, B. (1997). *The ambiguity of play*. Harvard University Press.
    Heft, H. (1988). Affordances of children's environments. Children's Environments Quarterly, 5(3), 29-37.

Sprint 5 implementation notes:
    - Use Mask R-CNN trained on toy/game classes.
    - Curvature via skimage ridge-detection on edge map.
    - Validate against Heft-style playscape affordance ratings.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class PlayfulnessExtractor(LatentExtractor):
    attribute_id = "L40"
    canonical_name = "cognitive.playfulness"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['colour.bright_palette_score', 'forms.whimsical_geometry_score', 'furniture.casual_seating_score', 'material.soft_furnishing_score', 'signage.ludic_tone_score']

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
            f"Sprint 5: vlm family detector for L40 "
            f"(cognitive.playfulness) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
