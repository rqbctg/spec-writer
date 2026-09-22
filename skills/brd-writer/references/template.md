Use this section structure. Adapt depth to how much there is to say, but never delete a section. One that genuinely doesn't apply is marked `Not applicable — <reason>`; one that applies but has nothing behind it yet is marked `Insufficient evidence — <what would resolve it>`. A BRD is circulated for approval, so a silently missing section reads as a decision nobody made.

```markdown
# Business Requirements Document: [Project Name]

**Owner:** [user's name, or "Business Analyst / Project Lead"]
**Date:** [today's date]
**Version:** 0.0.1
**Status:** Draft | In review | Approved | Superseded
**Scope:** Product | Feature | Change
**Platforms:** <carried verbatim from MRD Section 5 — or, where there is no MRD, the answer to the scope-and-platforms question, recorded here>
**Upstream:** <exact upstream filename — `invoice-tracker-mrd-v0.2.0.md` — or "Informal brief">
**Downstream:** PRD

## Revision History

| Version | Date | Author | Upstream version | Summary | IDs added | IDs changed | IDs removed |
|---|---|---|---|---|---|---|---|
| 0.0.1 | [today's date] | [author] | `<mrd filename>`, or Informal brief | Initial draft | BR-01–BR-09 (every ID in this draft) | — | — |

One appended row per version, never rewritten. The ID columns are what let a downstream document diff this one without re-reading it in full; `—` means none, and an empty cell means the change wasn't tracked, which is a gap worth fixing.

## 1. Executive Summary
One paragraph: what the project is, why it's happening, and what success looks like. Written last.

## 2. Project Objectives
The business goals this project should achieve, as SMART goals (Specific, Measurable, Achievable, Relevant, Time-specific) wherever the input supports it. Where the input doesn't support a genuinely measurable or time-bound goal, say so rather than inventing a number.

Each objective cites the MRD `GOAL-xx` it inherits. That citation is the whole outcome chain — `GOAL-xx` to objective to `BR-xx` to the PRD's `MET-xx` — and dropping it here is where it usually breaks.

| Objective | Upstream | Measure | By when |
|---|---|---|---|
| Prove freelancers will pay for invoice chasing before funding the full build | GOAL-01 | Paid conversion from trial ≥ 5% | 90 days after launch |

An objective with no upstream goal is marked `[no upstream — new in this document]` and raised in Section 11; it usually means the MRD missed a goal the sponsor actually holds.

## 3. Project Scope
In scope and out of scope: timeline, deliverables, and the requirements this project addresses. Include an explicit exclusions list — that's what actually prevents scope creep.

Budget lives in Section 9 and the team in Section 6; reference them here rather than restating them, or the two copies disagree by the second revision.

## 4. Business Requirements
The core of the document. One row per requirement, most concrete detail the input supports.

| ID | Requirement | Type | Platforms | Priority | Rationale / what depends on it | Upstream |
|---|---|---|---|---|---|---|
| BR-01 | The business must be able to track invoice status across all clients in one place | Business | All | Must | Missed follow-ups are the primary revenue leak | NEED-01 |
| BR-07 | Existing invoice history must be migrated before cutover | Transition | All | Must | Without it the first month reports incorrectly | NEED-01 |
| BR-09 | Field staff must be able to capture receipts without connectivity | Solution | Mobile | Should | Removes the paper step entirely | NEED-04 |

Never invent a parent ID. A row with no real upstream is marked `[no upstream — new in this document]` in the Upstream column and repeated in Assumptions and Open Questions — an orphan is either a gap in the parent document or scope creep, and both need a human.

## 5. Current State and Future State
How the work is done today, and how it will be done once this lands. A short as-is / to-be pair — process steps, systems touched, handoffs — is what makes the size of the change legible to someone approving it. Where the process is new rather than changed, say so.

## 6. Key Stakeholders (RACI)
Who builds it, leads it, approves it, and is affected by it — clients, end users, other teams. Use role placeholders like "[Engineering lead — TBD]" rather than omitting a row.

| Stakeholder / role | Interest in the outcome | R | A | C | I |
|---|---|:-:|:-:|:-:|:-:|
| Project sponsor | Funds it, owns the benefit | | ✓ | | |

Exactly one **A** (accountable) per decision area — two accountable parties means nobody is.

## 7. Constraints, Assumptions, and Dependencies
Kept separate, because they fail differently. **Constraints** are hard limits you must design within — budget ceiling, deadline, mandated platform, regulation. **Assumptions** are things believed true but unverified, each of which becomes a risk if wrong. **Dependencies** are other teams, systems, or deliveries this relies on, each with an owner and a needed-by date.

## 8. Risk Register

| ID | Risk | Likelihood | Impact | Score | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R-01 | | H/M/L | H/M/L | | | |

Score likelihood × impact so the register sorts. A risk with no named owner is not managed, only noted.

`R-xx` IDs are local to this document — nothing downstream traces to them. Number them in their own sequence and don't reuse a retired number.

## 9. Cost-Benefit Analysis
Estimated costs, expected benefits, total expected cost, and a rough ROI where the input supports any numbers at all. Where it doesn't, say plainly that costs and benefits aren't yet quantifiable and flag it as an open item — a confident invented ROI is worse than none.

Platform choice is a cost driver, so price it here rather than leaving it to engineering: each additional platform carries its own build, test, release, and support cost, plus store commissions on mobile and signing certificates on desktop. Where a platform is phased, say what phase 1 costs versus the full set.

## 10. Success Criteria and Benefits Realization
How the business will know this delivered, and when it will check. Each criterion cites the `GOAL-xx` or `BR-xx` it measures, so the PRD's `MET-xx` inherits an unbroken chain rather than re-deriving one.

| Criterion | Measures | Baseline | Target | Method | Review date |
|---|---|---|---|---|---|
| Overdue invoices followed up within 7 days | BR-01 | 34% | 70% | Follow-up events in the invoice log | 2027-01-15 |

Each criterion needs a baseline, a target, a measurement method, and a review date — otherwise benefits are claimed rather than realized. Where the baseline doesn't exist yet, write "none — pre-launch" rather than leaving it blank.

## 11. Assumptions and Open Questions
Every assumption made to fill a gap, every requirement with no upstream need, and anything that genuinely needs stakeholder input before this document is final.

## 12. Glossary
Every domain term, acronym, and role name used above, defined once. A BRD crosses departments; the glossary is what stops two readers approving different things.

## 13. Approval and Sign-off

| Name | Role | Decision | Date | Signature |
|---|---|---|---|---|
| | Project sponsor | Approve / Reject / Approve with conditions | | |
| | Business owner | | | |
| | Technical lead | | | |

A BRD without an approval block isn't a BRD — it's a proposal. Include it even when the approvers are TBD.

## Next Steps
Review and sign-off path, then the PRD — owner, and what must be true before it starts.
```
