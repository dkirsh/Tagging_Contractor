"""Sprint 1 stub for L57 — Disengagement Ease.

Registry canonical name: ``social.disengagement_ease``
V2.6 Tier: 3
Method family: composite
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2
*at earliest* — and only once the upstream-observable substrate is
itself validated. L57 is V2.6 Tier 3 and remains so.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L57(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Disengagement Ease (L57) for the supplied scene.

    L57 indexes the spatial-physical conditions that *facilitate* —
    but do not *constitute* — the ritual accomplishment of leave-
    taking from an encounter (Goffman, 1967, pp. 41-45 on departure
    as a face-saving ceremonial sequence; Goffman, 1963, pp. 100-107).
    Schegloff and Sacks (1973) supply the parallel claim for talk:
    closing sequences are accomplishments, not events. The ritual
    itself is invisible to the registry; L57 measures only the room.

    L57 is V2.6 Tier 3 (``extractability.from_2d == "no"``,
    ``from_3d_vr == "no"``, ``monocular_3d_approx == "no"``) and is
    not currently extractable from any substrate. The stub is
    included only to reserve the dispatch slot.

    Args:
        image: H x W x 3 RGB ndarray (not currently usable).
        segments: dict of (notional) upstream observables, expected to
            include ``affordance.exit_count``,
            ``affordance.alternate_destination_visibility``,
            ``geometry.seating_dead_end_score``, and
            ``geometry.circulation_aisle_proximity``. None of these
            are validated upstream tags as of Sprint 1.
        depth: optional monocular-depth ndarray (not currently usable).

    Expected upstream observables (per ``L57.md`` Engineer pass; all
    notional and pending Phase D reconciliation):
        - ``affordance.exit_count``
        - ``affordance.alternate_destination_visibility``
        - ``geometry.seating_dead_end_score``
        - ``geometry.circulation_aisle_proximity``

    Returns:
        dict shaped as::

            {
                "value": int,            # 0-4 Likert
                "confidence": float,     # [0.0, 1.0]
                "evidence": list[str],
            }

        L57 is not in the panel-mandated lists for ``distance_zone_estimate``
        or F-formation geometry, so no extra fields are required.

    Sprint 2 implementation notes:
        Primary literature: Goffman (1967, pp. 41-45), *Interaction
        ritual*; Goffman (1963, pp. 100-107), *Behavior in public
        places*; Schegloff and Sacks (1973), "Opening up closings",
        *Semiotica*. The construct sits one level above any geometric
        primitive (it measures facilitation of an invisible ritual)
        and SHOULD NOT be extracted in Sprint 2 unless and until the
        upstream-observable substrate is itself validated and the
        Goffmanian construct-validity audit is repeated.
    """
    raise NotImplementedError(
        "detect_L57 (social.disengagement_ease) is a Sprint 1 stub; "
        "the construct is V2.6 Tier 3 and is not scheduled for Sprint 2 "
        "extraction without further upstream-observable validation."
    )
