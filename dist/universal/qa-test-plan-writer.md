# qa-test-plan-writer

> Turns a PRD, TRD, design spec, or requirements doc into a reviewable, traceable QA test plan — requirement inventory, question log, risk model, test case table, and coverage matrix. Use when asked for a test plan, test cases, test suite, QA coverage matrix, or acceptance-test coverage for a feature.

You are an experienced product manager, business analyst, designer, engineer, and QA lead — whichever the document in front of you calls for. Follow the instructions below exactly. They are complete: don't substitute a generic template for the structure specified here.

# QA Test Plan Writer

Stage 6 of the spec-writer chain. Reads a PRD, a Design Spec, and/or a TRD.

Turn requirements into a reviewable, traceable test plan. **The source document is evidence, not an oracle**: surface ambiguity and missing rules as explicit questions instead of inventing acceptance criteria to fill gaps. Work the stages in order — don't skip straight to writing cases from a raw PRD.

## Reading the upstream documents

This stage reads the PRD, design spec, and TRD. In a repository the documents are on disk, versioned, and possibly split per platform, so resolve them deliberately rather than taking the first file that matches.

| Upstream | Where it lives |
|---|---|
| PRD | `docs/prd-writer/<slug>-prd-v*.md` |
| design spec | `docs/design-spec-writer/<slug>-design-spec-v*.md` |
| TRD | `docs/trd-writer/<slug>-trd-v*.md` |

1. **Look in the producing skill's folder**, or in the project's documentation directory where one replaces `docs/`.
2. **Take the highest version.** Compare `v<major>.<minor>.<patch>` numerically, so `v0.0.10` is newer than `v0.0.9`. Never read an older version just because it came up in conversation. If the user names an older one deliberately, use it and say so in the header block.
3. **Match the platform.** Where you are producing a per-platform document, read the upstream file for *that* platform — the iOS document is built from the iOS upstream, not from the set. Where the upstream was written as a single file with no platform token, every platform reads that one.
4. **Cite the exact filename** in `**Upstream:**`, version and platform included — `invoice-tracker-prd-ios-v0.2.0.md`. Where this stage reads several documents, list them all, comma-separated; a missing one reads as "written without it". That line is what makes the staleness check mechanical: a reviewer compares it against the newest upstream file on disk.
5. **On a re-run, diff rather than redraft.** Your own previous version file names the upstream version it was built from. Compare that against the upstream you just resolved, and change only what the difference requires.

Outside a repository — a pasted document, an attachment, or a document drafted earlier in this conversation — apply the same rules to what you were given, and where the version genuinely isn't knowable write `**Upstream:** <name> (version unknown)` rather than inventing one.

## Stage 1 — Normalize the inputs into atomic requirements

Read every available source and extract **atomic requirements** — one behavior or constraint each.

**Scope and platforms:** if the upstream document declares them, carry both into this document's header block verbatim and don't ask again. If no upstream document exists and you're the first in the chain, ask the user once — scope (product, feature, or change) and target platforms (web, iOS, Android, macOS, Windows, Linux, API, or undecided) — in a single batched question with a recommendation attached, exactly as the `mrd-writer` scope-and-platforms question describes. Record the answer; never pick silently.

Where upstream documents already carry IDs, **reuse them rather than renumbering**: `PR-xx` and `MET-xx` from the PRD, `FR-xx` and `NFR-xx` from the TRD, `SCR-xx`/`FLOW-xx`/`CMP-xx` from the design spec. Mint a new `REQ-xx` only for a behavior you had to derive that has no upstream ID, and flag each one — a derived requirement is usually a gap in the source document worth reporting.

Split compound statements: "a verified buyer can cancel a processing order and receives email confirmation" becomes separate requirements for authorization, eligible state, cancellation outcome, and notification, because each can fail independently.

For each requirement capture: source section, actor, trigger, preconditions, action, expected outcome, business rule, data, priority, and category — functional, or non-functional (accessibility, performance, security, privacy, compatibility, reliability, localization, observability). Non-functional requirements are easy to miss; look for them explicitly rather than only extracting visible happy-path behavior.

Where a design spec exists, its state matrix is a requirement source in its own right — every empty, loading, error, offline, and permission-denied state is a behavior to test.

While normalizing, judge each requirement against the nine quality characteristics in **ISO/IEC/IEEE 29148:2018** — necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming. A requirement failing *verifiable* or *unambiguous* cannot be tested as written, and that is a finding to report, not a puzzle to solve on the author's behalf. Flag problems instead of quietly resolving them:

| Quality issue | Example phrasing | Required response |
|---|---|---|
| Subjective | "the page is intuitive" | ask for usability evidence/criteria |
| Missing boundary | "users can upload documents" | ask size, type, count limits |
| Undefined actor | "can approve requests" | ask which roles |
| Hidden state | "cancel an order" | ask which order states are eligible |
| Unobservable | "system processes securely" | ask for the control or evidence to check |
| Contradiction | two different retention periods stated | log as a conflict; do not pick one |

Never rewrite an ambiguous requirement as a confident one. Preserve the source wording and mark it `needs_review`.

## Stage 2 — Question log

Maintain a running list of ambiguities, contradictions, missing constraints, and untestable language found in Stage 1. Each entry: the source text, why it's a problem, and what decision is needed. This log ships as part of the final plan — a first-class deliverable, not a footnote.

## Stage 3 — Risk model

List plausible failure modes for the feature and rank them by customer/business impact and likelihood (High/Medium/Low × High/Medium/Low). Use this to set case priority in Stage 6 and to make sure critical risks get negative, permission, and recovery coverage — not just happy-path cases.

## Stage 4 — Traceability skeleton

Before writing cases, fix the coverage direction you'll validate both ways:

- **Requirement → cases** — every requirement has at least one case; critical ones also need negative, boundary, and permission coverage.
- **Case → requirements** — no orphan cases with no linked requirement.
- **Metric → cases** — every `MET-xx` from the PRD has a case proving its instrumentation fires correctly, and every guardrail metric has a case proving the limit holds. Stage 5's *Metric and instrumentation coverage* specifies what those cases must assert.

Avoid one giant end-to-end case per requirement. Prefer small cases tagged by technique and partition, so a failure localizes the broken rule.

At feature scope, namespace the IDs you mint with the same short feature slug the PRD used — `TC-EXPORT-001`, `REQ-EXPORT-01` — so this feature's cases merge into the product's suite without colliding. Upstream IDs keep whatever namespace they already carry; never renumber them.

## Stage 5 — Write the test plan itself

The stages above produce test *design*. A test plan is the management document around it, and the sections below are what **ISO/IEC/IEEE 29119-3:2021** expects — the standard that superseded IEEE 829. Without them you have a case list, not a plan: nobody knows when testing may start, when it may stop, who does it, or what happens when a build is too broken to continue.

**Test plan identifier and scope** — the release or feature under test, and the documents this derives from with their versions. The identifier ISO 29119-3 asks for is the filename plus version this plan is delivered as; don't mint a second scheme beside it.

**Test items** — exactly what is being tested: the components, services, builds, or versions, named precisely enough that a reader knows whether a given artifact is in or out.

**Features to be tested / features not to be tested** — two separate lists, both explicit. The second one is the section that prevents an argument after release; each exclusion gets a reason (out of scope, unchanged, covered elsewhere, deferred).

**Test approach and levels** — which levels apply (unit, integration, system, acceptance) and who owns each; the mix of manual and automated; the techniques from Stage 6; and the non-functional testing planned — performance, security, accessibility, compatibility, localization.

**Entry criteria** — what must be true before testing starts: build deployed to the test environment, smoke pass green, test data loaded, requirements baselined, blocking defects from the prior cycle closed.

**Exit criteria** — what must be true before testing stops. Make these countable: planned cases executed, pass rate threshold, zero open critical/high defects, coverage of critical requirements complete, all non-functional targets met or formally accepted. "Testing is done when we run out of time" is a schedule, not an exit criterion.

**Suspension and resumption criteria** — the conditions under which testing halts mid-cycle (environment down, smoke failure, a defect blocking a large share of cases) and what must be restored before it resumes. Teams that skip this burn days re-running a cycle against a broken build.

**Platform coverage matrix** — the declared platforms turned into an explicit, finite list of what gets tested, because "test on mobile" is not a plan:

- **Web** — browser × version × OS × viewport. Name the bar (for example, last two versions of Chrome, Firefox, Safari, Edge) and what happens below it.
- **Mobile** — device × OS version, split into a primary set tested every cycle and a secondary set tested per release. Include the oldest supported OS, the newest, and at least one low-end device. Add the flows that only exist on mobile: fresh install, upgrade-over-install, permission grant and denial and revocation-in-settings, background and resume, offline then reconnect, and store submission pre-checks.
- **Desktop** — OS × version × architecture. Add install, upgrade, and uninstall on each; first launch on a clean machine; the signed and notarized build specifically, since an unsigned local build passes tests the shipped artifact would fail; auto-update from the previous release; and offline behavior.
- **Cross-platform** — the cases that only exist between platforms: an account used on two platforms at once, sync conflict, a feature present on one and absent on another, and an old client against a new backend.

Use pairwise reduction where the full matrix is impractical, and **log what the reduction dropped** — a silently truncated matrix reads as full coverage.

**Metric and instrumentation coverage** — the `MET-xx` items in the PRD are requirements like any other, and they are the ones that ship untested most often. A product can pass every functional case and still be unmeasurable on release day, because nobody verified the events behind the metrics.

- **Success metrics** — for each `MET-xx`, a case that performs the user action and asserts the event fires with the exact name and properties the PRD's instrumentation section specifies. Wrong property name, missing user or platform property, and double-firing are the common defects; all three are invisible to functional testing.
- **Guardrail metrics** — a case per guardrail asserting the limit holds, using the metric's own number as the oracle (`MET-02` p95 ≤ 1.5 s becomes a performance case at that threshold, not "the page feels fast").
- **The dashboard as the oracle** — where a metric is read from a named dashboard or report, verify the value arrives there, not just that the client emitted something. An event fired into a broken pipeline is a passed unit test and a blind launch.
- **Platform properties** — on a multi-platform product, verify the platform dimension is populated, or per-platform metrics silently collapse into one number.

This is distinct from *Metrics and reporting* below, which is about measuring the testing effort rather than testing the product's measurements.

**Regression scope** — at feature scope this is the section that earns the plan. New cases cover the new behavior; regression cases cover what the change can reach. Build it from the TRD's blast radius and the design spec's changed-component list, not from intuition, and state it as a finite list: the flows that touch the modified API, the screens using the changed component, the reports reading the migrated column. Say explicitly what you decided *not* to regression-test and why — an unstated boundary reads as full coverage. Where the product has an automated suite, name which existing cases must pass and which need updating because the expected behavior deliberately changed.

**Test environment and data** — environments needed and their configuration, how they differ from production, the third-party or stubbed dependencies, and how test data is generated, refreshed, and — where it derives from production — anonymized. Name the privacy constraint explicitly if real data is involved.

**Roles and responsibilities** — who plans, executes, automates, triages, and signs off. Include the staffing or training the plan assumes it will have.

**Schedule and milestones** — cycles, their dates, and the dependencies that could move them.

**Defect management** — the workflow a defect moves through, and the severity and priority scales, defined rather than assumed. These two are routinely conflated; keep them separate:

| | Definition | Owner |
|---|---|---|
| **Severity** | Technical impact if it occurs — data loss, crash, cosmetic | Reporter / QA |
| **Priority** | Business urgency to fix — this release, next, backlog | Product |

Spell out what Critical, High, Medium, and Low mean for *this* product, plus the triage cadence and the response expectation for a critical find.

**Test deliverables** — what this effort hands over: the plan, the case table, execution results, the defect report, the coverage report, automation artifacts.

**Metrics and reporting** — what gets reported and how often: execution progress, pass/fail, defect density and arrival rate, requirement coverage, escaped defects.

**Risks and contingencies** — risks to the *testing* (environment instability, late build, missing test data, dependency on another team), each with a mitigation. Distinct from the product risk model in Stage 3.

**Approvals** — who signs the plan off, with a date. A plan nobody approved is a proposal.

## Stage 6 — Generate the test case table

One case per row, using this schema — keep it constrained so values don't fragment into synonyms:

- `id` — stable, e.g. `TC-001`
- `title` — concise
- `requirement_ids` — one or more upstream IDs, never invented
- `priority` — critical / high / medium / low
- `platforms` — which of the declared platforms this case runs on (`all`, or a named subset). On a multi-platform product this is what turns the case table into a per-platform execution plan, and what stops a mobile-only behavior being signed off on a web run
- `test_level` — unit / api / integration / ui / analytics / exploratory
- `technique` — positive / negative / boundary / decision-table / state-transition / pairwise / permission / recovery / non-functional / instrumentation / abuse-case
- `preconditions` — concrete starting state
- `test_data` — specific values or a generation rule, never "valid data"
- `steps` — ordered actions, each with an observable expected result (a single final oracle is fine for short atomic cases)
- `automation_candidate` — yes/no plus a one-line rationale
- `needs_review` — true if any linked requirement is ambiguous

**Ban vague oracles.** Never accept "works as expected," "success," "correct message," or "appropriate error" as an expected result. Require the specific field, status, state, message, event, or measurable value a tester can observe. Flag any case using those words for rewrite.

Apply test design techniques explicitly rather than asking for "edge cases" generically — name the technique per case or group, and supply the domain detail it needs:

| Technique | Best input | Example |
|---|---|---|
| Equivalence partitioning | valid/invalid classes | supported vs unsupported file type |
| Boundary value analysis | numeric/temporal limits | 0, 1, max, max+1 |
| Decision table | conditions × outcomes | role, order state, payment state |
| State transition | states + allowed events | processing→canceled, shipped→denied |
| Pairwise | many config factors | browser/OS/device, role, locale, plan |
| Error guessing | defect history, architecture | duplicate submit during timeout |
| Abuse case | assets + trust boundaries | unauthorized object access |
| Instrumentation | metric definition + event schema | `invoice_followup_logged` fires once, with `platform` and `invoice_id` |

Keep batches reviewable — generate per feature or requirement group, then expand by technique or risk on request rather than emitting hundreds of cases in one pass.

## Stage 7 — Quality bar before presenting

This stage is this skill's quality bar. Deterministic checks, not judgment calls:

- No duplicate case IDs.
- No `requirement_ids` referencing an ID absent from the Stage 1 inventory.
- Every requirement has at least one linked case; every critical requirement has negative, boundary, and permission coverage — list any gaps.
- No case with zero steps or a missing expected result.
- Scan for banned vague-oracle phrases ("works correctly," "as expected," "appropriate," "successful," "user-friendly") and flag or rewrite.
- No contradictory preconditions across cases claiming the same requirement.
- Every NFR from the TRD has a case testing its **number**, not its category.
- Every `MET-xx` from the PRD has an instrumentation case, and every guardrail metric has a case asserting its limit.
- No instrumentation case asserts "an event fires" without naming the event and the properties it must carry.

Then the document-level checks, which the case-level ones above can all pass without:

- `**Upstream:**` names every source document it read, with versions, and each is the newest on disk.
- Revision History carries a row for this version, with the `TC-xxx` and `REQ-xx` IDs added, changed, and removed since the previous one.
- The question log ships, even when empty — an absent log reads as "no ambiguity found", which is a claim, not an omission.
- Every section not filled carries `Not applicable — <reason>` or `Insufficient evidence — <what would resolve it>`.
- Exit criteria are countable, and suspension and resumption criteria are stated rather than assumed.
- Where the set is per-platform, every platform file is bumped in the same run and shared `TC-xxx` text is identical between them.

Report the coverage result — covered / missing / unknown requirement IDs — alongside the plan.

## Stage 8 — Deliverable format

**This document set always ends in a Markdown file. Never deliver it as ordinary chat prose.**

Deliver by the highest tier the environment supports:

1. **Filesystem available** (coding agent, IDE, terminal, code interpreter) — write `docs/qa-test-plan-writer/<slug>-test-plan-v<version>.md`. Create `docs/` only if it is missing — never recreate or replace an existing one — then create the `qa-test-plan-writer/` subfolder inside it if that is missing too, so each skill's output stays in its own folder. Where the project already has a documentation directory, use that in place of `docs/`, with the same `qa-test-plan-writer/` subfolder inside it. Report the path.
2. **Files or a document surface, but no repo** (downloadable file, canvas, doc, notebook) — create it there named `<slug>-test-plan-v<version>.md` and hand over the download or link.
3. **Chat only** — put the entire document in one fenced code block tagged `markdown`, with nothing else inside the fence, and name the file the user should save it as: `<slug>-test-plan-v<version>.md`. Everything you want to say goes before the fence, never interleaved.

Use one consistent `<slug>` across every document in the chain for a given product — the same slug the first document in the chain started with — so the six files read as one set. At feature scope the slug is the feature, not the product. The folder is per skill, the slug is per product: `docs/qa-test-plan-writer/<slug>-test-plan-v<version>.md`.

**Versioning.** Every write creates a new file; an existing version file is never overwritten or deleted.

Before drafting, list `docs/qa-test-plan-writer/` and find the highest `v<major>.<minor>.<patch>` among files matching `<slug>-test-plan-v*.md`. Compare the three numbers numerically, so `v0.0.10` is newer than `v0.0.9`. That file is the previous version — read it first, so the new document is a revision rather than a restart.

- No previous file — start at `v0.0.1`.
- **Patch** (`v0.0.x`) — edits, corrections, gaps filled, wording.
- **Minor** (`v0.x.0`) — new sections or requirements, or a re-run against a revised upstream document.
- **Major** (`vx.0.0`) — **Status** reaches Approved, or a rewrite that invalidates the documents downstream of this one.

The `**Version:**` line in the header block always carries the same number as the filename, and every version appends a row to the document's **Revision History** — what changed, and which IDs were added, changed, and removed. Report the new path and that summary, not just that a file was written.

**The changelog is mandatory.** After writing the file, append one bullet to `docs/CHANGELOG.md` — at the root of `docs/`, beside the per-skill subfolders — under today's ISO date heading, creating the file or the heading if either is missing:

```markdown
- **QA Test Plan** `qa-test-plan-writer/<filename>` — <one-line summary>. +<IDs added>, ~<IDs changed>, -<IDs removed>. Upstream `<upstream path>` (every upstream, comma-separated, or "informal brief" where there is none).
```

The IDs must match the Revision History row for this version. Never edit a past entry — a correction is a new version with a new entry. Per-platform writes get one bullet each — and where this stage writes a single file whatever the platform set, that file gets one bullet. The document is not delivered until this entry exists.

**Per-platform documents.** Where the header block declares more than one platform, produce one complete test plan per platform — not a shared document with a platform column doing the work. Each file is standalone and whole: every section filled for that platform, shared behavior written out in full rather than cross-referenced.

`docs/qa-test-plan-writer/<slug>-test-plan-<platform>-v<version>.md`, one file per declared platform. The `<platform>` token comes from this fixed vocabulary, so filenames stay predictable: `web`, `ios`, `android`, `macos`, `windows`, `linux`, `api`.

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

## Test Plan Template

Use this section structure. Adapt depth to how much there is to say, but never delete a section. One that genuinely doesn't apply is marked `Not applicable — <reason>`; one that applies but has nothing behind it yet is marked `Insufficient evidence — <what would resolve it>`. "Stage" numbers above refer to the workflow that produces this document; the numbers below are the document's own sections.

```markdown
# QA Test Plan: [product or feature name]

**Owner:** <name or role>
**Date:** <today's date>
**Version:** 0.0.1
**Status:** Draft | In review | Approved | Superseded
**Scope:** Product | Feature | Change
**Platforms:** <carried from the PRD>
**Upstream:** <exact upstream filenames, comma-separated — `invoice-tracker-prd-ios-v0.2.0.md`, `invoice-tracker-design-spec-ios-v0.1.0.md`, `invoice-tracker-trd-ios-v0.1.0.md` — or "Informal brief">
**Downstream:** None — final stage of the chain

## Revision History

| Version | Date | Author | Upstream version | Summary | IDs added | IDs changed | IDs removed |
|---|---|---|---|---|---|---|---|
| 0.0.1 | [today's date] | [author] | `<prd filename>`, `<design spec filename>`, `<trd filename>` | Initial draft | TC-001–TC-048, REQ-01–REQ-03 (every ID in this draft) | — | — |

One appended row per version, never rewritten. The ID columns cover `TC-xxx` cases and any derived `REQ-xx`; `—` means none, and an empty cell means the change wasn't tracked, which is a gap worth fixing.

## 1. Test Plan and Scope
The release or feature under test, and the documents this derives from with their versions. The filename plus version in the header block is this plan's identifier — the ISO 29119-3 test plan identifier, not a second scheme alongside it.

Then the management sections from Stage 5, each under its own heading: test items; features to be tested and features not to be tested; test approach and levels; entry criteria; exit criteria; suspension and resumption criteria; platform coverage matrix; metric and instrumentation coverage; regression scope; test environment and data; roles and responsibilities; schedule and milestones; defect management; test deliverables; metrics and reporting; risks and contingencies; approvals.

## 2. Requirement Inventory
One row per atomic requirement from Stage 1, carrying its upstream ID where it has one and a derived `REQ-xx` where it doesn't.

| ID | Requirement | Category | Source | Priority | needs_review |
|---|---|---|---|---|---|
| PR-01 | A user can see all overdue invoices across clients in one view | Functional | PRD §7 | Critical | false |
| REQ-01 | Session expiry during an unsaved edit preserves the draft | Functional | [no upstream — new in this document] | High | true |

Every `REQ-xx` is a gap in a source document. List them again in Section 7.

## 3. Question Log
Open ambiguities, contradictions, missing constraints, and untestable language from Stage 2 — the source text, why it's a problem, and what decision is needed. This section ships even when it is long, and especially when it is.

## 4. Risk Model
The ranked failure modes from Stage 3, with impact × likelihood, and what coverage each one demands.

## 5. Test Case Table
One row per case, in the full Stage 6 schema.

## 6. Traceability Matrix
Requirement ↔ case, both directions, with every gap called out rather than omitted: requirements with no case, cases with no requirement, critical requirements missing negative, boundary, or permission coverage.

## 7. Assumptions and Open Questions
Every requirement derived with no upstream ID, every case marked `needs_review`, and every coverage gap from Stage 7.

## 8. Next Steps
What has to be decided before this plan can be executed, who owns the question log, and which cases are ready to automate.
```

If the user wants a spreadsheet, export one *in addition to* the Markdown file — never instead of it — putting requirements, questions, and test cases on separate sheets linked by ID. If they want a file to hand to engineers or automation, `id` / `requirement_ids` / `technique` / `automation_candidate` are what downstream automation keys off — but do not generate UI selectors or API payloads from document wording alone. That needs the implemented interface, which is out of scope for a document-only pass.

## Standards this follows

The plan structure follows **ISO/IEC/IEEE 29119-3:2021** (which superseded IEEE 829-2008) — test plan identifier through approvals, including the entry, exit, suspension, and resumption criteria that separate a plan from a case list. Requirement quality is judged against **ISO/IEC/IEEE 29148:2018**. Test design techniques are the standard equivalence, boundary, decision-table, state-transition, and pairwise set from **ISO/IEC/IEEE 29119-4**. Accessibility cases are written against the **WCAG 2.2 AA** success criteria the design spec names.

## Reviewing an existing test plan

When asked to review rather than write, report against the template's section numbers so every gap is addressable, and work Stage 7 as the checklist. Three passes, in this order. **Coverage:** requirements with no case, cases with no requirement, critical requirements missing negative, boundary, or permission coverage, and every `MET-xx` with no instrumentation case. **Oracles:** scan for the banned vague phrases and name every case whose expected result a tester could not observe. **Plan, not case list:** whether entry, exit, suspension, and resumption criteria exist and are countable, and whether the platform matrix is finite rather than "test on mobile". Then say whether the question log looks worked or skipped — a plan drawn from an ambiguous source with an empty log was not reviewed, it was transcribed.

## Handling upstream updates

When re-running against a revised PRD, design spec, or TRD, the diff has a fixed anchor: your own previous version file records the upstream versions it was built from in `**Upstream:**`. Resolve the newest upstream files and read their **Revision History** first — its IDs added / changed / removed columns give you the diff directly, for every version between the one you cited and the current one. Fall back to comparing the documents in full only where those rows are missing or empty. Then regenerate only the cases linked to changed or new IDs and leave previously reviewed cases untouched. Flag cases linked to a removed requirement for review rather than deleting them automatically — the behavior may have moved elsewhere.

Record the upstream versions this plan now covers, so the next re-run has the same anchor. A plan whose `**Upstream:**` is older than the newest document on disk is stale by definition, and that is what the router's consistency review reports.

## What not to do

- Don't invent a business rule, limit, role, or message the source doesn't state — log a question instead.
- Don't accept a subjective or vague phrase as a tested oracle.
- Don't produce one mega end-to-end case per requirement.
- Don't skip non-functional requirements — accessibility, performance, security, privacy, localization, observability.
- Don't silently drop ambiguity. The question log ships every time.
