# linux4AI

A library of advanced Linux debugging knowledge for enterprise servers, written to be consumed by AI agents (including small local LLMs) and used by support teams.

## Language

**Library**:
The full body of debugging knowledge in this repo: runbooks, reference material and skills.
_Avoid_: Knowledge base, docs, wiki

**Runbook**:
A single self-contained procedure that takes a symptom to a diagnosis or next action, with per-distro-family commands.
_Avoid_: Module, guide, chapter, page

**Legacy module**:
One of the original twelve `MOD_xx` files, kept in the archive as source material for runbooks.
_Avoid_: Old docs

**Skill**:
An Agent Skills (agentskills.io) folder with a `SKILL.md`, packaging an on-demand L3 workflow that routes into runbooks.
_Avoid_: Prompt, agent, playbook

**L3**:
The sole target persona: engineers who receive escalated cases and work them to root cause or vendor/upstream escalation. L1 and L2 are out of scope.
_Avoid_: Support team, SRE, operator

**Distro family**:
One of `rhel`, `sles` or `debian`, the unit at which commands are allowed to differ. Ubuntu is a sub-label of `debian`, used only where it diverges.
_Avoid_: Distro, OS, flavor

**Supported release**:
A specific enterprise release the Library commits to covering: RHEL 8/9/10, SLES 15 SP6/SP7 and 16, Debian 12/13, Ubuntu Server LTS 22.04/24.04. Home and desktop distros are out of scope.
_Avoid_: Version, target

**Verification tag**:
A per-command label stating how far the command was checked: `lab` (run on a real system), `man` (checked against primary documentation) or `unverified` (flagged for human review).
_Avoid_: Confidence, status

**Reviewed**:
A runbook flag set only by a human, meaning a person has vouched for it. Absent by default; no standing reviewer exists, so most runbooks stay unreviewed.
_Avoid_: Approved, validated, certified

**Primary source**:
Vendor or upstream documentation (kernel.org, Red Hat, SUSE, Ubuntu/Debian, hardware vendors) cited by URL to back a claim.
_Avoid_: Reference, link
