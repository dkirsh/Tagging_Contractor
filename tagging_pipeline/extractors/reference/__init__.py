"""Sprint 3 reference extractor implementations.

Five working extractors across method families:

    L29 LegibilityExtractor       (geometry — isovist / axial-integration based)
    L42 InteractionalVisibilityExtractor  (geometry — isovist mean-depth)
    L21 CoherenceOrderExtractor   (composite — orientation entropy + colour palette consistency)
    L46 HostingScriptClarityExtractor  (vlm — VLM prompted with PRS-style indicator items)
    L17 RestorativenessExtractor  (vlm — Hartig PRS items, structured-factor parent)

The implementations are real algorithms but use pure-Python / minimal-dependency
fallbacks where heavy ML libraries would normally be required (e.g. CLIP,
SAM segmentation models). The intent is pedagogical: students see the shape
of a working extractor and can replace the simplified inner loops with
production CV models in Sprint 4.
"""

from .legibility_l29 import LegibilityExtractor
from .interactional_visibility_l42 import InteractionalVisibilityExtractor
from .coherence_order_l21 import CoherenceOrderExtractor
from .hosting_script_clarity_l46 import HostingScriptClarityExtractor
from .restorativeness_l17 import RestorativenessExtractor

REFERENCE_EXTRACTORS = {
    "L29": LegibilityExtractor,
    "L42": InteractionalVisibilityExtractor,
    "L21": CoherenceOrderExtractor,
    "L46": HostingScriptClarityExtractor,
    "L17": RestorativenessExtractor,
}
