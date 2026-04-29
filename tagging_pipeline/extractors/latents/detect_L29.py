"""Sprint 2 stub for L29 (cognitive.legibility).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L29(image: "ndarray", segments: dict, depth: "ndarray | None" = None, floor_plan: "FloorPlan | None" = None) -> dict:
    """Detect Ease of understanding the spatial layout and routes through it..
    
    Construct: Ease of understanding the spatial layout and routes through it.
    Canonical name: cognitive.legibility
    L-number: L29
    Subdomain: wayfinding
    value_type: ordinal
    method_family: geometry
    interaction_mode: focused  |  valence_polarity: neutral  |  temporal_window: snapshot
    
    Definition:
        Legibility — Lynch's (1960) fourth element of *The Image of the City* and
        the legibility cell of Kaplan & Kaplan's (1989) Preference Matrix — names
        the ease with which an inhabitant can apprehend the structure of a spatial
        system, anticipate routes through it, and form a stable mental map. Lynch
        operationalises legibility through the five elements (paths, edges,
        districts, nodes, landmarks); space
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str], "configurational_substrate": str}
    
    Expected upstream observables (5):
        - configuration.axial_integration_local
        - configuration.convex_map_depth
        - affordance.sightline_extent_3d
        - affordance.decision_point_clarity
        - configuration.connectivity_graph
    
    Requires floor plan (configurational_measure: connectivity).
    
    Sprint 3 implementation notes — primary literature:
        Lynch, K. (1960). The image of the city. MIT Press.
        Hillier, B., & Hanson, J. (1984). The social logic of space. Cambridge University Press. https://doi.org/10.1017/CBO9780
        Hillier, B. (1996). Space is the machine: A configurational theory of architecture. Cambridge University Press.
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L29 (cognitive.legibility) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
