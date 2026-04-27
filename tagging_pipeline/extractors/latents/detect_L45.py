"""Sprint 1 stub for L45 — Peripheral Participation.

Registry canonical name: ``social.peripheral_participation``
V2.6 Tier: 1
Method family: composite
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L45(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Peripheral Participation (L45) for the supplied scene.

    L45 indexes the *spatial-physical* affordance for adjacent-but-not-
    incorporated presence — perches, edges, rails, benches facing a
    separable flow (Whyte, 1980; Goffman, 1963). The Lave and Wenger
    (1991) developmental sense of "legitimate peripheral participation"
    is explicitly *out of scope* for this image-extracted construct.

    Args:
        image: H x W x 3 RGB ndarray.
        segments: dict of upstream observables, expected to include
            ``affordance.perch_count``,
            ``affordance.edge_seating_orientation``,
            ``affordance.sightline_to_flow``, and
            ``affordance.rail_balcony_presence``.
        depth: optional monocular-depth ndarray for 3D scene-graph
            sightline-sweep computation.

    Expected upstream observables (per ``L45.md`` Engineer pass):
        - ``affordance.perch_count``
        - ``affordance.edge_seating_orientation``
        - ``affordance.sightline_to_flow``
        - ``affordance.rail_balcony_presence``

    Returns:
        dict shaped as::

            {
                "value": int,            # 0-4 Likert
                "confidence": float,     # [0.0, 1.0]
                "evidence": list[str],
            }

        L45 is not in the panel-mandated lists for ``distance_zone_estimate``
        or F-formation geometry, so no extra fields are required.

    Sprint 2 implementation notes:
        Primary literature: Whyte (1980, ch. 2) on perches and bench-edge
        sociality; Lave and Wenger (1991) for term provenance only
        (developmental sense out of scope); Goffman (1963) on unfocused
        interaction. The construct must be carefully discriminated from
        L41 (configurational), L56 (mingling), and the F-formation
        cluster (L44, L48, L49).
    """
    raise NotImplementedError(
        "detect_L45 (social.peripheral_participation) is a Sprint 1 stub; "
        "Sprint 2 will implement perch-and-edge-affordance scoring."
    )
