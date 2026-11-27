# Runbook template

File: `runbooks/<area>/<id>.md`. The file name without `.md` equals `id`. IDs are permanent.
Copy the skeleton at the end, fill every section or write `n/a`.

## Front matter (restricted YAML: `key: value`, inline lists `[a, b]`, no nesting)

| Key | Rule |
| - | - |
| `id` | `^[a-z0-9]+(-[a-z0-9]+)*$`, equals file name |
| `title` | one line |
| `area` | folder name: boot, kernel, memory, storage, network, hardware, cluster, tracing, collection, platform |
| `symptoms` | list of short phrases an L3 would search for; feeds `INDEX.md` |
| `families` | subset of `[rhel, sles, debian]` that the runbook covers |
| `releases` | subset of `rhel8 rhel9 rhel10 sles15sp6 sles15sp7 sles16 debian12 debian13 ubuntu2204 ubuntu2404` |
| `mode` | `offline` (artifact), `live` (running system) or `both` |
| `risk` | `read-only`, `intrusive` or `disruptive`; `read-only` requires `## Act` to be `n/a` |
| `requires_root` | `true` or `false` |
| `vendor` | `none` or a vendor name; vendor runbooks can be switched off |
| `verified` | lowest tag used in the body: `man` or `unverified` |
| `sources` | primary-source URLs (the body cites them as `[S1]`, `[S2]` by order) |
| `updated` | `YYYY-MM-DD` |
| `reviewed` | optional; only a human sets `true` |
| `lab_record` | optional; required when any command is tagged `lab` |

## Sections (fixed order, `##` headings)

1. `## When to use`: 2 to 3 lines: the symptom and the artifact or system needed.
2. `## Check first`: read-only steps.
3. `## Act`: intrusive or disruptive steps, each preceded by `CONFIRM WITH HUMAN: <impact>`. `n/a` when risk is read-only.
4. `## Interpret`: `if <observation> -> <action>` lines.
5. `## Next`: runbook IDs only, one per line as `- <id>: <when>`, or `n/a`.
6. `## Guardrails`: what to keep intact (state the positive target). `n/a` is not allowed.

## Step format (inside Check first and Act)

A step is a `### S<n> <title>` heading, one sentence on purpose, then a table with columns `Family | Command | Verified`.

- Family is `all`, or `rhel`, `sles`, `debian`, `ubuntu`.
- Use one `all` row when the command is identical on every family. Otherwise give `rhel`, `sles` and `debian` rows.
- A row may read `n/a: <one-line reason>` in the Command column.
- Verified is `man`, `lab` or `unverified`.
- Placeholders are written `<NAME>`; define each where first used.
- Release-specific commands name the release in the Family cell, for example `rhel8`.

## Skeleton

````markdown
---
id: example-id
title: Example title
area: kernel
symptoms: [short phrase, another phrase]
families: [rhel, sles, debian]
releases: [rhel9, sles15sp6, debian12]
mode: both
risk: read-only
requires_root: true
vendor: none
verified: man
sources: [https://example.org/doc]
updated: 2026-11-27
---

# Example title

## When to use
...

## Check first

### S1 Show status
Purpose in one sentence.

| Family | Command | Verified |
| - | - | - |
| all | `uname -r` | man |

## Act
n/a

## Interpret
- if <observation> -> <action>

## Next
- other-runbook-id: when

## Guardrails
- Keep ...
````
