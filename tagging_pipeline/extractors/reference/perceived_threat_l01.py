"""L01 Perceived Threat — composite-family Sprint-4 reference extractor.

Construct: Appraisal of danger/attack likelihood in a depicted setting
(Appleton 1975 prospect-refuge; Fisher & Nasar 1992; Stamps 2014).
Subdomain: safety_threat.

Sprint-2 registry method_family = "vlm"; Sprint-4 reference implementation
uses the *composite* family (concealment-corner-count + dim-corner-fraction).
The composite is the ground-truth proxy; a future VLM read can be added as a
cross-check, but the composite is the algorithmic anchor for this Sprint-4
working extractor.

Algorithm:

    Inputs: segmented image with semantic masks for `corners`,
    `concealment_pockets`, `lighting_dim_zones`.
    1. concealment_corner_count = |corner-pixels in concealment_pockets|
       normalised by total pixel count to a [0, 1] proxy.
    2. dim_corner_fraction = |dim corner-pixels| / |all corner-pixels|.
    3. composite_threat = 0.7 * concealment_corner_count + 0.3 * dim_corner_fraction
    4. Likert bin (Stamps 2014 prospect-refuge five-point):
         [0.00, 0.20) -> 0,  [0.20, 0.40) -> 1, [0.40, 0.60) -> 2,
         [0.60, 0.80) -> 3, [0.80, 1.00] -> 4

Pure-Python fallback: if segments unavailable, computes a neutral 2 with
zero confidence and an explanatory evidence string (Sprint-4 contract).

Citations:
    Appleton, J. (1975). The experience of landscape. Wiley.
    Fisher, B. S., & Nasar, J. L. (1992). Fear of crime in relation to three
        exterior site features: Prospect, refuge, and escape. Environment
        and Behavior, 24(1), 35-65. https://doi.org/10.1177/0013916592241002
    Stamps, A. E. (2014). Designing for refuge and prospect. Architectural
        Science Review, 57(1), 57-67.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


class PerceivedThreatExtractor(LatentExtractor):
    attribute_id = "L01"
    canonical_name = "cognitive.perceived_threat"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "lighting.shadow_density",
        "lighting.corner_illumination",
        "affordance.concealment_pockets",
        "affordance.blind_corner_count",
        "scene.passage_isolation",
    ]

    # Stamps (2014) panel: prospect-refuge weights from Appleton-line tradition
    W_CONCEALMENT = 0.7
    W_DIM_LIGHT = 0.3

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> ExtractorResult:
        if segments is None and image is None:
            return ExtractorResult(
                value=2, confidence=0.0,
                evidence=["L01 perceived-threat: no image or segments available; "
                          "neutral default 2 returned (Sprint-4 contract)."],
            )

        evidence: list[str] = []

        # ── Signal 1: concealment-corner count
        concealment_proxy = 0.0
        try:
            if segments and "concealment_pockets" in segments:
                cp = segments["concealment_pockets"]
                # Mask object: count true pixels via .sum() if available; else len-of-truthy
                cp_count = float(getattr(cp, "sum", lambda: sum(1 for x in cp if x))())
                total = float(getattr(cp, "size", None) or max(1, len(cp)))
                concealment_proxy = min(1.0, cp_count / total)
                evidence.append(f"concealment_pockets fraction={concealment_proxy:.3f}")
            elif segments and "corners" in segments:
                # Fall back to corner-count alone
                cs = segments["corners"]
                ccount = float(getattr(cs, "sum", lambda: sum(1 for x in cs if x))())
                total = float(getattr(cs, "size", None) or max(1, len(cs)))
                concealment_proxy = min(1.0, ccount / total)
                evidence.append(f"corner-only proxy={concealment_proxy:.3f}")
            else:
                evidence.append("no concealment/corner segment; concealment=0")
        except Exception as e:
            evidence.append(f"concealment compute fallback ({e}); 0")

        # ── Signal 2: dim-corner fraction
        dim_fraction = 0.0
        try:
            if segments and "lighting_dim_zones" in segments and "corners" in segments:
                dz = segments["lighting_dim_zones"]
                cs = segments["corners"]
                # dim-corner = AND mask
                if hasattr(dz, "__and__") and hasattr(cs, "__and__"):
                    dim_corner = dz & cs
                    dim_count = float(getattr(dim_corner, "sum", lambda: 0)())
                else:
                    # Iterable fallback
                    dim_count = float(sum(1 for d, c in zip(dz, cs) if d and c))
                corner_count = float(getattr(cs, "sum", lambda: sum(1 for x in cs if x))())
                if corner_count > 0:
                    dim_fraction = min(1.0, dim_count / corner_count)
                evidence.append(f"dim_corner_fraction={dim_fraction:.3f}")
            elif segments and "lighting_dim_zones" in segments:
                dz = segments["lighting_dim_zones"]
                d_count = float(getattr(dz, "sum", lambda: sum(1 for x in dz if x))())
                total = float(getattr(dz, "size", None) or max(1, len(dz)))
                dim_fraction = min(1.0, d_count / total)
                evidence.append(f"dim_zone_fraction (no corner mask)={dim_fraction:.3f}")
            else:
                evidence.append("no dim/corner masks; dim=0")
        except Exception as e:
            evidence.append(f"dim compute fallback ({e}); 0")

        score = self.W_CONCEALMENT * concealment_proxy + self.W_DIM_LIGHT * dim_fraction
        if score >= 0.80: value = 4
        elif score >= 0.60: value = 3
        elif score >= 0.40: value = 2
        elif score >= 0.20: value = 1
        else: value = 0

        evidence.append(
            f"composite_threat = {self.W_CONCEALMENT}*concealment "
            f"({concealment_proxy:.3f}) + {self.W_DIM_LIGHT}*dim "
            f"({dim_fraction:.3f}) = {score:.3f} -> Likert {value}"
        )
        evidence.append(
            "Stamps 2014 prospect-refuge five-point; "
            "Appleton 1975; Fisher & Nasar 1992 fear-of-crime."
        )
        # Confidence reflects how many signals were observable
        signals_present = sum([
            1 if concealment_proxy > 0 else 0,
            1 if dim_fraction > 0 else 0,
        ])
        confidence = 0.3 + 0.3 * signals_present  # 0.3..0.9
        return ExtractorResult(value=value, confidence=confidence, evidence=evidence)
