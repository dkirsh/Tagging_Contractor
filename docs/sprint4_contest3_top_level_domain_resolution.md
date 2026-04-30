# Sprint 4 — Contest 3 Resolution: Top-Level Domain Split for Social Latents

**Convened:** 29 April 2026
**Source contest:** §4(xi) of `docs/sprint1_panel_disposition_2026-04-28.md` ("Goffman's `interaction_order` vs `social_organization` top-level domain split. Rejected for Sprint 1 ... logged as a Sprint 4 architectural question.")
**Procedure:** Simulated panel vote with synthesised disposition. Four voices were elicited independently against the contest brief and reconciled into a hybrid disposition. Per-latent assignments were resolved by the chair against the substantive criteria the panel converged upon.

---

## 1. The contest as posed

The Sprint-1 registry assigns a single top-level domain — `domain: "social"` — to all eighteen social-interaction latents (L41–L58). Goffman's (1959/1963/1974) ontological distinction between the *interaction order* (the moment-by-moment focused encounter, governed by the rules of co-presence, civil inattention, exit ritual) and the *social organisation* of gatherings (the institutional roles, normative scripts, and field-positioned habituses that pre-structure encounters) is therefore not represented in the registry. Sprint 1 deferred the question on contract-renaming grounds.

The Sprint 4 question is whether the top-level `domain` field should be split into two distinct values — `interaction_order` and `social_organization` — or whether the analytical distinction can be carried in a different schema position.

## 2. Position statements

**Goffman (for the split).** The interaction order is not a sub-region of social organisation; it is an autonomous domain with its own laws (Goffman, 1983, "The Interaction Order" American Sociological Review 48: 1–17). Treating L46 (hosting/service script — an institutional performance) and L48 (dyadic intimacy — an interaction-order phenomenon) as siblings under the same top-level domain hides the categorial difference. *Frame Analysis* (Goffman, 1974) makes the same point in different idiom: the *frame* is what tells us which order we are in, and a registry that cannot represent the difference cannot represent frames. The split should be carried at the highest visible level.

**Bourdieu (for the split, on different grounds).** Field theory (Bourdieu, 1977; 1984) holds that L32 (prestige), L33 (care signal), L35 (placeness) are properties of *fields* — structured spaces of positions and capitals — and not of focused encounters. To represent a prestige cue as a "social" property without specifying that it is a *social-organisation* property and not an *interaction-order* property is to flatten the very distinction that lets one analyse symbolic capital. The top-level split gives field-theoretic analyses a registry hook they currently lack.

**Spohn (against the split).** The Bayesian-network engine treats `domain` as a tag-id namespace governing identifiability and parameter sharing across the eighteen latents. The Sprint-3 audit shows the current namespace is well-conditioned: identifiability holds, parameter-sharing across the eighteen is good, and structural priors are computable. A top-level split forces a registry-version bump (v0.3.0), consumer-contract renames, and recomputation of the structural prior — all for a distinction that can be represented without renaming. The cost-benefit ratio does not favour the split.

**Kahneman (against, on practical grounds).** Two top-level domains where there was one creates documentation overhead: every controlled-vocabulary entry must be assigned to a top-level domain, and the Sprint-2 cognitive-load / familiarity / wayfinding latents (L27–L40) span the boundary in ways that do not cleanly resolve. The cognitive cost of maintaining the split — for the students inheriting the system, for the downstream extractor authors, for anyone reading a registry diff — exceeds the analytical benefit. A semantic distinction that is *useful when needed* is better than a structural distinction that is *paid for always*.

## 3. Hybrid disposition

The panel adopts a **hybrid**: keep `domain: "social"` as the single top-level value, but introduce a new schema-level field `notes.social_layer` per latent, with values `interaction_order | social_organization | both`. This preserves Goffman's analytical distinction, gives Bourdieu's field-theoretic analysis a hook in the registry, and avoids Spohn's identifiability disruption and Kahneman's documentation overhead. The split is captured *semantically*, not *namespace-mechanically* — and Goffman, asked to confirm, accepted the compromise on the ground that the distinction is preserved in the schema even if not in the namespace.

The hybrid is symmetric with the Sprint-1 disposition on L42 (split-rejected, scope-note-adopted): the registry refuses ID-level splits whose only payoff is conceptual purity, but it does adopt schema fields that carry the conceptual content.

## 4. Per-latent assignment table

| ID | Latent | social_layer | Rationale |
|----|--------|--------------|-----------|
| L41 | Chance-Encounter Potential | both | Configurational affordance (organisation) for unfocused co-presence (interaction order) |
| L42 | Interactional Visibility | interaction_order | Civil-inattention substrate (Goffman, 1963) |
| L43 | Approach Invitation | interaction_order | Pre-engagement signalling within focused-encounter formation |
| L44 | Sociopetal Seating | interaction_order | Kendon F-formation geometry |
| L45 | Peripheral Participation | interaction_order | Lave-Wenger / Goffman-bystander role |
| L46 | Hosting Script Clarity | social_organization | Institutional service script |
| L47 | Queue Support | social_organization | Normative ordering institution |
| L48 | Dyadic Intimacy | interaction_order | Focused two-party encounter |
| L49 | Small Group Conversation | interaction_order | F-formation focused encounter |
| L50 | Collaborative Work | both | Task-organisational structure hosting focused encounters |
| L51 | Large-Group Assembly | both | Institutional gathering whose interior is interaction-order |
| L52 | One-to-Many Presentation | social_organization | Formal speaker-audience institutional form |
| L53 | Shared Attention Anchor | interaction_order | Joint-attention substrate of the focused encounter |
| L54 | Boundary Permeability | both | Configurational (organisation) governing entry/exit (interaction order) |
| L55 | Group Territorial Claimability | social_organization | Property/territory norms of gatherings |
| L56 | Mingling Affordance | interaction_order | Unfocused-to-focused encounter transition |
| L57 | Disengagement Ease | interaction_order | Goffman exit ritual (1971, ch. 3) |
| L58 | Interaction Diversity | both | Compositional property of organisation enabling varied interaction orders |

Tally: interaction_order = 9; social_organization = 4; both = 5.

## 5. Implementation note

`scripts/audit_semantics_simple.py` MUST validate, for every registry entry with `domain: "social"`, that `notes.social_layer` is present and takes one of the three values `{interaction_order, social_organization, both}`. The validator should emit a hard error (not a warning) on missing or out-of-vocabulary values. The check is small and the cost of a malformed registry value is high — every downstream consumer that reads `notes.social_layer` will fail silently or noisily depending on its tolerance, and silent failure is the worse risk.

A complementary registry-schema change is required: add `social_layer` to the `notes` block's documented fields with the enum constraint, and emit a migration note in the v0.2.x → v0.2.(x+1) changelog rather than bumping to v0.3.0 (the change is additive and backward-compatible — no consumer that ignores `notes.social_layer` will break).

## 6. Sprint 5 follow-up

Extend `notes.social_layer` to the forty cognitive-domain latents (L1–L40). Default value: `both`. Override to `interaction_order` where the construct is constitutively about co-presence (e.g., L19 if it concerns shared-attention affordance) and to `social_organization` where the construct is constitutively institutional/normative (e.g., L33 care-signal, L35 placeness, on Bourdieu's reading). The extension makes the registry uniformly searchable on `social_layer`, which lets Bourdieu-style field analyses and Goffman-style interaction-order analyses query the registry without tag-by-tag lookup. This is a Sprint-5 task, not Sprint-4, because the cognitive-domain audit is non-trivial and the Sprint-4 contest concerns only the eighteen social-domain latents.

## 7. References

Bourdieu, P. (1977). *Outline of a theory of practice* (R. Nice, Trans.). Cambridge University Press. (Original work published 1972)

Bourdieu, P. (1984). *Distinction: A social critique of the judgement of taste* (R. Nice, Trans.). Harvard University Press. (Original work published 1979)

Goffman, E. (1959). *The presentation of self in everyday life*. Doubleday.

Goffman, E. (1963). *Behavior in public places: Notes on the social organization of gatherings*. Free Press.

Goffman, E. (1971). *Relations in public: Microstudies of the public order*. Basic Books.

Goffman, E. (1974). *Frame analysis: An essay on the organization of experience*. Harvard University Press.

Goffman, E. (1983). The interaction order. *American Sociological Review*, *48*(1), 1–17. https://doi.org/10.2307/2095141

Kendon, A. (1990). *Conducting interaction: Patterns of behavior in focused encounters*. Cambridge University Press.

Spohn, W. (2012). *The laws of belief: Ranking theory and its philosophical applications*. Oxford University Press.

---

*End of resolution.*
