"""Sprint 1 stub for L51 — Large-Group Assembly Support.

Registry canonical name: ``social.large_group_assembly``
V2.6 Tier: 1
Method family: composite
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L51(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Large-Group Assembly Support (L51) for the supplied scene.

    L51 is the capacity-and-configuration affordance for 7+ person
    co-presence events (Goffman, 1963, pp. 18-24; Hillier and Hanson,
    1984; Hall, 1966, ch. 11 on the public-distance threshold). The
    construct requires floor-plan augmentation
    (``extractability.requires_floor_plan == true``) and uses
    ``configurational_measure: connectivity``.

    Args:
        image: H x W x 3 RGB ndarray (preferably wide-angle).
        segments: dict of upstream observables, expected to include
            ``affordance.seating_count``, ``affordance.isovist_area``,
            ``affordance.open_floor_polygon_m2``,
            ``affordance.focal_wall_present``,
            ``affordance.stage_height_estimate``, and
            ``affordance.aisle_connectivity_index``.
        depth: optional monocular-depth ndarray; in 3D mode the open-
            floor polygon and elevation discontinuities are recoverable
            directly.

    Expected upstream observables (per ``L51.md`` Engineer pass):
        - ``affordance.seating_count``
        - ``affordance.isovist_area``
        - ``affordance.open_floor_polygon_m2``
        - ``affordance.focal_wall_present``
        - ``affordance.stage_height_estimate``
        - ``affordance.aisle_connectivity_index``

    Returns:
        dict shaped as::

            {
                "value": int,                       # 0-4 Likert
                "confidence": float,                # [0.0, 1.0]
                "evidence": list[str],
                "distance_zone_estimate": str,      # Hall (1966) zone
            }

        Per panel disposition §3 viii (Hall mandate), L51 MUST emit a
        ``distance_zone_estimate`` in
        ``{intimate, personal_close, personal_far, social_close,
        social_far, public}``. For genuine assembly settings the zone
        is typically ``public`` (≥ 3.7 m).

    Sprint 2 implementation notes:
        Primary literature: Goffman (1963, pp. 18-24) on focused
        gatherings; Hillier and Hanson (1984) on the connectivity
        substrate; Whyte (1980) on bounded-setting capacity; Hall
        (1966, ch. 11) on the public-distance threshold. Narrow-FOV
        2D images of large halls are a known failure mode; the
        eventual extractor must downweight confidence accordingly.
    """
    raise NotImplementedError(
        "detect_L51 (social.large_group_assembly) is a Sprint 1 stub; "
        "Sprint 2 will implement capacity-plus-connectivity scoring."
    )
