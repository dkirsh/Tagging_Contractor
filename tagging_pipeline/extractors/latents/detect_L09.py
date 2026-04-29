"""Sprint 2 stub for L09 (cognitive.rule_tightness).
Sprint 3 will implement the body. This file reserves the dispatch slot.
"""
from __future__ import annotations


def detect_L09(image: "ndarray", segments: dict, depth: "ndarray | None" = None) -> dict:
    """Detect Rule Tightness — norm inference: strict vs permissive..
    
    Construct: Rule Tightness — norm inference: strict vs permissive.
    Canonical name: cognitive.rule_tightness
    L-number: L09
    Subdomain: control_autonomy
    value_type: ordinal
    method_family: composite
    interaction_mode: mixed  |  valence_polarity: neutral  |  temporal_window: snapshot
    
    Definition:
        The viewer's inference about whether the depicted space is governed by
        strict or permissive norms — whether what one does, says, wears, and touches
        in this space will be regulated by enforceable expectations or by loose
        tolerance. The construct draws on Gelfand et al.'s (2011) cross-national
        tight/loose taxonomy, on Goffman's (1959) frontstage/backstage analysis of
        behavioural region, and on Ciald
    
    Expected output dict shape:
        {"value": int (0-4), "confidence": float (0-1), "evidence": list[str]}
    
    Expected upstream observables (5):
        - wayfinding.prohibitive_signage
        - scene.formality_cue
        - affordance.barrier_density
        - object.uniform_indicator
        - scene.layout_formality
    
    Sprint 3 implementation notes — primary literature:
        Gelfand, M. J., Raver, J. L., Nishii, L., Leslie, L. M., Lun, J., Lim, B. C., … Yamaguchi, S. (2011). Differences betwee
        Goffman, E. (1959). The presentation of self in everyday life. Anchor.
        Cialdini, R. B., Reno, R. R., & Kallgren, C. A. (1990). A focus theory of normative conduct: Recycling the concept of no
    
    NOT YET IMPLEMENTED — Sprint 3 will populate this stub.
    """
    raise NotImplementedError(
        f"Sprint 3: detector for L09 (cognitive.rule_tightness) is not yet implemented. "
        "See docstring for the required upstream observables and output shape."
    )
