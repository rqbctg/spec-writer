Use this section structure. Adapt depth to how much there is to say, but never delete a section. One that genuinely doesn't apply is marked `Not applicable — <reason>`; one that applies but has nothing behind it yet is marked `Insufficient evidence — <what would resolve it>`. Both are more useful than a missing section, and the second is a research task the reader can pick up.

```markdown
# Market Requirements Document: [App Name]

**Owner:** [user's name, or "Solo / early-stage"]
**Date:** [today's date]
**Version:** 0.0.1
**Status:** Draft | In review | Approved | Superseded
**Scope:** Product | Feature | Change
**Platforms:** [the full set, primary marked — e.g. "web (primary), iOS, Android — desktop phase 2" — or "undecided"]
**Upstream:** Informal brief
**Downstream:** BRD / PRD

## Revision History

| Version | Date | Author | Upstream version | Summary | IDs added | IDs changed | IDs removed |
|---|---|---|---|---|---|---|---|
| 0.0.1 | [today's date] | [author] | Informal brief | Initial draft | NEED-01–NEED-08 (every ID in this draft) | — | — |

One appended row per version, never rewritten. The ID columns are what let a downstream document diff this one without re-reading it in full; `—` means none, and an empty cell means the change wasn't tracked, which is a gap worth fixing.

## 1. Executive Summary
One paragraph: the customer problem, the target market, the business objective, and the expected outcome. Written so a busy stakeholder gets the whole picture without reading further. Write this last.

## 2. Market Opportunity
The market gap, relevant trends, and why this matters *now*. Narrative and timing only — growth direction, not magnitude. Every number lives in Section 3, cited once; referencing it here is fine, restating it is how the two sections drift apart. Focus on the market, not the app's feature set.

## 3. Market Sizing
*Figures as of [date].* Every number in this document lives here; the rest of the document references these rows rather than restating them.

TAM, SAM, and SOM, each with the figure, the method used to reach it, and the source with its publication date. Where the evidence won't support a number, give a range and say what would narrow it — never a single confident figure with no derivation.

| Measure | Figure | Method | Source | Published |
|---|---|---|---|---|
| TAM | | top-down / bottom-up | | |
| SAM | | | | |
| SOM (12 mo) | | | | |

A source older than 24 months stays usable — say how old it is in the Published column and note the staleness in Section 14, rather than dropping the only evidence there is.

## 4. Target Audience
Segment the market, then profile the personas within it. **Separate the buyer from the user** — they are frequently different people with different pain, and conflating them is the most common way an MRD misleads. For each persona: role, context, the problem in their words, how often it bites, what they use today, and what would make them switch.

Be specific — "freelance designers billing 3–10 clients a month," not "freelancers."

## 5. Target Platforms
Which platforms this must reach, and why — a market question before it is a technical one, because it follows from where the buyers and users already are. State the platform here once; every document downstream inherits it rather than guessing.

| Platform | Primary | Priority | Why — evidence from research | Phase |
|---|:-:|---|---|---|
| Web (responsive) | ✓ | Must | Buyers evaluate at a desk; no install friction for trial | 1 |
| iOS | | Should | 60% of the segment's usage is mobile (source) | 2 |
| Android | | Should | Same usage pattern; larger share outside North America | 2 |
| Desktop (macOS/Windows) | | Could | Only if offline editing proves to be a real blocker | — |

Exactly one platform is primary — it ships first and breaks ties when platforms want different things. Then state the **parity intent** in a sentence, because it is the most expensive thing to leave unsaid in a multi-platform build:

> *Parity intent:* full feature parity between web and mobile, except bulk import and admin settings, which stay web-only. Desktop, if built, matches web.

Where platforms are phased, say what "phase 2" depends on — a date, a metric, or a decision — rather than leaving it as an intention.

Cover the ones that apply: **web** (responsive, PWA, browser support), **mobile** (iOS, Android, tablet), **desktop** (macOS, Windows, Linux — native or Electron-class), and any **non-UI surface** (API, CLI, embedded, watch, TV). Note where one platform is a hard requirement of the market rather than a preference — regulated industries that forbid mobile, field work with no connectivity, an enterprise buyer that mandates a desktop client.

If the platform genuinely isn't decided yet, say so explicitly and write the rest of the document platform-neutrally. An undecided platform is a legitimate early state; an unstated one silently becomes whatever the first engineer assumes.

## 6. Customer Problems and Pain Points
The concrete pain: who feels it, how often, and what it costs them in time, money, errors, or stress. Support with what research turned up — reviews, forum threads, survey data.

## 7. Market Research and Insights
A short synthesis of the research: relevant stats, report findings, observed patterns, each attributed to its source.

## 8. Competitive Analysis
Direct competitors, adjacent tools, and the manual workarounds people use today. Note strengths, weaknesses, pricing patterns, and where the gap is. A table works well here.

## 9. Business Goals
What building this should accomplish — validate a niche, generate revenue, build a portfolio piece, solve the founder's own problem at scale. Keep this honest to what the user actually said; mark it an open question if they didn't say. One row per goal, because Section 15 and every downstream metric cite these IDs rather than quoting the prose.

| ID | Goal | Why it matters | Evidence or source |
|---|---|---|---|
| GOAL-01 | Validate that freelancers will pay for invoice chasing before building the full product | Decides whether stage 2 happens at all | User's stated intent |

A goal the user didn't state is an open question in Section 14, not an invented `GOAL-xx`.

## 10. High-Level Product Requirements
What the product must let users accomplish, at a strategic level — not a feature list, not UI, not a stack. One row per need.

| ID | Need | Platforms | Which pain point it addresses | Priority |
|---|---|---|---|---|
| NEED-01 | Users need a way to see every overdue invoice across all clients at a glance | All | Section 6, missed follow-ups | Must |
| NEED-04 | Users need to capture a receipt photo at the moment of purchase | Mobile only | Section 6, lost receipts | Should |

The **Platforms** column is what keeps a multi-platform product traceable as it diverges. "All" is the common case; naming a subset is a decision that should survive into the PRD rather than being rediscovered during design.

## 11. Positioning
A single positioning statement, in the standard form, plus the one claim a competitor could not make:

> For **[target persona]** who **[statement of need]**, **[product]** is a **[category]** that **[key benefit]**. Unlike **[primary alternative]**, it **[primary differentiator]**.

## 12. Pricing, Packaging, and Distribution
What the market already pays and how it prefers to buy: competitor price points and models (subscription, usage, perpetual, free tier), the willingness-to-pay signal research turned up, plausible packaging tiers, and the channels this reaches buyers through. Mark as hypothesis where research is thin — but don't omit it. A product strategy with no pricing or channel view isn't a strategy.

## 13. Regulatory and Compliance Landscape
Rules that constrain entry or operation — data protection (GDPR, CCPA), sector rules (HIPAA, PCI DSS, SOC 2), accessibility mandates, platform or app-store policy, licensing. Where none apply, say so explicitly; an empty section reads as unexamined.

## 14. Assumptions and Open Questions
Every assumption made to fill a gap, plus market risks, competitive risks, and questions research couldn't resolve. Thin evidence and guesses get flagged here honestly.

## 15. Success Metrics
How the team would know this worked after launch — adoption, retention, activation, revenue. Every metric cites the `GOAL-xx` it measures; a metric with no goal is either a vanity number or a goal nobody wrote down, and both need resolving before the PRD inherits it.

| Metric | Measures | Baseline | Target | By when |
|---|---|---|---|---|
| Paid conversion from trial | GOAL-01 | None — pre-launch | 5% | 90 days after launch |

Give each a baseline, a target, and a date — a metric with no baseline can't be shown to have moved. Where the baseline doesn't exist yet, write "none — pre-launch" rather than leaving it blank. These are the anchors the PRD's `MET-xx` traces back to through `GOAL-xx`.

## Next Steps
The next document, its owner, and what must be true before it starts.
```
