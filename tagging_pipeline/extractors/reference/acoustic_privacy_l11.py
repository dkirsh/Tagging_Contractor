"""L11 Acoustic Privacy — composite family algorithmic skeleton.

Construct: Not being overheard.
Method family: composite
Subdomain: privacy_attention
Value type: ordinal; value states: [0, 1, 2, 3, 4]

Algorithm sketch (Sprint 5 implementer fills in):

    Step 1: Detect acoustic-absorbing surfaces (fabric, carpet, drapes, acoustic panels).
    Step 2: Compute room-volume + hard-surface ratio (concrete, glass, metal).
    Step 3: Detect partitions (walls, panels, booths) for occlusion.
    Step 4: Composite = 0.4*absorber_ratio + 0.3*partition_count + 0.3*(1/hard_ratio).
    Step 5: Bin to 0-4 Likert (lower = less acoustic privacy).

Citations:
    Sundstrom, E., Burt, R. E., & Kamp, D. (1980). Privacy at work: Architectural correlates of job satisfaction and job performance. Academy of Management Journal, 23(1), 101-117. https://doi.org/10.2307/255498
    Mehta, R., Zhu, R. J., & Cheema, A. (2010). Is noise always bad? Exploring the effects of ambient noise on creative cognition. Journal of Consumer Research, 39(4), 784-799. https://doi.org/10.1086/665048
    Hall, E. T. (1966). The hidden dimension. Doubleday.
    Cavanaugh, W. J., et al. (1962). Speech privacy in buildings. JASA, 34(4), 475-492.
    Bradley, J. S., & Gover, B. N. (2004). Speech privacy index. NRC Construction Research Centre.

Sprint 5 implementation notes:
    - Material classification via OpenSurfaces; map to absorption coefficients.
    - Volume estimation requires depth.
    - Validate against Bradley-Gover speech privacy index lab tests.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class AcousticPrivacyExtractor(LatentExtractor):
    attribute_id = "L11"
    canonical_name = "cognitive.acoustic_privacy"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = ['materials.soft_absorbent_surface_present', 'materials.acoustic_panel_present', 'geometry.enclosure_degree', 'geometry.partition_height', 'geometry.distance_to_nearest_workstation', 'scene.room_volume_estimate']

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
            f"Sprint 5: composite family detector for L11 "
            f"(cognitive.acoustic_privacy) is not yet implemented. "
            f"See module docstring for algorithm sketch."
        )
