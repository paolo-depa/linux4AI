## What changes

<!-- Runbook IDs or skill names touched. One runbook per PR is easiest to review. -->

## Checklist

- [ ] Wording is original; no copied man page, vendor doc or kernel `Documentation/` text
- [ ] Every command and claim cites a primary source in `sources:`
- [ ] Rows cover `rhel`, `sles` and `debian` (or `all`, or `n/a: <reason>`), release differences checked
- [ ] Verification tags are honest (`man` or `unverified`); I did not set `lab` or `reviewed`
- [ ] Intrusive or disruptive steps sit behind `CONFIRM WITH HUMAN:` and `risk` matches
- [ ] `python3 scripts/build.py` run and generated files committed
- [ ] `python3 scripts/validate.py` reports 0 errors
- [ ] No customer data (dumps, sosreports, hostnames, addresses)

## Needs maintainer approval (ADR required)

- [ ] Not applicable
- [ ] Changes supported releases, license, copyright policy, template/schema, top-level folders, personas or skill set
