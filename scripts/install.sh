#!/usr/bin/env bash
# Install linux4AI skills for an agent tool by copying real files (no symlinks, works offline).
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install.sh --tool <tool> [--scope user|project] [--from <dir|tarball>] [--skill <name>]... [--dest <dir>] [--dry-run]
       install.sh --list-tools

  --tool    target tool (see --list-tools)
  --scope   user (default, under $HOME) or project (under the current directory)
  --from    folder holding skill folders, or a linux4ai-skills.tar.gz (default: ../skills next to this script)
  --skill   install only this skill; repeat for several (default: all)
  --dest    override the destination skills directory
  --dry-run print what would be done
EOF
}

list_tools() {
  cat <<'EOF'
agents    user ~/.agents/skills                  project .agents/skills        (Codex, Gemini CLI, Cursor, Goose, Roo Code, Amp, OpenCode, Copilot)
claude    user ~/.claude/skills                  project .claude/skills        (Claude Code)
opencode  user ~/.config/opencode/skills         project .opencode/skills
gemini    user ~/.gemini/skills                  project .gemini/skills
copilot   user ~/.copilot/skills                 project .github/skills
cursor    user ~/.cursor/skills                  project .cursor/skills
cline     user ~/.cline/skills                   project .cline/skills
roo       user ~/.roo/skills                     project .roo/skills
continue  user ~/.continue/skills                project .continue/skills
EOF
}

die() { echo "install.sh: $*" >&2; exit 2; }

tool="" scope="user" from="" dest="" dry=0
skills=()
while [ $# -gt 0 ]; do
  case "$1" in
    --tool) tool="${2:?}"; shift 2 ;;
    --scope) scope="${2:?}"; shift 2 ;;
    --from) from="${2:?}"; shift 2 ;;
    --skill) skills+=("${2:?}"); shift 2 ;;
    --dest) dest="${2:?}"; shift 2 ;;
    --dry-run) dry=1; shift ;;
    --list-tools) list_tools; exit 0 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; die "unknown argument: $1" ;;
  esac
done

[ "$scope" = user ] || [ "$scope" = project ] || die "--scope must be user or project"

if [ -z "$dest" ]; then
  [ -n "$tool" ] || { usage >&2; die "--tool or --dest is required"; }
  case "$tool:$scope" in
    agents:user) dest="$HOME/.agents/skills" ;;
    agents:project) dest=".agents/skills" ;;
    claude:user) dest="$HOME/.claude/skills" ;;
    claude:project) dest=".claude/skills" ;;
    opencode:user) dest="$HOME/.config/opencode/skills" ;;
    opencode:project) dest=".opencode/skills" ;;
    gemini:user) dest="$HOME/.gemini/skills" ;;
    gemini:project) dest=".gemini/skills" ;;
    copilot:user) dest="$HOME/.copilot/skills" ;;
    copilot:project) dest=".github/skills" ;;
    cursor:user) dest="$HOME/.cursor/skills" ;;
    cursor:project) dest=".cursor/skills" ;;
    cline:user) dest="$HOME/.cline/skills" ;;
    cline:project) dest=".cline/skills" ;;
    roo:user) dest="$HOME/.roo/skills" ;;
    roo:project) dest=".roo/skills" ;;
    continue:user) dest="$HOME/.continue/skills" ;;
    continue:project) dest=".continue/skills" ;;
    *) die "unknown tool '$tool' (see --list-tools)" ;;
  esac
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -n "$from" ] || from="$script_dir/../skills"

tmp=""
cleanup() { [ -z "$tmp" ] || rm -rf "$tmp"; }
trap cleanup EXIT

if [ -f "$from" ]; then
  tmp="$(mktemp -d)"
  tar -xzf "$from" -C "$tmp"
  src="$(find "$tmp" -type d -name skills -path '*/linux4ai/skills' | head -n 1)"
  [ -n "$src" ] || die "no linux4ai/skills folder inside $from"
elif [ -d "$from" ]; then
  src="$from"
else
  die "--from path not found: $from"
fi

found=0
for dir in "$src"/*/; do
  [ -f "${dir}SKILL.md" ] || continue
  name="$(basename "$dir")"
  if [ "${#skills[@]}" -gt 0 ]; then
    match=0
    for s in "${skills[@]}"; do [ "$s" = "$name" ] && match=1; done
    [ "$match" = 1 ] || continue
  fi
  found=$((found + 1))
  if [ "$dry" = 1 ]; then
    echo "would install $name -> $dest/$name"
    continue
  fi
  mkdir -p "$dest"
  rm -rf "${dest:?}/$name"
  cp -R "${dir%/}" "$dest/$name"
  echo "installed $name -> $dest/$name"
done

[ "$found" -gt 0 ] || die "no matching skills found in $src"
echo "done: $found skill(s). Restart or reload the tool if it does not list them."
