"""Sprint 1 stub for L55 — Group Territorial Claimability.

Registry canonical name: ``social.group_territoriality``
V2.6 Tier: 2
Method family: composite
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L55(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Group Territorial Claimability (L55) for the supplied scene.

    L55 is the affordance for a co-located group (2-8) to convert a
    sub-region of public territory into a *secondary* territory for
    the duration of the encounter (Altman, 1975, ch. 6; Goffman, 1971,
    ch. 2 on territorial markers). Cross-cultural variance is *high*
    — what counts as a territorial marker (coats, drinks, papers vs.
    shoes, oshibori, shisha) varies sharply by setting (Hall, 1966,
    ch. 10).

    Args:
        image: H x W x 3 RGB ndarray.
        segments: dict of upstream observables, expected to include
            ``affordance.furniture_class_map``,
            ``affordance.surface_inventory``,
            ``affordance.bounding_count``,
            ``affordance.circulation_distance_px``,
            ``affordance.marker_presence``, and (3D only)
            ``affordance.spot_enclosure_isovist``.
        depth: optional monocular-depth ndarray; in 3D mode bounding
            and isovist measures become directly metric.

    Expected upstream observables (per ``L55.md`` Engineer pass):
        - ``affordance.furniture_class_map``
        - ``affordance.surface_inventory``
        - ``affordance.bounding_count``
        - ``affordance.circulation_distance_px``
        - ``affordance.marker_presence``
        - ``affordance.spot_enclosure_isovist`` (3D only)

    Returns:
        dict shaped as::

            {
                "value": int,            # 0-4 Likert
                "confidence": float,     # [0.0, 1.0]
                "evidence": list[str],
            }

        L55 is not in the panel-mandated lists for ``distance_zone_estimate``
        or F-formation geometry, so no extra fields are required.
        However, the eventual implementation MUST emit one score per
        candidate spot rather than one per image, and SHOULD attach a
        ``setting_cultural_class`` proxy and a
        ``defensibility_without_presence`` sub-score per spec.

    Sprint 2 implementation notes:
        Primary literature: Altman (1975, ch. 6), *The environment and
        social behavior*, on primary/secondary/public territory;
        Goffman (1971, ch. 2), *Relations in public*, on the marker
        mechanism; Hall (1966, ch. 10) on cross-cultural variance;
        Brown (1987) on marker effectiveness; Edney (1976) on
        territorial functional properties. The construct must be
        carefully discriminated from L48 (dyadic) and L51 (assembly).
    """
    raise NotImplementedError(
        "detect_L55 (social.group_territoriality) is a Sprint 1 stub; "
        "Sprint 2 will implement candidate-spot enumeration and "
        "boundedness-and-marker scoring."
    )
