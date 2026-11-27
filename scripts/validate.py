#!/usr/bin/env python3
"""Validate runbooks, skills and generated files. Exit 1 on any error.

Usage: scripts/validate.py [-q]
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _lib as lib  # noqa: E402
import build  # noqa: E402

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ROW_FAMILIES = {"all", "rhel", "sles", "debian", "ubuntu"} | set(lib.RELEASES)
RUNBOOK_KEYS = [
    "id", "title", "area", "symptoms", "families", "releases", "mode", "risk",
    "requires_root", "vendor", "verified", "sources", "updated",
]
OPTIONAL_KEYS = {"reviewed", "lab_record"}
TOKEN_WARN, TOKEN_ERROR = 1500, 2000
SKILL_BODY_WARN, SKILL_BODY_ERROR = 1000, 1500
DESC_WARN = 300


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, where, msg):
        self.errors.append(f"ERROR {where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"WARN  {where}: {msg}")


def parse_steps(section_text):
    """Return list of (title, preamble_lines, table_rows) for each `### S<n>` block."""
    steps = []
    for block in re.split(r"(?m)^### ", section_text)[1:]:
        title, _, rest = block.partition("\n")
        pre, rows, in_table = [], [], False
        for line in rest.split("\n"):
            if line.startswith("|"):
                in_table = True
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                rows.append(cells)
            elif not in_table:
                pre.append(line)
        steps.append((title.strip(), pre, rows))
    return steps


def check_steps(rep, where, section_text, needs_confirm, tags_used):
    steps = parse_steps(section_text)
    if not steps:
        rep.error(where, "no `### S<n>` steps found")
        return
    for title, pre, rows in steps:
        loc = f"{where} step '{title}'"
        if not re.match(r"^S\d+ \S", title):
            rep.error(loc, "step heading must look like `S<n> <title>`")
        if needs_confirm and not any(line.startswith("CONFIRM WITH HUMAN:") and len(line) > 20 for line in pre):
            rep.error(loc, "missing `CONFIRM WITH HUMAN: <impact>` line before the table")
        if len(rows) < 3 or [c.lower() for c in rows[0]] != ["family", "command", "verified"]:
            rep.error(loc, "table header must be `| Family | Command | Verified |`")
            continue
        families = set()
        for family, command, tag in rows[2:]:
            if len(command.strip()) == 0:
                rep.error(loc, "empty command cell")
            if family not in ROW_FAMILIES:
                rep.error(loc, f"unknown family `{family}`")
            if tag not in lib.TAGS:
                rep.error(loc, f"unknown verification tag `{tag}`")
            else:
                tags_used.add(tag)
            if command.startswith("n/a") and not re.match(r"^n/a: \S", command):
                rep.error(loc, "`n/a` needs a reason: `n/a: <reason>`")
            families.add(family)
        covered = {lib.RELEASES.get(f, "debian" if f == "ubuntu" else f) for f in families}
        if "all" not in families and not {"rhel", "sles", "debian"} <= covered:
            rep.error(loc, "need an `all` row or rows covering rhel, sles and debian (release rows count)")
        if "all" in families and families != {"all"}:
            rep.warn(loc, "`all` row mixed with family rows; keep one or the other")


def check_runbook(rep, rb, ids):
    where = rb.rel
    for e in rb.errors:
        rep.error(where, e)
    fm = rb.fm
    if rb.errors and not fm:
        return
    for key in RUNBOOK_KEYS:
        if key not in fm:
            rep.error(where, f"missing front matter key `{key}`")
    for key in fm:
        if key not in RUNBOOK_KEYS and key not in OPTIONAL_KEYS:
            rep.error(where, f"unknown front matter key `{key}`")
    if any(k not in fm for k in RUNBOOK_KEYS):
        return

    if not ID_RE.match(fm["id"]) or fm["id"] != rb.path.stem:
        rep.error(where, "`id` must be a slug equal to the file name")
    if fm["area"] != rb.path.parent.name or fm["area"] not in lib.AREAS:
        rep.error(where, f"`area` must equal folder name and be one of {lib.AREAS}")
    if not isinstance(fm["symptoms"], list) or not fm["symptoms"]:
        rep.error(where, "`symptoms` must be a non-empty inline list")
    if not isinstance(fm["families"], list) or not set(fm["families"]) <= set(lib.FAMILIES) or not fm["families"]:
        rep.error(where, f"`families` must be a non-empty subset of {lib.FAMILIES}")
    releases = fm["releases"] if isinstance(fm["releases"], list) else []
    if not releases or not set(releases) <= set(lib.RELEASES):
        rep.error(where, "`releases` must be a non-empty subset of the supported releases")
    elif isinstance(fm["families"], list):
        for r in releases:
            if lib.RELEASES[r] not in fm["families"]:
                rep.error(where, f"release `{r}` belongs to family `{lib.RELEASES[r]}` which is not in `families`")
    if fm["mode"] not in lib.MODES:
        rep.error(where, f"`mode` must be one of {lib.MODES}")
    if fm["risk"] not in lib.RISKS:
        rep.error(where, f"`risk` must be one of {lib.RISKS}")
    if fm["requires_root"] not in ("true", "false"):
        rep.error(where, "`requires_root` must be true or false")
    if not fm["vendor"]:
        rep.error(where, "`vendor` must be `none` or a vendor name")
    if fm["verified"] not in lib.TAGS:
        rep.error(where, f"`verified` must be one of {lib.TAGS}")
    if not DATE_RE.match(fm["updated"]):
        rep.error(where, "`updated` must be YYYY-MM-DD")
    if "reviewed" in fm and fm["reviewed"] != "true":
        rep.error(where, "`reviewed` may only be `true`")
    sources = fm["sources"] if isinstance(fm["sources"], list) else []
    if not sources or not all(s.startswith("https://") for s in sources):
        rep.error(where, "`sources` must list https:// primary-source URLs")

    body_sections = lib.sections(rb.body)
    if list(body_sections) != lib.SECTIONS:
        rep.error(where, f"sections must be exactly, in order: {lib.SECTIONS}; found {list(body_sections)}")
        return
    cites = {int(n) for n in re.findall(r"\[S(\d+)\]", rb.body)}
    if any(n < 1 or n > len(sources) for n in cites):
        rep.error(where, "citation `[Sn]` points outside `sources`")
    if not cites and sources:
        rep.warn(where, "no `[Sn]` citations in the body")

    tags_used = set()
    check_steps(rep, f"{where} Check first", body_sections["Check first"], False, tags_used)
    act = body_sections["Act"].strip()
    if fm["risk"] == "read-only":
        if act != "n/a":
            rep.error(where, "risk is read-only, so `## Act` must be exactly `n/a`")
    else:
        if act == "n/a":
            rep.error(where, f"risk is {fm['risk']}, so `## Act` needs confirmed steps")
        else:
            check_steps(rep, f"{where} Act", act, True, tags_used)
    if tags_used:
        lowest = min(tags_used, key=lib.TAGS.index)
        if fm["verified"] != lowest:
            rep.error(where, f"`verified: {fm['verified']}` must equal the lowest tag used (`{lowest}`)")
    if "lab" in tags_used and "lab_record" not in fm:
        rep.error(where, "`lab` tags require `lab_record` in front matter")

    interpret = [l for l in body_sections["Interpret"].split("\n") if l.strip()]
    if not interpret or not all(l.startswith("- if ") and " -> " in l for l in interpret):
        rep.error(where, "`## Interpret` lines must all look like `- if <observation> -> <action>`")
    nxt = body_sections["Next"].strip()
    if nxt != "n/a":
        for line in nxt.split("\n"):
            m = re.match(r"^- ([a-z0-9]+(?:-[a-z0-9]+)*): \S", line)
            if not m:
                rep.error(where, f"bad `## Next` line: {line!r}")
            elif m.group(1) not in ids:
                rep.error(where, f"`## Next` links to unknown runbook id `{m.group(1)}`")
    if body_sections["Guardrails"].strip() in ("", "n/a"):
        rep.error(where, "`## Guardrails` is required")
    if "../" in rb.body:
        rep.warn(where, "body contains `../`")

    n = lib.tokens(rb.text)
    if n > TOKEN_ERROR:
        rep.error(where, f"~{n} tokens exceeds hard limit {TOKEN_ERROR}")
    elif n > TOKEN_WARN:
        rep.warn(where, f"~{n} tokens exceeds budget {TOKEN_WARN}")


def check_skill(rep, sd, by_id):
    where = f"skills/{sd.name}"
    text = (sd / "SKILL.md").read_text(encoding="utf-8")
    fm_text, body = lib.split_front_matter(text)
    if fm_text is None:
        rep.error(where, "SKILL.md has no front matter")
        return
    fm, errs = lib.parse_yaml_subset(fm_text)
    for e in errs:
        rep.error(where, e)
    for key in fm:
        if key not in lib.SKILL_KEYS:
            rep.error(where, f"frontmatter key `{key}` is not defined by agentskills.io")
    name = fm.get("name", "")
    if name != sd.name or not ID_RE.match(name) or len(name) > 64:
        rep.error(where, "`name` must equal the folder name and be a lowercase hyphen slug up to 64 chars")
    desc = fm.get("description", "")
    if not desc or len(desc) > 1024:
        rep.error(where, "`description` must be 1 to 1024 characters")
    elif len(desc) > DESC_WARN:
        rep.warn(where, f"description is {len(desc)} chars; keep it under about {DESC_WARN}")
    n = lib.tokens(body)
    if n > SKILL_BODY_ERROR:
        rep.error(where, f"body ~{n} tokens exceeds hard limit {SKILL_BODY_ERROR}")
    elif n > SKILL_BODY_WARN:
        rep.warn(where, f"body ~{n} tokens exceeds budget {SKILL_BODY_WARN}")
    if "unverified" not in body.lower():
        rep.error(where, "body must tell the agent to state `unverified` for unreviewed runbooks")
    if "../" in text:
        rep.error(where, "`../` is not allowed in a skill")
    for f in sd.rglob("*"):
        if f.is_symlink():
            rep.error(where, f"symlink not allowed: {f.relative_to(sd)}")
    refs = build.skill_refs(sd)
    if not refs:
        rep.warn(where, "skill references no runbooks")
    for rid in refs:
        if rid not in by_id:
            rep.error(where, f"references unknown runbook `{rid}`")
    refs_dir = sd / "references"
    if refs_dir.exists():
        for f in refs_dir.iterdir():
            if f.stem not in refs:
                rep.error(where, f"orphan file in references/: {f.name} (run scripts/build.py)")


def check_generated(rep, runbooks):
    for path, content in build.render_all(runbooks).items():
        rel = path.relative_to(lib.ROOT)
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            rep.error(str(rel), "out of date; run scripts/build.py")
    if lib.tokens(build.render_index(runbooks)) > 2500:
        rep.warn("INDEX.md", "exceeds about 2,500 tokens")
    for dst, src in build.expected_skill_files(runbooks).items():
        rel = dst.relative_to(lib.ROOT)
        if not dst.exists():
            rep.error(str(rel), "missing generated copy; run scripts/build.py")
        elif dst.read_bytes() != src.read_bytes():
            rep.error(str(rel), "differs from its runbook source; run scripts/build.py")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-q", action="store_true", help="print errors only, not warnings")
    args = parser.parse_args()
    rep = Report()
    runbooks = lib.load_runbooks()
    ids = [rb.id for rb in runbooks]
    for dup in {i for i in ids if ids.count(i) > 1}:
        rep.error("runbooks", f"duplicate id `{dup}`")
    for rb in runbooks:
        check_runbook(rep, rb, set(ids))
    by_id = {rb.id: rb for rb in runbooks}
    for sd in build.skill_dirs():
        check_skill(rep, sd, by_id)
    check_generated(rep, runbooks)
    for line in rep.errors + ([] if args.q else rep.warnings):
        print(line)
    print(f"{len(runbooks)} runbooks, {len(build.skill_dirs())} skills: "
          f"{len(rep.errors)} errors, {len(rep.warnings)} warnings")
    sys.exit(1 if rep.errors else 0)


if __name__ == "__main__":
    main()
