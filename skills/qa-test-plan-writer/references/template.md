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
