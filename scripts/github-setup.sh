#!/usr/bin/env bash
# Apply repository metadata with the GitHub CLI. Needs `gh auth login` first. Safe to re-run.
set -euo pipefail

repo="${1:-paolo-depa/linux4AI}"
command -v gh >/dev/null || { echo "gh not found" >&2; exit 2; }
gh auth status >/dev/null 2>&1 || { echo "run 'gh auth login' first" >&2; exit 2; }

gh repo edit "$repo" \
  --description "Advanced Linux debugging runbooks and Agent Skills for L3 engineers on RHEL, SLES and Debian/Ubuntu, written for small local LLMs" \
  --enable-issues \
  --enable-wiki=false \
  --enable-projects=false \
  --delete-branch-on-merge \
  --enable-squash-merge \
  --enable-merge-commit=false \
  --enable-rebase-merge=false

topics=(linux debugging troubleshooting kernel kdump crash-dump runbooks agent-skills ai-agents llm
        local-llm rhel sles ubuntu debian sre support enterprise-linux agentskills)
args=()
for t in "${topics[@]}"; do args+=(--add-topic "$t"); done
gh repo edit "$repo" "${args[@]}"

gh repo view "$repo" --json description,repositoryTopics --jq '{description, topics: [.repositoryTopics[].name]}'
echo "Also in the web UI: enable private vulnerability reporting (Settings > Security), and upload a social preview image."
