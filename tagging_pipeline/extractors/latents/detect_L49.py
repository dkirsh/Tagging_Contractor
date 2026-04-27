"""Sprint 1 stub for L49 — Small-Group Conversation Support.

Registry canonical name: ``social.small_group_conversation``
V2.6 Tier: 1
Method family: composite
Value type: categorical (F-formation enum) with secondary ordinal Likert

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L49(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Small-Group Conversation Support (L49) for the supplied scene.

    L49 is the cluster-scale F-formation affordance for 3-6 person
    focused gatherings (Steiner, 1972; Kendon, 1990, ch. 7; Hall, 1966,
    ch. 10). Without metric distance estimation the construct collapses
    into L51 (large-group assembly), so the Hall distance-zone field is
    *doubly* load-bearing. Cross-cultural variance is *high*.

    Args:
        image: H x W x 3 RGB ndarray.
        segments: dict of upstream observables, expected to include
            ``furniture.chair_cluster_count``,
            ``furniture.round_table_present``,
            ``furniture.chair_orientation``,
            ``geometry.free_floor_pocket_radius``,
            ``geometry.cluster_distance_estimate``,
            ``scene.ambient_noise_proxy``, and
            ``geometry.o_space_centroid``.
        depth: optional monocular-depth ndarray; in 3D mode cluster
            distances become directly metric.

    Expected upstream observables (per ``L49.md`` Engineer pass):
        - ``furniture.chair_cluster_count``
        - ``furniture.round_table_present``
        - ``furniture.chair_orientation``
        - ``geometry.free_floor_pocket_radius``
        - ``geometry.cluster_distance_estimate``
        - ``scene.ambient_noise_proxy``
        - ``geometry.o_space_centroid``

    Returns:
        dict shaped as::

            {
                "value": str,                       # F-formation enum
                "secondary_value": int,             # 0-4 affordance Likert
                "confidence": float,                # [0.0, 1.0]
                "evidence": list[str],
                "distance_zone_estimate": str,      # Hall (1966) zone
                "o_space_centroid_xy": tuple,       # (float, float) in pixels
                "o_space_radius_px": float,
                "predominant_arrangement": str,     # F-formation enum
            }

        Per panel disposition §3 viii AND §3 ix, L49 MUST emit BOTH the
        Hall ``distance_zone_estimate`` (intimate, personal_close,
        personal_far, social_close, social_far, public) AND the Kendon
        F-formation-geometry sub-fields.

    Sprint 2 implementation notes:
        Primary literature: Kendon (1976, 1990, pp. 209-214); Hall
        (1966, ch. 10) — load-bearing for the L49/L51 size discrimination
        via Hall's personal-far/social-close band (1.2-2.5 m); Steiner
        (1972, ch. 4) on the 3-6 small-group band; Setti, Hung, and
        Cristani (2013) on still-image F-formation detection. An
        acoustic-tractability proxy must be emitted alongside the
        secondary Likert.
    """
    raise NotImplementedError(
        "detect_L49 (social.small_group_conversation) is a Sprint 1 stub; "
        "Sprint 2 will implement 3-6 person F-formation classification "
        "with Hall distance-zone gating."
    )
