Use this section structure whatever the stage. The stage decides how much of it exists, not what it is called — a speclet fills sections 1–5, a launch-ready PRD fills all of them. No section is ever deleted; an absent one is marked with one of three forms, and which one you pick is itself information:

- `Not yet — stage <n>` — this section belongs to a later stage. The common case in an early PRD.
- `Not applicable — <reason>` — this section will never apply to this product.
- `Insufficient evidence — <what would resolve it>` — it applies and is due now, but nothing supports it yet.

The header block and **Revision History** are not in this table because they are required at every stage without exception, a speclet included.

| Stage | Sections that must be real |
|---|---|
| 1 Speclet | 1–5 |
| 2 One-pager | 1–6, 10, 15, 17 |
| 3 Cross-functional | add 7, 11, 13 |
| 4 Solution review | add 8, 9 |
| 5 Launch readiness | all except 14 |
| 6 Impact review | all, 14 written after release |

**A stage advance is a version event.** Moving from one stage to the next is the most meaningful change this document undergoes, and it is the one bump the generic versioning rules below don't name. Advancing bumps the **minor** version, moves the `**Stage:**` header with it, and names the new stage in the Revision History summary — `stage 4 solution review`. A PRD whose Stage field disagrees with the sections it actually fills is the single most misleading state this document can be in.

```markdown
# Product Requirements Document: [Product or feature name]

**Owner:** <name or role>
**Date:** <today's date>
**Version:** 0.0.1
**Status:** Draft | In review | Approved | Superseded
**Stage:** Speclet | One-pager | Cross-functional | Solution review | Launch readiness | Impact review
**Scope:** Product | Feature | Change
**Platforms:** <carried from the BRD or MRD, unchanged — or "platform-neutral">
**Upstream:** <exact upstream filename — `invoice-tracker-brd-v0.2.0.md` — or "Informal brief">
**Downstream:** Design Spec, TRD, QA Test Plan

## Revision History

| Version | Date | Author | Upstream version | Summary | IDs added | IDs changed | IDs removed |
|---|---|---|---|---|---|---|---|
| 0.0.1 | [today's date] | [author] | `<brd or mrd filename>`, or Informal brief | Initial draft, stage 1 speclet | PR-01–PR-08, MET-01–MET-02 (every ID in this draft) | — | — |

One appended row per version, never rewritten. The ID columns are what let a downstream document diff this one without re-reading it in full; `—` means none, and an empty cell means the change wasn't tracked, which is a gap worth fixing.

## 1. Summary
One paragraph: the opportunity, the user it serves, the business outcome, and the decision this document is asking for. Write it last.

## 2. Problem and Evidence
The user problem in the user's terms, the segment it affects, and the evidence it is real — research, support volume, usage data, or the upstream MRD's `NEED-xx`. "Limited evidence" is a legitimate finding; an invented number is not.

## 3. Goals, Success Metrics, and Guardrails
What changes if this works, stated as measurable items with stable IDs so the TRD's NFRs and the test plan can cite them.

| ID | Metric | Type | Definition | Baseline | Target | Instrumentation | Upstream |
|---|---|---|---|---|---|---|---|
| MET-01 | Overdue invoices followed up within 7 days | Success | Share of overdue invoices with a logged follow-up | 34% | 70% by Q3 | `invoice_followup_logged` | BR-01 |
| MET-02 | Invoice list load time | Guardrail | p95 time to interactive on the overdue view | 1.4 s | ≤ 1.5 s | RUM timing | [no upstream — new in this document] |

Every metric names its type — success or guardrail — a number, and how it is measured. A metric with no instrumentation is a wish.

The Upstream column cites the `BR-xx` this metric serves, or the MRD's `GOAL-xx` where there is no BRD. A guardrail often has no parent — that is legitimate, and it carries `[no upstream — new in this document]` plus a Section 15 entry rather than a dash.

## 4. Target Users
The personas or segments this serves, carried from the MRD where one exists. At feature scope, cite the product's personas rather than restating them.

## 5. Scope and Non-Goals
What ships, and an explicit list of what does not. Carry the parity intent from MRD Section 5 here, so "not on mobile in phase 1" is a stated decision. Non-Goals is what prevents scope creep; a placeholder here makes the whole section worthless.

## 6. Solution and User Journey
The chosen direction and the journey through it, plus the alternatives rejected and why. State a recommendation rather than a pile of unranked options.

## 7. Product Requirements
The `PR-xx` table — see the requirement-table rules below for the columns, the platform rule, and the one-behavior rule. Stories, where used, go here in *As a / I want / so that* form with Given/When/Then acceptance criteria.

## 8. Quality Requirements
Accessibility, privacy, performance, security, localization, and platform policy, each as a product-level requirement with a number or a conformance level where one applies. What the TRD turns into `NFR-xx` starts here — which only works if each one is citable, so these take `PR-xx` IDs from the same sequence as Section 7, with Quality as the type.

| ID | Requirement | Type | Platforms | Target | Upstream |
|---|---|---|---|---|---|
| PR-11 | Every flow in Section 7 is operable by keyboard alone | Quality — accessibility | Web | WCAG 2.2 AA | BR-04 |
| PR-12 | The overdue view renders within 1.5 s at p95 on a mid-tier device | Quality — performance | All | ≤ 1.5 s | MET-02 |

An unnumbered quality requirement is one the TRD cannot cite and the test plan will not cover.

## 9. Platform Behavior
Per declared platform, what that platform owes — see the platform rules below. Specify shared behavior once and list only the deltas.

## 10. Dependencies, Risks, and Stakeholder Inputs
Other teams, systems, and decisions this relies on; the risks with owners; and the cross-functional inputs still outstanding, each with a named owner and a decision date.

## 11. Instrumentation
The events, properties, and dashboards behind Section 3 — what fires, when, with what payload, and where it lands. Name the dashboard or report each metric is read from.

## 12. Release Plan
Phases or milestones, what ships in each, the rollout mechanism (feature flag, percentage ramp, cohort, region), the kill switch, and the criteria for advancing a phase. "Ship it all at once" is a valid plan, but it should be a stated one.

## 13. Decision Log

| ID | Date | Decision | Made by | Alternatives rejected | Supersedes |
|---|---|---|---|---|---|
| DEC-01 | | | | | — |

Append, never overwrite. A superseded decision stays visible, with the `DEC-xx` that replaced it named in the Supersedes column of the new row — which is why the rows need IDs at all. `DEC-xx` is local to this document; nothing downstream traces to it.

## 14. Impact Review
After release: date, audience, rollout status, actual results against `MET-xx` targets and guardrails, user and operational feedback, and the decision — expand, iterate, hold, or roll back.

## 15. Assumptions and Open Questions
Facts filled by guess, decisions not yet made, evidence not yet gathered. Each with an owner where one exists.

## 16. Glossary
Every domain term, acronym, and metric name used above, defined once. The PRD is read by design, engineering, QA, support, and leadership; the glossary is what stops them approving different things.

## 17. Next Steps
- Next decision:
- Evidence or artifact needed:
- Owners / contributors:
- Exit criteria for the next stage:
```
