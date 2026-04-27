"""Sprint 1 stub for L58 — Interaction Diversity Potential.

Registry canonical name: ``social.interaction_diversity``
V2.6 Tier: 2
Method family: composite
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L58(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Interaction Diversity Potential (L58) for the supplied scene.

    L58 names the degree to which a single setting affords *several
    distinct kinds* of social interaction in parallel — the
    coexistence (not the sum) of micro-zones with differentiated
    furniture, postures, distances, and orientations (Whyte, 1980;
    Oldenburg, 1989; Gehl, 2010). The construct is a meta-construct
    over the L41-L57 affordance family and requires floor-plan
    augmentation (``extractability.requires_floor_plan == true``)
    with ``configurational_measure: connectivity``.

    Args:
        image: H x W x 3 RGB ndarray.
        segments: dict of upstream observables, expected to include
            ``furniture.class_inventory``,
            ``affordance.micro_zone_segmentation``,
            ``posture.afforded_set``,
            ``affordance.distance_regime_set``,
            ``geometry.level_variation``, and
            ``geometry.connectivity_graph``.
        depth: optional monocular-depth ndarray; in 3D mode the full
            spatial envelope is observable and a true cardinality of
            distinct micro-zones is computable.

    Expected upstream observables (per ``L58.md`` Engineer pass):
        - ``furniture.class_inventory``
        - ``affordance.micro_zone_segmentation``
        - ``posture.afforded_set``
        - ``affordance.distance_regime_set``
        - ``geometry.level_variation``
        - ``geometry.connectivity_graph``

    Returns:
        dict shaped as::

            {
                "value": int,            # 0-4 Likert
                "confidence": float,     # [0.0, 1.0]
                "evidence": list[str],
            }

        L58 is not in the panel-mandated lists for ``distance_zone_estimate``
        or F-formation geometry, so no extra fields are required.

    Sprint 2 implementation notes:
        Primary literature: Whyte (1980), *The social life of small
        urban spaces*, on portfolio-of-uses; Oldenburg (1989) on the
        third-place mixed-regulars criterion; Gehl (2010), *Cities for
        people*, on activity-diversity measurement. The Phase D BN
        audit must confirm L58's parents are upstream observables, not
        sibling latent IDs — otherwise L58 will collapse into a
        derived sum of L41-L57 and lose its meta-construct identity.
    """
    raise NotImplementedError(
        "detect_L58 (social.interaction_diversity) is a Sprint 1 stub; "
        "Sprint 2 will implement micro-zone enumeration and connectivity "
        "scoring."
    )
