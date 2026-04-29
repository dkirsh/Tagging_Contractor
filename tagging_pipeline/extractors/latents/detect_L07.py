"""Sprint 2 stub for L07 (cognitive.choice_richness).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L07(image: "ndarray", segments: dict, depth: "ndarray | None" = None) -> dict:
    """Detect Choice Richness — availability of distinct zones/options..
    
    Construct: Choice Richness — availability of distinct zones/options.
    Canonical name: cognitive.choice_richness
    L-number: L07
    Subdomain: control_autonomy
    value_type: ordinal
    method_family: composite
    interaction_mode: mixed  |  valence_polarity: positive  |  temporal_window: snapshot
    
    Definition:
        The availability of distinct zones, niches, or behavioural-setting options
        within the depicted space, conceived within Barker's (1968) ecological-
        psychology framework of behavioural settings and within Kaplan and Kaplan's
        (1989) concept of *compatibility* (the match between an environment and a
        person's intended activities). Choice richness is high when the space
        affords multiple distinguishable a
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - affordance.zone_count
        - furniture.seating_type_variety
        - lighting.zone_count
        - scene.niche_diversity
        - scene.activity_setting_count
    
    Sprint 3 implementation notes — primary literature:
        Barker, R. G. (1968). Ecological psychology: Concepts and methods for studying the environment of human behavior. Stanfo
        Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
        Deci, E. L., & Ryan, R. M. (1985). Intrinsic motivation and self-determination in human behavior. Plenum.
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L07 (cognitive.choice_richness) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
