# Runbooks with a fixed template, rewritten from scratch

The Library is a set of atomic runbooks (one symptom each, about 1,500 tokens) in a fixed template defined in `docs/runbook-template.md`, so small local models can follow them mechanically. The twelve original topic-dump modules were discarded: they were unsourced, mixed families and releases without saying so, and contained errors.

Runbooks are the single source of truth. `INDEX.md`, `index.json` and `llms.txt` are generated from front matter, and `scripts/validate.py` enforces the template, the token budget, verification tags and link integrity.

Deviation from the original proposal: "Check first" and "Commands by family" are merged into two sections, **Check first** (read-only steps) and **Act** (intrusive or disruptive steps behind `CONFIRM WITH HUMAN:`), so risk is visible by position.
