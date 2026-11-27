# Skills bundle generated copies of runbooks

Skills follow agentskills.io and must be self-contained: clients install a skill folder on its own, Gemini CLI only allows file access inside it, and symlinks are ignored or refused by `npx skills` and Open WebUI. So `runbooks/` remains the source of truth and `scripts/build.py` copies each runbook a skill references into `skills/<name>/references/` as real files. The copies are committed, because `npx skills add`, `gemini skills install` and git-based installs run no build step; `scripts/validate.py` fails on drift.

Rejected: one monolithic skill (imprecise triggering, large index for small models) and skills reaching into each other's folders (breaks on install).

Skills live flat in `skills/<name>/` with only agentskills.io frontmatter fields. Marketplace or plugin manifests are deferred; install paths are `npx skills`, `scripts/install.sh` and a release tarball.
