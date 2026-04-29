"""Sprint 2 stub for L20 (cognitive.compatibility).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L20(image: "ndarray", vlm_client: "VLMClient | None" = None) -> dict:
    """Detect Fit between space affordances and intended activity..
    
    Construct: Fit between space affordances and intended activity.
    Canonical name: cognitive.compatibility
    L-number: L20
    Subdomain: restoration
    value_type: ordinal
    method_family: vlm
    interaction_mode: mixed  |  valence_polarity: positive  |  temporal_window: sustained
    
    Definition:
        The appraised fit between the depicted space's affordances and the
        occupant's intended activity - the 'this place supports what I want to do
        here' dimension that is one of the four sub-components of Kaplan and
        Kaplan's (1989) Attention Restoration Theory. Operationalised through cues
        that predict affordance-activity match: presence of task-relevant equipment
        (a desk and chair for work, a mat and q
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - furniture.task_relevant_equipment_present
        - ergonomics.posture_support_index
        - geometry.layout_task_alignment
        - scene.intended_activity_inferred
        - scene.task_obstruction_absent
    
    Sprint 3 implementation notes — primary literature:
        Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological perspective. Cambridge University Press.
        Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. Journal of Environmental Psychol
        Hartig, T., Korpela, K., Evans, G. W., & Garling, T. (1997). A measure of restorative quality in environments. Scandinav
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L20 (cognitive.compatibility) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
