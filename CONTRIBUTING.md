# Contributing

Contributions by humans and agents follow the same rules. The authoritative rules are in [AGENTS.md](AGENTS.md); this page is the short version for people.

## Before you write

1. Read [GLOSSARY.md](GLOSSARY.md) and the ADRs in [docs/adr/](docs/adr/).
2. Read [docs/runbook-template.md](docs/runbook-template.md). One runbook covers one symptom.
3. Gather primary sources first: kernel.org, upstream tool docs, Red Hat, SUSE, Ubuntu and Debian documentation, vendor product docs. Blogs and forum answers are leads, not sources.

## Rules that reviewers enforce

- **Original wording.** No pasted man pages, vendor docs or kernel `Documentation/`. Vendor error catalogs: paraphrase cited codes, link the catalog, never copy tables.
- **Every command has a source and a tag.** `man` means checked in that family's documentation; `unverified` means not. Do not set `lab` or `reviewed: true` yourself; maintainers do, with a recorded run.
- **All three families.** Provide `rhel`, `sles` and `debian` rows, or one `all` row, or `n/a: <reason>`. Check release-level differences (cgroup v2, nftables, package names, renamed kernel fields).
- **Safety.** Start read-only. Put intrusive or disruptive steps behind `CONFIRM WITH HUMAN: <impact>`.
- **Small-model format.** About 1,500 tokens, fixed sections, `if <observation> -> <action>` lines, no pipes inside table cells.

## Workflow

```bash
python3 scripts/build.py      # regenerates INDEX.md, index.json, llms.txt, skills/*/references/
python3 scripts/validate.py   # must report 0 errors
```

Do not edit generated files by hand. Commit generated files together with the change. One runbook per pull request keeps review small.

Changing supported releases, the license or copyright policy, the template or schema, top-level folders, personas or the skill set needs an ADR and maintainer approval.

## Skills

A skill is an [agentskills.io](https://agentskills.io/specification.md) folder: only spec frontmatter fields, `name` equal to the folder, a description under about 300 characters, a body under about 1,000 tokens, and runbooks referenced as `references/<id>.md`. Optional extra check: `skills-ref validate skills/<name>`.

## Licensing of contributions

By contributing you agree your text is licensed CC-BY-4.0 and your code Apache-2.0, as described in [LICENSE](LICENSE). Do not submit text you did not write or have the right to license.

## Never commit customer data

No vmcores, sosreports, supportconfigs, logs with hostnames or addresses, or screenshots of customer systems. Use synthetic or redacted examples.
