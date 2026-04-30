"""Reference extractor implementations and Sprint-4 algorithmic skeletons.

This package contains:

  1. **Working reference extractors** (`REFERENCE_EXTRACTORS`) — extractors
     whose `.extract()` is implemented and returns a real value. Sprint 3
     shipped 5 of these; Sprint 4 will add 8 more (8 entries are commented
     out below with TODO markers — they are written separately by another
     agent).

  2. **Algorithmic skeletons** (`SKELETON_EXTRACTORS`) — Sprint-4 scaffolds
     for the remaining 46 latents. Each skeleton subclasses LatentExtractor,
     declares its registry-aligned class attributes (attribute_id,
     canonical_name, method_family, value_states, expected_upstream_observables),
     and ships a 4-6 line algorithm sketch in its module docstring. The
     `.extract()` method raises NotImplementedError; Sprint 5 implementers
     replace the stub with the algorithm described in the docstring.

The two dicts are kept distinct so the extractor doctor can report
*coverage* (what is implemented vs. what is scaffolded only). Combining
them would obscure that signal.

Sprint coverage map:

    Sprint 3 working refs (5):  L17, L21, L29, L42, L46
    Sprint 4 working refs (8):  L01, L06, L10, L14, L25, L28, L33, L38
        (added by sibling agent — currently TODO-marked imports below)
    Sprint 4 skeletons (46):    L02-L05, L07-L09, L11-L13, L15-L16, L17b,
                                L18-L20, L22-L24, L26-L27, L30-L32, L34-L37,
                                L39-L41, L43-L45, L47-L58
"""

# ─────────────────────────────────────────────────────────────────────
# Sprint 3 working reference extractors (5)
# ─────────────────────────────────────────────────────────────────────
from .legibility_l29 import LegibilityExtractor
from .interactional_visibility_l42 import InteractionalVisibilityExtractor
from .coherence_order_l21 import CoherenceOrderExtractor
from .hosting_script_clarity_l46 import HostingScriptClarityExtractor
from .restorativeness_l17 import RestorativenessExtractor

# ─────────────────────────────────────────────────────────────────────
# Sprint 4 working reference extractors (8) — Sprint-4 deliverable.
# ─────────────────────────────────────────────────────────────────────
from .perceived_threat_l01 import PerceivedThreatExtractor
from .perceived_control_l06 import PerceivedControlExtractor
from .visual_privacy_l10 import VisualPrivacyExtractor
from .crowding_pressure_l14 import CrowdingPressureExtractor
from .coziness_l25 import CozinessExtractor
from .clutter_load_l28 import ClutterLoadExtractor
from .care_signal_l33 import CareSignalExtractor
from .novelty_l38 import NoveltyExtractor

# ─────────────────────────────────────────────────────────────────────
# Sprint 4 algorithmic skeletons (46)
# ─────────────────────────────────────────────────────────────────────
from .escape_efficacy_l02 import EscapeEfficacyExtractor
from .visibility_control_l03 import VisibilityControlExtractor
from .surveillance_pressure_l04 import SurveillancePressureExtractor
from .contamination_risk_l05 import ContaminationRiskExtractor
from .choice_richness_l07 import ChoiceRichnessExtractor
from .predictability_l08 import PredictabilityExtractor
from .rule_tightness_l09 import RuleTightnessExtractor
from .acoustic_privacy_l11 import AcousticPrivacyExtractor
from .interruption_likelihood_l12 import InterruptionLikelihoodExtractor
from .territorial_support_l13 import TerritorialSupportExtractor
from .social_exposure_l15 import SocialExposureExtractor
from .resource_scarcity_l16 import ResourceScarcityExtractor
from .extent_l17b import ExtentExtractor
from .being_away_l18 import BeingAwayExtractor
from .soft_fascination_l19 import SoftFascinationExtractor
from .compatibility_l20 import CompatibilityExtractor
from .mystery_l22 import MysteryExtractor
from .arousal_potential_l23 import ArousalPotentialExtractor
from .valence_potential_l24 import ValencePotentialExtractor
from .visual_comfort_l26 import VisualComfortExtractor
from .perceptual_fluency_l27 import PerceptualFluencyExtractor
from .landmark_clarity_l30 import LandmarkClarityExtractor
from .decision_point_load_l31 import DecisionPointLoadExtractor
from .prestige_signal_l32 import PrestigeSignalExtractor
from .welcome_l34 import WelcomeExtractor
from .placeness_l35 import PlacenessExtractor
from .awe_l36 import AweExtractor
from .familiarity_l37 import FamiliarityExtractor
from .formality_l39 import FormalityExtractor
from .playfulness_l40 import PlayfulnessExtractor
from .chance_encounter_potential_l41 import ChanceEncounterPotentialExtractor
from .approach_invitation_l43 import ApproachInvitationExtractor
from .sociopetal_seating_l44 import SociopetalSeatingExtractor
from .peripheral_participation_l45 import PeripheralParticipationExtractor
from .queue_support_l47 import QueueSupportExtractor
from .dyadic_intimacy_l48 import DyadicIntimacyExtractor
from .small_group_conversation_l49 import SmallGroupConversationExtractor
from .collaborative_work_l50 import CollaborativeWorkExtractor
from .large_group_assembly_l51 import LargeGroupAssemblyExtractor
from .presentation_one_to_many_l52 import PresentationOneToManyExtractor
from .shared_attention_anchor_l53 import SharedAttentionAnchorExtractor
from .boundary_permeability_l54 import BoundaryPermeabilityExtractor
from .group_territoriality_l55 import GroupTerritorialityExtractor
from .mingling_l56 import MinglingExtractor
from .disengagement_ease_l57 import DisengagementEaseExtractor
from .interaction_diversity_l58 import InteractionDiversityExtractor


# ─────────────────────────────────────────────────────────────────────
# Public dictionaries
# ─────────────────────────────────────────────────────────────────────

REFERENCE_EXTRACTORS = {
    # Sprint 3 working refs
    "L17": RestorativenessExtractor,
    "L21": CoherenceOrderExtractor,
    "L29": LegibilityExtractor,
    "L42": InteractionalVisibilityExtractor,
    "L46": HostingScriptClarityExtractor,
    # Sprint 4 working refs (8 — Sprint-4 deliverable)
    "L01": PerceivedThreatExtractor,
    "L06": PerceivedControlExtractor,
    "L10": VisualPrivacyExtractor,
    "L14": CrowdingPressureExtractor,
    "L25": CozinessExtractor,
    "L28": ClutterLoadExtractor,
    "L33": CareSignalExtractor,
    "L38": NoveltyExtractor,
}


SKELETON_EXTRACTORS = {
    "L02": EscapeEfficacyExtractor,
    "L03": VisibilityControlExtractor,
    "L04": SurveillancePressureExtractor,
    "L05": ContaminationRiskExtractor,
    "L07": ChoiceRichnessExtractor,
    "L08": PredictabilityExtractor,
    "L09": RuleTightnessExtractor,
    "L11": AcousticPrivacyExtractor,
    "L12": InterruptionLikelihoodExtractor,
    "L13": TerritorialSupportExtractor,
    "L15": SocialExposureExtractor,
    "L16": ResourceScarcityExtractor,
    "L17b": ExtentExtractor,
    "L18": BeingAwayExtractor,
    "L19": SoftFascinationExtractor,
    "L20": CompatibilityExtractor,
    "L22": MysteryExtractor,
    "L23": ArousalPotentialExtractor,
    "L24": ValencePotentialExtractor,
    "L26": VisualComfortExtractor,
    "L27": PerceptualFluencyExtractor,
    "L30": LandmarkClarityExtractor,
    "L31": DecisionPointLoadExtractor,
    "L32": PrestigeSignalExtractor,
    "L34": WelcomeExtractor,
    "L35": PlacenessExtractor,
    "L36": AweExtractor,
    "L37": FamiliarityExtractor,
    "L39": FormalityExtractor,
    "L40": PlayfulnessExtractor,
    "L41": ChanceEncounterPotentialExtractor,
    "L43": ApproachInvitationExtractor,
    "L44": SociopetalSeatingExtractor,
    "L45": PeripheralParticipationExtractor,
    "L47": QueueSupportExtractor,
    "L48": DyadicIntimacyExtractor,
    "L49": SmallGroupConversationExtractor,
    "L50": CollaborativeWorkExtractor,
    "L51": LargeGroupAssemblyExtractor,
    "L52": PresentationOneToManyExtractor,
    "L53": SharedAttentionAnchorExtractor,
    "L54": BoundaryPermeabilityExtractor,
    "L55": GroupTerritorialityExtractor,
    "L56": MinglingExtractor,
    "L57": DisengagementEaseExtractor,
    "L58": InteractionDiversityExtractor,
}
