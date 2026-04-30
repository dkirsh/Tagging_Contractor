"""L14 Crowding Pressure — composite-family Sprint-4 reference extractor.

Construct: Appraised proxemic compression imposed on an occupant by density
and layout (Stokols 1972 social vs spatial density distinction; Hall 1966
proxemics; Evans 1979 crowding stress). Subdomain: crowding_density.

Algorithm:

    Inputs: segments with chair/seat instances, person/occupant masks, floor
    or open-area mask. Optional sightline geometry.

    1. person_density_proxy = chair_instance_count / floor_area_proxy
       — proxy for occupant density when persons are not directly counted
       (chairs are a stable proxy; Stokols 1972).
    2. sightline_blocking = fraction of sightlines blocked by other
       occupants/objects in the foreground (estimated from segment overlap
       with central viewing rays).
    3. composite = 0.6 * normalized_density + 0.4 * sightline_blocking
       Density normalised by 1.0 chair per 2.5 m^2 — Hall personal-distance
       threshold (a denser packing saturates the signal).
    4. Likert bin to [0..4].

Citations:
    Stokols, D. (1972). On the distinction between density and crowding.
        Psychological Review, 79(3), 275-277.
    Hall, E. T. (1966). The hidden dimension. Doubleday.
    Evans, G. W. (1979). Behavioral and physiological consequences of
        crowding in humans. JASP, 9(1), 27-46.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, ExtractorResult


CHAIR_OBJECTS = ("chair", "seat", "stool", "bench")
DENSITY_SATURATION = 1.0 / 2.5  # 1 chair per 2.5 m^2 saturates


class CrowdingPressureExtractor(LatentExtractor):
    attribute_id = "L14"
    canonical_name = "cognitive.crowding_pressure"
    method_family = "composite"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "scene.occupant_count",
        "scene.seat_to_floor_ratio",
        "geometry.aisle_width",
        "geometry.queue_indicator",
        "scene.persons_per_unit_area",
    ]

    W_DENSITY = 0.6
    W_SIGHTLINE = 0.4

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
                evidence=["L14 crowding-pressure: no segments/image; default 2."],
            )

        evidence: list[str] = []

        # ── Signal 1: person/chair density proxy
        density_signal = 0.0
        try:
            chair_count = 0
            if segments:
                for obj in CHAIR_OBJECTS:
                    if obj in segments:
                        m = segments[obj]
                        instances = getattr(m, "instance_count", None)
                        if instances is not None:
                            chair_count += int(instances)
                        else:
                            # Fall back to mask-area > 0 sentinel
                            chair_count += 1
            # Floor area in m^2: query segments['floor'] or estimate
            floor_area = 1.0
            if segments and "floor" in segments:
                fa = getattr(segments["floor"], "area_m2", None)
                if fa: floor_area = float(fa)
                else:
                    pix = float(getattr(segments["floor"], "sum", lambda: 1)())
                    # crude: 1 pixel ≈ 0.01 m^2 (placeholder; calibrated downstream)
                    floor_area = max(1.0, pix * 0.01)
            density = chair_count / floor_area
            density_signal = min(1.0, density / DENSITY_SATURATION)
            evidence.append(
                f"chair_count={chair_count}, floor_area={floor_area:.2f}m^2, "
                f"density={density:.3f}/m^2 -> signal={density_signal:.3f}"
            )
        except Exception as e:
            evidence.append(f"density fallback ({e}); 0")

        # ── Signal 2: sightline blocking
        sightline_signal = 0.0
        try:
            if segments and "sightline_blockers" in segments:
                sb = segments["sightline_blockers"]
                blocked = float(getattr(sb, "sum", lambda: 0)())
                total = float(getattr(sb, "size", None) or 1)
                sightline_signal = min(1.0, blocked / total * 2.0)
                evidence.append(
                    f"sightline_blocked_fraction={blocked/total:.3f} "
                    f"-> signal={sightline_signal:.3f}"
                )
            else:
                evidence.append("no sightline_blockers segment; signal=0")
        except Exception as e:
            evidence.append(f"sightline fallback ({e}); 0")

        score = self.W_DENSITY * density_signal + self.W_SIGHTLINE * sightline_signal
        if score >= 0.80: value = 4
        elif score >= 0.60: value = 3
        elif score >= 0.40: value = 2
        elif score >= 0.20: value = 1
        else: value = 0

        evidence.append(
            f"composite crowding = {self.W_DENSITY}*density({density_signal:.3f}) "
            f"+ {self.W_SIGHTLINE}*sightline({sightline_signal:.3f}) "
            f"= {score:.3f} -> Likert {value}"
        )
        evidence.append(
            "Stokols 1972 social-vs-spatial density; Hall 1966 proxemic thresholds; "
            "Evans 1979 crowding stress."
        )

        signals_present = sum([
            1 if density_signal > 0 else 0,
            1 if sightline_signal > 0 else 0,
        ])
        confidence = 0.3 + 0.3 * signals_present
        return ExtractorResult(value=value, confidence=confidence, evidence=evidence)
