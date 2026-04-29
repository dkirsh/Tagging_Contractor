"""Sprint 2 stub for L25 (cognitive.coziness).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L25(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Inviting softness, warmth, and enclosure that supports lingering..
    
    Construct: Inviting softness, warmth, and enclosure that supports lingering.
    Canonical name: cognitive.coziness
    L-number: L25
    Subdomain: aesthetic_affect
    value_type: ordinal
    method_family: vlm
    interaction_mode: mixed  |  valence_polarity: positive  |  temporal_window: snapshot
    
    Definition:
        Coziness names the cluster of perceptible properties that mark a space as
        inviting prolonged, low-arousal, positively-valenced occupancy: textiles and
        soft surfaces, warm-colour-temperature lighting, partial enclosure (a space
        within a space), localised pools of warm light against a darker ambient, and
        soft seating arrangements. The construct draws on Park & MacInnis's (2006)
        account of feelings a
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - appearance.textile_presence
        - appearance.warm_lighting_index
        - geometry.partial_enclosure_score
        - appearance.soft_seating_present
        - appearance.localised_warm_light_pools
    
    Sprint 3 implementation notes — primary literature:
        Park, C. W., & MacInnis, D. J. (2006). What's in and what's out: Questions on the boundaries of the attitude construct. 
        Linnet, J. T. (2011). Money can't buy me hygge: Danish middle-class consumption, egalitarianism, and the sanctity of inn
        Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L25 (cognitive.coziness) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
