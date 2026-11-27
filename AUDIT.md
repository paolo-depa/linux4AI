# Audit log

Corrections to existing claims: old claim, new claim, source. The original twelve topic modules were discarded rather than audited (see `docs/adr/0002-runbooks-with-fixed-template.md`); spot checks before removal found these problems, recorded so they are not reintroduced:

| Old claim (discarded) | Finding | Source |
| - | - | - |
| drgn snippet read `task.state` | Field renamed `__state` in newer kernels; per-release behavior must be checked | to verify per release when a drgn runbook is written |
| Xid 62 described as an NVLink internal failure | Meaning must be taken from NVIDIA's catalog, not memory | to verify when the GPU runbook is written |
| `nvidia-smi -pm 0` flushes InfoROM | Unsupported claim; omit unless a primary source confirms it | to verify when the GPU runbook is written |
