"""Sprint 2 stub for L13 (cognitive.territorial_support).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L13(image: "ndarray", segments: dict, depth: "ndarray | None" = None) -> dict:
    """Detect Ability to claim micro-territory..
    
    Construct: Ability to claim micro-territory.
    Canonical name: cognitive.territorial_support
    L-number: L13
    Subdomain: privacy_attention
    value_type: ordinal
    method_family: composite
    interaction_mode: mixed  |  valence_polarity: neutral  |  temporal_window: snapshot
    
    Definition:
        The appraised affordance for an individual to claim and personalise a
        defined micro-territory within the depicted space - a desk, chair, alcove,
        or other unit clearly bounded enough that an occupant can mark it as 'mine'
        for the duration of an activity. Operationalised through cues that predict
        claimability: defined desk units (assigned, not hot-desk), boundaries that
        visually delimit one person's
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - furniture.assigned_desk_present
        - furniture.armrest_or_boundary_present
        - surface.personalisation_artefact_present
        - geometry.individual_partition_height
        - furniture.individual_storage_present
    
    Sprint 3 implementation notes — primary literature:
        Altman, I. (1975). The environment and social behavior: Privacy, personal space, territory, crowding. Brooks/Cole.
        Brown, G., Lawrence, T. B., & Robinson, S. L. (2005). Territoriality in organizations. Academy of Management Review, 30(
        Hall, E. T. (1966). The hidden dimension. Doubleday.
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L13 (cognitive.territorial_support) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
