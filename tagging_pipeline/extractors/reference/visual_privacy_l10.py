"""L10 Visual Privacy — geometry-family Sprint-4 reference extractor.

Construct: Not being seen by others while occupying the depicted space
(Altman 1975 privacy regulation; Westin 1967 privacy taxonomy).
Subdomain: privacy_attention.

Algorithm (geometry-family per Sprint-4 spec — partition heights, alcoves,
door states are geometric features computed from segments):

    Inputs: segments dict containing partition masks (with per-mask height
    in metres or pixels), alcove/booth detection, and door-open/closed state.

    1. partition_mean_height: mean height across partition segments.
    2. alcove_present: 1.0 if at least one alcove or booth segment;
       else 0.0.
    3. door_closed_factor: 1.0 if doors detected as closed, 0.5 if state
       unknown, 0.0 if open.
    4. composite_privacy = 0.5 * normalized_partition_height
                          + 0.3 * alcove_present
                          + 0.2 * door_closed_factor
       Partition heights are normalised by 1.8 m (a standing-eye-height
       reference; Pedersen 1997 visual-privacy threshold).
    5. Likert bin to [0..4].

Citations:
    Altman, I. (1975). The environment and social behavior: Privacy,
        personal space, territory, and crowding. Brooks/Cole.
    Westin, A. F. (1967). Privacy and freedom. Atheneum.
    Pedersen, D. M. (1997). Psychological functions of privacy. Journal
        of Environmental Psychology, 17(2), 147-156.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, GeometryResult


PARTITION_REFERENCE_HEIGHT_M = 1.8  # standing-eye height
PARTITION_OBJECTS = ("partition", "wall_low", "screen", "divider", "cubicle_wall")
ALCOVE_OBJECTS = ("alcove", "booth", "nook", "recess")


class VisualPrivacyExtractor(LatentExtractor):
    attribute_id = "L10"
    canonical_name = "cognitive.visual_privacy"
    method_family = "geometry"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "affordance.partition_height",
        "affordance.door_present",
        "affordance.alcove_depth",
        "furniture.booth_indicator",
        "scene.sightline_to_viewpoint",
    ]

    W_PARTITION = 0.5
    W_ALCOVE = 0.3
    W_DOOR = 0.2

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> GeometryResult:
        if segments is None and floor_plan is None:
            return GeometryResult(
                value=2, confidence=0.0,
                evidence=["L10 visual-privacy: no segments/floor_plan; "
                          "neutral default 2."],
                configurational_substrate=None,
            )

        evidence: list[str] = []
        substrate_parts: list[str] = []

        # ── Signal 1: partition mean height
        partition_signal = 0.0
        try:
            heights = []
            if segments:
                for obj in PARTITION_OBJECTS:
                    if obj in segments:
                        m = segments[obj]
                        h = getattr(m, "height_metres", None)
                        if h is not None:
                            heights.append(float(h))
                        else:
                            # Estimate from pixel-bbox if available
                            bbox = getattr(m, "bbox", None)
                            if bbox is not None:
                                heights.append(float(bbox[3] - bbox[1]) / 600.0 * 2.5)  # crude
            if heights:
                mean_h = sum(heights) / len(heights)
                partition_signal = min(1.0, mean_h / PARTITION_REFERENCE_HEIGHT_M)
                evidence.append(
                    f"partition_mean_height={mean_h:.2f}m across {len(heights)} "
                    f"segments -> signal={partition_signal:.3f}"
                )
                substrate_parts.append(f"partition_h={mean_h:.2f}m")
            else:
                evidence.append("no partition segments with height data; partition=0")
        except Exception as e:
            evidence.append(f"partition fallback ({e}); 0")

        # ── Signal 2: alcove presence
        alcove_signal = 0.0
        try:
            if segments and any(obj in segments for obj in ALCOVE_OBJECTS):
                alcove_signal = 1.0
                evidence.append("alcove/booth detected -> alcove_signal=1.0")
                substrate_parts.append("alcove=1")
            else:
                evidence.append("no alcove/booth -> 0")
        except Exception as e:
            evidence.append(f"alcove fallback ({e}); 0")

        # ── Signal 3: door state
        door_signal = 0.5  # default unknown
        try:
            if segments and "door" in segments:
                door = segments["door"]
                state = getattr(door, "state", None)
                if state == "closed":
                    door_signal = 1.0
                elif state == "open":
                    door_signal = 0.0
                evidence.append(f"door_state={state} -> door_signal={door_signal}")
                substrate_parts.append(f"door_state={state}")
            else:
                evidence.append("door state unknown; door_signal=0.5")
        except Exception as e:
            evidence.append(f"door fallback ({e}); 0.5")

        score = (
            self.W_PARTITION * partition_signal
            + self.W_ALCOVE * alcove_signal
            + self.W_DOOR * door_signal
        )
        if score >= 0.80: value = 4
        elif score >= 0.60: value = 3
        elif score >= 0.40: value = 2
        elif score >= 0.20: value = 1
        else: value = 0

        evidence.append(
            f"composite privacy = {self.W_PARTITION}*partition({partition_signal:.3f}) "
            f"+ {self.W_ALCOVE}*alcove({alcove_signal:.3f}) "
            f"+ {self.W_DOOR}*door({door_signal:.3f}) = {score:.3f} -> Likert {value}"
        )
        evidence.append("Altman 1975 privacy regulation; Pedersen 1997 visual-privacy threshold.")

        signals_present = sum([
            1 if partition_signal > 0 else 0,
            1 if alcove_signal > 0 else 0,
            1 if door_signal != 0.5 else 0,
        ])
        confidence = 0.2 + 0.25 * signals_present
        return GeometryResult(
            value=value,
            confidence=confidence,
            evidence=evidence,
            configurational_substrate=", ".join(substrate_parts) if substrate_parts else None,
        )
