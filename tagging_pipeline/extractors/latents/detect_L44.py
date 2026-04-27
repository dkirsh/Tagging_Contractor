"""Sprint 1 stub for L44 — Sociopetal Seating Topology.

Registry canonical name: ``social.sociopetal_seating``
V2.6 Tier: 1
Method family: composite
Value type: categorical (F-formation enum) with secondary ordinal Likert

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L44(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Sociopetal Seating Topology (L44) for the supplied scene.

    L44 captures the Kendon F-formation arrangement implied by a
    multi-seat configuration (Osmond, 1957; Kendon, 1976, 1990). Cross-
    cultural variance is *high* (Hall, 1966, ch. 10); a Western-
    calibrated extractor will systematically misread Japanese,
    Mediterranean, and majlis-style arrangements.

    Args:
        image: H x W x 3 RGB ndarray.
        segments: dict of upstream observables, expected to include
            ``furniture.chair_instances``, ``furniture.chair_orientation``,
            ``furniture.chair_pairwise_angle``,
            ``furniture.chair_cluster_count``,
            ``furniture.intervening_artefact_present``,
            ``scene.floor_plane_normal``, and
            ``geometry.o_space_centroid``.
        depth: optional monocular-depth ndarray; in 3D mode the F-formation
            o-space is computable directly from chair-front rays.

    Expected upstream observables (per ``L44.md`` Engineer pass):
        - ``furniture.chair_instances``
        - ``furniture.chair_orientation``
        - ``furniture.chair_pairwise_angle``
        - ``furniture.chair_cluster_count``
        - ``furniture.intervening_artefact_present``
        - ``scene.floor_plane_normal``
        - ``geometry.o_space_centroid``

    Returns:
        dict shaped as::

            {
                "value": str,                       # one of
                                                    # vis_a_vis | l_arrangement |
                                                    # side_by_side | semicircular |
                                                    # circular | none
                "secondary_value": int,             # 0-4 affordance Likert
                "confidence": float,                # [0.0, 1.0]
                "evidence": list[str],
                "distance_zone_estimate": str,      # Hall (1966) zone
                "o_space_centroid_xy": tuple,       # (float, float) in pixels
                "o_space_radius_px": float,
                "predominant_arrangement": str,     # same enum as ``value``
            }

        Per panel disposition §3 viii AND §3 ix, L44 MUST emit BOTH the
        Hall ``distance_zone_estimate`` field
        (``{intimate, personal_close, personal_far, social_close,
        social_far, public}``) AND the Kendon F-formation-geometry
        sub-fields ``(o_space_centroid_xy, o_space_radius_px,
        predominant_arrangement)``.

    Sprint 2 implementation notes:
        Primary literature: Osmond (1957) on the sociopetal/sociofugal
        distinction; Kendon (1976, 1990, ch. 7 and pp. 209-214) on the
        F-formation system and o-space; Hall (1966, ch. 10) on cross-
        cultural variance; Setti, Hung, and Cristani (2013) on still-
        image F-formation detection. The dyad-distinction with L48 and
        the small-group distinction with L49 must be enforced via
        seat-count and o-space-radius gating.
    """
    raise NotImplementedError(
        "detect_L44 (social.sociopetal_seating) is a Sprint 1 stub; "
        "Sprint 2 will implement F-formation geometry classification."
    )
