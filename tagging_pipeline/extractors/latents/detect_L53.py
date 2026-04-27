"""Sprint 1 stub for L53 — Shared Attention Anchor Strength.

Registry canonical name: ``social.shared_attention_anchor``
V2.6 Tier: 1
Method family: composite
Value type: latent_score (binary 0/1)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L53(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Shared Attention Anchor Strength (L53) for the supplied scene.

    L53 is the binary judgment of whether the room commits to a
    triadic joint-attention substrate: a salient environmental anchor
    paired with seating actively oriented toward it (Tomasello, 1995,
    2008; Kendon, 1990 on the o-space focus; Goffman, 1963, ch. 6).
    Kendon's panel-mandated triadic-structure exclusion: focal object
    *without* seating oriented toward it is mere object presence, not
    a shared attention anchor.

    Args:
        image: H x W x 3 RGB ndarray.
        segments: dict of upstream observables, expected to include
            ``affordance.focal_object_present``,
            ``affordance.focal_object_saliency_score``,
            ``affordance.focal_object_polygon``,
            ``furniture.seating_centroid``,
            ``geometry.anchor_to_seating_axis_angle``, and
            ``pose.head_yaw_field``.
        depth: optional monocular-depth ndarray; in 3D mode chair-back
            normals and 3D saliency are directly recoverable.

    Expected upstream observables (per ``L53.md`` Engineer pass):
        - ``affordance.focal_object_present``
        - ``affordance.focal_object_saliency_score``
        - ``affordance.focal_object_polygon``
        - ``furniture.seating_centroid``
        - ``geometry.anchor_to_seating_axis_angle``
        - ``pose.head_yaw_field``

    Returns:
        dict shaped as::

            {
                "value": int,            # 0 or 1 (binary)
                "confidence": float,     # [0.0, 1.0]
                "evidence": list[str],
            }

        L53 is not in the panel-mandated lists for ``distance_zone_estimate``
        or F-formation geometry, so no extra fields are required.

    Sprint 2 implementation notes:
        Primary literature: Tomasello (1995), "Joint attention as social
        cognition", and Tomasello (2008), *Origins of human
        communication*; Kendon (1990, ch. 7) on the o-space focus;
        Goffman (1963, ch. 6); Carpenter, Nagell, and Tomasello (1998).
        ``notes.bn_notes`` flags L53 for Sprint-2 ranking-theoretic
        recoding (Spohn, 2012, §5.3) — ``no anchor`` as the disbelief-
        rank-0 default. The orientation-convergence criterion (≥ 60% of
        seating yaw vectors within ±35° of anchor-direction vector)
        operationalises Kendon's triadic-structure requirement.
    """
    raise NotImplementedError(
        "detect_L53 (social.shared_attention_anchor) is a Sprint 1 stub; "
        "Sprint 2 will implement triadic anchor-and-orientation scoring."
    )
