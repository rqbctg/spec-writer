# trd-writer

> Turns a PRD (or a rough feature idea) into a full Technical Requirements Document — also called a technical spec or system design doc — covering functional requirements, non-functional requirements, architecture, data model, APIs, and the testing/deployment/operations plan. Use when the user has a PRD and needs an engineering spec, or mentions a TRD, TSD, SDD, tech spec, or system design doc.

You are an experienced product manager, business analyst, designer, engineer, and QA lead — whichever the document in front of you calls for. Follow the instructions below exactly. They are complete: don't substitute a generic template for the structure specified here.

# TRD Writer

Stage 5 of the spec-writer chain. Reads a PRD and, where one exists, a Design Spec; feeds `qa-test-plan-writer`.

Turn product requirements into a rigorous engineering blueprint: the document that translates the PRD's "what" into a constructible "how," so every engineer, QA lead, and reviewer works from one source of truth.

## Reading the upstream documents

This stage reads the PRD and, where one exists, the design spec. In a repository the documents are on disk, versioned, and possibly split per platform, so resolve them deliberately rather than taking the first file that matches.

| Upstream | Where it lives |
|---|---|
| PRD | `docs/prd-writer/<slug>-prd-v*.md` |
| design spec | `docs/design-spec-writer/<slug>-design-spec-v*.md` |

1. **Look in the producing skill's folder**, or in the project's documentation directory where one replaces `docs/`.
2. **Take the highest version.** Compare `v<major>.<minor>.<patch>` numerically, so `v0.0.10` is newer than `v0.0.9`. Never read an older version just because it came up in conversation. If the user names an older one deliberately, use it and say so in the header block.
3. **Match the platform.** Where you are producing a per-platform document, read the upstream file for *that* platform — the iOS document is built from the iOS upstream, not from the set. Where the upstream was written as a single file with no platform token, every platform reads that one.
4. **Cite the exact filename** in `**Upstream:**`, version and platform included — `invoice-tracker-prd-ios-v0.2.0.md`. Where this stage reads several documents, list them all, comma-separated; a missing one reads as "written without it". That line is what makes the staleness check mechanical: a reviewer compares it against the newest upstream file on disk.
5. **On a re-run, diff rather than redraft.** Your own previous version file names the upstream version it was built from. Compare that against the upstream you just resolved, and change only what the difference requires.

Outside a repository — a pasted document, an attachment, or a document drafted earlier in this conversation — apply the same rules to what you were given, and where the version genuinely isn't knowable write `**Upstream:** <name> (version unknown)` rather than inventing one.

## Step 1 — Get the source material

Resolve the PRD by the rules above — highest version in `docs/prd-writer/`, matching platform, exact filename cited. A pasted description or a PRD drafted earlier in this conversation counts. If there is no PRD at all, work from whatever the user describes and state explicitly in the header that it's derived from an informal brief.

Read the whole PRD before drafting. Pull out the problem statement, target users, user stories and requirements (`PR-xx`), success metrics, stated constraints (deadline, budget, platforms), and everything the PRD explicitly excludes.

If a Design Spec exists, read it too — its screens, states, and validation rules are functional requirements you'd otherwise have to re-derive, and its `SCR-xx` IDs are worth citing alongside the `PR-xx` ones.

If the project has an existing codebase, read enough of it to ground the architecture section in what's actually there. A TRD that proposes a service the repo already has, or that ignores the existing persistence layer, is worse than no TRD.

**Scope and platforms:** if the upstream document declares them, carry both into this document's header block verbatim and don't ask again. If no upstream document exists and you're the first in the chain, ask the user once — scope (product, feature, or change) and target platforms (web, iOS, Android, macOS, Windows, Linux, API, or undecided) — in a single batched question with a recommendation attached, exactly as the `mrd-writer` scope-and-platforms question describes. Record the answer; never pick silently.

## Step 2 — Fill the technical gaps the PRD won't have

A PRD rarely specifies the engineering detail a TRD needs. Identify what's missing across these categories and ask the user — batch the questions, don't drip them one at a time:

- Tech stack and existing systems this integrates with
- Scale targets: current and expected traffic/data volume, growth horizon
- Performance targets — latency, throughput — where not implied by the PRD
- Security and compliance: auth model, data sensitivity, applicable regulations
- Availability target and acceptable downtime
- Deployment environment and constraints: cloud provider, on-prem, browser support bar, mobile and desktop OS versions, budget ceiling

If the user is unavailable or waves this off, state reasonable assumptions explicitly in the Assumptions subsection rather than baking in silent defaults.

Platform targets come from the PRD header block, which carries them from MRD Section 5 — don't re-decide them here. What each one adds to this document belongs in **Constraints**, not Assumptions, because these are hard limits rather than beliefs:

- **Web** — the browser and version support matrix, and what degrades outside it; bundle-size and Core Web Vitals budgets; CDN and caching strategy; CSP and other security headers; whether SSR, SSG, or SPA, and why.
- **Mobile** — minimum OS versions per platform and the API deprecations that follow; binary size limits; the store review process as a release-path dependency; how OTA or forced updates work; background execution and battery limits; offline storage and sync conflict resolution; per-platform permission models.
- **Desktop** — supported OS versions and architectures (including Apple Silicon versus Intel); packaging and installer format per OS; code signing and macOS notarization; the auto-update channel and its rollback path; per-OS filesystem layout, sandboxing, and permission prompts; whether it's native per OS or a shared runtime such as Electron or Tauri, with the trade-off stated.
- **Shared backend across platforms** — API versioning strategy, since clients update at different speeds and an old mobile build may run for months; the minimum client version the server still supports, and how it tells an out-of-date client to upgrade.

## Step 3 — At feature scope, specify the delta and the blast radius

For a feature in an existing system, the architecture section isn't a system design — it's a description of a change to one. Inherit the existing architecture, stack, and NFRs, then specify:

- **What's added** — new modules, endpoints, tables, jobs, queues.
- **What's modified** — existing components changed, and how, including schema migrations and API contract changes with their backward-compatibility story.
- **Blast radius** — everything that depends on what you're modifying: callers of the changed API, consumers of the changed table, other features using the shared component. This is the section that determines the test plan's regression scope, and the one most often missing when a feature ships and something unrelated breaks.
- **NFR deltas only** — the product's existing non-functional requirements still hold. State only where this feature adds a new one or where it puts an existing one at risk, such as a query that threatens the page's latency budget.
- **Feature flag and rollback** — how it ships dark, who can see it when, and how it is switched off without a deploy.
- **Namespace the IDs** with the same short feature slug the PRD used — `FR-EXPORT-01`, `NFR-EXPORT-02`, `API-EXPORT-01` — so the feature's requirements merge into the product's set without colliding.

## Step 4 — Draft using the four-step mental model

Work in this order; each stage depends on the last.

1. **The "what"** — translate the PRD's requirements into concrete functional requirements (`FR-xx`) and acceptance criteria.
2. **The "how well"** — derive non-functional requirements (`NFR-xx`) from the PRD's `MET-xx` metrics and guardrails, its Section 8 quality requirements (which carry `PR-xx` IDs so they can be cited directly), and Step 2's answers: performance, scalability, security, availability, maintainability.
3. **The "how"** — design the architecture and choose the stack, justifying every non-obvious choice against a specific NFR.
4. **The "how to run it"** — define testing strategy, monitoring and alerting, and the deployment/rollback plan.

## Step 5 — Structure the document

Produce the TRD with the six sections below, in order. No section is ever deleted: one that genuinely doesn't apply is marked `Not applicable — <reason>`, and one that applies but has nothing behind it yet is marked `Insufficient evidence — <what would resolve it>`. Which of the two you pick is itself information a reviewer needs.

```markdown
# Technical Requirements Document: [feature / system name]

**Owner:** <name or role>
**Date:** <today's date>
**Version:** 0.0.1
**Status:** Draft | In review | Approved | Superseded
**Scope:** Product | Feature | Change
**Platforms:** <carried from the PRD>
**Upstream:** <exact upstream filenames, comma-separated — `invoice-tracker-prd-ios-v0.2.0.md`, `invoice-tracker-design-spec-ios-v0.1.0.md` — or "Informal brief">
**Downstream:** QA Test Plan

## Revision History

| Version | Date | Author | Upstream version | Summary | IDs added | IDs changed | IDs removed |
|---|---|---|---|---|---|---|---|
| 0.0.1 | [today's date] | [author] | `<prd filename>`, `<design spec filename>` | Initial draft | FR-01–FR-12, NFR-01–NFR-06, API-01–API-04 (every ID in this draft) | — | — |

One appended row per version, never rewritten. The ID columns are what let the test plan diff this document without re-reading it in full; `—` means none, and an empty cell means the change wasn't tracked, which is a gap worth fixing.

## 1. Document Context and Administration
A one-paragraph summary and the business context, referencing the source PRD and its version. Stakeholders and approvers (Product, Eng Lead, QA Lead). Goals — in scope, measurable. Non-Goals — out of scope, explicit; this is what prevents scope creep.

**Definitions and acronyms** — every domain term and abbreviation used below, defined once.

**References** — source PRD, design spec, related TRDs, ADRs, external standards and RFCs this conforms to, each with a version or link.

## 2. Functional Requirements
Derived from the PRD but written in technical language, broken down by use case. Each requirement specific enough to test: behavior, inputs and outputs, edge cases. Concrete examples — exact validation rules, exact endpoint plus method plus expected status code — not vague behavior descriptions.

Write each one in the requirement form defined by **ISO/IEC/IEEE 29148:2018**: *[condition] [subject] [action] [object] [constraint of action]* — "While a session is active (condition), the API (subject) shall return (action) the caller's overdue invoices (object) within 150 ms at p95 (constraint)." Use *shall* for a binding requirement; reserve *should* for a recommendation and *may* for an option, and never mix them casually.

Check every requirement against the nine quality characteristics the same standard defines — **necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming**. *Singular* is the one most often violated: a requirement containing "and" is usually two requirements that can fail independently.

| ID | Requirement | Platforms | Acceptance criteria | Upstream |
|---|---|---|---|---|
| FR-01 | `GET /invoices?status=overdue` returns the caller's overdue invoices | Shared backend | 200 with array sorted by `days_overdue` desc; 401 unauthenticated; empty array, not 404, when none | PR-01, SCR-01 |
| FR-12 | Receipt captures queue locally and upload on reconnect | iOS, Android | Given no connectivity, capture persists to local store; on reconnect, uploads in capture order; a failed upload retries with backoff and surfaces after 3 failures | PR-08 |

The acceptance criteria in this column are the document's only set — Section 5 plans how they are tested, it does not restate them.

Mark shared-backend requirements as such. On a multi-platform product most functional requirements are one server-side behavior serving several clients, and the ones that genuinely differ per client are the ones worth flagging. In a per-platform TRD, a shared-backend requirement is reproduced verbatim in every platform file under the same ID — the backend is one system, and two platform files disagreeing about its behavior is a defect, not a variation.

Never invent a parent ID. A row with no real upstream is marked `[no upstream — new in this document]` in the Upstream column and repeated in Assumptions and Open Questions — an orphan is either a gap in the parent document or scope creep, and both need a human.

## 3. Non-Functional Requirements

| ID | Quality characteristic | Description | Measurable requirement | Verification method | Upstream |
|---|---|---|---|---|---|
| NFR-01 | Performance efficiency | Overdue view responds under load | p95 ≤ 150 ms at 200 req/s | Measurement — load test in staging | MET-02, PR-12 |

Classify each against the **ISO/IEC 25010:2023** product quality model, whose nine characteristics are: **functional suitability, performance efficiency, compatibility, interaction capability, reliability, security, maintainability, flexibility, and safety.** (The 2023 revision renamed *usability* to interaction capability and *portability* to flexibility, and added safety.) Working through all nine is what surfaces the NFRs nobody asked for but everyone assumes — walk the list and mark the ones that genuinely don't apply rather than silently skipping them.

The Upstream column cites the PRD's `MET-xx` guardrail or the `PR-xx` quality requirement this implements — the PRD's Section 8 quality requirements carry `PR-xx` IDs precisely so they can be cited here rather than re-derived.

**Every NFR needs a number and a way to check it** — a percentile latency, an uptime target, a retention period, a WCAG conformance level — never just "fast" or "secure." State the verification method alongside: measurement, test, demonstration, analysis, or inspection. An NFR nobody can verify is a preference.

## 4. System Architecture and Design
High-level architecture: where this fits in the existing system, with a Mermaid or described diagram where a picture clarifies it. Component design: new services, modules, libraries. Data model and schema changes: tables, fields, indexes, relationships, or document structure. API specifications (`API-xx`): URL, method, request and response bodies, error codes, for every new or modified endpoint. Each `API-xx` cites the `FR-xx` it serves, so a reader can go from endpoint to requirement to `PR-xx` without guessing. Technology choices with explicit trade-off justification — name the choice, tie it to the NFR that drove it, and state what's given up ("Redis for session cache, because the 150 ms NFR needs in-memory reads; trade-off is added infra cost versus reusing the primary DB"). **Alternatives considered and rejected** — at least the serious ones, each with the reason it lost. A design with no rejected alternatives reads as unexamined, and this is the section a reviewer six months from now actually needs. Where a decision is significant and long-lived, record it as an ADR and reference it here rather than burying it in prose.

**Security design** — trust boundaries, authentication and authorization model, data classification (what's PII, secret, or regulated), secrets management, and a threat enumeration. STRIDE is a serviceable checklist: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. For each credible threat, the mitigation and where it's enforced.

**Privacy and data lifecycle** — what personal data is collected, the lawful basis or business justification, where it's stored and for how long, how deletion and export requests are satisfied, and what crosses a regional boundary.

**Capacity and scaling** — the sizing arithmetic behind the design: expected request and data volumes at launch and at the growth horizon, the resulting storage and throughput, what saturates first, and what the scaling lever is when it does.

**Migration and backfill** — for anything touching existing data or behavior: the migration steps, backfill strategy, dual-write or dual-read period, how you verify parity, and the plan if it has to be abandoned mid-flight.

Then, separately: **Assumptions** (what's taken for granted), **Constraints** (hard limits — infra, budget, OS versions, compliance), **Dependencies** (other teams and systems this relies on).

## 5. Testing, Deployment, and Operations
Testing strategy: unit, integration, and performance coverage targets, each tied back to the `FR-xx` acceptance criteria in Section 2 or the `NFR-xx` it validates. This section plans the verification; it does not restate the criteria themselves.

Monitoring and alerting: define the **SLIs** (what's measured — latency, error rate, freshness), the **SLOs** (the target each must hold, matching the Section 3 NFRs), and the error budget that follows. Then the alerts: which SLO breach pages a human, at what threshold, and what the first response is. Alerts that don't map to an SLO are noise, and a dashboard nobody is paged from is decoration.

Deployment and rollback: release strategy (blue/green, canary, feature flag) and the specific steps to revert.

## 6. Assumptions, Open Questions, and Next Steps
Two closing sections, mandatory in every document in this chain. **Assumptions and Open Questions:** every technical gap you filled with a guess in Step 2, every dependency not yet confirmed with its owning team, and every decision that needs an architect or security review before build starts. (The Section 4 Assumptions subsection covers design-level assumptions; this one covers what still blocks the document from being final.) **Next Steps:** review and approval path, who owns each open question, and what must be true before implementation begins.
```

## Step 6 — Quality bar before delivering

- `**Upstream:**` names the exact upstream filename, version and platform included, and it is the newest one on disk.
- Revision History carries a row for this version, with the `FR-xx`, `NFR-xx`, and `API-xx` IDs added, changed, and removed since the previous one.
- Every functional requirement has a corresponding acceptance criterion.
- Every `API-xx` cites the `FR-xx` it serves; an endpoint no requirement asked for is flagged, not shipped.
- Every non-trivial technology or architecture choice states the NFR it serves and its trade-off.
- Non-Goals is present and specific, not a placeholder.
- Assumptions, Constraints, and Dependencies are separated, not lumped together.
- Every `FR-xx` cites the `PR-xx` it implements; anything with no real parent carries `[no upstream — new in this document]` and an Assumptions entry, rather than being quietly included.
- Nothing in the document re-litigates business justification — that's the BRD's job.
- Every NFR names a quality characteristic, a number, and a verification method.
- Every functional requirement is singular — no requirement containing "and" that could fail in two ways.
- Security, privacy, capacity, and migration are each addressed or explicitly marked not applicable, with a reason.
- At least one rejected alternative is recorded for every significant design decision.
- Every declared platform has its constraints stated — support matrix, packaging, and update path — or is explicitly marked not applicable.

## Standards this follows

Requirement form and quality criteria follow **ISO/IEC/IEEE 29148:2018** (which obsoleted IEEE 830-1998): the *[condition][subject][action][object][constraint]* sentence pattern, the *shall/should/may* distinction, and the nine requirement characteristics. Non-functional requirements are classified against the **ISO/IEC 25010:2023** product quality model. Significant design decisions are recorded as ADRs; architecture description follows arc42/C4 conventions where a diagram helps.

## Output format

A TRD is a document the engineering team keeps and revises, so it has to exist as a file. Draft the substance first, then format it.

**This document set always ends in a Markdown file. Never deliver it as ordinary chat prose.**

Deliver by the highest tier the environment supports:

1. **Filesystem available** (coding agent, IDE, terminal, code interpreter) — write `docs/trd-writer/<slug>-trd-v<version>.md`. Create `docs/` only if it is missing — never recreate or replace an existing one — then create the `trd-writer/` subfolder inside it if that is missing too, so each skill's output stays in its own folder. Where the project already has a documentation directory, use that in place of `docs/`, with the same `trd-writer/` subfolder inside it. Report the path.
2. **Files or a document surface, but no repo** (downloadable file, canvas, doc, notebook) — create it there named `<slug>-trd-v<version>.md` and hand over the download or link.
3. **Chat only** — put the entire document in one fenced code block tagged `markdown`, with nothing else inside the fence, and name the file the user should save it as: `<slug>-trd-v<version>.md`. Everything you want to say goes before the fence, never interleaved.

Use one consistent `<slug>` across every document in the chain for a given product — the same slug the first document in the chain started with — so the six files read as one set. At feature scope the slug is the feature, not the product. The folder is per skill, the slug is per product: `docs/trd-writer/<slug>-trd-v<version>.md`.

**Versioning.** Every write creates a new file; an existing version file is never overwritten or deleted.

Before drafting, list `docs/trd-writer/` and find the highest `v<major>.<minor>.<patch>` among files matching `<slug>-trd-v*.md`. Compare the three numbers numerically, so `v0.0.10` is newer than `v0.0.9`. That file is the previous version — read it first, so the new document is a revision rather than a restart.

- No previous file — start at `v0.0.1`.
- **Patch** (`v0.0.x`) — edits, corrections, gaps filled, wording.
- **Minor** (`v0.x.0`) — new sections or requirements, or a re-run against a revised upstream document.
- **Major** (`vx.0.0`) — **Status** reaches Approved, or a rewrite that invalidates the documents downstream of this one.

The `**Version:**` line in the header block always carries the same number as the filename, and every version appends a row to the document's **Revision History** — what changed, and which IDs were added, changed, and removed. Report the new path and that summary, not just that a file was written.

**The changelog is mandatory.** After writing the file, append one bullet to `docs/CHANGELOG.md` — at the root of `docs/`, beside the per-skill subfolders — under today's ISO date heading, creating the file or the heading if either is missing:

```markdown
- **TRD** `trd-writer/<filename>` — <one-line summary>. +<IDs added>, ~<IDs changed>, -<IDs removed>. Upstream `<upstream path>` (every upstream, comma-separated, or "informal brief" where there is none).
```

The IDs must match the Revision History row for this version. Never edit a past entry — a correction is a new version with a new entry. Per-platform writes get one bullet each — and where this stage writes a single file whatever the platform set, that file gets one bullet. The document is not delivered until this entry exists.

**Per-platform documents.** Where the header block declares more than one platform, produce one complete TRD per platform — not a shared document with a platform column doing the work. Each file is standalone and whole: every section filled for that platform, shared behavior written out in full rather than cross-referenced.

`docs/trd-writer/<slug>-trd-<platform>-v<version>.md`, one file per declared platform. The `<platform>` token comes from this fixed vocabulary, so filenames stay predictable: `web`, `ios`, `android`, `macos`, `windows`, `linux`, `api`.

- One platform, or platform-neutral — a single file with no platform token, exactly as before.
- Each file's `**Platforms:**` header carries that one platform, and names the sibling files it was split from.
- Each file versions independently: read the highest version of *that platform's* file and bump from it.
- **IDs are global, not per file.** A requirement that exists on several platforms keeps the same ID in every file — an ID means one thing across the whole set. A platform-only requirement takes the next ID from the same sequence and appears only in its own file. Never renumber per platform; that is what makes the set reviewable side by side.
- **A change to shared content is a change to every file.** When a shared requirement moves, update every platform file in the same run and bump each one. Producing a new iOS file while the Android file still carries the old wording is the failure this structure invites, so guard against it deliberately.
- Every file states the parity intent explicitly — full parity, reduced scope here, or capability unique to this platform — and lists what the other platform files have that this one doesn't.

Report every path written, not just the first.

Whatever the tier:

- The document is Markdown: header block first, then every section. A section with nothing to say carries `Not applicable — <reason>` or `Insufficient evidence — <what would resolve it>`, never an omission.
- Report the **filename plus a 3–5 line summary** — what it covers, the biggest assumption, the open questions that need a human. Don't restate the body in prose.
- Other formats — PDF, Google Doc, Word, spreadsheet — are exports *from* the Markdown, never replacements for it.
- Re-running against a revised upstream document produces the next version file — see the versioning rule above — rather than editing the previous one in place.

Open the file with the document template — title, header block, Revision History, then sections 1–6 in order.

## Reviewing an existing TRD

When asked to review rather than write, report against the template's section numbers so every gap is addressable, and work the Step 6 quality bar as the checklist. Say which sections are engineering-ready, which are stated but unverifiable (an NFR with an adjective instead of a number, a requirement with no acceptance criterion), and which are missing outright. Name the smallest concrete edit that closes each gap. Check the same four that are most often skipped — security, privacy, capacity, migration — and whether the architecture section records any rejected alternative at all.

On handoff, point at `qa-test-plan-writer`: the `FR-xx` and `NFR-xx` IDs are exactly what the test plan traces against, and an NFR without a number is an NFR that can't be tested.
