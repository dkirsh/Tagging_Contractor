#!/usr/bin/env python3
"""Sprint 3 — apply the four panel-contest decisions to registry_v0.2.8.json.

Contest 1 (L17 factor structure): structured-factor reorganisation.
  - L17 becomes the parent: bn.role = "structured_factor_parent",
    bn.child_tags = [L18, L19, L20, cognitive.extent].
  - L18, L19, L20 each get bn.parent_tags = [cognitive.restorativeness].
  - New latent cognitive.extent created (V2.7 ART fourth component).
  - bn_notes documents the reorganisation on all five entries.

Contest 2 (L08 continuous): hybrid encoding.
  - L08 keeps value_type = "ordinal" (rater capture).
  - L08 gains bn.posterior_distribution = {form: "continuous", support: [0.0, 1.0]}
    declaring that the BN's posterior over this node is continuous.

Contest 4 (cross-cultural variance): single edit.
  - L36 (cognitive.awe) cross_cultural_variance: "high" -> "medium".
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).parent.parent
REGISTRY = REPO / "core/trs-core/v0.2.8/registry/registry_v0.2.8.json"


def main() -> int:
    with REGISTRY.open() as f: reg = json.load(f)
    tags = reg["tags"]

    # ---------- Contest 1: L17 structured-factor reorganisation ----------
    L17 = "cognitive.restorativeness"
    L18 = "cognitive.being_away"
    L19 = "cognitive.soft_fascination"
    L20 = "cognitive.compatibility"
    L17_extent = "cognitive.extent"
    L21 = "cognitive.coherence_order"  # for related_tags reference in extent entry

    if L17 not in tags:
        print(f"ERROR: {L17} missing", file=sys.stderr); return 1

    # Edit 1 — promote L17 to structured-factor parent
    t17 = tags[L17]
    t17.setdefault("bn", {})
    t17["bn"]["role"] = "structured_factor_parent"
    t17["bn"]["child_tags"] = [L18, L19, L20, L17_extent]
    t17["bn"].setdefault("parent_tags", [])
    t17.setdefault("notes", {})
    bn_notes_text = ("Structured-factor parent over L18 (being-away), L19 (soft fascination), "
                     "L20 (compatibility), and L17_extent (cognitive.extent). Reorganisation "
                     "ratified in Sprint 3 contest #1 disposition (2026-04-29); Russell dissent "
                     "preserved — see docs/sprint3_contest1_L17_resolution.md §5.")
    existing = t17["notes"].get("bn_notes") or ""
    t17["notes"]["bn_notes"] = (existing + (" | " if existing else "") + bn_notes_text).strip()
    print(f"Edit 1: L17 promoted to structured_factor_parent over 4 children")

    # Edit 2 — reparent L18, L19, L20
    child_bn_note = ("Component of L17 (cognitive.restorativeness). Per Sprint 3 contest #1 "
                     "structured-factor reorganisation; the parent-child relationship is a "
                     "BN-structural commitment, not an extraction-time merger — independent "
                     "extractor stubs retained.")
    for child in (L18, L19, L20):
        if child not in tags:
            print(f"ERROR: child {child} missing", file=sys.stderr); return 1
        c = tags[child]
        c.setdefault("bn", {})
        existing_parents = c["bn"].get("parent_tags") or []
        if L17 not in existing_parents:
            existing_parents.append(L17)
        c["bn"]["parent_tags"] = existing_parents
        c.setdefault("notes", {})
        existing = c["notes"].get("bn_notes") or ""
        c["notes"]["bn_notes"] = (existing + (" | " if existing else "") + child_bn_note).strip()
    print(f"Edit 2: L18, L19, L20 now have bn.parent_tags = [{L17}]")

    # Edit 3 — create cognitive.extent
    extent = {
        "attribute_id": "L17b",  # 'extent' is the fourth ART component but not in the original L## numbering
        "canonical_name": L17_extent,
        "category": "cognitive",
        "domain": "cognitive_affect",
        "subdomain": "restoration",
        "status": "active",
        "value_type": "ordinal",
        "value_range": [0, 4],
        "unit": "likert_0_4",
        "owner": "claude-cowork-sprint3",
        "version_added": "v0.2.11",
        "version_modified": "v0.2.11",
        "change_log": [{
            "version": "v0.2.11",
            "date": "2026-04-29",
            "change": ("Initial introduction (Sprint 3 contest #1 disposition: fourth ART "
                       "component split out of L17 per Spohn structured-factor decision)")
        }],
        "definition": "Extent — sense that the environment is a coherent rich whole.",
        "extractability": {
            "from_2d": "no",  # judgability 3 -> from_2d "partial" by Sprint-2 mapping; but extent benefits from VR field-of-view; conservative default
            "from_3d_vr": "yes",
            "monocular_3d_approx": "no",
            "region_support": False,
            "confidence_available": True,
            "requires_floor_plan": False,
            "configurational_measure": "none",
        },
        "extraction": {
            "compute_from": "2D + scene-level coherence + spatial graph",
            "method_family": "vlm",
            "primary_extractors": [],
            "recipe_id": None,
            "expected_upstream_observables": [
                "scene.global_coherence_index",
                "geometry.scene_graph_completeness",
                "lighting.uniformity_index",
                "scene.world_richness_proxy"
            ],
        },
        "bn": {
            "evidence_role": "latent",
            "demand_state": "optional",
            "consumable": True,
            "parent_tags": [L17],
            "child_tags": [],
        },
        "semantics": {
            "definition_short": "Extent — the sense that the environment is a coherent rich whole.",
            "definition_long": (
                "Extent is the fourth Attention Restoration Theory (ART) component (Kaplan & "
                "Kaplan, 1989, pp. 184–187): the sense that the environment is rich and coherent "
                "enough to engage attention as a whole world rather than as a collection of "
                "disjointed elements. A small garden can have extent if it is internally "
                "coherent and inviting of mental exploration; a vast but disorganised parking "
                "lot lacks extent. Sprint 3 added this latent as a separate construct rather "
                "than absorbing it into restorativeness, per the contest #1 disposition (Spohn "
                "structured-factor decision, 2-1 over Russell's full split). See Hartig, Korpela, "
                "Evans, & Gärling (1997) for the validated PRS measurement of extent and Korpela, "
                "Hartig, Kaiser, & Fuhrer (2001) on extent's discriminant validity from coherence."
            ),
            "aliases": ["Extent", "ART extent", "scene world-richness", "coherent richness", "world-like coherence"],
            "examples_positive": [
                "A small Japanese garden whose paths invite continued mental exploration.",
                "A reading room with bookshelves that suggest a coherent intellectual world.",
                "A coastline view whose features suggest a continuous landscape system.",
                "A curated museum gallery whose objects relate as parts of a larger story.",
                "A craftsman's workshop whose tools form a coherent practice ecology.",
                "A wooded trail whose turns promise more of a coherent forest beyond view."
            ],
            "examples_negative": [
                "A blank corridor that suggests no further world.",
                "A cluttered storage room whose contents do not form a coherent set.",
                "A parking lot whose vastness lacks internal organisation.",
                "A room composed of mismatched furniture suggesting no shared purpose."
            ],
            "scope_includes": [
                "Whole-scene mental-world coherence judgements.",
                "Sense of an interpretable environment beyond what is currently visible.",
                "Coherent extension of the present view into an implied larger setting."
            ],
            "scope_excludes": [
                "Soft fascination (L19) — the *capture* of attention, distinct from the *world* the attention enters.",
                "Coherence/Order (L21) — local visual organisation, not the world-extent judgement.",
                "Compatibility (L20) — fit between user goals and environment, not the world's intrinsic richness."
            ],
            "extraction_notes_2d": (
                "Image-only extraction is degraded for extent because the construct requires "
                "judging whether the visible scene implies a coherent further world. Use a "
                "VLM prompted with the Hartig PRS-extent items (e.g., 'There is much to "
                "explore and discover here'); supplement with a scene-graph completeness "
                "score from upstream observables scene.global_coherence_index and "
                "geometry.scene_graph_completeness. Field-of-view matters: ≥ 90° horizontal "
                "improves judgability noticeably."
            ),
            "extraction_notes_3d": (
                "VR rendering improves extent judgement substantially because the user can "
                "look around and infer the wider world. Pair the VLM prompt with a VR-trial "
                "where the user rates extent after a 30-second free-look exploration. The "
                "comparison metric is intra-rater consistency between 2D and VR judgement."
            ),
            "factor_associations": ["ART"],
            "inverse_of": None,
            "related_tags": [L17, L19, L21],
        },
        "literature": {
            "key_refs": [
                ("Kaplan, R., & Kaplan, S. (1989). The experience of nature: A psychological "
                 "perspective. Cambridge University Press."),
                ("Hartig, T., Korpela, K., Evans, G. W., & Gärling, T. (1997). A measure of "
                 "restorative quality in environments. Scandinavian Housing and Planning "
                 "Research, 14(4), 175–194. https://doi.org/10.1080/02815739708730435"),
                ("Korpela, K., Hartig, T., Kaiser, F. G., & Fuhrer, U. (2001). Restorative "
                 "experience and self-regulation in favorite places. Environment and "
                 "Behavior, 33(4), 572–589.")
            ],
            "search_terms": ["ART extent", "Perceived Restorativeness Scale", "coherent richness",
                            "scene world coherence", "Hartig PRS"],
            "suggested_outcomes": [],
            "suggested_tests": [],
        },
        "notes": {
            "bn_notes": ("Component of L17 (cognitive.restorativeness) per Sprint 3 contest #1 "
                        "structured-factor disposition; the fourth ART component, separate from "
                        "L18 (being-away), L19 (soft fascination), L20 (compatibility)."),
            "extraction_notes": ("Sprint 3 introduced as a new latent. Image judgability is "
                               "marginal (Sprint 2 panel rule judg=3 → from_2d 'partial', but "
                               "the panel deliberately set from_2d='no' here because the "
                               "construct requires whole-world inference that monocular 2D "
                               "consistently fails on)."),
            "validation_notes": "Pending Sprint 4 panel vote",
            "interaction_mode": "mixed",
            "cross_cultural_variance": "medium",
            "temporal_window": "sustained",
            "valence_polarity": "positive",
            "l_number": "L17b",
        },
        "aliases": ["Extent", "ART extent", "scene world-richness", "coherent richness", "world-like coherence"],
    }
    tags[L17_extent] = extent
    print(f"Edit 3: created {L17_extent} with full semantic contract")

    # Edit 5 — bn_notes was already added above on the four parents/children
    # ---------- Contest 2: L08 continuous (hybrid) ----------
    L08 = "cognitive.predictability"
    if L08 in tags:
        t08 = tags[L08]
        t08.setdefault("bn", {})
        t08["bn"]["posterior_distribution"] = {
            "form": "continuous",
            "support": [0.0, 1.0],
            "rationale": ("Sprint 3 contest #2 hybrid disposition: ordinal Likert capture "
                         "from raters, but the BN's posterior over this node is computed as "
                         "a continuous distribution. Engine assumes Beta-distributed posterior "
                         "with conjugate updates from Likert observations.")
        }
        existing = t08["notes"].get("bn_notes") or ""
        addition = ("Sprint 3 contest #2 disposition: kept value_type=ordinal for rater "
                   "capture; added bn.posterior_distribution {form: continuous, support: "
                   "[0.0, 1.0]}. Kahneman position partially adopted via the hybrid encoding.")
        t08["notes"]["bn_notes"] = (existing + (" | " if existing else "") + addition).strip()
        print("Contest 2: L08 hybrid posterior_distribution applied")

    # ---------- Contest 4: L36 cross_cultural_variance high -> medium ----------
    L36 = "cognitive.awe"
    if L36 in tags:
        t36 = tags[L36]
        t36.setdefault("notes", {})
        prev = t36["notes"].get("cross_cultural_variance")
        t36["notes"]["cross_cultural_variance"] = "medium"
        existing = t36["notes"].get("bn_notes") or ""
        addition = ("Sprint 3 contest #4 disposition: cross_cultural_variance demoted from "
                   f"'{prev}' to 'medium'. Keltner & Haidt (2003) two-core-appraisal pattern "
                   "(vastness + need for accommodation) replicates across cultures; Yaden "
                   "et al. (2019) 23-country evidence supports universality of awe perception. "
                   "Cultural variance is in *meaning* and *downstream behavior*, not the "
                   "image-extractable appraisal. L25 and L40 retain 'high' (per contest #4 "
                   "per-latent vote).")
        t36["notes"]["bn_notes"] = (existing + (" | " if existing else "") + addition).strip()
        print(f"Contest 4: L36 cross_cultural_variance: {prev} -> medium")

    # Recompute statistics
    by_role = {}; by_status = {}
    for t in tags.values():
        r = (t.get("bn") or {}).get("evidence_role","unknown"); by_role[r] = by_role.get(r,0)+1
        s = t.get("status","unknown"); by_status[s] = by_status.get(s,0)+1
    reg.setdefault("statistics", {})
    reg["statistics"]["by_bn_role"] = by_role
    reg["statistics"]["by_status"] = by_status
    reg["statistics"]["total_tags"] = len(tags)
    reg["generated_at_utc"] = datetime.now(timezone.utc).isoformat()

    with REGISTRY.open("w") as f: json.dump(reg, f, indent=2, sort_keys=True)
    print(f"\nRegistry written. Total tags: {len(tags)}; latents: {by_role.get('latent', 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
