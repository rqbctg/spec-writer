---
name: design-spec-writer
description: "Turns a PRD (or a feature description) into a Design Specification: information architecture, user flows, screen-by-screen specs, every UI state, component inventory, interaction and motion, content and microcopy, accessibility, and responsive behavior. Use when the user mentions a design spec, UX spec, UI spec, design handoff, screen spec, or needs the user-facing detail engineers will build against."
---

# Design Spec Writer

Stage 4 of the spec-writer chain. Reads a PRD; feeds `trd-writer` and `qa-test-plan-writer`.

## What this does

Translates product requirements into the user-facing detail a frontend engineer can build from and a QA engineer can test against, without having to guess. A PRD says "a user can see all overdue invoices"; a design spec says which screen that lives on, how the user gets there, what the empty state says, what happens on a slow network, what the row looks like at 375px, and which component renders it.

This is a written specification, not a visual mockup. It can accompany a Figma file, describe one that doesn't exist yet, or stand alone — but its job is always to be unambiguous in text, because text is what survives handoff.

## Reading the upstream documents

This stage reads the PRD. In a repository the documents are on disk, versioned, and possibly split per platform, so resolve them deliberately rather than taking the first file that matches.

| Upstream | Where it lives |
|---|---|
| PRD | `docs/prd-writer/<slug>-prd-v*.md` |

1. **Look in the producing skill's folder**, or in the project's documentation directory where one replaces `docs/`.
2. **Take the highest version.** Compare `v<major>.<minor>.<patch>` numerically, so `v0.0.10` is newer than `v0.0.9`. Never read an older version just because it came up in conversation. If the user names an older one deliberately, use it and say so in the header block.
3. **Match the platform.** Where you are producing a per-platform document, read the upstream file for *that* platform — the iOS document is built from the iOS upstream, not from the set. Where the upstream was written as a single file with no platform token, every platform reads that one.
4. **Cite the exact filename** in `**Upstream:**`, version and platform included — `invoice-tracker-prd-ios-v0.2.0.md`. Where this stage reads several documents, list them all, comma-separated; a missing one reads as "written without it". That line is what makes the staleness check mechanical: a reviewer compares it against the newest upstream file on disk.
5. **On a re-run, diff rather than redraft.** Your own previous version file names the upstream version it was built from. Compare that against the upstream you just resolved, and change only what the difference requires.

Outside a repository — a pasted document, an attachment, or a document drafted earlier in this conversation — apply the same rules to what you were given, and where the version genuinely isn't knowable write `**Upstream:** <name> (version unknown)` rather than inventing one.

## The rule that matters most

**Every state, not just the happy path.** The single most common defect source in a UI is a state nobody specified: the empty list, the 40-character name, the expired session, the offline save, the partially-loaded page. A screen is not specified until all of its states are.

Use this checklist on every screen and every component that fetches, submits, or holds data:

| State | Specify |
|---|---|
| Empty (first use) | Illustration/icon, headline, body copy, primary action |
| Empty (cleared by filter/search) | Distinct from first-use empty — offer a way back |
| Loading (initial) | Skeleton, spinner, or optimistic render; what's visible meanwhile |
| Loading (incremental) | Pagination, infinite scroll, background refresh indicator |
| Partial | Some data loaded, some failed — what shows, what retries |
| Populated (typical) | The normal case, with realistic data |
| Populated (extremes) | 1 item, max items, longest string, largest number, oldest date |
| Error (recoverable) | Message, the specific cause, the retry affordance |
| Error (terminal) | Message, what the user does instead, support path |
| Offline / degraded | What's readable, what's blocked, what queues |
| Permission-denied | What a user without the role sees — hidden, disabled, or explained |
| Disabled / read-only | Why it's disabled, and whether the reason is visible |
| Success / confirmation | What confirms the action, for how long, and whether it's undoable |

## Workflow

### Step 1 — Read the PRD and inventory the surface area

Pull out every requirement with user-facing consequence. For each `PR-xx`, ask: what does the user see, what do they do, and where does it happen? Group those into screens and flows. Requirements with no surface area (background jobs, data retention) belong to the TRD, not here — note them and move on.

If there's no PRD, work from the description but say in the header that it's derived from an informal brief, and expect to make more assumptions.

**Scope and platforms:** if the upstream document declares them, carry both into this document's header block verbatim and don't ask again. If no upstream document exists and you're the first in the chain, ask the user once — scope (product, feature, or change) and target platforms (web, iOS, Android, macOS, Windows, Linux, API, or undecided) — in a single batched question with a recommendation attached, exactly as the `mrd-writer` scope-and-platforms question describes. Record the answer; never pick silently.

### Step 2 — At feature scope, specify the delta

For a feature inside an existing product, specify only what's new or changed, and be precise about which:

- **New screens** — full specification, every state.
- **Changed screens** — the changed region only, with a before-and-after for each modified element, and any state the change adds (a new empty state, a new error, a new permission case).
- **Changed components** — flag every other screen that uses the component, because that's where a shared-component change breaks something nobody was looking at.
- **Untouched** — say so explicitly. "No change to the invoice list" is a real statement that saves a reviewer from diffing.

Everything else — tokens, grid, voice, accessibility target, platform conventions — is inherited from the product's design spec and design system. Cite it rather than restating it.

**Namespace the IDs** with the same short feature slug the PRD used — `FLOW-EXPORT-01`, `SCR-EXPORT-02`, `CMP-EXPORT-01` — so this feature's screens and components merge into the product's set without colliding.

### Step 3 — Reuse before inventing

If the project has an existing design system, component library, or codebase, find it before specifying anything. Read the token definitions, the component names, and a couple of existing screens, and specify in *their* vocabulary — reusing `Button/primary` beats describing a blue rounded rectangle. Where you can actually reach the design tool — a Figma integration, an exported file, pasted screenshots — read the real thing rather than inventing component names.

Only design something new when nothing existing fits, and say explicitly that it's new — a new component is a cost that someone should get to weigh.

### Step 4 — Specify the flows before the screens

A screen list without flows hides the hard parts: entry points, branches, dead ends, and back behavior. Draw each flow as a Mermaid diagram plus a numbered step list, covering the success path, each branch, and each exit. Cancel and back are part of the flow.

### Step 5 — Specify each screen

Work through the document template. Be concrete: real copy, not "appropriate message"; a specific token, not "some padding"; the exact sort order, not "sorted sensibly."

### Step 6 — Quality bar before delivering

- `**Upstream:**` names the exact PRD filename with its version, and it is the newest one on disk.
- Revision History carries a row for this version, with the `FLOW-xx`, `SCR-xx`, and `CMP-xx` IDs added, changed, and removed since the previous one.
- Every `PR-xx` with user-facing consequence maps to at least one `SCR-xx` or `FLOW-xx`.
- Every `FLOW-xx` and `SCR-xx` names the `PR-xx` it serves, and every `CMP-xx` names the screens it's used on — or carries `[no upstream — new in this document]` and a Section 15 entry.
- Every screen has all thirteen states from the checklist addressed, or marked `Not applicable — <reason>`.
- Every interactive element has a name, a state set (default/hover/focus/active/disabled/loading), and a keyboard behavior.
- Every flow states its exits — completion, cancellation, abandonment, timeout — and what persists in each.
- Every piece of copy in the spec is final copy or explicitly marked `[draft copy]`.
- Every accessibility requirement cites a named WCAG success criterion, not a general aspiration.
- Every value is a token name; a raw hex, pixel, or millisecond figure means either the token is missing or it should have been used, and both get said out loud.
- Every motion has a stated duration, easing, and reduced-motion alternative.
- Every new component is flagged as new, with its anatomy, states, and responsive behavior specified.
- Every section not filled carries `Not applicable — <reason>` or `Insufficient evidence — <what would resolve it>`.
- Where the set is per-platform, every platform file is bumped in the same run and shared `SCR-xx` and `CMP-xx` text is identical between them.
- No adjective is doing the work of a specification — "fast," "clean," "intuitive," and "modern" are not specs.
- Nothing specifies an endpoint, a data model, a cache, or a query — that's the TRD. Where the design depends on one, state the requirement, not the implementation.

### Step 7 — Save and hand off

**This document set always ends in a Markdown file. Never deliver it as ordinary chat prose.**

Deliver by the highest tier the environment supports:

1. **Filesystem available** (coding agent, IDE, terminal, code interpreter) — write `docs/design-spec-writer/<slug>-design-spec-v<version>.md`. Create `docs/` only if it is missing — never recreate or replace an existing one — then create the `design-spec-writer/` subfolder inside it if that is missing too, so each skill's output stays in its own folder. Where the project already has a documentation directory, use that in place of `docs/`, with the same `design-spec-writer/` subfolder inside it. Report the path.
2. **Files or a document surface, but no repo** (downloadable file, canvas, doc, notebook) — create it there named `<slug>-design-spec-v<version>.md` and hand over the download or link.
3. **Chat only** — put the entire document in one fenced code block tagged `markdown`, with nothing else inside the fence, and name the file the user should save it as: `<slug>-design-spec-v<version>.md`. Everything you want to say goes before the fence, never interleaved.

Use one consistent `<slug>` across every document in the chain for a given product — the same slug the first document in the chain started with — so the six files read as one set. At feature scope the slug is the feature, not the product. The folder is per skill, the slug is per product: `docs/design-spec-writer/<slug>-design-spec-v<version>.md`.

**Versioning.** Every write creates a new file; an existing version file is never overwritten or deleted.

Before drafting, list `docs/design-spec-writer/` and find the highest `v<major>.<minor>.<patch>` among files matching `<slug>-design-spec-v*.md`. Compare the three numbers numerically, so `v0.0.10` is newer than `v0.0.9`. That file is the previous version — read it first, so the new document is a revision rather than a restart.

- No previous file — start at `v0.0.1`.
- **Patch** (`v0.0.x`) — edits, corrections, gaps filled, wording.
- **Minor** (`v0.x.0`) — new sections or requirements, or a re-run against a revised upstream document.
- **Major** (`vx.0.0`) — **Status** reaches Approved, or a rewrite that invalidates the documents downstream of this one.

The `**Version:**` line in the header block always carries the same number as the filename, and every version appends a row to the document's **Revision History** — what changed, and which IDs were added, changed, and removed. Report the new path and that summary, not just that a file was written.

**The changelog is mandatory.** After writing the file, append one bullet to `docs/CHANGELOG.md` — at the root of `docs/`, beside the per-skill subfolders — under today's ISO date heading, creating the file or the heading if either is missing:

```markdown
- **Design Spec** `design-spec-writer/<filename>` — <one-line summary>. +<IDs added>, ~<IDs changed>, -<IDs removed>. Upstream `<upstream path>` (every upstream, comma-separated, or "informal brief" where there is none).
```

The IDs must match the Revision History row for this version. Never edit a past entry — a correction is a new version with a new entry. Per-platform writes get one bullet each — and where this stage writes a single file whatever the platform set, that file gets one bullet. The document is not delivered until this entry exists.

**Per-platform documents.** Where the header block declares more than one platform, produce one complete design spec per platform — not a shared document with a platform column doing the work. Each file is standalone and whole: every section filled for that platform, shared behavior written out in full rather than cross-referenced.

`docs/design-spec-writer/<slug>-design-spec-<platform>-v<version>.md`, one file per declared platform. The `<platform>` token comes from this fixed vocabulary, so filenames stay predictable: `web`, `ios`, `android`, `macos`, `windows`, `linux`, `api`.

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

## Reviewing an existing design spec

When asked to review rather than write, report against the template's section numbers so every gap is addressable, and work the Step 6 quality bar as the checklist. The first pass is always the state matrix: take every screen against the thirteen states and list the ones neither specified nor waived, because that is where the defects come from. Then the traceability pass — `PR-xx` with no screen, screens serving no requirement — and the specificity pass, naming every adjective, "appropriate message", and raw value doing a specification's job. Name the smallest concrete edit that closes each gap.

## Handing off

The Markdown file is the deliverable even when a Figma file exists — the spec is what survives handoff. In the summary, note which parts still need visual design, then point at `trd-writer` for the engineering blueprint and `qa-test-plan-writer` for coverage of the state matrix.


## Design Spec Template

<!-- include-start: references/template.md -->
Read `references/template.md` in this skill folder before drafting, and follow it exactly — section list, header block, Revision History, and the absent-section markers.
<!-- include-end -->

## Standards this follows

Accessibility targets **WCAG 2.2 Level AA**, with specific success criteria cited per requirement rather than a blanket claim of conformance. Interaction states, tokens, and component anatomy follow prevailing design-system practice (Material, HIG, and the W3C ARIA Authoring Practices for component semantics and keyboard behavior). Where the product must meet a legal accessibility mandate — EN 301 549, Section 508, the European Accessibility Act — name it in Section 11 and treat it as a constraint, not a goal.

## Writing principles

- **Specify, don't describe.** "Sorted by days overdue, descending, ties broken by amount" is a spec. "Sorted sensibly" is a conversation someone will have to repeat during code review.
- **Real content, always.** Specify with the longest plausible name, the largest number, and the emptiest account — lorem ipsum hides every layout bug worth catching early.
- **Accessibility is in the spec, not appended to it.** Focus order and announcements belong in the screen section, next to the behavior they describe.
- **Name the reuse.** Every element should point at an existing component or be explicitly flagged new.
- **Stay out of the TRD.** Data models, endpoints, caching, and infrastructure belong downstream. If the design depends on one — pagination size, a real-time update — state the requirement, not the implementation.
