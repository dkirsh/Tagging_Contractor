"""Sprint 2 stub for L15 (cognitive.social_exposure).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L15(image: "ndarray", segments: dict, depth: "ndarray | None" = None) -> dict:
    """Detect Feeling on display..
    
    Construct: Feeling on display.
    Canonical name: cognitive.social_exposure
    L-number: L15
    Subdomain: crowding_density
    value_type: ordinal
    method_family: composite
    interaction_mode: unfocused  |  valence_polarity: negative  |  temporal_window: snapshot
    
    Definition:
        The appraised degree to which an occupant of the depicted space would feel
        visually on display to others - the 'all eyes could be on me' quality of the
        seat or position. Operationalised through cues that predict visual exposure:
        central seating versus peripheral seating, the visibility isovist of the
        seat (how much of the room can see the occupant), the intensity of key
        lighting falling on the sea
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - geometry.seat_centrality
        - geometry.visibility_isovist_at_seat
        - lighting.key_light_intensity_at_seat
        - scene.surrounding_observer_count
        - geometry.seat_back_to_wall_or_open
    
    Sprint 3 implementation notes — primary literature:
        Goffman, E. (1963). Behavior in public places: Notes on the social organization of gatherings. Free Press.
        Goffman, E. (1959). The presentation of self in everyday life. Anchor Books.
        Hall, E. T. (1966). The hidden dimension. Doubleday.
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L15 (cognitive.social_exposure) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
