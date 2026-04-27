"""Sprint 1 stub for L43 — Approach Invitation.

Registry canonical name: ``social.approach_invitation``
V2.6 Tier: 1
Method family: composite
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L43(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Approach Invitation (L43) for the supplied scene.

    L43 is the unfocused-encounter affordance for a stranger to initiate
    light contact with co-present others, scored on the entry-frontage-
    barrier triad (Whyte, 1980; Goffman, 1963, 1971). Cross-cultural
    variance is *high*: Western face-to-face frontal-approach norms do
    not transfer to Mediterranean, Japanese, or other settings (Hall,
    1966, ch. 10).

    Args:
        image: H x W x 3 RGB ndarray of the candidate setting.
        segments: dict of upstream observables, expected to include
            ``affordance.threshold_count``,
            ``affordance.entry_to_first_seat_distance_m``,
            ``affordance.host_barrier_present``,
            ``affordance.sittable_edge_length_m``,
            ``affordance.edge_orientation_to_circulation``, and
            ``affordance.barrier_count_at_approach_axis``.
        depth: optional H x W monocular-depth ndarray for 3D-augmented
            geometry estimation.

    Expected upstream observables (per ``L43.md`` Engineer pass):
        - ``affordance.threshold_count``
        - ``affordance.entry_to_first_seat_distance_m``
        - ``affordance.host_barrier_present``
        - ``affordance.sittable_edge_length_m``
        - ``affordance.edge_orientation_to_circulation``
        - ``affordance.barrier_count_at_approach_axis``

    Returns:
        dict shaped as::

            {
                "value": int,                       # 0-4 Likert
                "confidence": float,                # [0.0, 1.0]
                "evidence": list[str],
                "distance_zone_estimate": str,      # Hall (1966) zone
            }

        Per panel disposition §3 viii (Hall mandate), L43 MUST emit a
        ``distance_zone_estimate`` field with values
        ``{intimate, personal_close, personal_far, social_close,
        social_far, public}``. The Western-calibration warning must
        accompany any non-Western scene.

    Sprint 2 implementation notes:
        Primary literature: Whyte (1980), *The social life of small
        urban spaces*; Goffman (1963), *Behavior in public places*;
        Goffman (1971, pp. 19-27) on the with/single distinction
        (logged for L43a/b split); Oldenburg (1989) on third places;
        Hall (1966), *The hidden dimension*. The Spohn 50%-overlap
        rule with L44 is honoured by privileging entry-geometry and
        barrier-inventory observables over chair-orientation tags.
    """
    raise NotImplementedError(
        "detect_L43 (social.approach_invitation) is a Sprint 1 stub; "
        "Sprint 2 will implement entry-frontage-barrier scoring."
    )
