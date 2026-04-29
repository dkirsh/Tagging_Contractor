"""Sprint 2 stub for L18 (cognitive.being_away).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L18(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Psychological distance from demands..
    
    Construct: Psychological distance from demands.
    Canonical name: cognitive.being_away
    L-number: L18
    Subdomain: restoration
    value_type: ordinal
    method_family: vlm
    interaction_mode: mixed  |  valence_polarity: positive  |  temporal_window: snapshot
    
    Definition:
        The appraised psychological distance the depicted space affords from
        everyday demands - the 'I can be elsewhere here' affordance that is one of
        the four sub-components of Kaplan and Kaplan's (1989) Attention Restoration
        Theory. Operationalised through cues that predict demand-decoupling: visible
        thresholds (doorways, gates, transitions) that mark the depicted space as
        distinct from a demand-laden
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (4):
        - scene.threshold_present
        - geometry.separation_from_workspace
        - scene.natural_view_present
        - scene.demand_artefact_absent
    
    Sprint 3 implementation notes — primary literature:
        Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
        Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. Journal of Environmental Psychol
        Hartig, T., Korpela, K., Evans, G. W., & Garling, T. (1997). A measure of restorative quality in environments. Scandinav
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L18 (cognitive.being_away) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
