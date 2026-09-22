Produce the TRD with the six sections below, in order. No section is ever deleted: one that genuinely doesn't apply is marked `Not applicable — <reason>`, and one that applies but has nothing behind it yet is marked `Insufficient evidence — <what would resolve it>`. Which of the two you pick is itself information a reviewer needs.

```markdown
# Technical Requirements Document: [feature / system name]

**Owner:** <name or role>
**Date:** <today's date>
**Version:** 0.0.1
**Status:** Draft | In review | Approved | Superseded
**Scope:** Product | Feature | Change
**Platforms:** <carried from the PRD>
**Upstream:** <exact upstream filenames, comma-separated — `invoice-tracker-prd-ios-v0.2.0.md`, `invoice-tracker-design-spec-ios-v0.1.0.md` — or "Informal brief">
**Downstream:** QA Test Plan

## Revision History

| Version | Date | Author | Upstream version | Summary | IDs added | IDs changed | IDs removed |
|---|---|---|---|---|---|---|---|
| 0.0.1 | [today's date] | [author] | `<prd filename>`, `<design spec filename>` | Initial draft | FR-01–FR-12, NFR-01–NFR-06, API-01–API-04 (every ID in this draft) | — | — |

One appended row per version, never rewritten. The ID columns are what let the test plan diff this document without re-reading it in full; `—` means none, and an empty cell means the change wasn't tracked, which is a gap worth fixing.

## 1. Document Context and Administration
A one-paragraph summary and the business context, referencing the source PRD and its version. Stakeholders and approvers (Product, Eng Lead, QA Lead). Goals — in scope, measurable. Non-Goals — out of scope, explicit; this is what prevents scope creep.

**Definitions and acronyms** — every domain term and abbreviation used below, defined once.

**References** — source PRD, design spec, related TRDs, ADRs, external standards and RFCs this conforms to, each with a version or link.

## 2. Functional Requirements
Derived from the PRD but written in technical language, broken down by use case. Each requirement specific enough to test: behavior, inputs and outputs, edge cases. Concrete examples — exact validation rules, exact endpoint plus method plus expected status code — not vague behavior descriptions.

Write each one in the requirement form defined by **ISO/IEC/IEEE 29148:2018**: *[condition] [subject] [action] [object] [constraint of action]* — "While a session is active (condition), the API (subject) shall return (action) the caller's overdue invoices (object) within 150 ms at p95 (constraint)." Use *shall* for a binding requirement; reserve *should* for a recommendation and *may* for an option, and never mix them casually.

Check every requirement against the nine quality characteristics the same standard defines — **necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming**. *Singular* is the one most often violated: a requirement containing "and" is usually two requirements that can fail independently.

| ID | Requirement | Platforms | Acceptance criteria | Upstream |
|---|---|---|---|---|
| FR-01 | `GET /invoices?status=overdue` returns the caller's overdue invoices | Shared backend | 200 with array sorted by `days_overdue` desc; 401 unauthenticated; empty array, not 404, when none | PR-01, SCR-01 |
| FR-12 | Receipt captures queue locally and upload on reconnect | iOS, Android | Given no connectivity, capture persists to local store; on reconnect, uploads in capture order; a failed upload retries with backoff and surfaces after 3 failures | PR-08 |

The acceptance criteria in this column are the document's only set — Section 5 plans how they are tested, it does not restate them.

Mark shared-backend requirements as such. On a multi-platform product most functional requirements are one server-side behavior serving several clients, and the ones that genuinely differ per client are the ones worth flagging. In a per-platform TRD, a shared-backend requirement is reproduced verbatim in every platform file under the same ID — the backend is one system, and two platform files disagreeing about its behavior is a defect, not a variation.

Never invent a parent ID. A row with no real upstream is marked `[no upstream — new in this document]` in the Upstream column and repeated in Assumptions and Open Questions — an orphan is either a gap in the parent document or scope creep, and both need a human.

## 3. Non-Functional Requirements

| ID | Quality characteristic | Description | Measurable requirement | Verification method | Upstream |
|---|---|---|---|---|---|
| NFR-01 | Performance efficiency | Overdue view responds under load | p95 ≤ 150 ms at 200 req/s | Measurement — load test in staging | MET-02, PR-12 |

Classify each against the **ISO/IEC 25010:2023** product quality model, whose nine characteristics are: **functional suitability, performance efficiency, compatibility, interaction capability, reliability, security, maintainability, flexibility, and safety.** (The 2023 revision renamed *usability* to interaction capability and *portability* to flexibility, and added safety.) Working through all nine is what surfaces the NFRs nobody asked for but everyone assumes — walk the list and mark the ones that genuinely don't apply rather than silently skipping them.

The Upstream column cites the PRD's `MET-xx` guardrail or the `PR-xx` quality requirement this implements — the PRD's Section 8 quality requirements carry `PR-xx` IDs precisely so they can be cited here rather than re-derived.

**Every NFR needs a number and a way to check it** — a percentile latency, an uptime target, a retention period, a WCAG conformance level — never just "fast" or "secure." State the verification method alongside: measurement, test, demonstration, analysis, or inspection. An NFR nobody can verify is a preference.

## 4. System Architecture and Design
High-level architecture: where this fits in the existing system, with a Mermaid or described diagram where a picture clarifies it. Component design: new services, modules, libraries. Data model and schema changes: tables, fields, indexes, relationships, or document structure. API specifications (`API-xx`): URL, method, request and response bodies, error codes, for every new or modified endpoint. Each `API-xx` cites the `FR-xx` it serves, so a reader can go from endpoint to requirement to `PR-xx` without guessing. Technology choices with explicit trade-off justification — name the choice, tie it to the NFR that drove it, and state what's given up ("Redis for session cache, because the 150 ms NFR needs in-memory reads; trade-off is added infra cost versus reusing the primary DB"). **Alternatives considered and rejected** — at least the serious ones, each with the reason it lost. A design with no rejected alternatives reads as unexamined, and this is the section a reviewer six months from now actually needs. Where a decision is significant and long-lived, record it as an ADR and reference it here rather than burying it in prose.

**Security design** — trust boundaries, authentication and authorization model, data classification (what's PII, secret, or regulated), secrets management, and a threat enumeration. STRIDE is a serviceable checklist: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. For each credible threat, the mitigation and where it's enforced.

**Privacy and data lifecycle** — what personal data is collected, the lawful basis or business justification, where it's stored and for how long, how deletion and export requests are satisfied, and what crosses a regional boundary.

**Capacity and scaling** — the sizing arithmetic behind the design: expected request and data volumes at launch and at the growth horizon, the resulting storage and throughput, what saturates first, and what the scaling lever is when it does.

**Migration and backfill** — for anything touching existing data or behavior: the migration steps, backfill strategy, dual-write or dual-read period, how you verify parity, and the plan if it has to be abandoned mid-flight.

Then, separately: **Assumptions** (what's taken for granted), **Constraints** (hard limits — infra, budget, OS versions, compliance), **Dependencies** (other teams and systems this relies on).

## 5. Testing, Deployment, and Operations
Testing strategy: unit, integration, and performance coverage targets, each tied back to the `FR-xx` acceptance criteria in Section 2 or the `NFR-xx` it validates. This section plans the verification; it does not restate the criteria themselves.

Monitoring and alerting: define the **SLIs** (what's measured — latency, error rate, freshness), the **SLOs** (the target each must hold, matching the Section 3 NFRs), and the error budget that follows. Then the alerts: which SLO breach pages a human, at what threshold, and what the first response is. Alerts that don't map to an SLO are noise, and a dashboard nobody is paged from is decoration.

Deployment and rollback: release strategy (blue/green, canary, feature flag) and the specific steps to revert.

## 6. Assumptions, Open Questions, and Next Steps
Two closing sections, mandatory in every document in this chain. **Assumptions and Open Questions:** every technical gap you filled with a guess in Step 2, every dependency not yet confirmed with its owning team, and every decision that needs an architect or security review before build starts. (The Section 4 Assumptions subsection covers design-level assumptions; this one covers what still blocks the document from being final.) **Next Steps:** review and approval path, who owns each open question, and what must be true before implementation begins.
```
