# Platforms

The instructions in `skills/` are plain Markdown and vendor-neutral — no Claude-specific tool calls, no assumed filesystem, no assumed web search. `build.py` repackages them for each assistant that needs a different wrapper.

```
npx @rqbctg/spec-writer install     # install wherever it's wanted
python3 build.py                  # regenerate dist/ after editing skills/
```

The CLI is dependency-free — Node 18+ and nothing else — so `npx` starts immediately and there's no dependency tree to audit.

| Assistant | Use | Writes files? |
|---|---|---|
| **Claude Code** | `npx @rqbctg/spec-writer install claude`, or the plugin manifest | Yes → `docs/` |
| **Claude (web/desktop)** | Upload `dist/universal/spec-writer-complete.md` to a Project | Yes, as an artifact |
| **ChatGPT** | Custom GPT, Project, or plain chat — see `dist/platforms/chatgpt.md` | With Code Interpreter |
| **Grok** | Custom instructions, project files, or plain chat — see `dist/platforms/grok.md` | No → tier 3 |
| **Gemini** | Gems or Gemini CLI — see `dist/platforms/gemini.md` | CLI only |
| **Cursor** | `npx @rqbctg/spec-writer install cursor` | Yes → `docs/` |
| **GitHub Copilot** | `npx @rqbctg/spec-writer install copilot` | Yes → `docs/` |
| **Codex / Jules / other agents** | `npx @rqbctg/spec-writer install agents` | Yes → `docs/` |
| **Anything else** | `npx @rqbctg/spec-writer copy <doc>`, paste, then your idea | Depends |

## How the output survives a platform with no filesystem

Every module carries the same three-tier output contract, so the deliverable is always a Markdown document no matter where it runs:

1. **Filesystem available** — write `docs/<skill-name>/<slug>-<type>-v<version>.md` and report the path; `docs/` is created only when missing, each skill owns its own subfolder, and the version is bumped from the highest file already in that folder (first write is `v0.0.1`). With more than one platform declared, the PRD, design spec, TRD, and test plan are written once per platform as `<slug>-<type>-<platform>-v<version>.md`. Claude Code, Cursor, Copilot, Gemini CLI, Codex.
2. **Files or a document surface, no repo** — produce a downloadable file, canvas, or doc named `<slug>-<type>.md`. ChatGPT with Code Interpreter, Claude artifacts, Gemini Canvas.
3. **Chat only** — the entire document in one fenced Markdown block, filename named, ready to paste into a `.md`. Grok, plain ChatGPT, anything embedded.

The filename is identical in all three tiers, which is what keeps a six-document set coherent when the stages are produced on different platforms — an MRD written in Grok and a PRD written in Claude Code still chain together by `NEED-01` → `BR-01` → `PR-01`.

## Degrading gracefully

- **No web search** (most chat-only setups): the MRD module says so in its Market Research section and marks every research-dependent claim unverified, rather than inventing figures.
- **No design tool access**: the Design Spec module specifies components in text and flags what still needs visual design.
- **No repo access**: the TRD module works from the PRD alone and records what it couldn't check against the codebase as an assumption.
- **Small instruction fields** (8000 chars on Custom GPTs, Gems, and Grok custom instructions): use the `dist/instructions/` stub and upload the matching `dist/universal/` file as knowledge, rather than pasting a whole module. Every stub is under 1700 characters.

## Scope

Product, feature, or change — declared in the header block and set once. At feature scope the MRD and BRD usually drop out entirely and the chain starts at the PRD. See `skills/spec-writer/SKILL.md`.

## Standards

Each stage is structured on the recognised standard for its document type, so the output is reviewable by someone who has never seen this chain — and so a section that doesn't apply is visibly marked rather than silently missing.

| Document | Standard |
|---|---|
| MRD | Pragmatic Institute framework — market problem, buyer vs user personas, TAM/SAM/SOM, positioning |
| BRD | BABOK v3 (IIBA); ISO/IEC/IEEE 29148:2018 BRS — requirement types, RACI, risk register, sign-off |
| PRD | INVEST user stories, Given/When/Then acceptance criteria, MoSCoW prioritization |
| Design Spec | WCAG 2.2 AA; W3C ARIA Authoring Practices |
| TRD | ISO/IEC/IEEE 29148:2018 requirement form and quality; ISO/IEC 25010:2023 quality model |
| QA Test Plan | ISO/IEC/IEEE 29119-3:2021 (superseded IEEE 829-2008) |

## Layout

```
bin/cli.js               the npx installer — no dependencies
skills/                  source of truth — portable Markdown, edit here
build.py                 regenerates dist/
.claude-plugin/          Claude Code plugin manifest (reads skills/ directly)
dist/universal/          paste-anywhere prompts, and the files you upload as knowledge
dist/instructions/       short stubs for capped instruction fields
dist/platforms/          install notes for ChatGPT, Grok, Gemini
dist/agents/             AGENTS.md, Cursor .mdc rules, Copilot instructions
```
