#!/usr/bin/env python3
"""Build platform-specific bundles from the portable sources in skills/.

The Markdown in skills/*/SKILL.md is the single source of truth and is written
to be model- and vendor-neutral. This script repackages it for each assistant
that needs a different wrapper. Run: python3 build.py
Pass --check to verify dist/ matches skills/ without writing anything.
"""
import os, re, shutil, sys, tempfile

ROOT  = os.path.dirname(os.path.abspath(__file__))
SRC   = os.path.join(ROOT, "skills")
DIST  = os.path.join(ROOT, "dist")

ORDER = ["spec-writer", "mrd-writer", "brd-writer", "prd-writer",
         "design-spec-writer", "trd-writer", "qa-test-plan-writer"]

TITLES = {"spec-writer":        "Router — shared conventions",
          "mrd-writer":         "MRD — Market Requirements",
          "brd-writer":         "BRD — Business Requirements",
          "prd-writer":         "PRD — Product Requirements",
          "design-spec-writer": "Design Spec",
          "trd-writer":         "TRD — Technical Requirements",
          "qa-test-plan-writer":"QA Test Plan"}

# Documented instruction-field limit, in characters. ChatGPT, Grok, and Gemini
# all cap at roughly this, so one stub serves all three. Sources change it
# without notice; the build warns rather than truncating.
INSTRUCTION_LIMIT = 8000


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v.strip()


def parse_frontmatter(text, path):
    """Read a YAML-ish frontmatter block: any key order, any extra keys, and
    values folded over continuation lines. Only name and description are used;
    the rest (allowed-tools, license, version) is carried but ignored."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        sys.exit(f"no frontmatter block: {path}")
    end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    if end is None:
        sys.exit(f"unterminated frontmatter: {path}")

    meta, key = {}, None
    for i, line in enumerate(lines[1:end], 2):
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            meta[key] = m.group(2)
        elif line[:1] in (" ", "\t") and key:
            meta[key] += " " + line.strip()          # folded continuation
        else:
            sys.exit(f"{path}:{i}: can't parse frontmatter line: {line!r}")

    for required in ("name", "description"):
        if not unquote(meta.get(required, "")):
            sys.exit(f"{path}: frontmatter is missing {required}")
    return {k: unquote(v) for k, v in meta.items()}, "\n".join(lines[end + 1:]).strip()


INCLUDE = re.compile(
    r"^<!-- include-start: (?P<ref>[\w./-]+) -->\n.*?^<!-- include-end -->\n?",
    re.M | re.S)


def expand_includes(body, skill, path):
    """Skills use progressive disclosure: bulk material — templates, platform
    tables — lives in skills/<name>/references/ and SKILL.md carries a pointer
    to it between include markers. The dist/ bundles have no folder to read, so
    the marked span is replaced by the reference file itself and every generated
    file stays standalone."""
    used = []

    def swap(m):
        ref = m.group("ref")
        full = os.path.join(SRC, skill, ref)
        if not os.path.isfile(full):
            sys.exit(f"{path}: include target does not exist: {ref}")
        used.append(os.path.normpath(full))
        return open(full).read().strip() + "\n"

    out = INCLUDE.sub(swap, body)
    for stray in ("<!-- include-start", "<!-- include-end"):
        if stray in out:
            sys.exit(f"{path}: unmatched {stray} marker")
    return out, used


def load():
    docs, included = {}, set()
    for name in ORDER:
        path = os.path.join(SRC, name, "SKILL.md")
        meta, body = parse_frontmatter(open(path).read(), path)
        if meta["name"] != name:
            sys.exit(f"{path}: frontmatter name {meta['name']!r} != directory {name!r}")
        body, used = expand_includes(body, name, path)
        included.update(used)
        docs[name] = {"name": meta["name"], "description": meta["description"],
                      "body": body.strip()}

    for name in ORDER:                              # orphaned reference files
        refdir = os.path.join(SRC, name, "references")
        for f in sorted(os.listdir(refdir)) if os.path.isdir(refdir) else []:
            full = os.path.normpath(os.path.join(refdir, f))
            if full not in included:
                sys.exit(f"{full}: no SKILL.md includes this reference file")
    return docs


def write(rel, text):
    path = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text.rstrip() + "\n")
    return len(text)


def preamble(d):
    return (f"# {d['name']}\n\n"
            f"> {d['description']}\n\n"
            "You are an experienced product manager, business analyst, designer, engineer, and QA lead — "
            "whichever the document in front of you calls for. Follow the instructions below exactly. "
            "They are complete: don't substitute a generic template for the structure specified here.\n")


# --------------------------------------------------------------------------- #
def build_universal(docs):
    """Self-contained prompts that paste into any assistant, any interface."""
    for name, d in docs.items():
        write(f"universal/{name}.md", preamble(d) + "\n" + d["body"])
    combined = ["# spec-writer — complete instruction set\n",
                "Six connected product documents: MRD, BRD, PRD, Design Spec, TRD, QA Test Plan. "
                "Start with the router, then follow the module for the stage you're on.\n"]
    for name in ORDER:
        combined.append(f"\n\n---\n\n# MODULE: {name}\n\n> {docs[name]['description']}\n\n{docs[name]['body']}")
    write("universal/spec-writer-complete.md", "\n".join(combined))


def build_instructions(docs):
    """One shared set of instruction stubs. ChatGPT, Grok, and Gemini all cap
    their instruction field at roughly the same size and take the same stub,
    so it is built once. The stub points at the matching universal/ file,
    which is what gets uploaded as knowledge."""
    limit = INSTRUCTION_LIMIT
    for name, d in docs.items():
        stub = (f"{preamble(d)}\n"
                f"## How to work\n\n"
                f"The complete specification for this document is in the attached knowledge file "
                f"**{name}.md** (in `dist/universal/`). Read it in full before drafting, and follow its workflow, template, "
                f"section structure, ID scheme, and output contract exactly — it is authoritative over "
                f"any general template you might otherwise reach for.\n\n"
                f"Two rules override everything else if they ever conflict with brevity:\n\n"
                f"1. **Never invent evidence.** No fabricated market sizes, budgets, stakeholders, "
                f"business rules, or limits. An honest gap goes in Assumptions and Open Questions.\n"
                f"2. **Always deliver a Markdown document.** Follow the output contract in the knowledge "
                f"file. In a chat-only interface that means the whole document in one fenced code block "
                f"tagged markdown, with the filename named explicitly.\n\n"
                f"Don't interrogate the user before starting. Draft from thin input, label the "
                f"assumptions, and batch any genuinely blocking questions into a single pass.\n")
        n = write(f"instructions/{name}.md", stub)
        if n > limit:
            print(f"  WARN instructions/{name}.md is {n} chars, over the {limit} limit")


def build_agents(docs):
    """AGENTS.md — read by Codex, Cursor, Copilot, Gemini CLI, Jules, and others."""
    lines = ["# AGENTS.md — spec-writer\n",
             "Product documentation instructions for any coding agent working in this repository.\n",
             "## Documents\n",
             "| Stage | Document | Instructions | Output |",
             "|---|---|---|---|"]
    files = {n: f"docs/{n}/<slug>-{suf}-v<version>.md" for n, suf in
             (("mrd-writer", "mrd"), ("brd-writer", "brd"), ("prd-writer", "prd"),
              ("design-spec-writer", "design-spec"), ("trd-writer", "trd"),
              ("qa-test-plan-writer", "test-plan"))}
    for i, name in enumerate([n for n in ORDER if n != "spec-writer"], 1):
        lines.append(f"| {i} | {TITLES[name]} | `skills/{name}/SKILL.md` | `{files[name]}` |")
    lines += ["",
              "When asked for any of these documents, read the matching `skills/<name>/SKILL.md` in full "
              "and follow it exactly, along with the files in its `references/` folder that it points "
              "at — the document template lives there. `skills/spec-writer/SKILL.md` holds the shared conventions — "
              "traceability IDs, layer discipline, the header block, and the output contract — and routes "
              "to the right stage when the request doesn't name one.",
              "",
              "## Non-negotiables",
              "",
              "- Write the document to a `.md` file and report the path. Never deliver it as chat prose. "
              "Each skill writes into its own `docs/<skill-name>/` subfolder; `docs/` is created only when missing.",
              "- Version every file: the name ends in `-v<major>.<minor>.<patch>`, starting at `v0.0.1`. Read the "
              "highest version already in the folder and write the next one beside it — never overwrite. "
              "Where more than one platform is declared, the PRD, design spec, TRD, and test plan are written "
              "once per platform as `<slug>-<type>-<platform>-v<version>.md`.",
              "- Resolve upstream documents from the producing skill's folder, newest version and matching "
              "platform, and cite that exact filename in the header's `Upstream:` line.",
              "- Never invent a market size, budget, stakeholder, business rule, or limit. Gaps go in "
              "*Assumptions and Open Questions*.",
              "- Every numbered item carries a stable ID and cites its upstream parent "
              "(`NEED-01` → `BR-01` → `PR-01` → `SCR-01`/`FR-01` → `TC-001`).",
              "- Stay in the document's layer: no feature lists in an MRD, no databases in a PRD, "
              "no endpoints in a Design Spec.",
              "- Every document opens with a *Revision History* table and ends with *Assumptions and Open "
              "Questions* and *Next Steps*.",
              "- Every new version appends one Revision History row: summary, upstream version, and the IDs "
              "added, changed, and removed. Never rewrite an existing row.",
              "- Every version also appends a bullet to `docs/CHANGELOG.md` under today's date — document, path, "
              "one-line summary, `+`/`~`/`-` ID deltas, upstream path. A version with no changelog entry is not "
              "delivered."]
    write("agents/AGENTS.md", "\n".join(lines))

    for name, d in docs.items():
        if name == "spec-writer":
            fm = ("---\ndescription: Router and shared conventions for the product documentation chain\n"
                  "alwaysApply: false\n---\n\n")
        else:
            fm = f"---\ndescription: {d['description']}\nalwaysApply: false\n---\n\n"
        write(f"agents/cursor-rules/{name}.mdc", fm + preamble(d) + "\n" + d["body"])

    write("agents/copilot-instructions.md",
          "# Copilot instructions — spec-writer\n\n"
          "Product documentation lives in `docs/<skill-name>/`, one versioned file per document. When asked for "
          "an MRD, BRD, PRD, Design Spec, TRD, or QA Test Plan, read the matching "
          "`skills/<type>-writer/SKILL.md` in this repository and follow it exactly, including its "
          "template, ID scheme, versioning rule, and output contract.\n\n"
          + "\n".join(f"- **{docs[n]['name']}** — {docs[n]['description']}" for n in ORDER))


# --------------------------------------------------------------------------- #
CHATGPT_README = """# ChatGPT

Two ways to install, depending on whether you want one assistant or six.

## One GPT for the whole chain (recommended)

1. **Explore GPTs → Create**.
2. Paste `../instructions/spec-writer.md` into **Instructions**.
3. Under **Knowledge**, upload `../universal/spec-writer-complete.md`.
4. Enable **Web Browsing** (the MRD stage needs it) and **Code Interpreter** (so it can hand back a real `.md` file instead of a chat block).

## A separate GPT per document

Same steps, but paste `../instructions/<name>.md` and upload the matching `../universal/<name>.md`.

## Projects

Paste `../universal/spec-writer-complete.md` into the project instructions, or attach it as a project file. Every chat in the project inherits it.

## Plain chat

Paste `../universal/<name>.md`, then your idea as the next message.

Without Code Interpreter, ChatGPT can't write a file — the output contract's tier 3 handles this: it emits the whole document in one fenced Markdown block, named, ready to save as `.md`.
"""

GROK_README = """# Grok

## Custom instructions

Settings → **Customize** → paste `../instructions/<name>.md`, or `../universal/spec-writer-complete.md` for the whole chain in one go.

## Projects / attached files

Create a project for the product, attach `../universal/spec-writer-complete.md` as a file, and every conversation in it inherits the full chain. Attach each upstream document as you produce it — the next stage reads the file, not the conversation.

## Plain chat

Paste `../universal/<name>.md`, then your idea as the next message. Grok's DeepSearch is worth turning on for the MRD stage.

Grok replies in chat rather than writing files, so the output contract's tier 3 applies: the whole document arrives in one fenced Markdown block with its filename named, ready to save.
"""

GEMINI_README = """# Gemini

## Gems

**Gems → New Gem** → paste `../instructions/<name>.md` into the instructions field and upload the matching `../universal/<name>.md` as a knowledge file. For one Gem covering the whole chain, use `../instructions/spec-writer.md` with `../universal/spec-writer-complete.md`.

## Gemini CLI / Code Assist

Use `../agents/AGENTS.md`, or point it at `skills/<name>/SKILL.md` directly — it can write files, so tier 1 of the output contract applies and documents land in `docs/`.

## Plain chat

Paste `../universal/<name>.md`, then your idea as the next message.
"""

def build_all():
    docs = load()
    build_universal(docs)
    build_instructions(docs)
    write("platforms/chatgpt.md", CHATGPT_README)
    write("platforms/grok.md",    GROK_README)
    write("platforms/gemini.md",  GEMINI_README)
    build_agents(docs)
    write("README.md",
          "# dist/ — generated\n\n"
          "Built from `skills/` by `build.py`. Don't edit anything here; edit the source and rebuild.\n\n"
          "| Directory | For |\n|---|---|\n"
          "| `universal/` | Paste into any assistant — also the files you upload as knowledge |\n"
          "| `instructions/` | Short stubs for capped instruction fields (Custom GPTs, Gems, Grok) |\n"
          "| `platforms/` | Install notes per assistant |\n"
          "| `agents/` | AGENTS.md, Cursor rules, Copilot instructions |\n\n"
          "Claude Code reads `skills/` directly through the plugin manifest — no build step.\n")
    return sum(len(fs) for _, _, fs in os.walk(DIST))


def tree(root):
    out = {}
    for dirpath, _, names in os.walk(root):
        for f in names:
            full = os.path.join(dirpath, f)
            out[os.path.relpath(full, root)] = open(full, "rb").read()
    return out


def check():
    """Rebuild into a temp directory and compare. Non-zero exit means dist/ is
    stale — someone edited skills/ and didn't rerun the build."""
    global DIST
    published, DIST = DIST, tempfile.mkdtemp(prefix="spec-writer-build-")
    try:
        build_all()
        fresh = tree(DIST)
    finally:
        shutil.rmtree(DIST, ignore_errors=True)
        DIST = published

    current = tree(published) if os.path.isdir(published) else {}
    stale = sorted(set(fresh) ^ set(current)) + \
            sorted(k for k in set(fresh) & set(current) if fresh[k] != current[k])
    if stale:
        print("dist/ is out of date — run: python3 build.py")
        for rel in stale:
            print(f"  {rel}")
        sys.exit(1)
    print(f"dist/ is up to date ({len(fresh)} files)")


# --------------------------------------------------------------------------- #
# The output-contract blocks below are deliberately copied into every skill:
# each dist/universal/<name>.md has to stand alone, so it can't cross-reference
# the router. Copies drift. These checks normalise away the per-skill tokens
# and fail when two copies of the same block stop matching.

SUFFIX = {"mrd-writer": "mrd", "brd-writer": "brd", "prd-writer": "prd",
          "design-spec-writer": "design-spec", "trd-writer": "trd",
          "qa-test-plan-writer": "test-plan"}

LABEL = {"mrd-writer": ["MRD"], "brd-writer": ["BRD"], "prd-writer": ["PRD"],
         "design-spec-writer": ["Design Spec", "design spec"],
         "trd-writer": ["TRD"], "qa-test-plan-writer": ["QA Test Plan", "test plan"]}

# block name -> (start marker, end markers, skills that must carry it)
SHARED = {
    "reading-upstream": ("1. **Look in the producing skill's folder**", ("\n## ",),
                         ["brd-writer", "prd-writer", "design-spec-writer", "trd-writer",
                          "qa-test-plan-writer"]),
    "versioning":       ("**Versioning.**", ("\n**The changelog is mandatory.**",),
                         list(SUFFIX)),
    "changelog":        ("**The changelog is mandatory.**",
                         ("\n**Per-platform documents.**", "\nWhatever the tier:"),
                         list(SUFFIX)),
    "per-platform":     ("**Per-platform documents.**", ("\nWhatever the tier:",),
                         ["prd-writer", "design-spec-writer", "trd-writer", "qa-test-plan-writer"]),
    "delivery-tiers":   ("Deliver by the highest tier the environment supports:",
                         ("\n**Versioning.**",), list(SUFFIX)),
    # Only the three bullets every stage shares: the tail continues past them
    # into per-stage handoff prose, and the MRD's last bullet is its own because
    # it has no upstream document to re-run against.
    "delivery-tail":    ("Whatever the tier:", ("\n- Re-running",), list(SUFFIX)),
}


def extract(text, start, ends):
    i = text.find(start)
    if i < 0:
        return None
    j = min([k for k in (text.find(e, i) for e in ends) if k > 0] or [len(text)])
    return text[i:j].strip()


def normalise(block, skill):
    """Strip the tokens a block is allowed to differ by: the skill's own name,
    its filename suffix, and the labels it calls its document."""
    out = block.replace(f"docs/{skill}/", "docs/SKILL/").replace(f"`{skill}/", "`SKILL/")
    out = out.replace(f"<slug>-{SUFFIX[skill]}-", "<slug>-TYPE-")
    for label in LABEL[skill]:
        out = out.replace(f"**{label}**", "**LABEL**").replace(f" {label} ", " LABEL ")
    return out


def check_shared_blocks():
    problems = []
    raw = {n: open(os.path.join(SRC, n, "SKILL.md")).read() for n in ORDER if n != "spec-writer"}
    for block, (start, ends, expected) in SHARED.items():
        seen = {}
        for skill in expected:
            text = extract(raw[skill], start, ends)
            if text is None:
                problems.append(f"{skill}: missing the {block} block")
                continue
            seen.setdefault(normalise(text, skill), []).append(skill)
        for skill in raw:
            if skill not in expected and extract(raw[skill], start, ends) is not None:
                problems.append(f"{skill}: carries the {block} block but shouldn't")
        if len(seen) > 1:
            groups = " vs ".join("/".join(v) for v in seen.values())
            problems.append(f"{block}: copies have drifted apart — {groups}")
    return problems


def check_versions():
    """package.json, the plugin manifest, and the marketplace entry each carry a
    version. A release bumps one and forgets the others; this says so."""
    import json
    seen, problems = {}, []
    pkg = json.load(open(os.path.join(ROOT, "package.json")))
    seen["package.json"] = pkg.get("version")

    plugin_path = os.path.join(ROOT, ".claude-plugin", "plugin.json")
    if os.path.exists(plugin_path):
        seen[".claude-plugin/plugin.json"] = json.load(open(plugin_path)).get("version")

    market_path = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
    if os.path.exists(market_path):
        market = json.load(open(market_path))
        seen[".claude-plugin/marketplace.json metadata"] = market.get("metadata", {}).get("version")
        for i, entry in enumerate(market.get("plugins", [])):
            seen[f".claude-plugin/marketplace.json plugins[{i}]"] = entry.get("version")

    missing = [k for k, v in seen.items() if not v]
    for k in missing:
        problems.append(f"{k}: no version")
    values = {v for v in seen.values() if v}
    if len(values) > 1:
        problems.append("versions disagree — " +
                        ", ".join(f"{k}={v}" for k, v in seen.items()))
    return problems


def main():
    drift = check_shared_blocks()
    if drift:
        print("shared output-contract blocks are out of sync:")
        for d in drift:
            print(f"  {d}")
        sys.exit(1)
    versions = check_versions()
    if versions:
        print("manifest versions are out of sync:")
        for v in versions:
            print(f"  {v}")
        sys.exit(1)
    if "--check" in sys.argv[1:]:
        return check()
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    print(f"built {build_all()} files into dist/")


if __name__ == "__main__":
    main()
