# Tagging_Contractor Rescue And Interface Plan — 2026-04-20

## What this repo is

Tagging_Contractor is not the whole image-tagging application. It is the
**registry, semantics, governance, and extractability-planning layer** for the
CNFA tag system.

At present it already contains four distinct product surfaces:

1. **Registry source of truth**
   - `core/trs-core/v0.2.8/registry/registry_v0.2.8.json`
   - This defines the 424 tags, their semantics, and their extraction notes.

2. **CLI and audit surface**
   - `./bin/tc`, `scripts/audit.py`, `scripts/doctor.py`,
     `scripts/validate_registry.py`, `scripts/release.py`
   - This is the operational control plane for maintainers.

3. **Backend API**
   - `backend/app/routes.py`
   - `backend/app/routes_search.py`
   - `backend/app/routes_proposals.py`
   - This already exposes registry read APIs, fuzzy search, suggestion, and
     proposal/review endpoints.

4. **Prototype UI**
   - `frontend_streamlit/app.py`
   - This is a serviceable maintainer console, not yet a coherent user-facing
     product.

## The present problem

The repo has two difficulties.

### 1. It is operationally cluttered

The worktree was obscured by local backup debris:

- `Archive 2/`
- `Random Files Saved/`
- backup Dockerfiles
- local checksum sidecars
- local report snapshots

These are not the product. They are local residue. The first cleanup step is to
ignore them so the source tree again shows the real code.

### 2. The course materials blur two different systems

The Knowledge Atlas materials describe Track 1 in two different ways:

- In some places, Track 1 means **registry and scientific tagging logic**:
  triage tags, define operationalizations, validate extractability, build tag
  passports.
- In other places, Track 1 means the **full image-tagger product** with upload,
  automated extractors, review workflow, and stimulus-image linking.

Those are related, but they are not the same repo.

The important distinction is:

- **Tagging_Contractor** = defines *what* a tag means, what evidence it needs,
  and how it may be governed.
- **Image Tagger application** = implements *how* images are processed and
  reviewed operationally.

If this distinction is not made explicit, students are asked to build an
impossible mixture of registry governance, CV extraction, and polished product
UI in one term.

## What has just been cleaned

The first safe cleanup step has been applied in `.gitignore`:

- ignored local archive directories
- ignored backup Dockerfiles
- ignored local release checksum sidecars
- ignored `reports/snapshots/`

This does not delete anything. It simply stops local clutter from masquerading
as repository work.

## What should happen next

The development plan should separate the repo into five deliberate interface
surfaces, each tied to a user journey.

## Interface plan by user journey

### 1. Public Tag Explorer

**User:** researcher, student, contributor, curious visitor

**Question being answered:** "What does this tag mean, and how is it related to
the rest of the ontology?"

**Needed surface:**

- read-only tag browser
- tag detail page
- alias and fuzzy search
- domain / subdomain filters
- extraction-phase badge
- evidence requirements badge (`2D`, `3D`, `computed`, `metadata`, `sensor`)
- links to example tags and related tags

**Current ingredients already exist:**

- `/registry`
- `/api/search`
- `/api/suggest`
- `frontend_streamlit/app.py` browser + inspector

**Work needed:**

- replace the maintainer-looking Streamlit presentation with a cleaner web
  explorer
- make it embeddable or callable from Knowledge Atlas journey pages

### 2. Contributor Proposal Desk

**User:** contributor, advanced student, domain curator

**Question being answered:** "How do I propose a new tag or a change to an
existing one without damaging the registry?"

**Needed surface:**

- submit new-tag proposal
- submit modify-tag proposal
- attach evidence DOI and rationale
- preview diff against current tag
- status tracking for submitted proposals

**Current ingredients already exist:**

- proposal models and endpoints in `backend/app/routes_proposals.py`
- proposal queue in `frontend_streamlit/app.py`

**Work needed:**

- make proposal creation easier than raw JSON editing
- add a structured diff preview
- show reviewer comments in a public, legible way

### 3. Reviewer And Release Console

**User:** instructor, maintainer, registry steward

**Question being answered:** "What is safe to approve, and is this registry
release fit to publish?"

**Needed surface:**

- pending proposal queue
- review decisions
- audit summary
- registry integrity status
- release preview and release notes

**Current ingredients already exist:**

- `scripts/doctor.py`
- `scripts/validate_registry.py`
- `scripts/release.py`
- reviewer endpoints in `routes_proposals.py`

**Work needed:**

- one consolidated release console
- explicit green / yellow / red gates
- version delta summary by release

### 4. Extractability Planner / Handoff Builder

**User:** Track 1 team, image-tagger implementer, contractor, research engineer

**Question being answered:** "Which tags can actually be built from a given kind
of evidence, and what is the next operational batch?"

**Needed surface:**

- filter tags by required evidence phase
- group by method family
- export next-batch worklists
- show blocked tags and the reason they are blocked

**Current ingredients already exist:**

- handoff zips in `reports/`
- extraction audits and notes in the registry
- localized specification documents in `docs/neuroarch_localized_spec/`

**Work needed:**

- promote this from static zip bundles to an explicit planner interface
- tie it to the class-track deliverables

### 5. Downstream Consumer API

**User:** Knowledge Atlas, Article Finder, image-tagger system, future GUI work

**Question being answered:** "How does another system reliably query and consume
the registry without copying it badly?"

**Needed surface:**

- stable read API for registry and contracts
- search API
- versioned schema/contract endpoints
- client examples

**Current ingredients already exist:**

- `/registry`
- `/contracts/latest`
- `/schemas/...`
- `/resolve`
- `/api/search`
- `/api/suggest`

**Work needed:**

- publish this as a stable contract, not merely as app routes
- add one or two client examples for Atlas consumers

## Recommended development order

1. **Clarify the product boundary**
   - Amend Track 1 documentation so students are not told that
     Tagging_Contractor is the same thing as the full image-tagger application.

2. **Stabilize the read surfaces**
   - Public Tag Explorer
   - Downstream Consumer API

3. **Stabilize governance**
   - Contributor Proposal Desk
   - Reviewer And Release Console

4. **Then build the extractability planner**
   - This is the bridge to user journeys and to the class track.

## What the COGS 160 track should become if there are no takers

If Track 1 has no takers, the correct response is not to leave the repo vague.
It is to shrink the scope to a maintainable instructor-led or contractor-led
program.

### Minimum viable non-student program

1. **Registry maintenance lane**
   - keep tag semantics and extractability fields coherent

2. **Planner lane**
   - produce validated batches of tags for downstream implementation

3. **Interface lane**
   - build the Public Tag Explorer and Proposal Desk so later students or
     contributors can enter the system sanely

### What should not be promised

Do not promise that this repo by itself will deliver:

- the full image-tagging application
- complete CV extractor implementation
- a polished experimental stimulus browser

Those are adjacent systems.

## Recommendation for immediate next work

### Immediate engineering next step

Build a small, stable **Tag Explorer** page on top of the existing API. That is
the missing public surface and the natural first interface for several user
journeys.

### Immediate documentation next step

Patch the Track 1 materials in Knowledge Atlas so they say plainly:

- Tagging_Contractor defines the tag ontology and governance layer.
- The separate image-tagger system implements the operational image pipeline.
- Track 1 work may touch both, but they are not the same codebase.

### Immediate class-track next step

If there are still no student takers, reframe the track as a smaller
contractor-style workstream with three deliverables:

1. tag triage and bilingual augmentation
2. extractability-planner worklists
3. tag explorer and proposal interface

That is intellectually coherent and operationally achievable.
