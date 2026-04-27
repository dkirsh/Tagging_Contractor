"""Sprint 1 stub for L48 — Dyadic Intimacy Support.

Registry canonical name: ``social.dyadic_intimacy``
V2.6 Tier: 1
Method family: composite
Value type: categorical (F-formation enum) with secondary ordinal Likert

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L48(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Dyadic Intimacy Support (L48) for the supplied scene.

    L48 is the *exactly-two-seat* affordance whose seat separation
    (Hall, 1966, ch. 10), mutual orientation, and surrounding partial
    enclosure jointly afford a sustained dyadic encounter (Kendon, 1990,
    ch. 7; Goffman, 1971, ch. 2; Sommer, 1969). Cross-cultural variance
    is *high*; Hall's distance zones are calibrated on North-American
    middle-class samples.

    Args:
        image: H x W x 3 RGB ndarray.
        segments: dict of upstream observables, expected to include
            ``furniture.paired_seat_cluster``,
            ``furniture.seat_separation_distance_estimate``,
            ``furniture.intervening_small_artefact_present``,
            ``enclosure.partial_screen_present``,
            ``enclosure.alcove_or_corner_present``,
            ``furniture.chair_back_height``, and
            ``geometry.dyad_midpoint_isovist``.
        depth: optional monocular-depth ndarray; in 3D mode seat
            distances and partial-enclosure surfaces become directly
            metric.

    Expected upstream observables (per ``L48.md`` Engineer pass):
        - ``furniture.paired_seat_cluster``
        - ``furniture.seat_separation_distance_estimate``
        - ``furniture.intervening_small_artefact_present``
        - ``enclosure.partial_screen_present``
        - ``enclosure.alcove_or_corner_present``
        - ``furniture.chair_back_height``
        - ``geometry.dyad_midpoint_isovist``

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

        Per panel disposition §3 viii AND §3 ix, L48 MUST emit BOTH the
        Hall ``distance_zone_estimate`` field (intimate, personal_close,
        personal_far, social_close, social_far, public) AND the Kendon
        F-formation-geometry sub-fields. Without the distance estimate
        the categorical/Likert outputs are not interpretable for L48.

    Sprint 2 implementation notes:
        Primary literature: Hall (1966, ch. 10) — load-bearing for the
        distance-zone requirement; Kendon (1990, pp. 209-217) on
        dyadic interactional ecologies; Goffman (1971, ch. 2) on
        territorial preserves; Hall (1959); Sommer (1969) on the
        L-arrangement corner preference. The dyad-specific parent-tag
        emphasis is the load-bearing fix against the Spohn 50%-overlap
        risk against L44 and L49.
    """
    raise NotImplementedError(
        "detect_L48 (social.dyadic_intimacy) is a Sprint 1 stub; "
        "Sprint 2 will implement two-seat F-formation classification with "
        "Hall distance-zone and partial-enclosure scoring."
    )
