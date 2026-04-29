"""Sprint 2 stub for L40 (cognitive.playfulness).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L40(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Ludic, informal tone — invitation to non-serious engagement..
    
    Construct: Ludic, informal tone — invitation to non-serious engagement.
    Canonical name: cognitive.playfulness
    L-number: L40
    Subdomain: familiarity_novelty
    value_type: ordinal
    method_family: vlm
    interaction_mode: mixed  |  valence_polarity: positive  |  temporal_window: snapshot
    
    Definition:
        Playfulness is the perceiver's inference that the space invites non-serious,
        ludic engagement — a tonal register where play, exploration, humour, and
        creative re-purposing are welcomed rather than penalised. Following
        Bateson's (1955) *play frame* analysis, playfulness is metacommunicative:
        the space signals 'this is play' and thereby suspends the normal serious
        construal of activity within it. Fo
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - colour.bright_palette_score
        - forms.whimsical_geometry_score
        - furniture.casual_seating_score
        - material.soft_furnishing_score
        - signage.ludic_tone_score
    
    Sprint 3 implementation notes — primary literature:
        Bateson, G. (1955). A theory of play and fantasy. *Psychiatric Research Reports*, *2*, 39-51. (Reprinted in *Steps to an
        Bekoff, M. (2014). The significance of ethological studies: Playing and peeing. In M. Bekoff, *Why dogs hump and bees ge
        Sutton-Smith, B. (1997). *The ambiguity of play*. Harvard University Press.
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L40 (cognitive.playfulness) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
