---
name: prd-writer
description: "Turns a BRD, an MRD, or a rough idea into a Product Requirements Document, and evolves it as a living decision record from early hypothesis through launch readiness and impact review. Use whenever the user mentions a PRD, product spec, feature requirements, product roadmap planning, or asks what the product should do; not for purely technical design documents, which are a TRD."
---

# PRD Writer

Stage 3 of the spec-writer chain. Reads a BRD, an MRD, or a brief; feeds `design-spec-writer`, `trd-writer`, and `qa-test-plan-writer`.

Build the PRD to match the team's current confidence and the decision it needs to enable. Don't pretend an early hunch has launch-ready certainty, and don't force every request through every stage.

Start by identifying the current stage, the audience, the decision being made, and the unknowns. Where those aren't clear, make reasonable assumptions and label them; ask only where the missing answer materially changes product direction.

**Scope and platforms:** if the upstream document declares them, carry both into this document's header block verbatim and don't ask again. If no upstream document exists and you're the first in the chain, ask the user once — scope (product, feature, or change) and target platforms (web, iOS, Android, macOS, Windows, Linux, API, or undecided) — in a single batched question with a recommendation attached, exactly as the `mrd-writer` scope-and-platforms question describes. Record the answer; never pick silently.

## Reading the upstream documents

This stage reads the BRD or MRD. In a repository the documents are on disk, versioned, and possibly split per platform, so resolve them deliberately rather than taking the first file that matches.

| Upstream | Where it lives |
|---|---|
| BRD | `docs/brd-writer/<slug>-brd-v*.md` |
| MRD | `docs/mrd-writer/<slug>-mrd-v*.md` |

1. **Look in the producing skill's folder**, or in the project's documentation directory where one replaces `docs/`.
2. **Take the highest version.** Compare `v<major>.<minor>.<patch>` numerically, so `v0.0.10` is newer than `v0.0.9`. Never read an older version just because it came up in conversation. If the user names an older one deliberately, use it and say so in the header block.
3. **Match the platform.** Where you are producing a per-platform document, read the upstream file for *that* platform — the iOS document is built from the iOS upstream, not from the set. Where the upstream was written as a single file with no platform token, every platform reads that one.
4. **Cite the exact filename** in `**Upstream:**`, version and platform included — `invoice-tracker-prd-ios-v0.2.0.md`. Where this stage reads several documents, list them all, comma-separated; a missing one reads as "written without it". That line is what makes the staleness check mechanical: a reviewer compares it against the newest upstream file on disk.
5. **On a re-run, diff rather than redraft.** Your own previous version file names the upstream version it was built from. Compare that against the upstream you just resolved, and change only what the difference requires.

Outside a repository — a pasted document, an attachment, or a document drafted earlier in this conversation — apply the same rules to what you were given, and where the version genuinely isn't knowable write `**Upstream:** <name> (version unknown)` rather than inventing one.

## Where the input comes from

- **From a BRD** — each `BR-xx` becomes one or more product requirements. The BRD's objectives become the PRD's outcomes, and each carries the `GOAL-xx` the objective cited, so `MET-xx` can trace through to it; its scope boundary becomes the PRD's non-goals; its constraints carry over untouched.
- **From an MRD** — the `NEED-xx` items become the requirement seed list, and the market evidence becomes the problem statement. Note that no one has signed off on scope or budget yet.
- **From a brief** — fine. Say in the header that it's derived from an informal brief, and expect the Assumptions section to carry more weight.

## Feature scope

This is where most feature work starts, because a feature rarely needs an MRD or a BRD. When the input is an addition to an existing product:

- **Inherit the product context.** Personas, platforms, metrics framework, design system, and compliance posture come from the product's existing documents. Cite them; don't restate them. The PRD's job here is the delta.
- **State what it touches.** Name the existing screens, flows, shared components, API contracts, and data this feature modifies. This is the single most useful section in a feature PRD — it becomes the design spec's changed-screen list, the TRD's blast radius, and the test plan's regression scope.
- **Namespace the IDs** with a short feature slug — `PR-EXPORT-01` — so this feature's requirements merge into the product's set without colliding.
- **Pick the stage honestly.** Most features enter at stage 2 or 4 rather than stage 1; a small one may only ever need stage 5. Don't walk a two-week feature through six stages.
- **Say what it doesn't change.** An explicit non-goals list matters more at feature scope than product scope, because a feature sits inside working software and the obvious question is how far it reaches.

The six stages below still apply — they're about confidence and the decision at hand, not document size. A feature simply moves through them faster and with shorter sections.

## Six stages

### 1. Team kickoff — the speclet

For an early opportunity with a business metric to move and a well-supported user-problem direction, but no settled problem framing or solution. Capture only:

- Opportunity / title
- Target user and current pain
- Business outcome and leading signal
- Best current hypothesis
- Known unknowns and exploration owners

Its job is shared starting context for product, design, and engineering — not approval of a solution.

### 2. Planning review — the one-pager

For when exploration has sharpened the problem and a roadmap or investment decision is needed. Add:

- Problem statement, evidence, and affected user segment
- Why now, strategic fit, and alternatives considered
- Desired outcome, measurable success criteria, and guardrails
- Proposed scope, explicitly out of scope
- Risks, dependencies, and the decision requested

Write for leadership: concise, decision-oriented, honest about unresolved choices.

### 3. Cross-functional kickoff

For inviting stakeholders into the solution space before it hardens — design, engineering, data, marketing, support, legal, privacy, compliance, operations, QA, as relevant. Update the PRD with:

- Initial user journey and supporting data
- Stakeholder inputs needed, named owners, decision dates
- Privacy, policy, accessibility, localization, support, and go-to-market considerations where relevant
- Assumptions to validate and open questions

Don't manufacture stakeholder sections that don't apply.

### 4. Solution review

For when exploration is mature enough to choose a direction. State the recommendation and the reasoning rather than presenting a pile of unranked options. Document:

- Chosen solution and user flows
- Key requirements and acceptance criteria at the product level
- Alternatives rejected, and why
- Experiment, prototype, research, or feasibility evidence
- Trade-offs, risks, rollout approach, approval needed

For major bets, turn this into a presentation-ready narrative without losing the source-of-truth PRD.

### 5. Launch readiness

The engineering-ready contract, after cross-functional feedback and solution decisions are complete. Coordinate with the TRD rather than duplicating implementation detail. Make concrete:

- Final scope and non-goals
- Functional requirements, flows, states, edge cases, failure behavior
- Metrics instrumentation: events, properties, dashboards, success thresholds, guardrails
- Quality requirements: accessibility, privacy, performance, security, localization, platform policy as applicable
- Dependencies, rollout and rollback plan, QA scenarios, support and marketing readiness
- Remaining decisions, owners, sign-off status

Use unambiguous language. Every requirement must be testable — but avoid prescribing technical architecture unless a product constraint genuinely requires it.

### 6. Impact review

Launch is a learning milestone, not the end of the document. Add a linked results write-up or a concise outcome section:

- Release date, audience, rollout status
- Actual results versus targets and guardrails
- User and operational feedback
- Decision: expand, iterate, hold, or roll back
- Follow-up work, owners, and what changed in the product

This makes the PRD traceable from original hypothesis to outcome.

## PRD Template

<!-- include-start: references/template.md -->
Read `references/template.md` in this skill folder before drafting, and follow it exactly — section list, header block, Revision History, the stage rule, and the absent-section markers.
<!-- include-end -->

## User stories

Where the PRD expresses requirements as stories, write them in the standard form — *As a [persona], I want [capability], so that [outcome]* — and hold each to **INVEST**: Independent, Negotiable, Valuable, Estimable, Small, Testable. The *so that* clause is not decoration; a story that can't state its outcome usually can't justify its existence.

Give every story acceptance criteria in Given/When/Then form, which is what makes them directly consumable by `qa-test-plan-writer`:

> **Given** an account with at least one invoice past its due date
> **When** the user opens the overdue view
> **Then** each overdue invoice is listed with client, amount, and days overdue, sorted by days overdue descending

## Requirement table

From stage 4 onward, requirements live in a table so the design spec, TRD, and test plan have stable anchors to cite:

| ID | Requirement | Platforms | Acceptance criteria | Priority | Upstream |
|---|---|---|---|---|---|
| PR-01 | A user can see all overdue invoices across clients in one view | All | Given ≥1 invoice past its due date, the overdue view lists each with client, amount, and days overdue, sorted by days overdue descending | Must | BR-01 |
| PR-08 | A user can capture a receipt photo and attach it to an invoice | iOS, Android | Given camera permission is granted, capturing a photo attaches it to the invoice and queues upload; offline captures sync on reconnect | Should | BR-09 |

Every requirement names its platforms — `All` for the common case, a subset when it diverges. Inside a single file, where the same requirement behaves differently per platform, keep one row and put the difference in the acceptance criteria rather than splitting it into near-duplicate rows that drift apart. The column stays useful even in a per-platform file: it says which sibling files carry the same ID, which is what lets a reviewer read the set side by side.

Parity intent is carried into Section 5 — see that section; it is stated once there and referenced everywhere else.

Every requirement is one behavior. Split compound statements — "a user can cancel and receives a confirmation email" is two requirements, because each can fail independently. Every requirement needs an acceptance criterion a tester could observe; "works as expected" is not one.

Never invent a parent ID. A row with no real upstream is marked `[no upstream — new in this document]` in the Upstream column and repeated in Assumptions and Open Questions — an orphan is either a gap in the parent document or scope creep, and both need a human.

## Release plan and decision log

Sections 12 and 13 specify both; this is only about when they earn their place. Both are stage-5 sections — a launch-ready PRD needs them and an early-stage one doesn't, so a speclet marks them `Not yet — stage 5` rather than filling them with intentions.

The decision log is the part of a PRD that still has value a year later: it stops a settled question being reopened every sprint. Start it at stage 3, as soon as decisions are actually being made, rather than waiting for launch readiness.

## Writing principles

- Separate facts, assumptions, decisions, and open questions. Date material changes.
- Tie scope to a user problem and a measurable outcome; avoid feature lists without rationale.
- Use the smallest document that enables the next decision. Expand as confidence and execution needs grow.
- Preserve decision history: amend superseded decisions instead of silently rewriting them.
- Keep product requirements distinct from technical implementation. Link the TRD when one exists.
- Carry the platforms declared in MRD Section 5 into the header block, and specify what each one owes in Section 9 — that section is where per-platform detail lives, so it is written there once rather than repeated across the document. Where no platform is declared, write neutrally — "opens," "selects," "confirms" — rather than "taps" or "clicks." What each platform owes at this layer:
  - **Web** — supported browsers and the minimum version bar, responsive breakpoints, SEO and shareable-URL requirements, whether it installs as a PWA, and what works offline.
  - **Mobile** — supported OS versions, every permission requested and the moment it's asked for, offline behavior and conflict resolution on sync, push notifications, deep links, background activity, and App Store / Play policy implications.
  - **Desktop** — supported OS versions, window behavior and sizing, native menu and keyboard-shortcut expectations, file-system access, how the app updates itself, whether it launches at login, and how it is distributed (direct download, Mac App Store, MSI, Homebrew, package manager).
  - **Multi-platform** — parity intent belongs in Section 5, stated outright: full parity, a reduced scope on one platform, or capability that exists on only one. Then specify shared behavior once and list only the deltas.

## Standards this follows

Stories follow the standard *As a / I want / so that* form held to **INVEST**, with acceptance criteria in **Given/When/Then**, so they transfer directly into test cases. Prioritization uses **MoSCoW** (Must/Should/Could/Won't) or a stated equivalent. Requirements stay at the product layer — the technical specification layer is the TRD's, per the document separation in **ISO/IEC/IEEE 29148:2018**.

## Quality bar before delivering

- `**Stage:**` is declared, and the sections the stage table requires are genuinely filled — not stubbed with a heading and a sentence.
- Every section not filled carries `Not yet — stage <n>`, `Not applicable — <reason>`, or `Insufficient evidence — <what would resolve it>`.
- `**Upstream:**` names the exact BRD or MRD filename with its version, and it is the newest one on disk.
- Revision History carries a row for this version, with the `PR-xx` and `MET-xx` IDs added, changed, and removed since the previous one.
- Every `PR-xx` is one behavior — no requirement containing "and" that could fail in two ways.
- Every `PR-xx` has an acceptance criterion a tester could observe; "works as expected" is not one.
- Every `PR-xx` and `MET-xx` cites a real parent, or carries `[no upstream — new in this document]` and a Section 15 entry. Never a dash.
- Every quality requirement in Section 8 has a `PR-xx` ID, so the TRD can cite it.
- Every metric names its type, a number, a baseline, and its instrumentation.
- Every requirement names its platforms, and the parity intent from MRD Section 5 is carried into Section 5 here.
- Non-Goals is specific and real — a placeholder there makes the section worthless.
- From stage 5: release plan states a rollout mechanism and a kill switch, and the decision log has rows.
- Where the set is per-platform, every platform file is bumped in the same run and shared `PR-xx` text is identical between them.
- Nothing names a database, a queue, a component prop, or an endpoint — that's the TRD and the design spec.

## Output format

**This document set always ends in a Markdown file. Never deliver it as ordinary chat prose.**

Deliver by the highest tier the environment supports:

1. **Filesystem available** (coding agent, IDE, terminal, code interpreter) — write `docs/prd-writer/<slug>-prd-v<version>.md`. Create `docs/` only if it is missing — never recreate or replace an existing one — then create the `prd-writer/` subfolder inside it if that is missing too, so each skill's output stays in its own folder. Where the project already has a documentation directory, use that in place of `docs/`, with the same `prd-writer/` subfolder inside it. Report the path.
2. **Files or a document surface, but no repo** (downloadable file, canvas, doc, notebook) — create it there named `<slug>-prd-v<version>.md` and hand over the download or link.
3. **Chat only** — put the entire document in one fenced code block tagged `markdown`, with nothing else inside the fence, and name the file the user should save it as: `<slug>-prd-v<version>.md`. Everything you want to say goes before the fence, never interleaved.

Use one consistent `<slug>` across every document in the chain for a given product — the same slug the first document in the chain started with — so the six files read as one set. At feature scope the slug is the feature, not the product. The folder is per skill, the slug is per product: `docs/prd-writer/<slug>-prd-v<version>.md`.

**Versioning.** Every write creates a new file; an existing version file is never overwritten or deleted.

Before drafting, list `docs/prd-writer/` and find the highest `v<major>.<minor>.<patch>` among files matching `<slug>-prd-v*.md`. Compare the three numbers numerically, so `v0.0.10` is newer than `v0.0.9`. That file is the previous version — read it first, so the new document is a revision rather than a restart.

- No previous file — start at `v0.0.1`.
- **Patch** (`v0.0.x`) — edits, corrections, gaps filled, wording.
- **Minor** (`v0.x.0`) — new sections or requirements, or a re-run against a revised upstream document.
- **Major** (`vx.0.0`) — **Status** reaches Approved, or a rewrite that invalidates the documents downstream of this one.

The `**Version:**` line in the header block always carries the same number as the filename, and every version appends a row to the document's **Revision History** — what changed, and which IDs were added, changed, and removed. Report the new path and that summary, not just that a file was written.

**The changelog is mandatory.** After writing the file, append one bullet to `docs/CHANGELOG.md` — at the root of `docs/`, beside the per-skill subfolders — under today's ISO date heading, creating the file or the heading if either is missing:

```markdown
- **PRD** `prd-writer/<filename>` — <one-line summary>. +<IDs added>, ~<IDs changed>, -<IDs removed>. Upstream `<upstream path>` (every upstream, comma-separated, or "informal brief" where there is none).
```

The IDs must match the Revision History row for this version. Never edit a past entry — a correction is a new version with a new entry. Per-platform writes get one bullet each — and where this stage writes a single file whatever the platform set, that file gets one bullet. The document is not delivered until this entry exists.

**Per-platform documents.** Where the header block declares more than one platform, produce one complete PRD per platform — not a shared document with a platform column doing the work. Each file is standalone and whole: every section filled for that platform, shared behavior written out in full rather than cross-referenced.

`docs/prd-writer/<slug>-prd-<platform>-v<version>.md`, one file per declared platform. The `<platform>` token comes from this fixed vocabulary, so filenames stay predictable: `web`, `ios`, `android`, `macos`, `windows`, `linux`, `api`.

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

Open the file with the header block from the PRD Template above, then its sections in order. **Assumptions and Open Questions** and **Next Steps** are mandatory at every stage — Section 17's four-line block is this document's Next Steps, and it stays even in a speclet.

## Reviewing an existing PRD

When asked to review rather than write, identify its likely stage, what is decision-ready, what is premature or missing for the next stage, and the smallest concrete edits needed to get there. Report against the template's section numbers so the gaps are addressable.

## How a PRD differs from the rest of the chain

The MRD argues the market is real and the BRD argues the business should fund it; the PRD decides what the product does about it. It stays at the product layer — behavior a user can observe — and hands architecture, data models, and endpoints to the TRD, screens and states to the design spec, and coverage to the test plan. When a sentence in the PRD names a database, a queue, or a component prop, it belongs one layer down.

## Handing off

Once the PRD reaches stage 4–5, it can feed three documents in parallel: `design-spec-writer` for user-facing surface area, `trd-writer` for the engineering blueprint, and `qa-test-plan-writer` for coverage. Each cites `PR-xx` IDs, so keep those stable — renumber only when a requirement is genuinely removed, and note the removal rather than silently reusing the ID.
