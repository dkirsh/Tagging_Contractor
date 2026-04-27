# TASKS.md — Tagging_Contractor

*Last updated: 2026-04-26*

This file persists the project task ledger across sessions, per the root `CLAUDE.md` task-tracking protocol. Live in-session tasks are also tracked via the Cowork TaskList tool, but this file is the durable record.

---

## Active Topics

| ID | Topic | Started | Status | Branch | Notes |
|----|-------|---------|--------|--------|-------|
| TOP-009 | Latent variables L41–L58 (social-interaction) integration | 2026-04-26 | IN_PROGRESS | `track1/latents/L41-L58-claude-sprint1` | Sprint 1 of multi-sprint integration. Executor: Claude (Cowork). Plan: `outputs/SPRINT1_LATENT_INTEGRATION_PLAN.md`. Panel disposition: `docs/sprint1_panel_disposition_2026-04-28.md`. |

---

## In Progress (Sprint 1, TOP-009)

| ID | Task | Started | Notes |
|----|------|---------|-------|
| S1.A | Phase A: cut branch, write V2.6→registry field-map | 2026-04-26 | Branch cut; field-map document pending |
| S1.B | Phase B: per-latent deliberation for L41–L58 | pending | 18 latents × medium-procedure (3 sub-agents each) |
| S1.C | Phase C: author 18 JSON tag entries | pending | Validator must pass |
| S1.D | Phase D: add tc doctor --prod, audit-semantics, audit-extraction-plan | pending | Includes Spohn 50% upstream-overlap rule |
| S1.E | Phase E: extractor stubs in tagging_pipeline/extractors/latents/ | pending | With distance-zone and F-formation docstring requirements |
| S1.F | Phase F: repo-level adversarial blind-read | pending | |
| S1.F5 | Phase F.5: construct-validity panel vote | pending | |
| S1.G | Phase G: handoff bundle, release v0.2.9-rc1, PR | pending | |

---

## Completed

| ID | Task | Completed | Outcome |
|----|------|-----------|---------|
| S1.A5 | Phase A.5: architectural panel deliberation (Goffman, Hall, Kendon, Hillier, Spohn) | 2026-04-26 | Five sub-agent critiques produced. Disposition committed at `docs/sprint1_panel_disposition_2026-04-28.md`. Six revisions adopted; three deferred; four contests handed to students. Plan re-versioned v1.0 → v1.1. |

---

## Pending (post-Sprint 1)

| ID | Task | Added | Context |
|----|------|-------|---------|
| **S2.LATENT** | **Sprint 2: integrate latent variables L01–L40 into Tagging_Contractor (cognitive / affect / perception layer; V2.6 Parts I–IX). DO NOT FORGET — the registry currently covers only 18 of the 58 latents in V2.6.** | **2026-04-26** | **See `SPRINT2_PLUS_LATENT_BACKLOG_L01-L40.md` in repo root for the full self-contained brief: scope, inherited infrastructure from Sprint 1, new panel composition (Kahneman, Treisman, Gibson, Damasio, Russell, Kaplan, Ulrich, Spohn), BN identifiability concern at 63 latent nodes, estimated 15–20 working days, and the first-day actions when reactivated. Trigger: Sprint 1 (TOP-009) closes (Phases F, F.5, G complete + PR merged) AND downstream consumers begin extractor integration.** |
| S2.* | Sprint 2 follow-on: implement the 18 extractor stubs created in S1.E | 2026-04-26 | Inherited contract: distance-zone + F-formation geometry outputs. Independent of S2.LATENT but compatible. |
| S2.RT | Evaluate ranking-theoretic encoding for L46, L52, L53 | 2026-04-26 | Spohn deferral from Sprint 1 panel disposition |
| S2.L42b | Decide whether to split L42 into exposure / civil-inattention-support | 2026-04-26 | Goffman Sprint-1 deferral |
| S4.split | Decide whether to split top-level domain into `interaction_order` / `social_organization` | 2026-04-26 | Goffman deep-architectural Sprint-1 deferral |

---

## Branch Records

See `SPRINT1_BRANCH_LEDGER.md` for the explicit branch-cut record.
