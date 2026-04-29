"""L46 Hosting/Service Script Clarity — vlm-family reference extractor.

Construct: clarity of the service script (Goffman 1959 service performance;
Schank & Abelson 1977 scripts). Binary: latent_score in {0, 1}.

Algorithm:

    Prompt a Visual Language Model (CLIP, GPT-4V, Gemini Vision, Claude
    Vision, etc.) with the V2.6 indicator items as prompts; gather
    confidence scores for each item; aggregate.

    The five canonical PRS-style indicators for L46 (from V2.7 workbook):
      1. "There is an obvious place to ask for help."
      2. "I would know within 30 seconds where to go for service."
      3. "There is a clear staff/customer separation visible."
      4. "Wayfinding signage is present and clear."
      5. "The service script (queue, counter, cashier) is unambiguous."

    Aggregation: at least 3 of 5 items > 0.5 -> value=1; else 0.

    Without a VLM client, returns value=0 with confidence=0 and evidence
    indicating the dependency.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


PROMPTS = [
    "There is an obvious place to ask for help.",
    "I would know within 30 seconds where to go for service.",
    "There is a clear staff/customer separation visible.",
    "Wayfinding signage is present and clear.",
    "The service script (queue, counter, cashier) is unambiguous.",
]


class HostingScriptClarityExtractor(LatentExtractor):
    attribute_id = "L46"
    canonical_name = "social.hosting_script_clarity"
    method_family = "vlm"
    value_states = [0, 1]
    expected_upstream_observables = [
        "affordance.service_counter_present",
        "signage.role_text_presence",
        "queue.stanchion_count",
        "scene.staff_customer_segmentation",
    ]

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> ExtractorResult:
        if image is None:
            return ExtractorResult(value=0, confidence=0.0,
                                   evidence=["image unavailable"])
        if vlm_client is None:
            return ExtractorResult(
                value=0,
                confidence=0.0,
                evidence=["VLM client unavailable; L46 requires VLM (Sprint 4 will inject)"],
            )

        # Probe VLM with each indicator item
        scores = []
        evidence = []
        for prompt in PROMPTS:
            try:
                # API contract: vlm_client.score(image, statement) -> float in [0, 1]
                s = vlm_client.score(image, prompt)
                scores.append(s)
                evidence.append(f"  '{prompt[:50]}...' -> {s:.2f}")
            except Exception as e:
                scores.append(0.5)
                evidence.append(f"  '{prompt[:50]}...' -> 0.50 (VLM error: {e})")

        # Aggregate: ≥3 of 5 items at >0.5 indicates clear script
        n_strong = sum(1 for s in scores if s > 0.5)
        value = 1 if n_strong >= 3 else 0
        confidence = sum(scores) / len(scores) if scores else 0.0

        evidence.insert(0, f"L46 VLM aggregate: {n_strong}/5 items strong; value={value}")
        evidence.append("Goffman 1959 service-encounter performance; Schank & Abelson 1977 scripts")
        return ExtractorResult(value=value, confidence=confidence, evidence=evidence)
