"""Sprint 1 stub for L41 — Chance-Encounter Potential.

Registry canonical name: ``social.chance_encounter_potential``
V2.6 Tier: 2 (panel-overridden to Tier 3; see panel disposition §3 ii)
Method family: composite
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401


def detect_L41(
    image: "ndarray",
    segments: dict,
    depth: "ndarray | None" = None,
) -> dict:
    """Score Chance-Encounter Potential (L41) for the supplied scene.

    Per the Hillier (1996) natural-movement theorem, chance-encounter
    potential is a property of the *whole* spatial configuration (the
    integration value in the global axial map) and is not in principle
    recoverable from a single still image. The Sprint 1 architectural panel
    therefore demoted L41 from V2.6 Tier 2 to Tier 3
    (``extractability.from_2d == "no"``); this stub is included to reserve
    the dispatch slot, document the contract, and surface the construct
    contest to the student handoff (see
    ``docs/sprint1_latent_specs/L41.md`` and
    ``docs/sprint1_panel_disposition_2026-04-28.md`` §3 ii).

    Args:
        image: H x W x 3 RGB ndarray (the photograph; primarily used for
            region localisation against an externally supplied floor plan).
        segments: dict of upstream segmentation/observable products keyed
            by tag id. The Sprint 2 implementation will look up the
            floor-plan-derived ``configuration.axial_integration_global``
            value here, plus ``affordance.path_count_visible``,
            ``affordance.intersection_density``,
            ``geometry.threshold_segments_3d``, and
            ``affordance.sightline_extent_3d`` for region anchoring.
        depth: optional H x W monocular-depth ndarray; not load-bearing
            for L41 (a 3D scan of one room still lacks the global axial
            map).

    Expected upstream observables (per ``L41.md`` Engineer pass):
        - ``configuration.axial_integration_global``
        - ``affordance.path_count_visible``
        - ``affordance.intersection_density``
        - ``geometry.threshold_segments_3d``
        - ``affordance.sightline_extent_3d``

    Returns:
        dict shaped as::

            {
                "value": int,            # 0-4 Likert
                "confidence": float,     # [0.0, 1.0]
                "evidence": list[str],   # human-readable evidence strings
            }

        When called without floor-plan augmentation the eventual
        implementation must return ``value=None`` (or sentinel) with
        ``confidence=0.0`` and an evidence flag indicating
        ``requires_floor_plan: true``. No panel-mandated distance-zone
        or F-formation-geometry sub-fields apply to L41.

    Sprint 2 implementation notes:
        Primary literature: Hillier (1996, ch. 4) on the natural-movement
        theorem; Hillier and Hanson (1984) on configurational analysis;
        Whyte (1980) on the empirical co-presence corollary at urban
        plaza scale. The Sprint 2 implementer must consume a floor-plan
        axial map (not the image) as the load-bearing input, and must
        treat any "image cue" inferences (corridors crossing, central
        nodes) as suggestive context only — not as extraction substrates.
    """
    raise NotImplementedError(
        "detect_L41 (social.chance_encounter_potential) is a Sprint 1 stub; "
        "real extraction is scheduled for Sprint 2 once floor-plan "
        "augmentation is wired into the registry consumer."
    )
