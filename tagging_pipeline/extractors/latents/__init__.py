"""Latent extractor dispatch table for L01-L58.
Auto-generated; edit detect_L*.py files individually rather than this dispatcher.
"""
from __future__ import annotations

from .detect_L01 import detect_L01
from .detect_L02 import detect_L02
from .detect_L03 import detect_L03
from .detect_L04 import detect_L04
from .detect_L05 import detect_L05
from .detect_L06 import detect_L06
from .detect_L07 import detect_L07
from .detect_L08 import detect_L08
from .detect_L09 import detect_L09
from .detect_L10 import detect_L10
from .detect_L11 import detect_L11
from .detect_L12 import detect_L12
from .detect_L13 import detect_L13
from .detect_L14 import detect_L14
from .detect_L15 import detect_L15
from .detect_L16 import detect_L16
from .detect_L17 import detect_L17
from .detect_L18 import detect_L18
from .detect_L19 import detect_L19
from .detect_L20 import detect_L20
from .detect_L21 import detect_L21
from .detect_L22 import detect_L22
from .detect_L23 import detect_L23
from .detect_L24 import detect_L24
from .detect_L25 import detect_L25
from .detect_L26 import detect_L26
from .detect_L27 import detect_L27
from .detect_L28 import detect_L28
from .detect_L29 import detect_L29
from .detect_L30 import detect_L30
from .detect_L31 import detect_L31
from .detect_L32 import detect_L32
from .detect_L33 import detect_L33
from .detect_L34 import detect_L34
from .detect_L35 import detect_L35
from .detect_L36 import detect_L36
from .detect_L37 import detect_L37
from .detect_L38 import detect_L38
from .detect_L39 import detect_L39
from .detect_L40 import detect_L40
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

LATENT_EXTRACTORS = {
    "L01": detect_L01,
    "L02": detect_L02,
    "L03": detect_L03,
    "L04": detect_L04,
    "L05": detect_L05,
    "L06": detect_L06,
    "L07": detect_L07,
    "L08": detect_L08,
    "L09": detect_L09,
    "L10": detect_L10,
    "L11": detect_L11,
    "L12": detect_L12,
    "L13": detect_L13,
    "L14": detect_L14,
    "L15": detect_L15,
    "L16": detect_L16,
    "L17": detect_L17,
    "L18": detect_L18,
    "L19": detect_L19,
    "L20": detect_L20,
    "L21": detect_L21,
    "L22": detect_L22,
    "L23": detect_L23,
    "L24": detect_L24,
    "L25": detect_L25,
    "L26": detect_L26,
    "L27": detect_L27,
    "L28": detect_L28,
    "L29": detect_L29,
    "L30": detect_L30,
    "L31": detect_L31,
    "L32": detect_L32,
    "L33": detect_L33,
    "L34": detect_L34,
    "L35": detect_L35,
    "L36": detect_L36,
    "L37": detect_L37,
    "L38": detect_L38,
    "L39": detect_L39,
    "L40": detect_L40,
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

def get_extractor(attribute_id: str):
    """Look up the detector function by L-id."""
    return LATENT_EXTRACTORS.get(attribute_id)
