"""Sprint 1 stub for L54 — Boundary Permeability.

Registry canonical name: ``social.boundary_permeability``
V2.6 Tier: 2
Method family: geometry
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L54(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Boundary Permeability (L54) for the supplied scene.

    L54 is the ease of entering or leaving a socially bounded region,
    operationalised as depth in the convex map (Hillier and Hanson,
    1984) qualified by normative-control affordances (Goffman, 1963,
    pp. 151-164). The construct requires floor-plan augmentation
    (``extractability.requires_floor_plan == true``) with
    ``configurational_measure: depth``.

    Args:
        image: H x W x 3 RGB ndarray (used for local-cue fallback only).
        segments: dict of upstream observables, expected to include
            ``affordance.threshold_count``,
            ``affordance.threshold_aperture_width``,
            ``affordance.door_state``, ``affordance.barrier_height``,
            ``affordance.normative_control_present``,
            ``affordance.convex_depth_to_exterior``, and
            ``affordance.convex_connectivity``.
        depth: optional monocular-depth ndarray; in 3D mode the convex
            partition can be computed directly from the navigable floor
            mesh.

    Expected upstream observables (per ``L54.md`` Engineer pass):
        - ``affordance.threshold_count``
        - ``affordance.threshold_aperture_width``
        - ``affordance.door_state``
        - ``affordance.barrier_height``
        - ``affordance.normative_control_present``
        - ``affordance.convex_depth_to_exterior``
        - ``affordance.convex_connectivity``

    Returns:
        dict shaped as::

            {
                "value": int,            # 0-4 Likert
                "confidence": float,     # [0.0, 1.0]
                "evidence": list[str],
            }

        L54 is not in the panel-mandated lists for ``distance_zone_estimate``
        or F-formation geometry, so no extra fields are required.

    Sprint 2 implementation notes:
        Primary literature: Hillier and Hanson (1984), *The social
        logic of space*; Hillier (1996), *Space is the machine*;
        Goffman (1963, pp. 151-164) on ritual permission to cross;
        Whyte (1980) on plaza permeability. Visual surrogates listed
        in the spec are a low-confidence fallback when the floor plan
        is absent. The Spohn 50%-overlap pair {L42, L54} must be
        re-checked at Phase D — L54's parents deliberately exclude
        sightline observables (which belong to L42).
    """
    raise NotImplementedError(
        "detect_L54 (social.boundary_permeability) is a Sprint 1 stub; "
        "Sprint 2 will implement convex-map-depth scoring with floor-plan "
        "augmentation."
    )
