---
name: brd-writer
description: "Turns an MRD or a plain description of a project into a full Business Requirements Document (BRD) covering executive summary, objectives, scope, business requirements, stakeholders, constraints, and cost-benefit analysis. Use whenever the user mentions a BRD, business requirements, wants to formalize a project idea or MRD for stakeholder sign-off, or asks what a project needs before development starts."
---

# BRD Writer

Stage 2 of the spec-writer chain. Reads an MRD (or a brief); feeds `prd-writer`.

## What this does

Takes an existing Market Requirements Document or a plain-language project description — a paragraph, a bullet list, a rough brief — and turns it into a complete Business Requirements Document: the formal report that aligns stakeholders on what a project is, why it's happening, and what it will take to deliver. A BRD answers "what business outcome should this support," "what's in and out of scope," "who signs off," and "is this worth the cost." It stays at the business level; it does not specify how the system works.

An MRD input is the common case: the MRD explains the market opportunity, and the BRD is the natural next step once someone decides to greenlight a project around it — translating market validation into a business-outcome-and-scope document a sponsor can approve. This works just as well from a few sentences with no prior document.

## Reading the upstream documents

This stage reads the MRD. In a repository the documents are on disk, versioned, and possibly split per platform, so resolve them deliberately rather than taking the first file that matches.

| Upstream | Where it lives |
|---|---|
| MRD | `docs/mrd-writer/<slug>-mrd-v*.md` |

1. **Look in the producing skill's folder**, or in the project's documentation directory where one replaces `docs/`.
2. **Take the highest version.** Compare `v<major>.<minor>.<patch>` numerically, so `v0.0.10` is newer than `v0.0.9`. Never read an older version just because it came up in conversation. If the user names an older one deliberately, use it and say so in the header block.
3. **Match the platform.** Where you are producing a per-platform document, read the upstream file for *that* platform — the iOS document is built from the iOS upstream, not from the set. Where the upstream was written as a single file with no platform token, every platform reads that one.
4. **Cite the exact filename** in `**Upstream:**`, version and platform included — `invoice-tracker-prd-ios-v0.2.0.md`. Where this stage reads several documents, list them all, comma-separated; a missing one reads as "written without it". That line is what makes the staleness check mechanical: a reviewer compares it against the newest upstream file on disk.
5. **On a re-run, diff rather than redraft.** Your own previous version file names the upstream version it was built from. Compare that against the upstream you just resolved, and change only what the difference requires.

Outside a repository — a pasted document, an attachment, or a document drafted earlier in this conversation — apply the same rules to what you were given, and where the version genuinely isn't knowable write `**Upstream:** <name> (version unknown)` rather than inventing one.

## Workflow

### Step 1 — Understand the input

**From an MRD:** read it in full and map what carries over — the problem and opportunity become context for objectives; the target audience becomes stakeholder and user context; the `GOAL-xx` business goals become project objectives, keeping their IDs as the objectives' upstream; the `NEED-xx` items become the starting point for business requirements, reframed as business needs rather than product features. Note what an MRD does *not* give you and a BRD needs: a concrete scope boundary, a stakeholder roster, project constraints, and a cost-benefit analysis. Derive or assume those, and label them.

**From plain text:** identify what the project is, who wants it, and what problem it solves. Most of the rest will be inferred or flagged as an assumption — expected and fine.

### Step 2 — Carry scope and platforms forward

If the MRD declares them, copy both into this document's header block verbatim and don't ask again. If there's no MRD and this is the first document in the chain, ask the user once — scope (product, feature, or change) and target platforms (web, iOS, Android, macOS, Windows, Linux, API, or undecided) — in a single batched question with a recommendation attached, exactly as the `mrd-writer` scope-and-platforms question describes. Record the answer; never pick silently.

Scope then decides whether this document is needed at all. A BRD exists to get a project approved and funded. At **feature scope** that's usually already true — the product is funded, the team exists, and the sponsor signed off long ago. Write one for a feature only when it needs its own money, headcount, vendor, or formal sign-off, or when it carries a compliance or contractual obligation.

When you do, inherit the product's stakeholders, constraints, and glossary rather than rebuilding them, and keep the document to what this feature changes: its objectives, its scope boundary, its incremental cost, and its risks. Otherwise say so plainly and point the user at `prd-writer`.

### Step 3 — Ask only if genuinely stuck

Don't interrogate the user. A BRD can be drafted from thin input as long as gaps are handled honestly. Ask only when something is unknowable *and* materially changes the document — the input is ambiguous between two very different projects, or the cost-benefit analysis needs figures there's no reasonable way to estimate. Batch the questions into one pass.

### Step 4 — Draft the BRD

Use the document template. Keep every section at the business level — if you catch yourself describing UI, a tech stack, or step-by-step system behavior, cut it or reframe it as a business need ("users need to see overdue invoices at a glance" rather than "add a red badge to the dashboard").

Classify each requirement the way BABOK v3 does, because the four types get approved by different people and satisfied by different work: **business** (the enterprise-level outcome), **stakeholder** (what a specific group needs), **solution** (functional and non-functional capability), and **transition** (temporary — migration, training, cutover — retired once the change lands). Transition requirements are the ones teams forget until go-live week.

Give each business requirement a `BR-xx` ID, a type, a priority, a one-line rationale, and the `NEED-xx` it traces to — or the `GOAL-xx` where the requirement serves a business outcome rather than a customer need. A requirement with no upstream need is either a gap in the MRD or scope creep — mark it `[no upstream — new in this document]` and raise it in Section 11.

At feature scope, namespace the IDs with the feature's slug — `BR-EXPORT-01` — so this feature's requirements merge into the product's set without colliding. Use the same slug the feature's other documents use.

### Step 5 — Write the executive summary last

Draft every other section first, then come back to the summary. Writing it last is what makes it accurate rather than a guess at what the document will say.

### Step 6 — Quality bar before delivering

- `**Upstream:**` names the exact MRD filename with its version, and it is the newest one on disk.
- Revision History carries a row for this version, with the `BR-xx` IDs added, changed, and removed since the previous one.
- Every objective in Section 2 cites the `GOAL-xx` it inherits, or carries `[no upstream — new in this document]` and an entry in Section 11.
- Every `BR-xx` has a type, a priority, a Platforms value, a rationale, and a real upstream ID — never an invented one.
- All four BABOK types are considered, and transition requirements are present or explicitly declared none — they are the ones teams discover in go-live week.
- Section 3 carries an explicit exclusions list; an empty one means scope isn't bounded yet.
- Exactly one **A** per decision area in the RACI, and no row left without a named role or a `[TBD]` placeholder.
- Constraints, assumptions, and dependencies are separated in Section 7, and every dependency has an owner and a needed-by date.
- Every risk is scored and owned; an unowned risk is noted, not managed.
- Cost-benefit is either quantified or plainly declared not yet quantifiable — never a confident invented ROI.
- Every success criterion cites a `GOAL-xx` or `BR-xx` and has a baseline, a target, a method, and a review date.
- The glossary defines every acronym and role name used above; a BRD crosses departments.
- The approval block is present, even where every approver is TBD.
- Every section that doesn't apply is marked `Not applicable — <reason>` or `Insufficient evidence — <what would resolve it>`, never deleted.
- Nothing in the document specifies UI, stack, or system behavior — that's the PRD and TRD, and the most common way this document fails.

### Step 7 — Save and deliver

**This document set always ends in a Markdown file. Never deliver it as ordinary chat prose.**

Deliver by the highest tier the environment supports:

1. **Filesystem available** (coding agent, IDE, terminal, code interpreter) — write `docs/brd-writer/<slug>-brd-v<version>.md`. Create `docs/` only if it is missing — never recreate or replace an existing one — then create the `brd-writer/` subfolder inside it if that is missing too, so each skill's output stays in its own folder. Where the project already has a documentation directory, use that in place of `docs/`, with the same `brd-writer/` subfolder inside it. Report the path.
2. **Files or a document surface, but no repo** (downloadable file, canvas, doc, notebook) — create it there named `<slug>-brd-v<version>.md` and hand over the download or link.
3. **Chat only** — put the entire document in one fenced code block tagged `markdown`, with nothing else inside the fence, and name the file the user should save it as: `<slug>-brd-v<version>.md`. Everything you want to say goes before the fence, never interleaved.

Use one consistent `<slug>` across every document in the chain for a given product — the same slug the first document in the chain started with — so the six files read as one set. At feature scope the slug is the feature, not the product. The folder is per skill, the slug is per product: `docs/brd-writer/<slug>-brd-v<version>.md`.

**Versioning.** Every write creates a new file; an existing version file is never overwritten or deleted.

Before drafting, list `docs/brd-writer/` and find the highest `v<major>.<minor>.<patch>` among files matching `<slug>-brd-v*.md`. Compare the three numbers numerically, so `v0.0.10` is newer than `v0.0.9`. That file is the previous version — read it first, so the new document is a revision rather than a restart.

- No previous file — start at `v0.0.1`.
- **Patch** (`v0.0.x`) — edits, corrections, gaps filled, wording.
- **Minor** (`v0.x.0`) — new sections or requirements, or a re-run against a revised upstream document.
- **Major** (`vx.0.0`) — **Status** reaches Approved, or a rewrite that invalidates the documents downstream of this one.

The `**Version:**` line in the header block always carries the same number as the filename, and every version appends a row to the document's **Revision History** — what changed, and which IDs were added, changed, and removed. Report the new path and that summary, not just that a file was written.

**The changelog is mandatory.** After writing the file, append one bullet to `docs/CHANGELOG.md` — at the root of `docs/`, beside the per-skill subfolders — under today's ISO date heading, creating the file or the heading if either is missing:

```markdown
- **BRD** `brd-writer/<filename>` — <one-line summary>. +<IDs added>, ~<IDs changed>, -<IDs removed>. Upstream `<upstream path>` (every upstream, comma-separated, or "informal brief" where there is none).
```

The IDs must match the Revision History row for this version. Never edit a past entry — a correction is a new version with a new entry. Per-platform writes get one bullet each — and where this stage writes a single file whatever the platform set, that file gets one bullet. The document is not delivered until this entry exists.

Whatever the tier:

- The document is Markdown: header block first, then every section. A section with nothing to say carries `Not applicable — <reason>` or `Insufficient evidence — <what would resolve it>`, never an omission.
- Report the **filename plus a 3–5 line summary** — what it covers, the biggest assumption, the open questions that need a human. Don't restate the body in prose.
- Other formats — PDF, Google Doc, Word, spreadsheet — are exports *from* the Markdown, never replacements for it.
- Re-running against a revised upstream document produces the next version file — see the versioning rule above — rather than editing the previous one in place.

A BRD is circulated for review and sign-off, so the file matters more here than anywhere else in the chain — a document that only exists in a chat transcript cannot be approved.


### Step 8 — Hand off

Note that a BRD is meant to be reviewed with stakeholders and formally approved before development starts, and that the next document is the PRD (`prd-writer`), which specifies what the product does to satisfy each approved business requirement.

## BRD Template

<!-- include-start: references/template.md -->
Read `references/template.md` in this skill folder before drafting, and follow it exactly — section list, header block, Revision History, and the absent-section markers.
<!-- include-end -->

## Reviewing an existing BRD

When asked to review rather than write, report against the template's section numbers so every gap is addressable, and work the Step 6 quality bar as the checklist. A BRD is reviewed to be approved, so review it the way an approver reads it. **Can it be signed?** Approval block present, exactly one accountable party per decision area, every dependency owned and dated, every risk scored and owned. **Is the ask bounded?** An explicit exclusions list, a cost-benefit either quantified or honestly declared unquantifiable, and no requirement without a type, a priority, and a real upstream ID. **Is it still a BRD?** Anything specifying system behavior, UI, or stack belongs downstream. Name the smallest concrete edit that closes each gap, and say which open questions block sign-off rather than merely improving the document.

## Standards this follows

Requirement classification and stakeholder analysis follow **BABOK v3** (IIBA): the four requirement types, RACI stakeholder analysis, and a risk register with likelihood, impact, and named owners. The document's scope maps to the Business Requirements Specification (BRS) in **ISO/IEC/IEEE 29148:2018** — business-level need, deliberately above solution detail.

## Writing principles

- **Business outcome, not product design.** A BRD explains what the project must achieve and why it matters — never how the system works. System behavior, UI, and stack belong downstream.
- **Concrete over vague.** Push every objective and requirement toward something a stakeholder could verify was met.
- **Honest about gaps.** Translating from an MRD or a short brief leaves most BRD sections under-informed. Say so in Section 11 rather than inventing stakeholders, budgets, or ROI.
- **Prioritize, don't just list.** Every requirement carries a priority — that's what tells a reader what has to happen first.
- **Concise, not exhaustive.** This document exists to be read and approved.

## How a BRD differs from the rest of the chain

- **MRD** — what market problem should we solve? (often the input here)
- **BRD** (this document) — what business outcome should this support, and what will it take?
- **PRD** — what should the product actually do? (the next document once this is approved)
- **Design Spec / TRD / QA Test Plan** — how it looks, how it's built, how it's proven.

If the user asks for functional requirements or a feature spec next, that's a PRD — don't fold implementation detail into the BRD.
