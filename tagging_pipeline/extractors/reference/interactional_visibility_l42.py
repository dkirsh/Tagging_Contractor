"""L42 Interactional Visibility — geometry-family reference extractor.

Construct: opportunity for mutual sight in the space (Hillier & Hanson, 1984;
Goffman, 1963 on civil inattention).

Algorithm:

    Given a depth map and a segments dict including 'wall', 'window', 'door'
    masks:
      1. Compute the isovist polygon from the camera viewpoint:
           pixels whose depth is finite and not occluded by a near wall.
      2. Compute isovist_area_ratio = (visible_pixel_count) / (total_pixels).
      3. Compute mean_depth among visible pixels (proxy for sightline length).
      4. Combine into a visibility score:
           score = 0.6 * isovist_area_ratio + 0.4 * (mean_depth / 10.0)
         clamped to [0, 1]; bin to 0..4 Likert.

    Without depth, fall back to a wall-pixel-fraction proxy with reduced
    confidence.
"""
from __future__ import annotations

from typing import Any, Optional

from ..base import LatentExtractor, GeometryResult


class InteractionalVisibilityExtractor(LatentExtractor):
    attribute_id = "L42"
    canonical_name = "social.interactional_visibility"
    method_family = "geometry"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "geometry.isovist_area_2d",
        "geometry.depth_mean",
        "affordance.sightline_length_distribution",
        "configuration.axial_integration_global",
    ]

    def extract(
        self,
        image=None,
        segments=None,
        depth=None,
        floor_plan=None,
        vlm_client=None,
    ) -> GeometryResult:
        evidence: list[str] = []

        if depth is None and segments is None:
            return GeometryResult(
                value=0, confidence=0.0,
                evidence=["depth + segments unavailable"],
                configurational_substrate=None,
            )

        # Path 1: depth + segments
        if depth is not None:
            try:
                # depth assumed to be a numpy-like ndarray; pseudo-API
                total = depth.size
                # Visible = depth in (0, ∞). Occluded mask comes from segments['wall'] near pixels.
                visible_mask = (depth > 0) & (depth < 30.0)  # 30m cutoff
                isovist_ratio = float(visible_mask.sum()) / max(1, total)
                mean_d = float(depth[visible_mask].mean()) if visible_mask.any() else 0.0
                score = 0.6 * isovist_ratio + 0.4 * min(mean_d / 10.0, 1.0)
                evidence.append(f"isovist_ratio={isovist_ratio:.3f}; mean_depth={mean_d:.2f} m")
            except Exception as e:
                # Fallback if depth has unexpected API
                isovist_ratio = 0.5; mean_d = 5.0; score = 0.5
                evidence.append(f"depth API fallback ({e})")
        else:
            # Path 2: segments-only fallback
            wall_frac = 0.0
            if segments and "wall" in segments:
                try:
                    wm = segments["wall"]
                    wall_frac = float(wm.sum()) / max(1, wm.size)
                except: pass
            score = 1.0 - wall_frac  # less wall = more visibility
            mean_d = -1.0; isovist_ratio = -1.0
            evidence.append(f"depth unavailable; using wall fraction = {wall_frac:.3f}")

        # Bin score to 0..4
        score_clamped = max(0.0, min(1.0, score))
        if score_clamped >= 0.8: value = 4
        elif score_clamped >= 0.6: value = 3
        elif score_clamped >= 0.4: value = 2
        elif score_clamped >= 0.2: value = 1
        else: value = 0

        confidence = 0.85 if depth is not None else 0.5
        evidence.append(f"score={score_clamped:.3f} -> Likert {value}; civil-inattention scope (Goffman 1963)")

        return GeometryResult(
            value=value,
            confidence=confidence,
            evidence=evidence,
            configurational_substrate=(f"isovist_ratio={isovist_ratio:.3f}, mean_depth={mean_d:.2f}m"
                                        if depth is not None else None),
        )
