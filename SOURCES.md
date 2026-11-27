# Sources

Every runbook lists its own primary sources in front matter (`sources:`). This file lists sources used for repo-level documents and the source classes accepted as primary.

## Accepted primary sources

- Upstream projects: kernel.org documentation, kexec-tools, makedumpfile, crash, drgn, elfutils (debuginfod), systemd, bpftrace.
- Distribution vendors: Red Hat (docs.redhat.com), SUSE (documentation.suse.com, support TIDs), Ubuntu (documentation.ubuntu.com, manpages.ubuntu.com), Debian (wiki.debian.org, manpages.debian.org).
- Hardware vendors: public product documentation only; error-code meanings are paraphrased and linked, never copied as tables.

## Repo-level documents

| Document | Sources |
| - | - |
| `docs/INSTALL.md` | https://agentskills.io/specification.md, https://agentskills.io/client-implementation/adding-skills-support.md, plus the per-tool pages linked inside that file |
| `docs/runbook-template.md`, `AGENTS.md` | https://agentskills.io/skill-creation/best-practices.md (progressive disclosure, gotchas, validation loops) |
| Method names | USE Method: Brendan Gregg, https://www.brendangregg.com/usemethod.html |
