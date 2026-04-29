"""Sprint 2 stub for L16 (cognitive.resource_scarcity).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L16(image: "ndarray", segments: dict, depth: "ndarray | None" = None) -> dict:
    """Detect Competition for seats/outlets/space..
    
    Construct: Competition for seats/outlets/space.
    Canonical name: cognitive.resource_scarcity
    L-number: L16
    Subdomain: crowding_density
    value_type: ordinal
    method_family: composite
    interaction_mode: unfocused  |  valence_polarity: negative  |  temporal_window: snapshot
    
    Definition:
        The appraised competition for finite spatial resources - seats, electrical
        outlets, surface area, restrooms, amenities - among occupants of the
        depicted space. Operationalised through cues that predict supply-demand
        imbalance: the ratio of available seats to plausible occupants, the per-
        occupant share of finite amenities (outlets per seat, sinks per restroom),
        and the visible signs of contention (
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - scene.seat_to_occupant_ratio
        - furniture.outlet_count
        - furniture.outlet_to_seat_ratio
        - furniture.surface_area_per_occupant
        - scene.amenity_supply_count
    
    Sprint 3 implementation notes — primary literature:
        Barker, R. G. (1968). Ecological psychology: Concepts and methods for studying the environment of human behavior. Stanfo
        Wicker, A. W. (1979). An introduction to ecological psychology. Brooks/Cole.
        Stokols, D. (1972). On the distinction between density and crowding: Some implications for future research. Psychologica
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L16 (cognitive.resource_scarcity) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
