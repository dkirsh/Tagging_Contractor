"""Sprint 2 stub for L22 (cognitive.mystery).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L22(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Promise of further information beyond the visible vantage — invitation to explore..
    
    Construct: Promise of further information beyond the visible vantage — invitation to explore.
    Canonical name: cognitive.mystery
    L-number: L22
    Subdomain: aesthetic_affect
    value_type: ordinal
    method_family: vlm
    interaction_mode: mixed  |  valence_polarity: mixed  |  temporal_window: snapshot
    
    Definition:
        Mystery — in the Kaplan & Kaplan (1989) sense — names the degree to which a
        scene promises information beyond what is presently visible, such that an
        observer would learn more by moving deeper into it. It is the inferred-
        environment cell of the Preference Matrix, paired with legibility as the
        higher-order pair, and is operationalised by partial occlusion (a wall edge
        that hides part of a room beyo
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - geometry.partial_occlusion_score
        - affordance.curving_path_present
        - affordance.deflected_sightline_count
        - appearance.luminance_gradient_into_depth
        - geometry.foreground_partial_screen
    
    Sprint 3 implementation notes — primary literature:
        Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
        Berlyne, D. E. (1971). Aesthetics and psychobiology. Appleton-Century-Crofts.
        Kaplan, S. (1987). Aesthetics, affect, and cognition: Environmental preference from an evolutionary perspective. Environ
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L22 (cognitive.mystery) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
