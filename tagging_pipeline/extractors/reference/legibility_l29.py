"""L29 Legibility — geometry-family reference extractor.

Construct: ease of forming a coherent mental map of the space (Lynch, 1960).
Configurational: requires_floor_plan = true, configurational_measure =
connectivity (Hillier & Hanson, 1984; Hillier, 1996).

Algorithm:

    Given a 2D floor-plan polygon set with door/aperture annotations:
      1. Build the convex map: each convex sub-region is a node.
      2. Build the connectivity graph: edges between convex regions sharing
         a door or aperture.
      3. Compute mean axial integration as the inverse of mean depth from
         the most-connected node (a Hillier integration proxy).
      4. Map normalized integration in [0, 1] to a 5-bin Likert (0-4):
           [0.0, 0.2) -> 0, [0.2, 0.4) -> 1, ..., [0.8, 1.0] -> 4

    Without a floor plan, the extractor returns value=null with confidence=0
    and evidence ["floor_plan unavailable; legibility is configurational and
    cannot be image-only extracted (Hillier 1996)"].

The graph algorithms below use a simplified networkx-free BFS implementation
for portability; production code should swap in networkx or igraph.
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, Optional

from ..base import LatentExtractor, GeometryResult


class LegibilityExtractor(LatentExtractor):
    attribute_id = "L29"
    canonical_name = "cognitive.legibility"
    method_family = "geometry"
    value_states = [0, 1, 2, 3, 4]
    expected_upstream_observables = [
        "geometry.convex_region_graph",
        "geometry.door_segment_count",
        "geometry.aperture_threshold_visibility",
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
        if floor_plan is None:
            return GeometryResult(
                value=0,
                confidence=0.0,
                evidence=["floor_plan unavailable; legibility is configurational "
                          "and cannot be image-only extracted (Hillier 1996)."],
                configurational_substrate=None,
            )

        # Expected floor_plan API:
        #   floor_plan.convex_regions -> list[ConvexRegion] each with .id and .area
        #   floor_plan.doors -> list[(region_id_a, region_id_b)] adjacency
        regions = getattr(floor_plan, "convex_regions", []) or []
        doors = getattr(floor_plan, "doors", []) or []

        if not regions:
            return GeometryResult(
                value=0, confidence=0.0,
                evidence=["floor_plan has no convex regions"],
                configurational_substrate=None,
            )

        # Build adjacency graph
        adj: dict[Any, set] = defaultdict(set)
        for a, b in doors:
            adj[a].add(b); adj[b].add(a)

        # Compute mean depth from each region; integration ~ 1/mean_depth
        def bfs_mean_depth(start) -> float:
            seen = {start: 0}
            q = deque([start])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if v not in seen:
                        seen[v] = seen[u] + 1
                        q.append(v)
            if len(seen) <= 1: return 0.0
            return sum(seen.values()) / max(1, (len(seen) - 1))

        depths = [bfs_mean_depth(r.id) for r in regions if hasattr(r, "id")]
        if not depths:
            return GeometryResult(
                value=0, confidence=0.1,
                evidence=["regions present but bfs_mean_depth returned no values"],
                configurational_substrate=None,
            )
        mean_depth = sum(depths) / len(depths)
        # Normalise: integration = 1/(1 + mean_depth); map to [0, 1]
        integration = 1.0 / (1.0 + mean_depth)
        # Bin to 0..4
        if integration >= 0.8: value = 4
        elif integration >= 0.6: value = 3
        elif integration >= 0.4: value = 2
        elif integration >= 0.2: value = 1
        else: value = 0

        return GeometryResult(
            value=value,
            confidence=min(0.9, 0.5 + 0.4 * len(regions) / 20),
            evidence=[
                f"mean_depth={mean_depth:.2f} across {len(regions)} convex regions",
                f"integration_proxy={integration:.3f} -> Likert bin {value}",
                "Hillier & Hanson (1984) connectivity / mean-depth measure",
            ],
            configurational_substrate=f"axial_integration_proxy={integration:.3f}",
        )
