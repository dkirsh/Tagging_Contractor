"""Sprint 2 stub for L03 (cognitive.visibility_control).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L03(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Visibility Control — ability to monitor environment without being monitored..
    
    Construct: Visibility Control — ability to monitor environment without being monitored.
    Canonical name: cognitive.visibility_control
    L-number: L03
    Subdomain: safety_threat
    value_type: ordinal
    method_family: vlm
    interaction_mode: unfocused  |  valence_polarity: neutral  |  temporal_window: snapshot
    
    Definition:
        The asymmetric-visibility construct from Appleton's (1975) prospect-refuge
        analysis: the viewer's perceived ability to monitor the surrounding
        environment from a vantage point without being readily monitored in turn.
        Hildebrand (1999) elaborated the construct in architectural settings,
        arguing that the most pleasurable spaces combine a prospect over a wider
        field with a refuge that limits the view
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - affordance.vantage_point
        - scene.sightline_extent
        - affordance.partition_height
        - affordance.mirror_presence
        - scene.openness_index
    
    Sprint 3 implementation notes — primary literature:
        Appleton, J. (1975). The experience of landscape. Wiley.
        Hildebrand, G. (1999). Origins of architectural pleasure. University of California Press.
        Stamps, A. E. (2005). Visual permeability, locomotive permeability, safety, and enclosure. Environment and Behavior, 37(
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L03 (cognitive.visibility_control) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
