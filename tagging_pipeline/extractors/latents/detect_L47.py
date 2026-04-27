"""Sprint 1 stub for L47 — Turn-Taking and Queue Support.

Registry canonical name: ``social.queue_support``
V2.6 Tier: 2
Method family: vlm
Value type: ordinal (Likert 0-4)

This module reserves the API surface; real extraction lands in Sprint 2.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-only for type hints
    from numpy import ndarray  # noqa: F401

    class VLMClient:  # noqa: D401 - placeholder class for type hint only
        """Forward-declared placeholder for the visual-language-model client."""


def detect_L47(
    image: "ndarray",
    vlm_client: "VLMClient | None" = None,
) -> dict:
    """Score Turn-Taking & Queue Support (L47) for the supplied scene.

    L47 measures the *spatial scaffolding* a setting publishes for
    sequential service interactions (Mann, 1969; Larson, 1987;
    Goffman, 1963, pp. 23-24 on withs and singles). The extractor is
    a VLM that aggregates three sub-cues: defined waiting line, single
    point of service, and clear next-position cue. A critical 2D
    failure mode is mistaking *stored* stanchions for deployed queue
    infrastructure — the prompt must penalise apparent storage.

    Args:
        image: H x W x 3 RGB ndarray.
        vlm_client: optional VLM client. When ``None`` the Sprint 2
            implementation should fall back to a default endpoint or
            raise a configuration error.

    Expected upstream observables (per ``L47.md`` Engineer pass):
        - ``affordance.stanchion_count``
        - ``affordance.floor_marking_present``
        - ``furniture.counter_count``
        - ``signage.numeric_display_present``
        - ``signage.next_customer_marker``
        - ``signage.queue_directional_marker``
        - ``floor_marking.text_present``

    Returns:
        dict shaped as::

            {
                "value": int,            # 0-4 Likert
                "confidence": float,     # [0.0, 1.0]
                "evidence": list[str],
            }

        L47 is not in the panel-mandated lists for ``distance_zone_estimate``
        or F-formation geometry, so no extra fields are required.

    Sprint 2 implementation notes:
        Primary literature: Mann (1969), "Queue culture: The waiting
        line as a social system"; Larson (1987), "Perspectives on
        queues: Social justice and the psychology of queueing";
        Goffman (1963, pp. 23-24); Whyte (1980) on plaza queue
        formation. Sprint 2 BN modelling may benefit from a noisy-AND
        of the three sub-cues rather than a 5-state CPT.
    """
    raise NotImplementedError(
        "detect_L47 (social.queue_support) is a Sprint 1 stub; "
        "Sprint 2 will implement the VLM-based queue-scaffolding scorer."
    )
