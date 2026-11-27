# linux4AI

Advanced Linux debugging runbooks and [Agent Skills](https://agentskills.io) for **L3 engineers** on enterprise **RHEL, SLES and Debian/Ubuntu**, written so that small, locally hosted LLMs can follow them.

Each runbook covers one symptom, stays near 1,500 tokens, and gives every command per distro family with a verification tag. Skills package the runbooks into on-demand workflows for agent tools such as OpenCode, Codex, Claude Code, Gemini CLI, Copilot, Cursor, Goose and Open WebUI.

> **Trust model.** Commands are checked against primary documentation (`man`) or flagged `unverified`. Nothing here is tagged `lab` yet, and no runbook is human-reviewed. Agents using these skills are instructed to say "unverified" when they relay unreviewed content. Read the cited sources before running anything on a production system.

## Scope

| | |
| - | - |
| Audience | L3 support engineers working escalated cases, mostly offline on artifacts (vmcore, supportconfig, sosreport) |
| Families | `rhel`, `sles`, `debian` (Ubuntu as a sub-label) |
| Releases | RHEL 8, 9, 10; SLES 15 SP6, SP7, 16; Debian 12, 13; Ubuntu 22.04, 24.04 |
| Out of scope | Fedora, openSUSE, Arch, desktop distros, L1/L2 triage |

## Quick start

Install the skills into your agent tool:

```bash
npx skills@latest add paolo-depa/linux4AI -a <agent>      # online
scripts/install.sh --tool <tool> --scope user              # from a checkout
scripts/install.sh --tool <tool> --from linux4ai-skills.tar.gz   # air-gapped
```

Per-tool folders, explicit invocation syntax, local-model setups and the air-gapped procedure are in [docs/INSTALL.md](docs/INSTALL.md).

Without an agent, start at [INDEX.md](INDEX.md): find the symptom, open the runbook.

## What is in the library

| Skill | Status | Runbooks |
| - | - | - |
| `kernel-crash-analysis` | available | `kdump-enable-verify`, `kdump-trigger-test`, `kdump-vmcore-locate`, `kernel-debuginfo-install`, `kernel-vmcore-open` |
| `l3-case-intake`, `kernel-hang-analysis`, `memory-oom-analysis`, `storage-io-analysis`, `network-drop-analysis`, `hardware-ras-analysis`, `ha-cluster-analysis`, `performance-tracing`, `boot-failure-analysis`, `vendor-escalation-writeup` | planned | not written yet |

Machine-readable catalog: [index.json](index.json), [llms.txt](llms.txt).

## Repository layout

| Path | Purpose |
| - | - |
| `runbooks/<area>/<id>.md` | Source of truth, one symptom each |
| `skills/<name>/` | Agent Skills; `references/` holds generated copies of the runbooks each skill uses |
| `docs/runbook-template.md` | The runbook template and front-matter schema |
| `docs/adr/` | Decisions that look odd without context |
| `scripts/` | `build.py` (generate), `validate.py` (check), `install.sh` (install) |
| `GLOSSARY.md`, `AGENTS.md` | Project vocabulary and rules for agents and contributors |

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). In short: original wording, a cited primary source for every claim, all three distro families, then `scripts/build.py` and `scripts/validate.py` must pass.

Found a wrong command or claim? Open an issue with the runbook ID and a source. Wrong commands are a safety problem in this project; see [SECURITY.md](SECURITY.md) for dangerous ones.

## License

Text is [CC-BY-4.0](LICENSES/CC-BY-4.0.txt); code is [Apache-2.0](LICENSES/Apache-2.0.txt). See [LICENSE](LICENSE). Vendor names and error-code meanings belong to their owners; runbooks paraphrase and link, they do not reproduce vendor catalogs.
