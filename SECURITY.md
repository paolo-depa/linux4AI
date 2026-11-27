# Security policy

linux4AI contains runbooks that agents and engineers execute on production Linux systems. A wrong or unsafe command is a security and availability issue here.

## Report privately

Use GitHub's private vulnerability reporting (Security tab, "Report a vulnerability") for:

- a command or procedure that can cause data loss, an outage, privilege escalation or information disclosure and is presented as safe (for example a destructive step missing its `CONFIRM WITH HUMAN:` gate, or a wrong `risk` level);
- prompt-injection paths: runbook or skill text that would cause an agent to follow instructions found in logs, dumps or command output;
- a script in `scripts/` that mishandles paths, archives or permissions;
- customer data accidentally committed to the repository.

Expect an acknowledgment within a week. Fixes land as normal commits with the reason recorded in `AUDIT.md`.

## Report publicly

Ordinary factual errors (wrong flag, wrong path, outdated release behavior) go to a normal issue with the runbook ID and a primary-source URL.

## Supported versions

Only the `main` branch is maintained.

## What is not covered

No claim here is a guarantee of correctness. Commands tagged `unverified` are explicitly unchecked, and no runbook is human-reviewed unless its front matter says `reviewed: true`.
