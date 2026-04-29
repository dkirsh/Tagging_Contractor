"""Sprint 2 stub for L04 (cognitive.surveillance_pressure).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L04(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Surveillance Pressure — feeling watched/judged..
    
    Construct: Surveillance Pressure — feeling watched/judged.
    Canonical name: cognitive.surveillance_pressure
    L-number: L04
    Subdomain: safety_threat
    value_type: ordinal
    method_family: vlm
    interaction_mode: unfocused  |  valence_polarity: negative  |  temporal_window: snapshot
    
    Definition:
        The viewer's anticipated experience of being watched, evaluated, or judged
        in the depicted space, drawing theoretically on Foucault's (1977) panopticon
        analysis of architectural surveillance and on Zajonc's (1965) social-
        facilitation work showing that the mere presence (or implication) of an
        audience changes performance and arousal. Surveillance pressure is the
        affective complement of low visibili
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - object.camera_presence
        - scene.openplan_exposure
        - lighting.spotlight_pattern
        - scene.gaze_lines
        - scene.elevated_platform_focus
    
    Sprint 3 implementation notes — primary literature:
        Foucault, M. (1977). Discipline and punish: The birth of the prison (A. Sheridan, Trans.). Pantheon Books.
        Zajonc, R. B. (1965). Social facilitation. Science, 149(3681), 269–274. https://doi.org/10.1126/science.149.3681.269
        Ulrich, R. S. (1991). Effects of interior design on wellness: Theory and recent scientific research. Journal of Health C
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L04 (cognitive.surveillance_pressure) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
