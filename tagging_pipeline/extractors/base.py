"""LatentExtractor base class — Sprint 3 framework.

A typed contract that all detect_L## extractors honour. Sprint 3 ships this
base class plus five reference implementations across method families
(geometry, composite, vlm). Sprint 2's stubs (detect_L01..L58) are still in
place; Sprint 3 reference implementations subclass LatentExtractor and replace
five of the stubs with working code.

Design intent:

  1. Every extractor has the same input shape: an Image (numpy ndarray HxWx3),
     plus optional segments (a dict from semantic-class name to mask), depth
     (HxW float ndarray or None), and floor_plan (a FloorPlan object or None).
  2. Every extractor returns a typed Result dict with at least
     {value, confidence, evidence}; specific subclasses extend this with
     panel-mandated fields (distance_zone_estimate, F-formation triple, etc.).
  3. The framework exposes a class-level `manifest()` method that returns
     the parameter manifest (JSON-Schema shape) so the registry and the
     extractor are kept in lockstep — drift is mechanical to detect.
  4. NotImplementedError is raised when called by Sprint 2 stubs; Sprint 3
     reference implementations override .extract().
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


# ──────────────────────────────────────────────────────────────────
# Type stubs for the duck-typed inputs (kept minimal for portability;
# real implementations would import numpy / PIL / etc.).
# ──────────────────────────────────────────────────────────────────

class Image:
    """Type alias for an HxWx3 ndarray. Real impls import numpy."""

class Mask:
    """Type alias for an HxW boolean ndarray."""

class DepthMap:
    """Type alias for an HxW float ndarray (metres)."""

class FloorPlan:
    """A 2D floor-plan abstraction with axial/convex graph access for
    configurational latents (L29, L41, L42, L51, L54, L56, L58).
    """


# ──────────────────────────────────────────────────────────────────
# Result types
# ──────────────────────────────────────────────────────────────────

@dataclass
class ExtractorResult:
    """Common result shape for all latent extractors.

    Attributes:
        value: int (0..N-1 for ordinal/categorical) or 0/1 for binary.
        confidence: float in [0, 1] expressing the extractor's posterior
            confidence in the value (used by downstream BN ingestion).
        evidence: list of free-form strings citing what observables supported
            the value (used by HITL review and audit).
    """
    value: int | str | float
    confidence: float
    evidence: list[str]

    def to_dict(self) -> dict[str, Any]:
        d = {"value": self.value, "confidence": self.confidence, "evidence": self.evidence}
        return d


@dataclass
class GeometryResult(ExtractorResult):
    """Geometry-based extractor result; adds an isovist or convex-graph metric."""
    configurational_substrate: Optional[str] = None  # e.g. "isovist_area=18.4 m²"


@dataclass
class FFormationResult(ExtractorResult):
    """F-formation extractor result (L44, L48, L49, L52); adds the Kendon triple."""
    o_space_centroid_xy: Optional[tuple[float, float]] = None
    o_space_radius_px: Optional[float] = None
    predominant_arrangement: Optional[str] = None  # vis_a_vis | l_arrangement | side_by_side | semicircular | circular | none


@dataclass
class DistanceAwareResult(ExtractorResult):
    """Hall-aware extractor result (L42, L43, L44, L48, L49, L50, L51, L56)."""
    distance_zone_estimate: Optional[str] = None  # intimate | personal_close | personal_far | social_close | social_far | public


# ──────────────────────────────────────────────────────────────────
# Abstract base
# ──────────────────────────────────────────────────────────────────

class LatentExtractor:
    """Abstract latent-tag extractor. Subclass per L##.

    Class attributes (set by subclass):
        attribute_id: e.g. "L29"
        canonical_name: e.g. "cognitive.legibility"
        method_family: "geometry" | "composite" | "vlm"
        value_states: list of admissible value labels (e.g. [0,1,2,3,4] or
            ["vis_a_vis","l_arrangement",...]).
        expected_upstream_observables: list[str] — the upstream tag IDs the
            extractor depends on. Must match the registry's
            extraction.expected_upstream_observables for this latent.
    """
    attribute_id: str = ""
    canonical_name: str = ""
    method_family: str = ""
    value_states: list = []
    expected_upstream_observables: list[str] = []

    def extract(
        self,
        image: Optional[Image] = None,
        segments: Optional[dict[str, Mask]] = None,
        depth: Optional[DepthMap] = None,
        floor_plan: Optional[FloorPlan] = None,
        vlm_client: Optional[Any] = None,
    ) -> ExtractorResult:
        """Compute the latent value for the given inputs.

        Sprint 2 stubs raise NotImplementedError; Sprint 3 reference
        implementations override this method with real algorithms.
        """
        raise NotImplementedError(
            f"Sprint 3+: extractor for {self.attribute_id} ({self.canonical_name}) "
            f"is not yet implemented. Sprint 2 shipped the stub; Sprint 3 ships "
            f"the framework. Subclass LatentExtractor and override .extract()."
        )

    def manifest(self) -> dict[str, Any]:
        """Return the JSON-Schema-shaped parameter manifest for this latent."""
        return {
            "attribute_id": self.attribute_id,
            "canonical_name": self.canonical_name,
            "method_family": self.method_family,
            "value_states": self.value_states,
            "expected_upstream_observables": list(self.expected_upstream_observables),
        }
