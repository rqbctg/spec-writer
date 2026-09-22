---
name: spec-writer
description: "Router and shared conventions for the product documentation chain — MRD, BRD, PRD, Design Spec, TRD, QA Test Plan. Use when the user wants product/project documentation but hasn't named a specific document type, asks which document they need, wants several documents produced in sequence, or asks to check that an existing set of docs is consistent and traceable."
---

# Spec Writer

The entry point for a six-document chain. Each document answers one question, at one altitude, for one audience — and each is generated from the one above it so a product can be traced from market opportunity all the way to test coverage.

| # | Document | Module | Answers | Primary audience |
|---|---|---|---|---|
| 1 | MRD — Market Requirements | `mrd-writer` | What market problem should we solve, and is it worth solving? | Founders, exec sponsors |
| 2 | BRD — Business Requirements | `brd-writer` | What business outcome does this support, and what will it take? | Sponsors, approvers, finance |
| 3 | PRD — Product Requirements | `prd-writer` | What should the product actually do? | Product, design, engineering |
| 4 | Design Spec | `design-spec-writer` | What does the user see and do, screen by screen? | Design, frontend, QA |
| 5 | TRD — Technical Requirements | `trd-writer` | How will engineering build it? | Engineering, architecture |
| 6 | QA Test Plan | `qa-test-plan-writer` | How do we prove it works? | QA, automation |

## Routing

Pick the stage by what the user *has*, not by what they said:

First settle the scope (see below), because it decides how many stages even apply. Then:

- Only an idea, a sentence, a hunch → **`mrd-writer`**. If they explicitly don't want market validation and just want to build, go straight to `prd-writer` and say you skipped the MRD/BRD.
- An MRD, or a project that's already been decided on but needs sponsor/budget sign-off → **`brd-writer`**.
- A validated problem and a decision to build → **`prd-writer`**.
- A PRD with user-facing surface area (any UI at all) → **`design-spec-writer`**.
- A PRD, with or without a design spec → **`trd-writer`**.
- A PRD, design spec, or TRD, and a need for coverage → **`qa-test-plan-writer`**.
- "Give me the full set" / "document this idea end to end" → run the chain in order, stopping after each document to confirm before spending effort on the next. Do not silently generate six documents from one sentence; each one inherits the previous one's assumptions, and a wrong turn at the MRD stage poisons all five below it.
- A feature being added to something that already exists → **`prd-writer`**, at feature scope, inheriting the product's existing documents. Don't start at the MRD unless the feature opens a new market segment.
- "Review / check my docs" → read what exists, then report against **Traceability** and **Layer discipline** below.

Skip stages the user genuinely doesn't need — a small internal tool rarely needs an MRD and a BRD. State plainly which stages you skipped and why, so the gap is a decision rather than an oversight.

## Scope: whole product, or one feature

The chain works at three scopes. Pick one before routing — running product-scale documents for a single feature is the fastest way to make the whole set something nobody reads.

| | **Product** | **Feature** | **Change** |
|---|---|---|---|
| Typical input | A new product or product line | A substantial addition to something that exists | A fix, tweak, or small enhancement |
| MRD | Full | Only if it opens a new segment or changes positioning — otherwise a paragraph of evidence inside the PRD | Skip |
| BRD | Full | Only if it needs its own funding, headcount, or sponsor sign-off | Skip |
| PRD | Full | **Start here.** Scoped to the feature, inheriting product context | One page: problem, requirements, acceptance criteria |
| Design Spec | Full | New and changed screens only, plus the states they add to existing ones | Only if the UI changes |
| TRD | Full | The delta: what's added, what's modified, what the blast radius is | Only if the design is non-obvious |
| QA Test Plan | Full | New cases, plus regression scope for what the change can reach | Cases for the change, plus its regression scope |

### Working at feature scope

**Inherit, don't re-derive.** Personas, platforms, design tokens, architecture, NFRs, and compliance posture all come from the product's existing documents. Cite them and state only what this feature *changes*. A feature PRD that restates the product's personas has buried its one new idea in recycled context.

**Namespace the IDs** with a short feature slug so the feature's documents merge into the product's set without collision: `PR-EXPORT-01`, `SCR-EXPORT-02`, `FR-EXPORT-01`, `TC-EXPORT-001`. Keep the same slug across all of the feature's documents.

**Say what it touches.** The most valuable section in any feature document is the one naming existing behavior this could break — the screens it modifies, the shared components it changes, the API contracts it alters, the data it migrates. That section is what the test plan's regression scope is built from, and the thing most often missing when a feature ships and something unrelated breaks.

**Keep the required sections, shrink them.** *Assumptions and Open Questions* and *Next Steps* stay at every scope. A section that genuinely doesn't apply is marked `Not applicable — <reason>`, never deleted — see **Absent sections** below; at feature scope most sections are a sentence rather than a page.

If the user hands you a feature but wants the full chain anyway, produce it — just say which stages you'd normally collapse and why, so the choice is theirs rather than yours.

## Shared conventions

Every stage in this chain follows these. They are what make six documents one system instead of six unrelated files.

### Layer discipline

Each document stays at its own altitude. The most common failure in requirement docs is content leaking down a layer — an MRD that lists features, a PRD that picks a database, a design spec that describes API pagination.

| Layer | Belongs here | Belongs elsewhere |
|---|---|---|
| MRD | Market, users, pain, competitors | Any feature list → PRD |
| BRD | Outcomes, scope, cost, sign-off | System behavior → PRD/TRD |
| PRD | Product behavior, requirements, metrics | Architecture, stack → TRD |
| Design Spec | Screens, flows, states, content | Data models, endpoints → TRD |
| TRD | Architecture, APIs, data, NFRs | Business justification → BRD |
| QA Test Plan | Cases, coverage, risk | New business rules → question log |

When you catch a sentence in the wrong layer, move it or cut it — and if it's genuinely new information, note it for the document where it belongs.

### Traceability IDs

Every numbered item gets a stable ID, and every ID cites its parent. This is what lets a reviewer ask "which market need does this test case ultimately serve?" and get an answer.

```
MRD   NEED-01   market need / high-level product requirement
      GOAL-01   business goal                 → no upstream; the root of the outcome chain
BRD   BR-01     business requirement          → traces to NEED-xx (or GOAL-xx)
      R-01      risk register entry           → document-local; nothing downstream traces to it
PRD   PR-01     product requirement           → traces to BR-xx (or NEED-xx)
      MET-01    success metric or guardrail   → traces to BR-xx (or GOAL-xx)
      DEC-01    decision-log entry            → document-local; supersedes an earlier DEC-xx
DS    FLOW-01   user flow                     → traces to PR-xx
      SCR-01    screen / surface              → traces to PR-xx
      CMP-01    component                     → traces to SCR-xx
TRD   FR-01     functional requirement        → traces to PR-xx (and SCR-xx where a design spec exists)
      NFR-01    non-functional requirement    → traces to MET-xx, a PR-xx, or a BRD constraint
      API-01    endpoint / interface          → traces to FR-xx
QA    REQ-01    derived requirement           → no upstream; flags a gap in the source document
      TC-001    test case                     → traces to any ID above
```

Never invent a parent ID. If an item has no upstream parent, mark it `[no upstream — new in this document]` and add it to Assumptions and Open Questions. Orphans are usually either a genuine gap in the parent doc or scope creep, and both are worth surfacing.

### Document header

Every generated document opens with this block, so its lineage is readable without opening anything else:

```markdown
**Owner:** <name or role>
**Date:** <today's date>
**Version:** 0.0.1
**Status:** Draft | In review | Approved | Superseded
**Scope:** Product | Feature | Change
**Platforms:** <declared in the MRD; carried unchanged, or "platform-neutral">
**Upstream:** <exact upstream filename — `invoice-tracker-prd-ios-v0.2.0.md` — or "Informal brief">
**Downstream:** <what this document feeds next>
```

Two stages extend this block, and only these two: the PRD adds `**Stage:**`, naming which of its six stages the document is at, and the design spec adds `**Design file:**`, linking the visual source or saying "none yet". Any other field is one a reader has to guess at.

### Reading upstream

A document is built from a file, not from the conversation, so resolving that file is part of the work. Every stage below the MRD follows the same four rules:

1. **The producing skill's folder is the source** — `docs/prd-writer/` for a PRD, `docs/trd-writer/` for a TRD, or the project's own documentation directory where one replaces `docs/`.
2. **Highest version wins.** Compare `v<major>.<minor>.<patch>` numerically (`v0.0.10` is newer than `v0.0.9`). Read an older version only when the user asks for it by name, and say so in the header block.
3. **Platform matches platform.** A per-platform document is built from its own platform's upstream file; where the upstream is a single file with no platform token, every platform reads that one.
4. **The exact filename goes in `**Upstream:**`** — version and platform included. A stage reading several documents lists them all, comma-separated, one filename each: the TRD cites its PRD and design spec, the test plan cites all three. A missing one reads as "this document was written without it". Combined with rule 2, that is what makes the staleness check below mechanical rather than a judgement call: compare the cited filename against the newest file in the upstream folder.

On a re-run, the document's own previous version records which upstream version it was built from. Diff the newest upstream against that one and change only what the difference requires, rather than redrafting from scratch.

### Absent sections

No section is ever deleted from a template — an omission is invisible, and the shape of the standard is what makes a gap legible. A section with nothing in it carries one of three markers, and which one you pick is itself information:

| Marker | Means |
|---|---|
| `Not applicable — <reason>` | This section will never apply to this product. |
| `Insufficient evidence — <what would resolve it>` | It applies and is due now, but nothing supports it yet. This is a research task someone can pick up. |
| `Not yet — stage <n>` | PRD only: the section belongs to a later stage of that document's six. |

The second is the one that earns its keep: "insufficient evidence" is an honest finding, and a fabricated number in its place is not.

### Mandatory sections

Three sections appear in every document in this chain, regardless of type:

- **Revision History** — one appended row per version, directly under the header block (see below).
- **Assumptions and Open Questions** — every gap you filled with a guess, and every question that genuinely needs a human. Fabricating a number, a stakeholder, a business rule, or a limit is worse than admitting it's unknown.
- **Next Steps** — the next document or decision, who owns it, and what has to be true before it starts.

### Revision history

Filenames carry versions; the Revision History says what those versions *mean*. Every document opens with this table, directly below the header block, and every new version appends one row — rows are never rewritten or removed.

```markdown
## Revision History

| Version | Date | Author | Upstream version | Summary | IDs added | IDs changed | IDs removed |
|---|---|---|---|---|---|---|---|
| 0.1.0 | 2026-09-22 | A. Rahman | `invoice-tracker-brd-v0.2.0.md` | Offline receipt capture added | PR-08, MET-02 | PR-01 | PR-04 |
| 0.0.1 | 2026-09-14 | A. Rahman | `invoice-tracker-brd-v0.1.0.md` | Initial draft | — | — | — |
```

The three ID columns are what make this more than a diary. A downstream stage re-running against a revised document reads these rows instead of re-reading the whole document, and the staleness check can then say *what* went stale rather than just that something did. `—` means none; an empty cell means the change wasn't tracked, which is a gap to fix rather than a state to leave.

### The changelog

`docs/CHANGELOG.md` is **mandatory**. Writing a document version is not finished until its entry is in the changelog — the Revision History says what changed inside one document, and the changelog is the one place that answers "what moved across the whole set, and when."

It lives at the root of `docs/` (or of whatever documentation directory replaces it), beside the per-skill subfolders, and covers every document in the set. Create it on the first write if it is missing; never rewrite an existing entry.

```markdown
# Changelog — invoice-tracker

Specification documents for this product, newest first. One entry per document
version: `+` added, `~` changed, `-` removed.

## 2026-09-22

- **PRD** `prd-writer/invoice-tracker-prd-ios-v0.1.0.md` — offline receipt capture added.
  +PR-08, +MET-02, ~PR-01, -PR-04. Upstream `brd-writer/invoice-tracker-brd-v0.2.0.md`.
- **TRD** `trd-writer/invoice-tracker-trd-ios-v0.0.2.md` — queue and retry design for offline capture.
  +FR-12, +API-04. Upstream `prd-writer/invoice-tracker-prd-ios-v0.1.0.md`.

## 2026-09-14

- **PRD** `prd-writer/invoice-tracker-prd-ios-v0.0.1.md` — initial draft. Upstream `brd-writer/invoice-tracker-brd-v0.1.0.md`.
```

Rules, so the file stays mechanical rather than becoming prose:

1. **One bullet per document version**, under an ISO date heading. Append to today's heading, or create it at the top if it isn't there.
2. **The path is repo-relative from `docs/`**, so a reader can open it directly.
3. **The ID deltas match that version's Revision History row** exactly — same IDs, shortened to `+` / `~` / `-`. If the two disagree, the Revision History is right and the changelog entry is wrong.
4. **Per-platform writes get one bullet each**, because they are separate files with separate versions. A shared change touching four platform files appears four times, which is exactly the visibility that structure needs.
5. **Never edit a past entry.** A correction is a new version with a new entry.

Where a team cuts releases, add a `## Release 1.2 — 2026-10-01` heading above the dates it covers. That grouping is optional; the per-version entries are not.

### Quality bar and review mode

Every stage carries two things beyond its template, and both are part of the contract:

**A quality bar** — a pre-delivery checklist in the skill, worked before the file is written, not after. The checks are deterministic: does `**Upstream:**` name the newest file on disk, does every ID cite a real parent, does every number have a source, is every absent section marked. A document delivered without its bar worked is a draft presented as a deliverable. The bar is per stage because what can be checked mechanically differs by layer — an MRD checks that every figure has a method and a date; a design spec checks thirteen states per screen; a test plan checks that no case ships a vague oracle.

**A review mode** — what to do when asked to review an existing document rather than write one. Report against the template's section numbers so every gap is addressable, work that stage's quality bar as the checklist, and name the smallest concrete edit that closes each gap. Reviewing is not rewriting: report what's missing, don't quietly fill it.

### Working style

- **Don't interrogate.** Draft from thin input, label the assumptions, and move. Ask only when the answer materially changes the document — and batch the questions into one pass.
- **Evidence over assertion.** Cite the source, the user's own words, or the upstream document. "Limited evidence" is a legitimate finding; an invented market-size figure is not.
- **Concrete over vague.** "Reduce invoice processing time by 30% by Q2" beats "improve invoicing." Push every requirement toward something a reader could verify was met.
- **Concise, not exhaustive.** These documents exist to be read and acted on. A tight paragraph beats a wall of bullets.
- **Deliver a file, not a chat dump.** See the output contract below — every stage in this chain produces a Markdown file and names it.
- **Living documents.** Say so on handoff. When re-running against a revised upstream doc, diff it, update only affected IDs, bump the version, and preserve decision history rather than silently rewriting it.

## Standards each document follows

Each stage is structured on the recognised standard for its document type, so the output is reviewable by someone who has never seen this chain. When a template section looks unnecessary for a small project, keep it and mark it with one of the **Absent sections** markers — the shape of the standard is what makes an omission visible.

| Stage | Standard | What it governs |
|---|---|---|
| MRD | Pragmatic Institute framework | Market problem, buyer vs user personas, TAM/SAM/SOM, positioning, distribution |
| BRD | BABOK v3 (IIBA); ISO/IEC/IEEE 29148:2018 BRS | Requirement classification, RACI, risk register, sign-off |
| PRD | INVEST stories, Given/When/Then, MoSCoW | Product-layer requirements and acceptance criteria |
| Design Spec | WCAG 2.2 AA, W3C ARIA Authoring Practices | States, components, accessibility, localization |
| TRD | ISO/IEC/IEEE 29148:2018; ISO/IEC 25010:2023 | Requirement form and quality; NFR classification |
| QA Test Plan | ISO/IEC/IEEE 29119-3:2021 (superseded IEEE 829) | Plan structure, entry/exit, suspension/resumption |

Two conventions run across all six. Requirements use the **29148** sentence form — *[condition] [subject] [action] [object] [constraint]* — with *shall* binding, *should* recommended, *may* optional. And every requirement is judged against the nine **29148** quality characteristics: necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming.

## Platforms

<!-- include-start: references/platforms.md -->
Where a platform is declared, read `references/platforms.md` in this skill folder — what each platform owes each stage, the multi-platform rules (primary platform, parity intent, platform column), and the per-platform file split.
<!-- include-end -->

## Output contract

Every document in this chain is delivered as a Markdown file. A document that exists only in a chat transcript can't be reviewed, approved, diffed, or handed to the next stage — so the file is the deliverable, and the message is just the pointer to it.

Deliver by the highest tier the environment supports: **(1)** write to the filesystem where one is available, **(2)** produce a downloadable file or document surface where there's no repo, or **(3)** in a chat-only environment, emit the whole document in one fenced code block tagged `markdown` and name the file to save it as. The filename is the same in all three cases.

| Stage | Module | File |
|---|---|---|
| 1 | `mrd-writer` | `docs/mrd-writer/<slug>-mrd-v<version>.md` |
| 2 | `brd-writer` | `docs/brd-writer/<slug>-brd-v<version>.md` |
| 3 | `prd-writer` | `docs/prd-writer/<slug>-prd-v<version>.md`, or one per platform |
| 4 | `design-spec-writer` | `docs/design-spec-writer/<slug>-design-spec-v<version>.md`, or one per platform |
| 5 | `trd-writer` | `docs/trd-writer/<slug>-trd-v<version>.md`, or one per platform |
| 6 | `qa-test-plan-writer` | `docs/qa-test-plan-writer/<slug>-test-plan-v<version>.md`, or one per platform |

Each skill owns one subfolder of `docs/`, named after the skill, so a product's six documents are grouped by the stage that produced them. Use one consistent `<slug>` across all six files for a given product — that's what makes the set readable as a set.

Where a filesystem exists, create `docs/` only when it is missing; if it already exists, write into it untouched. Create the skill's subfolder inside it the same way. Where the project already has a documentation directory (`documentation/`, `doc/`, a docs site's content folder), use that instead of creating `docs/`, with the same per-skill subfolder inside it.

After writing, report the path and a 3–5 line summary: what the document covers, the biggest assumption made, and the open questions that need a human. Don't reprint the body.

If the user asks for another format — PDF, Google Doc, Word, spreadsheet — write the Markdown first and export from it, so one file stays the source of truth.

### Versioning

Every document filename ends in its version: `<slug>-<type>-v<major>.<minor>.<patch>.md`. Versions accumulate — a new version is a new file, and an existing one is never overwritten or deleted, so the folder is the document's history.

Before writing anything, list the skill's subfolder and find the highest version already there for that `<slug>`. Compare the three numbers numerically, so `v0.0.10` is newer than `v0.0.9`. Read that file before drafting; the new document is a revision of it.

| Bump | When |
|---|---|
| first write | `v0.0.1` |
| patch `v0.0.x` | edits, corrections, gaps filled |
| minor `v0.x.0` | new sections or requirements, or a re-run against a revised upstream document |
| major `vx.0.0` | **Status** reaches Approved, or a rewrite that invalidates downstream documents |

The header block's **Version** always matches the filename's version, and a document cites the exact upstream version it was built from — `Upstream: invoice-tracker-prd-v0.2.0.md`. That pairing is what makes the staleness check below mechanical rather than a judgement call.

When running several stages in sequence, confirm each document is delivered before starting the next — the next stage reads the document, not the conversation. In a chat-only environment, that means the previous document's Markdown block must be complete and on screen before the next stage begins.

## Consistency review

<!-- include-start: references/consistency-review.md -->
When asked to check an existing set rather than write one, read `references/consistency-review.md` in this skill folder and report against its nine checks.
<!-- include-end -->
