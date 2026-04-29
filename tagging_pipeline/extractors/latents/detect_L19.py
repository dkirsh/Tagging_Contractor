"""Sprint 2 stub for L19 (cognitive.soft_fascination).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L19(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Effortless attention capture (non-demanding)..
    
    Construct: Effortless attention capture (non-demanding).
    Canonical name: cognitive.soft_fascination
    L-number: L19
    Subdomain: restoration
    value_type: ordinal
    method_family: vlm
    interaction_mode: mixed  |  valence_polarity: positive  |  temporal_window: sustained
    
    Definition:
        The appraised affordance for effortless, non-demanding attention capture per
        Kaplan and Kaplan's (1989) Attention Restoration Theory. Soft fascination is
        involuntary attention drawn to gentle, sub-demanding stimuli - moving water,
        swaying leaves, fractal natural patterns, drifting clouds - that holds the
        mind without requiring directed effort, allowing the directed-attention
        system to recover. Ope
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - scene.water_feature_present
        - scene.gentle_motion_indicator
        - texture.fractal_pattern_strength
        - scene.natural_pattern_density
        - scene.gentle_complexity_index
    
    Sprint 3 implementation notes — primary literature:
        Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
        Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. Journal of Environmental Psychol
        Berman, M. G., Jonides, J., & Kaplan, S. (2008). The cognitive benefits of interacting with nature. Psychological Scienc
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L19 (cognitive.soft_fascination) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
