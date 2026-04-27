"""L41-L58 social-interaction latent extractor stubs (Sprint 1).

This subpackage hosts one stub module per latent in the L41-L58 range.
Each ``detect_L##`` function reserves the runtime API surface that
Sprint 2 will fill in. The dispatch table ``LATENT_EXTRACTORS`` exposes
the stubs by ``attribute_id`` so that downstream consumers can wire
against the agreed-upon function signatures and output dict shapes
today.

Per panel disposition (28 April 2026, ``docs/sprint1_panel_disposition_2026-04-28.md``):

- L42, L43, L44, L48, L49, L50, L51, L56 must emit ``distance_zone_estimate``
  (one of intimate, personal_close, personal_far, social_close, social_far,
  public).
- L44, L48, L49, L52 must additionally emit
  ``(o_space_centroid_xy, o_space_radius_px, predominant_arrangement)``
  (predominant_arrangement is one of vis_a_vis, l_arrangement,
  side_by_side, semicircular, circular, none).
"""

from typing import Callable, Dict

from .detect_L41 import detect_L41
from .detect_L42 import detect_L42
from .detect_L43 import detect_L43
from .detect_L44 import detect_L44
from .detect_L45 import detect_L45
from .detect_L46 import detect_L46
from .detect_L47 import detect_L47
from .detect_L48 import detect_L48
from .detect_L49 import detect_L49
from .detect_L50 import detect_L50
from .detect_L51 import detect_L51
from .detect_L52 import detect_L52
from .detect_L53 import detect_L53
from .detect_L54 import detect_L54
from .detect_L55 import detect_L55
from .detect_L56 import detect_L56
from .detect_L57 import detect_L57
from .detect_L58 import detect_L58


# Dispatch table keyed by ``attribute_id`` (e.g., "L41" -> detect_L41).
# Sprint 2 implementations will replace the stubs without changing this
# mapping or the call signatures of the values.
LATENT_EXTRACTORS: Dict[str, Callable[..., dict]] = {
    "L41": detect_L41,
    "L42": detect_L42,
    "L43": detect_L43,
    "L44": detect_L44,
    "L45": detect_L45,
    "L46": detect_L46,
    "L47": detect_L47,
    "L48": detect_L48,
    "L49": detect_L49,
    "L50": detect_L50,
    "L51": detect_L51,
    "L52": detect_L52,
    "L53": detect_L53,
    "L54": detect_L54,
    "L55": detect_L55,
    "L56": detect_L56,
    "L57": detect_L57,
    "L58": detect_L58,
}


def get_extractor(attribute_id: str) -> Callable[..., dict]:
    """Return the extractor callable registered for ``attribute_id``.

    Args:
        attribute_id: registry attribute id, e.g. ``"L41"``.

    Returns:
        The ``detect_L##`` callable. Currently every callable raises
        ``NotImplementedError`` (Sprint 1 stubs); Sprint 2 implementations
        will replace the bodies without changing the dispatch contract.

    Raises:
        KeyError: when no extractor is registered for ``attribute_id``.
    """
    try:
        return LATENT_EXTRACTORS[attribute_id]
    except KeyError as exc:
        raise KeyError(
            f"No latent extractor registered for attribute_id={attribute_id!r}; "
            f"known ids: {sorted(LATENT_EXTRACTORS)}"
        ) from exc


__all__ = [
    "LATENT_EXTRACTORS",
    "get_extractor",
    "detect_L41",
    "detect_L42",
    "detect_L43",
    "detect_L44",
    "detect_L45",
    "detect_L46",
    "detect_L47",
    "detect_L48",
    "detect_L49",
    "detect_L50",
    "detect_L51",
    "detect_L52",
    "detect_L53",
    "detect_L54",
    "detect_L55",
    "detect_L56",
    "detect_L57",
    "detect_L58",
]
