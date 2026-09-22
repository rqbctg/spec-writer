#!/usr/bin/env python3
"""Contract tests for skills/.

build.py already proves dist/ is fresh and that the copied output-contract
blocks still match each other. These are the checks above that: that each
SKILL.md is loadable by an agent, that the conventions the router defines are
the ones the six stages actually use, and that an install carries everything a
skill points at. Run: python3 tests/test_skills.py
"""
import json, os, re, subprocess, sys, tempfile

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
ROUTER = "spec-writer"
STAGES = ["mrd-writer", "brd-writer", "prd-writer",
          "design-spec-writer", "trd-writer", "qa-test-plan-writer"]

SUFFIX = {"mrd-writer": "mrd", "brd-writer": "brd", "prd-writer": "prd",
          "design-spec-writer": "design-spec", "trd-writer": "trd",
          "qa-test-plan-writer": "test-plan"}

HEADER = ["Owner", "Date", "Version", "Status", "Scope", "Platforms",
          "Upstream", "Downstream"]
EXTRA_HEADER = {"prd-writer": {"Stage"}, "design-spec-writer": {"Design file"}}

# The router's Traceability IDs block is the whole vocabulary. A stage that
# mints a prefix outside it has invented an ID scheme nobody downstream reads.
ID_PREFIXES = {"NEED", "GOAL", "BR", "R", "PR", "MET", "DEC", "FLOW", "SCR",
               "CMP", "FR", "NFR", "API", "REQ", "TC"}

MARKERS = ["Not applicable — ", "Insufficient evidence — ", "Not yet — stage "]

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
    return cond


def read(*parts):
    return open(os.path.join(SKILLS, *parts)).read()


def frontmatter(text, path):
    lines = text.split("\n")
    if not check(lines[0].strip() == "---", f"{path}: no frontmatter"):
        return {}, text
    end = next(i for i, l in enumerate(lines[1:], 1) if l.strip() == "---")
    meta = {}
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return meta, "\n".join(lines[end + 1:])


# --------------------------------------------------------------------------- #
def header_fields(text):
    """The header block is the run of **Field:** lines under the document title.
    Later sections use the same bold-label form for screen and flow specs, so
    stop at the first line that isn't one."""
    fields, started = [], False
    for line in text.split("\n"):
        m = re.match(r"^\*\*([A-Za-z ]+):\*\*", line)
        if m:
            fields.append(m.group(1))
            started = True
        elif started and line.strip():
            break
    return fields


def test_frontmatter():
    """Every skill loads: name matches its folder, description fits the field."""
    for name in [ROUTER] + STAGES:
        path = f"skills/{name}/SKILL.md"
        meta, _ = frontmatter(read(name, "SKILL.md"), path)
        check(meta.get("name") == name,
              f"{path}: frontmatter name {meta.get('name')!r} != folder {name!r}")
        desc = meta.get("description", "")
        check(len(desc) > 80, f"{path}: description too thin to route on")
        check(len(desc) <= 1024, f"{path}: description is {len(desc)} chars, over the 1024 limit")
        check("Use when" in desc or "Use whenever" in desc,
              f"{path}: description names no trigger (\"Use when…\")")


def test_fences_balanced():
    """An unclosed fence swallows the rest of the file — the template most of all."""
    for name in [ROUTER] + STAGES:
        files = [(f"skills/{name}/SKILL.md", read(name, "SKILL.md"))]
        refdir = os.path.join(SKILLS, name, "references")
        for f in sorted(os.listdir(refdir)) if os.path.isdir(refdir) else []:
            files.append((f"skills/{name}/references/{f}", read(name, "references", f)))
        for path, text in files:
            depth, opener = 0, None
            for line in text.split("\n"):
                m = re.match(r"^(`{3,})", line)
                if not m:
                    continue
                if depth == 0:
                    depth, opener = 1, m.group(1)
                elif len(m.group(1)) >= len(opener):
                    depth, opener = 0, None
            check(depth == 0, f"{path}: unclosed code fence")


def test_includes_resolve():
    """Progressive disclosure only works if the pointer resolves both ways:
    SKILL.md names a file that exists, and no reference file is stranded."""
    used = set()
    for name in [ROUTER] + STAGES:
        path = f"skills/{name}/SKILL.md"
        text = read(name, "SKILL.md")
        spans = re.findall(r"<!-- include-start: ([\w./-]+) -->(.*?)<!-- include-end -->",
                           text, re.S)
        check(spans, f"{path}: no include markers — the template should live in references/")
        for ref, pointer in spans:
            full = os.path.join(SKILLS, name, ref)
            check(os.path.isfile(full), f"{path}: include target missing: {ref}")
            check(ref in pointer,
                  f"{path}: the {ref} pointer doesn't name the file an agent has to open")
            used.add(os.path.normpath(full))
        check(text.count("<!-- include-start") == text.count("<!-- include-end"),
              f"{path}: unbalanced include markers")

    for name in [ROUTER] + STAGES:
        refdir = os.path.join(SKILLS, name, "references")
        for f in sorted(os.listdir(refdir)) if os.path.isdir(refdir) else []:
            full = os.path.normpath(os.path.join(refdir, f))
            check(full in used, f"skills/{name}/references/{f}: nothing includes this file")


def test_header_block():
    """One header block across the chain — the router allows exactly two extras."""
    for name in STAGES:
        path = f"skills/{name}/references/template.md"
        text = read(name, "references", "template.md")
        fields = header_fields(text)
        missing = [f for f in HEADER if f not in fields]
        check(not missing, f"{path}: header block is missing {missing}")
        extra = set(fields) - set(HEADER) - EXTRA_HEADER.get(name, set())
        check(not extra, f"{path}: header block carries undeclared field(s) {sorted(extra)}")


def test_required_sections():
    """What every stage owes beyond its template."""
    owed = {
        "a quality bar":            r"Quality bar before",
        "a review mode":            r"Review|review",
        "the changelog mandate":    r"\*\*The changelog is mandatory\.\*\*",
        "the delivery tiers":       r"Deliver by the highest tier",
        "a versioning rule":        r"\*\*Versioning\.\*\*",
    }
    for name in STAGES:
        text = read(name, "SKILL.md")
        for label, pattern in owed.items():
            check(re.search(pattern, text), f"skills/{name}/SKILL.md: missing {label}")
        tmpl = read(name, "references", "template.md")
        for section in ("Revision History", "Assumptions and Open Questions", "Next Steps"):
            check(section in tmpl,
                  f"skills/{name}/references/template.md: no {section} section")


def test_output_paths():
    """The router's output contract and each stage's own delivery step have to
    name the same file — they are read by different agents at different times."""
    router = read(ROUTER, "SKILL.md")
    for name, suffix in SUFFIX.items():
        want = f"docs/{name}/<slug>-{suffix}-v<version>.md"
        check(want in router, f"skills/{ROUTER}/SKILL.md: output contract is missing {want}")
        check(want in read(name, "SKILL.md"),
              f"skills/{name}/SKILL.md: never names its own output path {want}")


def test_id_vocabulary():
    """No stage invents an ID prefix the router never declared."""
    pattern = re.compile(r"\b([A-Z]{2,4})-(?:[A-Z]{2,10}-)?\d{2,3}\b")
    for name in STAGES:
        for rel, text in (("SKILL.md", read(name, "SKILL.md")),
                          ("references/template.md", read(name, "references", "template.md"))):
            for prefix in sorted(set(pattern.findall(text))):
                check(prefix in ID_PREFIXES,
                      f"skills/{name}/{rel}: ID prefix {prefix}-xx is not in the router's scheme")


def test_absent_section_markers():
    """One vocabulary for an empty section. A near-miss phrasing reads as a
    marker to a human and as nothing at all to the consistency review."""
    banned = ["insufficient information", "no information available", "TBD section"]
    for name in [ROUTER] + STAGES:
        files = [("SKILL.md", read(name, "SKILL.md"))]
        refdir = os.path.join(SKILLS, name, "references")
        for f in sorted(os.listdir(refdir)) if os.path.isdir(refdir) else []:
            files.append((f"references/{f}", read(name, "references", f)))
        for rel, text in files:
            low = text.lower()
            for phrase in banned:
                check(phrase not in low,
                      f"skills/{name}/{rel}: uses {phrase!r} instead of an absent-section marker")
        check(any(m in read(name, "SKILL.md") or
                  (os.path.isdir(refdir) and any(m in read(name, "references", f)
                                                 for f in os.listdir(refdir)))
                  for m in MARKERS),
              f"skills/{name}: never names an absent-section marker")


def test_orphan_marker():
    """One spelling of the orphan marker, because the router's consistency
    review greps for it verbatim."""
    marker = "[no upstream — new in this document]"
    check(marker in read(ROUTER, "SKILL.md"), f"skills/{ROUTER}/SKILL.md: orphan marker not defined")
    near = re.compile(r"\[no upstream[^\]]*\]")
    for name in [ROUTER] + STAGES:
        files = [("SKILL.md", read(name, "SKILL.md"))]
        refdir = os.path.join(SKILLS, name, "references")
        for f in sorted(os.listdir(refdir)) if os.path.isdir(refdir) else []:
            files.append((f"references/{f}", read(name, "references", f)))
        for rel, text in files:
            for found in set(near.findall(text)):
                check(found == marker,
                      f"skills/{name}/{rel}: orphan marker spelled {found!r}, not {marker!r}")


def test_install_carries_references():
    """A skill installed without the files it points at is a skill with no
    template. This is the check that would have caught the npx installer."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["node", os.path.join(ROOT, "bin", "cli.js"), "install", "claude",
                        "--dir", tmp], check=True, capture_output=True)
        base = os.path.join(tmp, ".claude", "skills")
        for name in [ROUTER] + STAGES:
            check(os.path.isfile(os.path.join(base, name, "SKILL.md")),
                  f"install: {name}/SKILL.md not installed")
            refdir = os.path.join(SKILLS, name, "references")
            for f in sorted(os.listdir(refdir)) if os.path.isdir(refdir) else []:
                check(os.path.isfile(os.path.join(base, name, "references", f)),
                      f"install: {name}/references/{f} not installed — the skill ships without it")


def test_bundles_are_standalone():
    """dist/ has no folder to read, so every reference file must be inlined."""
    for name in STAGES:
        tmpl = read(name, "references", "template.md")
        probe = [l for l in tmpl.split("\n") if l.startswith("# ")][:1]
        check(probe, f"skills/{name}/references/template.md: no document title to probe for")
        if not probe:
            continue
        bundle = open(os.path.join(ROOT, "dist", "universal", f"{name}.md")).read()
        check(probe[0] in bundle,
              f"dist/universal/{name}.md: template not inlined — the bundle ships without it")
        check("include-start" not in bundle,
              f"dist/universal/{name}.md: include marker leaked into the bundle")


def test_manifests():
    """The plugin manifest lists a real plugin; every manifest agrees on version."""
    plugin = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
    market = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json")))
    pkg    = json.load(open(os.path.join(ROOT, "package.json")))
    versions = {plugin["version"], pkg["version"], market["metadata"]["version"]} | \
               {p["version"] for p in market["plugins"]}
    check(len(versions) == 1, f"manifest versions disagree: {sorted(versions)}")
    check(plugin["name"] == "spec-writer", "plugin.json: unexpected plugin name")


def test_build_is_clean():
    """dist/ fresh, shared blocks in sync — build.py's own checks, run here so
    one command covers the repository."""
    r = subprocess.run([sys.executable, os.path.join(ROOT, "build.py"), "--check"],
                       capture_output=True, text=True, cwd=ROOT)
    check(r.returncode == 0, f"build.py --check failed:\n{r.stdout}{r.stderr}")


# --------------------------------------------------------------------------- #
def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        before = len(failures)
        t()
        status = "ok  " if len(failures) == before else "FAIL"
        print(f"  {status} {t.__name__}")
    print()
    if failures:
        print(f"{len(failures)} failure(s):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print(f"{len(tests)} checks passed")


if __name__ == "__main__":
    main()
