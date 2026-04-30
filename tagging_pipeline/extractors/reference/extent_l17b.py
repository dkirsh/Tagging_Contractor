"""L17b Extent — vlm family algorithmic skeleton.

Construct: Extent — the sense that the environment is a coherent rich whole.
Method family: vlm
Subdomain: restoration
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Compute scene scope (depth quartile range; estimated layout metres).
    Step 2: Compute boundary-richness (count of distinct semantic elements per region).
    Step 3: VLM probe: 'This place feels like a whole world of its own' (PRS Extent items).
    Step 4: Composite = 0.4*scope_norm + 0.3*boundary_richness + 0.3*VLM.
    Step 5: Bin to 0-4 (Hartig PRS Extent subscale).

Citations:
    Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
    Hartig, T., Korpela, K., Evans, G. W., & Gärling, T. (1997). A measure of restorative quality in environments. Scandinavian Housing and Planning Research, 14(4), 175–194. https://doi.org/10.1080/02815739708730435
    Korpela, K., Hartig, T., Kaiser, F. G., & Fuhrer, U. (2001). Restorative experience and self-regulation in favorite places. Environment and Behavior, 33(4), 572–589.
    Hartig, T., Korpela, K., Evans, G. W., & Garling, T. (1997). A measure of restorative quality in environments. Scandinavian Housing & Planning Research, 14(4), 175-194.

Sprint 5 implementation notes:
    - Scope estimation requires monocular depth (MiDaS / DPT).
    - Boundary-richness via panoptic segmentation entropy.
    - Cross-check VLM ratings against Hartig PRS-26 Extent items.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class ExtentExtractor(LatentExtractor):
    attribute_id = "L17b"
    canonical_name = "cognitive.extent"
    method_family = "vlm"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['scene.global_coherence_index', 'geometry.scene_graph_completeness', 'lighting.uniformity_index', 'scene.world_richness_proxy']

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
            f"Sprint 5: vlm family detector for L17b "
            f"(cognitive.extent) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
