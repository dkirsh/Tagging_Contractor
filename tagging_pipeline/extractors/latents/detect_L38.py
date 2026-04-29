"""Sprint 2 stub for L38 (cognitive.novelty).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L38(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Unexpectedness and distinctiveness — the encountered-information dual of familiarity..
    
    Construct: Unexpectedness and distinctiveness — the encountered-information dual of familiarity.
    Canonical name: cognitive.novelty
    L-number: L38
    Subdomain: familiarity_novelty
    value_type: ordinal
    method_family: vlm
    interaction_mode: unfocused  |  valence_polarity: mixed  |  temporal_window: snapshot
    
    Definition:
        Novelty is the perceiver's appraisal that the space is unexpected, atypical,
        or schema-violating relative to their prior corpus of similar settings.
        Following Berlyne (1971), novelty is one of the *collative variables* —
        properties that emerge from comparison between the stimulus and prior
        exposure rather than residing in the stimulus alone — and is paired with
        complexity, surprise, and incongruit
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (4):
        - objects.unusual_fixture_class_presence
        - material.novel_combination_score
        - layout.graph_distance_from_centroid
        - style.corpus_distance_score
    
    Sprint 3 implementation notes — primary literature:
        Berlyne, D. E. (1971). *Aesthetics and psychobiology*. Appleton-Century-Crofts.
        Silvia, P. J. (2005). What is interesting? Exploring the appraisal structure of interest. *Emotion*, *5*(1), 89-102. htt
        Berlyne, D. E. (1960). *Conflict, arousal, and curiosity*. McGraw-Hill. https://doi.org/10.1037/11164-000
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L38 (cognitive.novelty) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
