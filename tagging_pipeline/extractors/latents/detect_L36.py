"""Sprint 2 stub for L36 (cognitive.awe).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L36(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Vastness and need for cognitive accommodation — the architectural cathedral effect..
    
    Construct: Vastness and need for cognitive accommodation — the architectural cathedral effect.
    Canonical name: cognitive.awe
    L-number: L36
    Subdomain: social_signal
    value_type: ordinal
    method_family: vlm
    interaction_mode: unfocused  |  valence_polarity: positive  |  temporal_window: snapshot
    
    Definition:
        Awe/Grandeur is the perceiver's awe response to architectural vastness — the
        dual condition of perceived vastness and a corresponding need for cognitive
        accommodation that, in Keltner and Haidt's (2003) prototypical
        specification, defines awe as an emotion. The architectural correlate has
        been documented experimentally by Vartanian and colleagues (2015), whose
        work on the cathedral effect shows th
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - geometry.ceiling_height_proxy
        - geometry.vertical_aspect_ratio
        - geometry.proportional_canon_score
        - light.above_eye_level_illumination
        - compositional.vista_terminus_present
    
    Sprint 3 implementation notes — primary literature:
        Vartanian, O., Navarrete, G., Chatterjee, A., Fich, L. B., Leder, H., Modrono, C., Nadal, M., Rostrup, N., & Skov, M. (2
        Keltner, D., & Haidt, J. (2003). Approaching awe, a moral, spiritual, and aesthetic emotion. *Cognition and Emotion*, *1
        Bermudez, J., Krizaj, D., Lipschitz, D. L., Bueler, C. E., Rogowska, J., Yurgelun-Todd, D., & Nakamura, Y. (2017). Exter
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L36 (cognitive.awe) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
