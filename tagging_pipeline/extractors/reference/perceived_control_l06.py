"""L06 Perceived Control — composite-family Sprint-4 reference extractor.

Construct: Sense of agency over the conditions of the depicted space
(Bandura 1977 self-efficacy; Karasek 1979 job demand-control; Veitch &
Gifford 1996 environmental control). Subdomain: control_autonomy.

Algorithm:

    Inputs: segmented image with masks for `dimmer`, `thermostat`, `blind`
    (visible-control objects) and `furniture_movable_indicator` plus
    `furniture_fixed_indicator`.

    1. visible_controls = count of pixels in (dimmer | thermostat | blind),
       normalised by image area, capped at a saturation point of 0.05
       (a small fraction of pixels saturates the signal).
    2. movable_furniture_fraction = movable / (movable + fixed) area.
    3. composite = 0.55 * normalized_controls + 0.45 * movable_fraction
       (weights from Veitch-Gifford analysis: control affordances slightly
       dominate but movable furniture contributes; a sensitivity check is
       in the Sprint-5 panel queue).
    4. Likert bin to [0..4].

Citations:
    Bandura, A. (1977). Self-efficacy: Toward a unifying theory of
        behavioral change. Psychological Review, 84(2), 191-215.
    Karasek, R. A. (1979). Job demands, job decision latitude, and mental
        strain: Implications for job redesign. Administrative Science
        Quarterly, 24(2), 285-308.
    Veitch, J. A., & Gifford, R. (1996). Choice, perceived control, and
        performance decrements in the physical environment. Journal of
        Environmental Psychology, 16(3), 269-276.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


CONTROL_OBJECTS = ("dimmer", "thermostat", "blind", "switch", "control_panel")


class PerceivedControlExtractor(LatentExtractor):
    attribute_id = "L06"
    canonical_name = "cognitive.perceived_control"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "object.dimmer_visible",
        "object.thermostat_visible",
        "object.blind_visible",
        "furniture.movable_indicator",
        "affordance.zone_count",
    ]

    W_CONTROLS = 0.55
    W_MOVABLE = 0.45
    SATURATION_FRACTION = 0.05  # >5% of pixels saturates the controls signal

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
                evidence=["L06 perceived-control: no segments/image; "
                          "neutral default 2."],
            )

        evidence: list[str] = []

        # ── Signal 1: visible controls
        controls_signal = 0.0
        try:
            controls_pixels = 0.0
            total_pixels = 0.0
            if segments:
                for obj in CONTROL_OBJECTS:
                    if obj in segments:
                        m = segments[obj]
                        controls_pixels += float(getattr(m, "sum", lambda: sum(1 for x in m if x))())
                        if total_pixels == 0:
                            total_pixels = float(getattr(m, "size", None) or max(1, len(m)))
                if total_pixels == 0:
                    total_pixels = 1.0
                fraction = controls_pixels / total_pixels
                controls_signal = min(1.0, fraction / self.SATURATION_FRACTION)
                evidence.append(
                    f"visible_controls_fraction={fraction:.4f} -> "
                    f"signal={controls_signal:.3f} (saturated at "
                    f"{self.SATURATION_FRACTION:.3f})"
                )
            else:
                evidence.append("no segments; controls signal=0")
        except Exception as e:
            evidence.append(f"controls fallback ({e}); 0")

        # ── Signal 2: movable furniture fraction
        movable_signal = 0.0
        try:
            if segments and "furniture_movable_indicator" in segments:
                mv = segments["furniture_movable_indicator"]
                mv_count = float(getattr(mv, "sum", lambda: sum(1 for x in mv if x))())
                fx = segments.get("furniture_fixed_indicator")
                fx_count = float(getattr(fx, "sum", lambda: sum(1 for x in fx if x))()) if fx is not None else 0.0
                denom = mv_count + fx_count
                if denom > 0:
                    movable_signal = mv_count / denom
                evidence.append(
                    f"movable_fraction = {mv_count:.0f} / "
                    f"({mv_count:.0f}+{fx_count:.0f}) = {movable_signal:.3f}"
                )
            else:
                evidence.append("no furniture_movable_indicator; movable=0")
        except Exception as e:
            evidence.append(f"movable fallback ({e}); 0")

        score = self.W_CONTROLS * controls_signal + self.W_MOVABLE * movable_signal
        if score >= 0.80: value = 4
        elif score >= 0.60: value = 3
        elif score >= 0.40: value = 2
        elif score >= 0.20: value = 1
        else: value = 0

        evidence.append(
            f"composite control = {self.W_CONTROLS}*controls "
            f"({controls_signal:.3f}) + {self.W_MOVABLE}*movable "
            f"({movable_signal:.3f}) = {score:.3f} -> Likert {value}"
        )
        evidence.append("Bandura 1977 self-efficacy; Karasek 1979 demand-control; Veitch & Gifford 1996.")

        signals_present = sum([
            1 if controls_signal > 0 else 0,
            1 if movable_signal > 0 else 0,
        ])
        confidence = 0.3 + 0.3 * signals_present
        return ExtractorResult(value=value, confidence=confidence, evidence=evidence)
