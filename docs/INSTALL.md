# Installing the L3 skills

Skills follow the [Agent Skills](https://agentskills.io/specification.md) format: a folder with `SKILL.md`, here with runbooks in `references/`. Facts below come from each tool's official docs (checked 2026-11-27); `UNCONFIRMED` marks what the docs did not settle. Prefer the tool's own docs if they disagree with this page.

## Quick path

| Situation | Command |
| - | - |
| Online, any tool | `npx skills@latest add <owner>/linux4AI -a <agent>` (needs Node.js 22.20+; `--copy` if symlinks fail) |
| Offline or air-gapped | `scripts/install.sh --tool <tool> --scope user --from linux4ai-skills.tar.gz` |
| From a checkout | `scripts/install.sh --tool <tool> --scope project` |
| Open WebUI | upload `dist/zips/<skill>.zip` in Workspace > Skills |

`scripts/install.sh --list-tools` prints the supported tool names and target folders. It copies real files, replaces an existing copy of the same skill, and never uses symlinks. Build the archives with `scripts/build.py --dist dist`.

`npx skills` sends anonymous telemetry; set `DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1` to disable it. Review skills before installing them.

## Where each tool looks

| Tool | Project folder | User folder | `install.sh --tool` |
| - | - | - | - |
| Claude Code | `.claude/skills` | `~/.claude/skills` | `claude` |
| OpenCode | `.opencode/skills`, `.claude/skills`, `.agents/skills` | `~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills` | `opencode` or `agents` |
| Codex CLI | `.agents/skills` | `~/.agents/skills` | `agents` |
| Gemini CLI | `.gemini/skills`, `.agents/skills` | `~/.gemini/skills`, `~/.agents/skills` | `gemini` or `agents` |
| GitHub Copilot | `.github/skills`, `.claude/skills`, `.agents/skills` | `~/.copilot/skills`, `~/.agents/skills` | `copilot` or `agents` |
| Cursor | `.cursor/skills`, `.agents/skills` | `~/.cursor/skills`, `~/.agents/skills` | `cursor` or `agents` |
| Goose | `.agents/skills` | `~/.agents/skills` | `agents` |
| Roo Code | `.roo/skills`, `.agents/skills` | `~/.roo/skills`, `~/.agents/skills` | `roo` or `agents` |
| Cline | `.cline/skills`, `.clinerules/skills`, `.claude/skills` | `~/.cline/skills` | `cline` |
| Continue | `.continue/skills` | UNCONFIRMED | `continue` |
| Amp | `.agents/skills` | `~/.config/agents/skills`, `~/.agents/skills` | `agents` |

Portable choice: install to `.agents/skills` (project) or `~/.agents/skills` (user), and also to `.claude/skills` for Claude Code. Project skills override user skills with the same name (Cline does the opposite: global wins). Sources: [Claude Code](https://code.claude.com/docs/en/skills), [OpenCode](https://opencode.ai/docs/skills/), [Codex](https://developers.openai.com/codex/skills), [Gemini CLI](https://geminicli.com/docs/cli/skills/), [Copilot](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [Cursor](https://cursor.com/docs/context/skills), [Goose](https://goose-docs.ai/docs/guides/context-engineering/using-skills), [Roo Code](https://docs.roocode.com/features/skills), [Cline](https://docs.cline.bot/customization/skills), [Amp](https://ampcode.com/docs/customize/skills), [Continue PR](https://github.com/continuedev/continue/pull/9353).

## Invoking a skill explicitly

Small models pick skills poorly on their own; name the skill.

| Tool | Syntax |
| - | - |
| Claude Code, Copilot, Cursor | `/<skill-name>` |
| Codex | `$<skill-name>` or `/skills` |
| OpenCode | `@<skill-name>` |
| Open WebUI | type `$` in chat |
| Goose | ask "use the <skill-name> skill", or `/skills <name>` |
| Gemini CLI, Amp, Roo Code, Continue | UNCONFIRMED; the model loads the skill from its description |

## Tool-specific commands

- **Claude Code**: copy or run `install.sh --tool claude`. Run `/reload-skills` if a new skill is missing.
- **OpenCode**: the skill ID comes from the folder name, not the `name` field. Extra sources can be listed in the `skills` array of `opencode.json`. Mention `@<id>` to load one.
- **Codex**: new skills are picked up automatically; restart if one is missing. The skills list is capped at about 2% of the context window and descriptions are shortened first, which is why these skills keep descriptions short.
- **Gemini CLI**: `gemini skills install <git-url-or-dir> --scope user|workspace --path skills`, then `/skills reload`. Activation shows a consent prompt.
- **Copilot CLI**: `copilot skill add <dir>`, then `/skills reload`. Whether the VS Code Copilot harness itself reads `.agents/skills` is UNCONFIRMED; use `.github/skills` there.
- **Cursor**: no install command; copy to a skills folder. Cloud agents and remote SSH sessions do not see `~/.agents/skills`.
- **Amp**: `amp skill add <path-or-git-url> [--global]`.
- **Goose**: needs the Developer extension to read bundled files.

## Local and self-hosted models

| Stack | Skills | Notes |
| - | - | - |
| OpenCode + Ollama, LM Studio or vLLM | yes | built-in provider discovery; vLLM models start with tools disabled; Ollama says 64k+ context |
| Codex `--oss` (Ollama, LM Studio) or custom provider | yes | Ollama says 64k+ context |
| Goose + Ollama | yes | configure with `goose configure` |
| Open WebUI + Ollama or OpenAI-compatible | yes | needs native function calling and Builtin Tools; otherwise skill text is injected into every message |
| Claude Code via `ANTHROPIC_BASE_URL` (Ollama, LM Studio) | skills load client-side | not supported by Anthropic; whether small models follow skills is UNCONFIRMED |
| Cline, Roo Code, Continue + Ollama | skills yes, local endpoint only partly confirmed | |
| Gemini CLI, Copilot, Cursor, Amp | local endpoint UNCONFIRMED | |
| Ollama, LM Studio, llama.cpp alone | no skills loader | model servers only; pair with a client above |

Context floor for this Library: 64k for agent harnesses, 32k for Open WebUI prompt injection (each skill body is about 1,000 tokens or less, each runbook about 1,500).

## Air-gapped sites

1. On a connected host: `scripts/build.py --dist dist`.
2. Move `dist/linux4ai-skills.tar.gz` (and `dist/zips/` for Open WebUI) inside.
3. Run `tar -xzf linux4ai-skills.tar.gz`, then `linux4ai/scripts/install.sh --tool <tool> --scope user --from linux4ai-skills.tar.gz`.

## Check the install

Ask the tool to list its skills (`/skills`, `gemini skills list`, `copilot skill list`, `amp skills list`, `goose skills list`). Each skill from this Library should appear by folder name. To validate the folders themselves: `skills-ref validate skills/<name>` ([agentskills.io](https://agentskills.io/specification.md)).
