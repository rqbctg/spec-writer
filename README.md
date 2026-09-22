# spec-writer

A connected set of software specification and product-documentation instructions that runs on any AI assistant — Claude, ChatGPT, Grok, Gemini, Cursor, Copilot, or anything else that reads a prompt. Six documents, one chain — each generated from the one above it, each carrying traceable requirement IDs, so an idea can be followed from market opportunity through to test coverage.

| # | Document | Skill | Answers |
|---|---|---|---|
| 1 | MRD — Market Requirements | `mrd-writer` | What market problem should we solve, and is it worth solving? |
| 2 | BRD — Business Requirements | `brd-writer` | What business outcome does this support, and what will it take? |
| 3 | PRD — Product Requirements | `prd-writer` | What should the product actually do? |
| 4 | Design Spec | `design-spec-writer` | What does the user see and do, screen by screen? |
| 5 | TRD — Technical Requirements | `trd-writer` | How will engineering build it? |
| 6 | QA Test Plan | `qa-test-plan-writer` | How do we prove it works? |

`spec-writer` is the router skill: it picks the right stage, holds the shared conventions, and can review an existing set of documents for coverage, orphans, layer violations, staleness, and contradictions.

The PRD is a living document rather than a one-off: it moves through six stages — speclet, one-pager, cross-functional kickoff, solution review, launch readiness, impact review — filling more of the same 17-section template as confidence grows, so an early hunch isn't dressed up as a launch-ready contract.

## Install

**Any editor or agent, one command:**

```
npx spec-writer install          # detects Claude Code, Cursor, Copilot, AGENTS.md
npx spec-writer install all      # install into every one of them
npx spec-writer install claude --global
```

**ChatGPT, Grok, Gemini** — nothing to install; they take a pasted prompt:

```
npx spec-writer copy prd         # to clipboard, paste and send your idea
npx spec-writer print all > spec-writer.md
```

```
npx spec-writer list             # the six documents
npx spec-writer --help
```

**Claude Code** — or as a local plugin marketplace, if you prefer plugins to skills:

```
/plugin marketplace add rqbctg/spec-writer
/plugin install spec-writer@spec-writer
```

**Everywhere else** — `dist/` holds ready-made bundles: paste-anywhere prompts in `dist/universal/`, short stubs for capped instruction fields in `dist/instructions/`, Cursor `.mdc` rules, Copilot instructions, and `AGENTS.md` in `dist/agents/`. Per-assistant install notes are in `dist/platforms/`. See **[PLATFORMS.md](PLATFORMS.md)**.

The Markdown in `skills/` is the source of truth and is vendor-neutral. After editing it, run `python3 build.py` to regenerate `dist/`.

## Use

Three ways to start, all equivalent:

```
/prd-writer  a way for freelancers to chase overdue invoices     # name the stage
/spec-writer  I need docs for this idea, not sure which          # let the router pick
"write me a PRD for this"                                        # no command at all
```

Skills trigger on their own — asking for "a test plan", "a tech spec", or "requirements for this feature" reaches the right one without naming it. `/spec-writer` is for when you don't know which document you need, or want several in sequence.

### A full run, start to finish

The example below is a product-scope run on three platforms. Type each command after the previous document exists — every stage reads the file, not the conversation.

**1. Start at the top.** No upstream document exists, so this stage asks you two things once — scope and platforms — and never asks again:

```
/mrd-writer  freelancers lose money chasing overdue invoices by hand
```

> Scope? **Product**. Platforms? **web (primary), iOS, Android**, full parity.

```
docs/mrd-writer/invoice-tracker-mrd-v0.0.1.md
docs/CHANGELOG.md                                    ← created, first entry
```

The MRD carries `NEED-01…` market needs, the primary platform, and the parity intent. Everything downstream inherits both without re-asking.

**2. Business case, if someone has to fund or approve it.** Skip it when nobody signs off:

```
/brd-writer
```

```
docs/brd-writer/invoice-tracker-brd-v0.0.1.md        ← BR-01 → NEED-01
```

**3. The PRD.** Three platforms were declared, so this writes three complete documents, not one with a platform column:

```
/prd-writer  launch readiness stage
```

```
docs/prd-writer/invoice-tracker-prd-web-v0.0.1.md
docs/prd-writer/invoice-tracker-prd-ios-v0.0.1.md
docs/prd-writer/invoice-tracker-prd-android-v0.0.1.md
```

`PR-01` means the same requirement in all three; a mobile-only requirement like `PR-06` (scan a paper invoice with the camera) exists only in the two mobile files. Success metrics get IDs too — `MET-01` — so the TRD's NFRs and the test plan can cite them.

**4. Design spec, TRD, test plan.** These can run in parallel once the PRD is at solution-review or launch-readiness stage:

```
/design-spec-writer     # screens, states, components, accessibility
/trd-writer             # architecture, data model, APIs, NFRs
/qa-test-plan-writer    # cases, coverage, regression scope
```

Each resolves its own upstream from disk — newest version, matching platform — and records exactly which file it read:

```markdown
**Upstream:** `invoice-tracker-prd-ios-v0.0.1.md`, `invoice-tracker-design-spec-ios-v0.0.1.md`
```

### Revising a document

Say the PRD changes. Re-run the stage; it finds the highest version on disk, writes the next one beside it, and never touches the old file:

```
/prd-writer  add offline receipt capture, mobile only
```

```
docs/prd-writer/invoice-tracker-prd-ios-v0.1.0.md        ← v0.0.1 still there
```

Minor bump, because requirements were added. Inside the file, a Revision History row; in `docs/CHANGELOG.md`, a bullet:

```markdown
## 2026-09-22

- **PRD** `prd-writer/invoice-tracker-prd-ios-v0.1.0.md` — offline receipt capture added.
  +PR-08, +MET-02, ~PR-01. Upstream `brd-writer/invoice-tracker-brd-v0.0.1.md`.
```

Now re-run the test plan. It reads those `+`/`~` IDs instead of re-reading the whole PRD, and regenerates only the affected cases:

```
/qa-test-plan-writer
```

### One feature, not a whole product

Most work starts here. Skip the MRD and BRD, start at the PRD, and namespace the IDs so they merge into the product's existing set:

```
/prd-writer  CSV export for the invoice list, web only — feature scope
```

```
docs/prd-writer/invoice-export-prd-v0.0.1.md     ← PR-EXPORT-01, PR-EXPORT-02
```

One file, because the feature ships on one platform. Its own slug, so it sits beside the product's documents rather than inside them.

The section that earns its place at this scope is *what it touches* — the screens, shared components, API contracts, and data the feature modifies. That list becomes the TRD's blast radius and the test plan's regression scope.

### Checking an existing set

```
/spec-writer  review my docs
```

Reports coverage (a parent ID with no child), orphans (a child citing a parent that doesn't exist), layer violations (a database in the PRD), staleness (a document built from an upstream version that's no longer newest), contradictions, platform drift between per-platform files, and any version missing its changelog entry.

### Outside a coding agent

ChatGPT, Grok, and Gemini can't write files, so the same chain runs by paste:

```
npx spec-writer copy prd        # full instructions to clipboard
```

Paste, send your idea, and the document comes back in one fenced Markdown block with its filename named — save it as `docs/prd-writer/<slug>-prd-v0.0.1.md` yourself and attach it when you run the next stage.

## Output

Every document is a Markdown file. Each skill owns one subfolder of `docs/`, named after the skill, and `docs/` itself is created only when it is missing — an existing one is written into untouched. Where the project already has a documentation directory, that is used instead, with the same per-skill subfolders inside it.

```
docs/
  CHANGELOG.md         every document version, newest first
  mrd-writer/          invoice-tracker-mrd-v0.0.1.md
  brd-writer/          invoice-tracker-brd-v0.0.1.md
  prd-writer/          invoice-tracker-prd-ios-v0.1.0.md
                       invoice-tracker-prd-android-v0.1.0.md
                       invoice-tracker-prd-web-v0.1.0.md
  design-spec-writer/  invoice-tracker-design-spec-ios-v0.0.2.md
  trd-writer/          invoice-tracker-trd-ios-v0.0.1.md
  qa-test-plan-writer/ invoice-tracker-test-plan-ios-v0.0.1.md
```

### Versioning

The filename ends in its version. Each skill reads the highest version already in its folder, then writes the next one **alongside** it — nothing is overwritten or deleted, so the folder is the document's history and every document can cite the exact upstream version it was built from.

| Bump | When |
|---|---|
| `v0.0.1` | first write |
| patch `v0.0.x` | edits, corrections, gaps filled |
| minor `v0.x.0` | new sections or requirements, or a re-run against a revised upstream document |
| major `vx.0.0` | **Status** reaches Approved, or a rewrite that invalidates downstream documents |

Versions compare numerically, so `v0.0.10` is newer than `v0.0.9`. The header block's **Version** always matches the filename.

Two records go with every version, and both are required. Inside the document, a **Revision History** row: summary, upstream version, and the IDs added, changed, and removed. Across the set, a bullet in `docs/CHANGELOG.md`:

```markdown
## 2026-09-22

- **PRD** `prd-writer/invoice-tracker-prd-ios-v0.1.0.md` — offline receipt capture added.
  +PR-08, +MET-02, ~PR-01, -PR-04. Upstream `brd-writer/invoice-tracker-brd-v0.2.0.md`.
```

Entries are appended, never rewritten; a correction is a new version with a new entry. Per-platform writes get one bullet each. Downstream stages read the Revision History rows to diff an upstream document instead of re-reading it in full.

### One document per platform

Where more than one platform is declared, four stages produce a complete document per platform — **PRD, design spec, TRD, and QA test plan**. The MRD and BRD stay single; market and business cases are not platform-bound.

`<slug>-<type>-<platform>-v<version>.md`, with `<platform>` one of `web`, `ios`, `android`, `macos`, `windows`, `linux`, `api`. A single platform, or none, means one file with no platform token.

Each file is standalone — shared behavior written out in full, not cross-referenced — which costs duplication, so four rules keep the set honest:

- **IDs are global.** `PR-01` is the same requirement in every file; a platform-only requirement takes the next ID from the same sequence and appears in one file.
- **Shared content is written identically**, so a diff between two platform files shows only real divergence.
- **A shared change touches every file** in the same run, each bumped to its next version.
- **Parity is stated in every file**, with the sibling files named.

`spec-writer`'s consistency review checks for platform drift: a shared ID whose text differs between files, or a platform file left behind at an older version.

## Scope

Works at three scopes — a whole product, a single feature of an existing one, or a small change. Pick the scope and the chain shortens accordingly, rather than putting a two-week feature through six product-scale documents.

| | **Product** | **Feature** | **Change** |
|---|---|---|---|
| MRD | Full | Only if it opens a new segment | Skip |
| BRD | Full | Only if it needs its own funding or sign-off | Skip |
| PRD | Full | **Start here** — scoped to the feature | One page |
| Design Spec | Full | New and changed screens only | Only if the UI changes |
| TRD | Full | The delta, plus blast radius | Only if non-obvious |
| QA Test Plan | Full | New cases plus regression scope | Cases plus regression scope |

At feature scope the rules are: inherit product context rather than restating it, namespace IDs with a feature slug (`PR-EXPORT-01`) so they merge into the product's set, and name what the feature *touches* — that section becomes the TRD's blast radius and the test plan's regression scope.

## Traceability

Every numbered item gets a stable ID and cites its parent, so any test case can be traced back to the market need that justifies it.

```
MRD   NEED-01                       market need
      GOAL-01                       business goal — root of the outcome chain
BRD   BR-01      → NEED-xx/GOAL-xx  business requirement
      R-01       → document-local   risk register entry
PRD   PR-01      → BR-xx/NEED-xx    product requirement
      MET-01     → BR-xx/GOAL-xx    success metric or guardrail
      DEC-01     → document-local   decision-log entry
DS    FLOW-01    → PR-xx            user flow
      SCR-01     → PR-xx            screen
      CMP-01     → SCR-xx           component
TRD   FR-01      → PR-xx/SCR-xx     functional requirement
      NFR-01     → MET-xx/PR-xx     non-functional requirement, or a BRD constraint
      API-01     → FR-xx            endpoint
QA    REQ-01     → no upstream      derived requirement — flags a gap in the source
      TC-001     → any ID above     test case
```

Multiple platforms are the normal case, so every numbered item also carries the platforms it applies to — `All`, or a named subset — which is what keeps a product traceable as its platforms diverge:

```
NEED-04 → BR-09 → PR-08 → SCR-09 / CMP-07 → FR-12 → TC-041     all Mobile only
```

The MRD names one **primary** platform and states the **parity intent** — full parity, reduced scope somewhere, or single-platform capability — because unstated parity is the most expensive assumption in a multi-platform build.

An item with no upstream parent is marked `[no upstream — new in this document]` and raised in Assumptions and Open Questions — it's either a gap in the parent document or scope creep, and both are worth surfacing.

## Standards

| Document | Standard |
|---|---|
| MRD | Pragmatic Institute framework |
| BRD | BABOK v3; ISO/IEC/IEEE 29148:2018 (BRS) |
| PRD | INVEST stories, Given/When/Then, MoSCoW |
| Design Spec | WCAG 2.2 AA; W3C ARIA Authoring Practices |
| TRD | ISO/IEC/IEEE 29148:2018; ISO/IEC 25010:2023 |
| QA Test Plan | ISO/IEC/IEEE 29119-3:2021 |

Requirements use the 29148 sentence form — *[condition] [subject] [action] [object] [constraint]*, with *shall* binding — and are judged against its nine quality characteristics: necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming.

## Shared rules

Every skill in the chain follows the same conventions, defined in `skills/spec-writer/SKILL.md`:

- **Layer discipline** — no feature lists in an MRD, no databases in a PRD, no endpoints in a design spec.
- **Ask once, for scope and platforms** — the first document in the chain asks the user both, with a recommendation attached; every document after inherits them and never re-asks. Beyond that, don't interrogate: draft from thin input and label the assumptions.
- **Evidence over assertion** — cite the source or admit the gap; never invent a market size, a budget, or a business rule.
- **Mandatory sections** — every document opens with a *Revision History* table and ends with *Assumptions and Open Questions* and *Next Steps*.
- **Track what changed** — each new version appends one Revision History row: summary, upstream version, and the IDs added, changed, and removed. Downstream stages diff from those rows instead of re-reading the document.
- **Changelog is mandatory** — every document version also appends a bullet to `docs/CHANGELOG.md`, the one place that answers what moved across the whole set and when. A version with no entry is an incomplete delivery.
- **Resolve upstream from disk** — each stage reads the newest version in the producing skill's folder, matching its own platform, and cites that exact filename in `**Upstream:**`. That line is what makes the staleness check mechanical.
- **Deliver a file** — always a Markdown document, by the highest tier the environment supports: written to `docs/<skill-name>/`, handed over as a download, or emitted as one fenced block with its filename named. Never loose chat prose. Naming, versioning, and the per-platform split are in **[Output](#output)** above.

## Layout

```
bin/cli.js                        the npx installer
skills/                           source of truth — portable Markdown
build.py                          regenerates dist/ for every platform
dist/                             generated bundles for every other assistant
.claude-plugin/                   Claude Code plugin manifest
skills/spec-writer/                router + shared conventions
skills/mrd-writer/                stage 1
skills/brd-writer/                stage 2
skills/prd-writer/                stage 3
skills/design-spec-writer/        stage 4
skills/trd-writer/                stage 5
skills/qa-test-plan-writer/       stage 6
```

Each skill folder holds a short `SKILL.md` — routing, workflow, and quality bar — plus a
`references/` folder carrying the bulk it points at: the document template, and for the
router the platform tables and the consistency-review checks. An agent loads `SKILL.md`
first and reads a reference file only when it reaches the step that needs it. `build.py`
inlines every reference into `dist/`, so the generated bundles stay standalone.
