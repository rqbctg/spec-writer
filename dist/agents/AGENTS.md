# AGENTS.md — spec-writer

Product documentation instructions for any coding agent working in this repository.

## Documents

| Stage | Document | Instructions | Output |
|---|---|---|---|
| 1 | MRD — Market Requirements | `skills/mrd-writer/SKILL.md` | `docs/mrd-writer/<slug>-mrd-v<version>.md` |
| 2 | BRD — Business Requirements | `skills/brd-writer/SKILL.md` | `docs/brd-writer/<slug>-brd-v<version>.md` |
| 3 | PRD — Product Requirements | `skills/prd-writer/SKILL.md` | `docs/prd-writer/<slug>-prd-v<version>.md` |
| 4 | Design Spec | `skills/design-spec-writer/SKILL.md` | `docs/design-spec-writer/<slug>-design-spec-v<version>.md` |
| 5 | TRD — Technical Requirements | `skills/trd-writer/SKILL.md` | `docs/trd-writer/<slug>-trd-v<version>.md` |
| 6 | QA Test Plan | `skills/qa-test-plan-writer/SKILL.md` | `docs/qa-test-plan-writer/<slug>-test-plan-v<version>.md` |

When asked for any of these documents, read the matching `skills/<name>/SKILL.md` in full and follow it exactly, along with the files in its `references/` folder that it points at — the document template lives there. `skills/spec-writer/SKILL.md` holds the shared conventions — traceability IDs, layer discipline, the header block, and the output contract — and routes to the right stage when the request doesn't name one.

## Non-negotiables

- Write the document to a `.md` file and report the path. Never deliver it as chat prose. Each skill writes into its own `docs/<skill-name>/` subfolder; `docs/` is created only when missing.
- Version every file: the name ends in `-v<major>.<minor>.<patch>`, starting at `v0.0.1`. Read the highest version already in the folder and write the next one beside it — never overwrite. Where more than one platform is declared, the PRD, design spec, TRD, and test plan are written once per platform as `<slug>-<type>-<platform>-v<version>.md`.
- Resolve upstream documents from the producing skill's folder, newest version and matching platform, and cite that exact filename in the header's `Upstream:` line.
- Never invent a market size, budget, stakeholder, business rule, or limit. Gaps go in *Assumptions and Open Questions*.
- Every numbered item carries a stable ID and cites its upstream parent (`NEED-01` → `BR-01` → `PR-01` → `SCR-01`/`FR-01` → `TC-001`).
- Stay in the document's layer: no feature lists in an MRD, no databases in a PRD, no endpoints in a Design Spec.
- Every document opens with a *Revision History* table and ends with *Assumptions and Open Questions* and *Next Steps*.
- Every new version appends one Revision History row: summary, upstream version, and the IDs added, changed, and removed. Never rewrite an existing row.
- Every version also appends a bullet to `docs/CHANGELOG.md` under today's date — document, path, one-line summary, `+`/`~`/`-` ID deltas, upstream path. A version with no changelog entry is not delivered.
