"""Sprint 1 stub for L56 — Mingling Affordance.

Registry canonical name: ``social.mingling``
V2.6 Tier: 1
Method family: composite
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L56(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Mingling Affordance (L56) for the supplied scene.

    L56 is the room-level affordance for unfocused, standing,
    mobile-with-light-anchoring sociability (Whyte, 1980; Oldenburg,
    1989; Hillier and Hanson, 1984). The construct fuses local pocket
    geometry (image-extractable) with global configurational
    frequentation; floor-plan augmentation is required
    (``extractability.requires_floor_plan == true``) with
    ``configurational_measure: integration``. A future Sprint may
    split into L56a (local) and L56b (configurational).

    Args:
        image: H x W x 3 RGB ndarray.
        segments: dict of upstream observables, expected to include
            ``furniture.standing_surface_count``,
            ``affordance.free_floor_area_fraction``,
            ``affordance.circulation_path_clearance``, and
            (floor-plan-only) ``affordance.spatial_integration``.
        depth: optional monocular-depth ndarray; in 3D mode standing-
            surface heights and clearance corridors become metric.

    Expected upstream observables (per ``L56.md`` Engineer pass):
        - ``furniture.standing_surface_count``
        - ``affordance.free_floor_area_fraction``
        - ``affordance.circulation_path_clearance``
        - ``affordance.spatial_integration`` (floor-plan-only)

    Returns:
        dict shaped as::

            {
                "value": int,                       # 0-4 Likert
                "confidence": float,                # [0.0, 1.0]
                "evidence": list[str],
                "distance_zone_estimate": str,      # Hall (1966) zone
            }

        Per panel disposition §3 viii (Hall mandate), L56 MUST emit a
        ``distance_zone_estimate`` in
        ``{intimate, personal_close, personal_far, social_close,
        social_far, public}`` for the *expected inter-cluster spacing*
        (cluster geometry is itself culturally indexed).

    Sprint 2 implementation notes:
        Primary literature: Whyte (1980, pp. 16-25); Oldenburg (1989)
        on third places and the come-and-go criterion; Hillier and
        Hanson (1984) on the integration substrate for frequentation;
        Hall (1966) for the Western-calibration warning at medium
        variance. The integration parent is conditionally activated
        (image-only contexts lack it); Sprint 2 BN modelling should
        treat the missingness as informative rather than averaging
        over a missing-parent surrogate.
    """
    raise NotImplementedError(
        "detect_L56 (social.mingling) is a Sprint 1 stub; "
        "Sprint 2 will implement standing-affordance and integration scoring."
    )
