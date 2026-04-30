"""L54 Boundary Permeability — geometry family algorithmic skeleton.

Construct: Ease of entering or leaving a bounded social region, indexed by convex-map depth.
Method family: geometry
Subdomain: encounter
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect boundary elements: walls, fences, glass partitions, half-walls.
    Step 2: Classify each boundary by permeability (full | half | visual-only | none).
    Step 3: Compute weighted permeability (walls=0, half=0.5, glass=0.7, opening=1.0).
    Step 4: Aggregate per-boundary scores into mean permeability.
    Step 5: Bin to 0-4 Likert (Hillier-Hanson permeability gradient).

Citations:
    Hillier, B., & Hanson, J. (1984). *The social logic of space*. Cambridge University Press. https://doi.org/10.1017/CBO9780511597237
    Goffman, E. (1963). *Behavior in public places: Notes on the social organization of gatherings*. Free Press.
    Whyte, W. H. (1980). *The social life of small urban spaces*. Conservation Foundation.
    Newman, O. (1972). Defensible space. Macmillan.

Sprint 5 implementation notes:
    - Boundary classification via panoptic segmentation 'wall' / 'fence' / 'window' classes.
    - Permeability coefficients per Hillier-Hanson 1984.
    - Validate against Newman defensible-space photo datasets.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult, GeometryResult


class BoundaryPermeabilityExtractor(LatentExtractor):
    attribute_id = "L54"
    canonical_name = "social.boundary_permeability"
    method_family = "geometry"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['affordance.threshold_count', 'affordance.threshold_aperture_width', 'affordance.door_state', 'affordance.barrier_height', 'affordance.normative_control_present', 'affordance.convex_depth_to_exterior', 'affordance.convex_connectivity']

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> GeometryResult:
        # Sprint 5: implement per algorithm sketch in module docstring.
        raise NotImplementedError(
            f"Sprint 5: geometry family detector for L54 "
            f"(social.boundary_permeability) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
