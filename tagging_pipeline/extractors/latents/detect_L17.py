"""Sprint 2 stub for L17 (cognitive.restorativeness).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L17(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Being-away, fascination, coherence, compatibility..
    
    Construct: Being-away, fascination, coherence, compatibility.
    Canonical name: cognitive.restorativeness
    L-number: L17
    Subdomain: restoration
    value_type: ordinal
    method_family: vlm
    interaction_mode: mixed  |  valence_polarity: positive  |  temporal_window: snapshot
    
    Definition:
        The integrated appraised affordance of the depicted space for psychological
        restoration per Kaplan and Kaplan's (1989) Attention Restoration Theory
        (ART). The construct integrates four sub-components: being-away
        (psychological distance from demands; L18), fascination (effortless
        attention capture; L19), coherence (the scene's extent and self-
        consistency), and compatibility (fit between space and i
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - scene.greenery_presence
        - lighting.daylight_present
        - geometry.openness_index
        - scene.calm_visual_field_indicator
        - scene.retreat_nook_present
    
    Sprint 3 implementation notes — primary literature:
        Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
        Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. Journal of Environmental Psychol
        Hartig, T., Korpela, K., Evans, G. W., & Garling, T. (1997). A measure of restorative quality in environments. Scandinav
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L17 (cognitive.restorativeness) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
