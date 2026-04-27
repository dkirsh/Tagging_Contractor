"""Sprint 1 stub for L42 — Interactional Visibility.

Registry canonical name: ``social.interactional_visibility``
V2.6 Tier: 1
Method family: geometry
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L42(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Interactional Visibility (L42) for the supplied scene.

    L42 is the configurational opportunity for co-present persons to be
    visible to and to see one another, operationalised as an isovist
    (Hillier and Hanson, 1984; Benedikt, 1979). The eventual implementation
    requires floor-plan augmentation (``extractability.requires_floor_plan
    == true``) and uses ``configurational_measure: isovist_area``.

    Args:
        image: H x W x 3 RGB ndarray of the bounded social setting.
        segments: dict of upstream observables keyed by tag id, expected
            to include ``affordance.isovist_area``,
            ``geometry.partition_height_field``,
            ``geometry.glazing_transparency_mask``, and
            ``affordance.sightline_length_distribution``.
        depth: optional H x W monocular-depth ndarray; in 3D mode the
            implementer can compute the isovist polyhedron directly via
            ``geometry.mesh_occlusion_field`` and ``geometry.eye_height_band``.

    Expected upstream observables (per ``L42.md`` Engineer pass):
        - ``affordance.isovist_area``
        - ``geometry.partition_height_field``
        - ``geometry.glazing_transparency_mask``
        - ``affordance.sightline_length_distribution``

    Returns:
        dict shaped as::

            {
                "value": int,                       # 0-4 Likert
                "confidence": float,                # [0.0, 1.0]
                "evidence": list[str],
                "distance_zone_estimate": str,      # Hall (1966) zone
            }

        Per panel disposition §3 viii (Hall mandate), L42 MUST emit a
        ``distance_zone_estimate`` field taking one of
        ``{intimate, personal_close, personal_far, social_close,
        social_far, public}``.

    Sprint 2 implementation notes:
        Primary literature: Hillier and Hanson (1984), *The social logic
        of space*; Benedikt (1979), "To take hold of space: Isovists and
        isovist fields"; Turner et al. (2001), "From isovists to
        visibility graphs"; Whyte (1980); Goffman (1963, pp. 83-88) on
        civil inattention (deferred candidate L42b). Implementer note:
        pixel-level openness is *not* the substrate — vantage-sampled
        isovist area is. The Spohn 50%-overlap pair {L42, L54} must be
        re-checked at Phase D when implementing.
    """
    raise NotImplementedError(
        "detect_L42 (social.interactional_visibility) is a Sprint 1 stub; "
        "Sprint 2 will implement isovist-based scoring with floor-plan "
        "augmentation."
    )
