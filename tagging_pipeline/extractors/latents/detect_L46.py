"""Sprint 1 stub for L46 — Hosting/Service Script Clarity.

Registry canonical name: ``social.hosting_script_clarity``
V2.6 Tier: 1
Method family: vlm
Value type: latent_score (binary 0/1)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401

    class VLMClient:  # noqa: D401 - placeholder class for type hint only
        """Forward-declared placeholder for the visual-language-model client."""


def detect_L46(
    image: "ndarray",
    vlm_client: "VLMClient | None" = None,
) -> dict:
    """Score Hosting/Service Script Clarity (L46) for the supplied scene.

    L46 is the binary judgment of whether a service-encounter setting
    legibly publishes role asymmetry and the help-seeking locus
    (Goffman, 1959; Schank and Abelson, 1977). Because no clean
    geometric primitive captures script clarity, the extractor is a
    visual-language-model composition over signage OCR, attire
    classification, and furniture-class evidence.

    Args:
        image: H x W x 3 RGB ndarray.
        vlm_client: optional visual-language-model client. When ``None``
            the Sprint 2 implementation should fall back to a default
            registered VLM endpoint or raise a configuration error.

    Expected upstream observables (per ``L46.md`` Engineer pass):
        - ``furniture.service_counter_presence``
        - ``signage.service_role_text_presence``
        - ``person.staff_attire_indicator``
        - ``furniture.queue_infrastructure_presence``

    Returns:
        dict shaped as::

            {
                "value": int,            # 0 or 1 (binary)
                "confidence": float,     # [0.0, 1.0]
                "evidence": list[str],
            }

        L46 is not in the panel-mandated lists for ``distance_zone_estimate``
        or F-formation geometry, so no extra fields are required.

    Sprint 2 implementation notes:
        Primary literature: Goffman (1959), *The presentation of self in
        everyday life*, ch. 3 on front/back-region performance; Schank
        and Abelson (1977) on scripts; Hall (1966) for the cross-
        cultural calibration warning (desk-less Japanese omakase, etc.).
        The VLM prompt template MUST list non-Western desk-less script
        exemplars to avoid Western-calibration bias. ``notes.bn_notes``
        flags L46 for Sprint-2 ranking-theoretic recoding (Spohn, 2012,
        §5.3).
    """
    raise NotImplementedError(
        "detect_L46 (social.hosting_script_clarity) is a Sprint 1 stub; "
        "Sprint 2 will implement the VLM-based binary scorer."
    )
