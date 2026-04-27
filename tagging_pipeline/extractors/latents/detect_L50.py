"""Sprint 1 stub for L50 — Collaborative Work Interaction.

Registry canonical name: ``social.collaborative_work``
V2.6 Tier: 1
Method family: composite
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L50(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Collaborative Work Interaction (L50) for the supplied scene.

    L50 is the affordance for *task-focused coordination* around a
    shared artifact or work surface (Hutchins, 1995; Suchman, 1987;
    Kirsh, 1995). The geometric primitive is Kendon's L-arrangement
    F-formation (Kendon, 1990, pp. 209ff): bodies oriented toward a
    shared task object on the surface, not vis-à-vis across it. The
    discriminating cue against L44/L48/L49 is the *content* of the
    shared surface (task artifacts vs. consumption objects).

    Args:
        image: H x W x 3 RGB ndarray.
        segments: dict of upstream observables, expected to include
            ``furniture.table_instances``, ``surface.area_m2``,
            ``surface.height_class``, ``affordance.whiteboard_present``,
            ``affordance.large_display_present``,
            ``affordance.writable_surface_count``,
            ``affordance.display_co_viewability``,
            ``affordance.tool_instance_count_on_surface``,
            ``affordance.task_artifact_present``,
            ``affordance.consumption_object_ratio``, and
            ``geometry.chair_l_arrangement_count``.
        depth: optional monocular-depth ndarray; in 3D mode surface
            heights, display normals, and chair-front-projected angles
            become metric.

    Expected upstream observables (per ``L50.md`` Engineer pass):
        - ``furniture.table_instances``
        - ``surface.area_m2``
        - ``surface.height_class``
        - ``affordance.whiteboard_present``
        - ``affordance.large_display_present``
        - ``affordance.writable_surface_count``
        - ``affordance.display_co_viewability``
        - ``affordance.tool_instance_count_on_surface``
        - ``affordance.task_artifact_present``
        - ``affordance.consumption_object_ratio``
        - ``geometry.chair_l_arrangement_count``

    Returns:
        dict shaped as::

            {
                "value": int,                       # 0-4 Likert
                "confidence": float,                # [0.0, 1.0]
                "evidence": list[str],
                "distance_zone_estimate": str,      # Hall (1966) zone
            }

        Per panel disposition §3 viii (Hall mandate), L50 MUST emit a
        ``distance_zone_estimate`` in
        ``{intimate, personal_close, personal_far, social_close,
        social_far, public}``. (For L50 the typical zone is intimate-
        to-personal-near; personal-far at high score should warn.)

    Sprint 2 implementation notes:
        Primary literature: Hutchins (1995, ch. 3), *Cognition in the
        wild*, on the cockpit as the canonical L50 prototype; Suchman
        (1987, ch. 5) on situated action; Kirsh (1995), "The intelligent
        use of space"; Kirsh (2005) on multi-tasking and collaborative
        cognition; Kendon (1990, pp. 209ff) on the L-arrangement
        F-formation; Goffman (1963) for the focused-mode framing. The
        artifact-and-tool parents must dominate the chair-geometry
        parents in any future BN structure to preserve the construct's
        meaning.
    """
    raise NotImplementedError(
        "detect_L50 (social.collaborative_work) is a Sprint 1 stub; "
        "Sprint 2 will implement L-arrangement-around-task-surface scoring."
    )
