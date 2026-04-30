"""L50 Collaborative Work — composite family algorithmic skeleton.

Construct: Setting affordance for task-focused coordination around a shared artifact or work surface.
Method family: composite
Subdomain: conversation
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect collaborative-work affordances (large tables, whiteboards, monitors).
    Step 2: Detect technology infrastructure (projectors, screens, power outlets).
    Step 3: Detect seat clustering supporting 2-8 collaborators.
    Step 4: Composite = 0.4*affordance + 0.3*tech + 0.3*cluster.
    Step 5: Bin to 0-4 Likert (Allen MIT collaboration gradient).

Citations:
    Hutchins, E. (1995). *Cognition in the wild*. MIT Press. (Foundational distributed-cognition argument that coordination is constituted by the local artifact configuration; ch. 3 on the cockpit as cognitive system is the canonical L50 prototype.)
    Suchman, L. A. (1987). *Plans and situated actions: The problem of human-machine communication*. Cambridge University Press. (Situated-action analysis of how shared artifacts and the local material field organise joint activity; ch. 5 on the photocopier-help interaction.)
    Kirsh, D. (1995). The intelligent use of space. *Artificial Intelligence*, *73*(1–2), 31–68. https://doi.org/10.1016/0004-3702(94)00017-U
    Allen, T. J. (1977). Managing the flow of technology. MIT Press.
    Heerwagen, J. H., et al. (2004). Collaborative knowledge work environments. Building Research & Information, 32(6), 510-528.

Sprint 5 implementation notes:
    - Whiteboard detection via fine-tuned object detector.
    - Power-outlet detection requires high-res image; OCR for outlet symbols.
    - Validate against Allen MIT R&D-team productivity correlations.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult, DistanceAwareResult


class CollaborativeWorkExtractor(LatentExtractor):
    attribute_id = "L50"
    canonical_name = "social.collaborative_work"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['furniture.table_instances', 'surface.area_m2', 'surface.height_class', 'affordance.whiteboard_present', 'affordance.large_display_present', 'affordance.writable_surface_count', 'affordance.display_co_viewability', 'affordance.tool_instance_count_on_surface', 'affordance.task_artifact_present', 'affordance.consumption_object_ratio', 'geometry.chair_l_arrangement_count']

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
            f"Sprint 5: composite family detector for L50 "
            f"(social.collaborative_work) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
