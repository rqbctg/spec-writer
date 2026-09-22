---
name: mrd-writer
description: "Turns a simple app or product idea into a full Market Requirements Document (MRD) with market research and competitive analysis. Use whenever the user mentions an MRD, wants to validate a product/app idea before building it, or asks about market opportunity, target audience, or competitors for an idea."
---

# MRD Writer

Stage 1 of the spec-writer chain. Feeds `brd-writer` and `prd-writer`.

## What this does

Takes a simple app or product idea — sometimes just a sentence — and turns it into a complete Market Requirements Document: a strategic document that explains *why* the idea is worth building, before anyone talks about features or a build plan. An MRD answers "what market opportunity is this chasing," "who actually has this problem," "how are they solving it today," and "how will we know this worked." It deliberately stays away from feature lists and technical specs — that's the PRD's job.

Because the input is usually a rough idea rather than a company with a research team, do the market research yourself, reason about the audience and competitive landscape, and produce a document that reads like it came out of a real product-discovery process — not a template with blanks.

## Workflow

### Step 1 — Understand the idea

Read what the user gave you. A "simple app idea" might be one line ("an app that helps freelancers track invoices") or a short paragraph. Identify, even tentatively: what the app does, who it's plausibly for, and what problem it solves.

### Step 2 — Ask the user for scope and platforms

**This is the one question to ask before drafting.** The MRD is where scope and platform are decided for the entire chain — every document below inherits both from here — so guessing them wrong is expensive in a way no other early guess is. Ask once, in a single batched question, and offer a recommendation so the user can accept rather than compose an answer.

Ask for:

1. **Scope** — is this a whole product, or a feature of something that already exists? Recommend based on what they described.
2. **Platforms** — web, iOS, Android, macOS, Windows, Linux, API or CLI, or undecided. **Multiple platforms are the normal answer, not the exception**, so ask for a set rather than a single choice, and for three things about that set: which platform is **primary** (the one that ships first and wins a tie), which are **phased** and roughly when, and what the **parity intent** is — full parity, deliberately reduced scope on some platforms, or capability that exists on only one. Say which way the research points and why, so they're confirming a recommendation rather than starting from a blank.

Then act on the answer:

- **Whole product** → continue with the full MRD below.
- **A feature** → an MRD is usually the wrong document, because the market, personas, and positioning are already settled and re-deriving them buries the one new question. Say so and point at `prd-writer` at feature scope. Write a feature-scale MRD only when the feature genuinely opens a new market — a new segment, a new buyer, a change in positioning, or a new pricing tier — and then keep it to what actually changes: that segment, its evidence, the competitive response, and sizing for it alone.
- **Platforms named** → record the full set verbatim in the header block and Section 5 — with the primary marked, the phasing kept, and the parity intent stated — and let them shape the research: store economics and review policy for mobile, browser reach and no-install trial for web, procurement and offline field use for desktop. With several platforms, research each one's economics separately; a segment that's cheap to reach on web can be expensive to reach through a store.
- **Undecided, or the user defers** → that's a legitimate answer, not a failure. Record "undecided," write the document platform-neutrally, and use Section 5 to lay out the evidence for each candidate so the decision has something to stand on later. Never silently pick one.

Don't hold up the whole document waiting. If the user doesn't answer, state your assumption plainly in the header and in Section 14, and draft — an assumption on the record is recoverable; a silent one isn't.

### Step 3 — Otherwise, ask only if genuinely stuck

Beyond scope and platforms, don't interrogate — most gaps can be filled with reasonable assumptions plus research, and over-questioning a "simple idea" defeats the point. Ask only when a core fact is unknowable from research *and* materially changes the document: the idea is ambiguous between two very different products, or the user has a specific target market in mind you shouldn't guess at. State assumptions in Section 14 rather than blocking on them.

Where you do have more to ask, fold it into the Step 2 question rather than sending a second round.

### Step 4 — Research the market

Ground the document in reality rather than invented numbers. Where you have web search or browsing, use it. Where you don't, say so plainly in Section 7 and mark every research-dependent claim as unverified — a document that admits it couldn't check is far more useful than one that guesses confidently. Look for:

- **Market sizing** — TAM, SAM, and SOM, each with the method stated (top-down from an analyst figure, or bottom-up from users × price). An unsourced number with no method is worse than a range with one
- Growth signals for the category or an adjacent one
- Evidence the target users actually experience the problem — forum complaints, review-site pain points, survey or industry-report stats
- How people solve this today — direct competitors, adjacent tools, manual workarounds (spreadsheets, generic tools bent into shape)
- Competitor strengths, weaknesses, pricing patterns, and gaps to differentiate on
- Trends that make this a good or bad time to build — platform changes, regulatory shifts, technology enablers

Cite what you find inline (source name, and a link where you have one) rather than presenting it as settled fact. Where research is thin or conflicting, say so — an honest "limited evidence" beats a confident fabrication, and it belongs in the risks section anyway.

**Date every figure.** Market data goes stale faster than anything else in this chain. Prefer sources published within the last 24 months, give each figure its publication date inline, and state the as-of date at the head of Section 3. Where the only available figure is older than that, use it and say how old it is — a dated number a reader can discount beats an undated one they have to trust.

### Step 5 — Draft the MRD

Use the document template. Keep it grounded in the customer problem, not the feature set — if you catch yourself listing UI details or a tech stack, that content belongs in a PRD or TRD. Every non-obvious claim should be traceable to research or to something the user told you.

Give each item in Section 10 a `NEED-xx` ID, and each goal in Section 9 a `GOAL-xx` ID. These are the anchors the rest of the chain traces back to, so write them as durable customer needs and outcomes, not as features that might change.

At feature scope, namespace both with the feature's slug — `NEED-EXPORT-01`, `GOAL-EXPORT-01` — so the feature's IDs merge into the product's set without colliding. Use the same slug across every document for that feature.

### Step 6 — Quality bar before delivering

- Exactly one platform is marked primary, and the parity intent is stated in a sentence — not implied by the table.
- Every phased platform names what phase 2 depends on: a date, a metric, or a decision.
- Every `NEED-xx` has a Platforms value; `All` is a choice, not a default to fall back on.
- Every `NEED-xx` is a durable customer need, not a feature — no UI, no screens, no stack.
- Every TAM/SAM/SOM cell has a figure, a method, and a source; a figure with no derivation is replaced by a range plus what would narrow it.
- Every research-dependent claim is either cited or explicitly marked unverified, with the reason stated in Section 7.
- Every figure carries its publication date, and Section 3 states its as-of date.
- Buyer and user are separated in Section 4 wherever they are different people.
- Every `GOAL-xx` traces to something the user actually said; the rest are open questions in Section 14.
- Every metric in Section 15 cites a `GOAL-xx` and has a baseline, a target, and a date.
- Sections 12 and 13 are present and answered — a hypothesis or an explicit "none apply", never an omission.
- Revision History carries a row for this version, with the `NEED-xx` and `GOAL-xx` IDs added, changed, and removed since the previous one.
- Every section that doesn't apply is marked `Not applicable — <reason>` or `Insufficient evidence — <what would resolve it>`, never deleted.
- Nothing in the document describes how the product works — that's the PRD's job, and the most common way this document fails.

### Step 7 — Save and deliver

**This document set always ends in a Markdown file. Never deliver it as ordinary chat prose.**

Deliver by the highest tier the environment supports:

1. **Filesystem available** (coding agent, IDE, terminal, code interpreter) — write `docs/mrd-writer/<slug>-mrd-v<version>.md`. Create `docs/` only if it is missing — never recreate or replace an existing one — then create the `mrd-writer/` subfolder inside it if that is missing too, so each skill's output stays in its own folder. Where the project already has a documentation directory, use that in place of `docs/`, with the same `mrd-writer/` subfolder inside it. Report the path.
2. **Files or a document surface, but no repo** (downloadable file, canvas, doc, notebook) — create it there named `<slug>-mrd-v<version>.md` and hand over the download or link.
3. **Chat only** — put the entire document in one fenced code block tagged `markdown`, with nothing else inside the fence, and name the file the user should save it as: `<slug>-mrd-v<version>.md`. Everything you want to say goes before the fence, never interleaved.

Use one consistent `<slug>` across every document in the chain for a given product — the same slug the first document in the chain started with — so the six files read as one set. At feature scope the slug is the feature, not the product. The folder is per skill, the slug is per product: `docs/mrd-writer/<slug>-mrd-v<version>.md`.

**Versioning.** Every write creates a new file; an existing version file is never overwritten or deleted.

Before drafting, list `docs/mrd-writer/` and find the highest `v<major>.<minor>.<patch>` among files matching `<slug>-mrd-v*.md`. Compare the three numbers numerically, so `v0.0.10` is newer than `v0.0.9`. That file is the previous version — read it first, so the new document is a revision rather than a restart.

- No previous file — start at `v0.0.1`.
- **Patch** (`v0.0.x`) — edits, corrections, gaps filled, wording.
- **Minor** (`v0.x.0`) — new sections or requirements, or a re-run against a revised upstream document.
- **Major** (`vx.0.0`) — **Status** reaches Approved, or a rewrite that invalidates the documents downstream of this one.

The `**Version:**` line in the header block always carries the same number as the filename, and every version appends a row to the document's **Revision History** — what changed, and which IDs were added, changed, and removed. Report the new path and that summary, not just that a file was written.

**The changelog is mandatory.** After writing the file, append one bullet to `docs/CHANGELOG.md` — at the root of `docs/`, beside the per-skill subfolders — under today's ISO date heading, creating the file or the heading if either is missing:

```markdown
- **MRD** `mrd-writer/<filename>` — <one-line summary>. +<IDs added>, ~<IDs changed>, -<IDs removed>. Upstream `<upstream path>` (every upstream, comma-separated, or "informal brief" where there is none).
```

The IDs must match the Revision History row for this version. Never edit a past entry — a correction is a new version with a new entry. Per-platform writes get one bullet each — and where this stage writes a single file whatever the platform set, that file gets one bullet. The document is not delivered until this entry exists.

Whatever the tier:

- The document is Markdown: header block first, then every section. A section with nothing to say carries `Not applicable — <reason>` or `Insufficient evidence — <what would resolve it>`, never an omission.
- Report the **filename plus a 3–5 line summary** — what it covers, the biggest assumption, the open questions that need a human. Don't restate the body in prose.
- Other formats — PDF, Google Doc, Word, spreadsheet — are exports *from* the Markdown, never replacements for it.
- Re-running after the idea changes or new research lands produces the next version file — see the versioning rule above — rather than editing the previous one in place.


### Step 8 — Hand off

Note that an MRD is a living document, meant to be revisited as the idea evolves or new research lands. Point at the natural next step: `brd-writer` if the project needs sponsor or budget sign-off, `prd-writer` if the user is building it themselves and just needs to decide what to build.

## MRD Template

<!-- include-start: references/template.md -->
Read `references/template.md` in this skill folder before drafting, and follow it exactly — section list, header block, Revision History, and the absent-section markers.
<!-- include-end -->

## Reviewing an existing MRD

When asked to review rather than write, report against the template's section numbers so every gap is addressable, and work the Step 6 quality bar as the checklist. Three passes. **Evidence:** every figure with no method, no source, or no date, and every claim asserted where the document elsewhere admits it couldn't verify — market data is the first thing to go stale, so check Section 3's as-of date before anything else. **Layer:** every sentence describing how the product works rather than what problem it solves for whom; that content belongs in the PRD and its presence here is the most common way this document fails. **Decisions:** whether exactly one platform is primary, whether the parity intent is stated, and whether every `NEED-xx` and `GOAL-xx` still reflects what the user actually said. Then name the smallest concrete edit that closes each gap, and say plainly if the research now argues against the opportunity — that is a finding, not a failure of the review.

## Standards this follows

Structured on the **Pragmatic Institute** market-requirements framework: market problem first, buyer and user personas separated, sizing quantified, positioning stated explicitly, and a distribution and pricing view rather than features. Where a section can't be evidenced, it stays in the document marked as a gap — the shape of the standard is what makes the gap visible.

## Writing principles

- **Problem before solution.** The point of an MRD is validating that a problem is real and worth solving before anyone designs anything. Resist the pull toward describing the app.
- **Evidence over assertion.** A cited source or the user's own context is worth far more than a confident guess. Where you have no evidence, say so instead of inventing a number.
- **Concise, not exhaustive.** A tight, well-reasoned paragraph beats a wall of bullets.
- **Don't let it become a PRD.** If a sentence describes *how* the product works rather than *what problem it solves for whom*, cut it or move it out.
- **It's a real decision input.** The user may use this to decide whether to build at all — give your honest read, including when the research suggests the opportunity is weak or heavily contested.

## How an MRD differs from the rest of the chain

- **MRD** (this document) — what market problem should we solve?
- **BRD** — what business outcome should this support, and what will it take?
- **PRD** — what should the product actually do?
- **Design Spec** — what does the user see and do?
- **TRD** — how will engineering build it?
- **QA Test Plan** — how do we prove it works?

If the user asks for a PRD, feature spec, or roadmap next, that's a natural follow-on but a different document — don't fold it into the MRD.
