---
id: kernel-vmcore-open
title: Open a vmcore with crash or drgn and confirm the symbols match
area: kernel
symptoms: [open vmcore, crash will not start on vmcore, drgn warns symbols do not match, verify vmlinux matches dump]
families: [rhel, sles, debian]
releases: [rhel8, rhel9, rhel10, sles15sp6, sles15sp7, sles16, debian12, debian13, ubuntu2204, ubuntu2404]
mode: offline
risk: intrusive
requires_root: true
vendor: none
verified: unverified
sources: [https://raw.githubusercontent.com/crash-utility/crash/master/help.c, https://crash-utility.github.io/crash/changelog.html, https://access.redhat.com/solutions/9907, https://documentation.suse.com/sles/15-SP7/html/SLES-all/cha-tuning-kexec.html, https://documentation.ubuntu.com/server/how-to/software/kernel-crash-dump/, https://drgn.readthedocs.io/en/latest/man/drgn.html, https://drgn.readthedocs.io/en/latest/installation.html]
updated: 2026-11-27
---

# Open a vmcore with crash or drgn and confirm the symbols match

## When to use
You have a vmcore (see `kdump-vmcore-locate`) and the matching debug symbols (see `kernel-debuginfo-install`). `<VMCORE>` is the dump file; `<KVER>` is the kernel release; `<VMLINUX>` is the symbol file. If S1 shows `crash` missing, run S5 first.

## Check first

### S1 Are the analysis tools installed?
Sources [S3] [S4] [S7].

| Family | Command | Verified |
| - | - | - |
| rhel | `rpm -q crash drgn` | man |
| sles | `rpm -q crash python3-drgn` | man |
| debian | `dpkg -s crash python3-drgn` | man |

### S2 Read the dump's kernel release and build-id
Sources [S1] [S2].

| Family | Command | Verified |
| - | - | - |
| all | `crash --osrelease <VMCORE>` | man |
| all | `crash --build-id <VMCORE>` | man |

### S3 Open the dump with crash
Run from a copy of the dump. Sources [S3] [S4] [S5].

| Family | Command | Verified |
| - | - | - |
| rhel | `crash /usr/lib/debug/lib/modules/<KVER>/vmlinux <VMCORE>` | man |
| sles15sp6 | `crash /boot/vmlinux-<KVER>.gz <VMCORE>` | man |
| sles15sp7 | `crash /boot/vmlinux-<KVER>.gz <VMCORE>` | man |
| sles16 | n/a: SLES 16 vmlinux path is not documented; find it with the package file list | unverified |
| debian | `crash /usr/lib/debug/boot/vmlinux-<KVER> <VMCORE>` | man |

### S4 Open the dump with drgn
Use when scripted traversal is needed. Sources [S6].

| Family | Command | Verified |
| - | - | - |
| all | `drgn -c <VMCORE> -s <VMLINUX>` | man |

## Act

### S5 Install crash and drgn if S2 shows them missing
CONFIRM WITH HUMAN: installs packages; on SLES the crash package comes from the Development Tools Module (15) and drgn from Package Hub.
Sources [S3] [S4] [S7].

| Family | Command | Verified |
| - | - | - |
| rhel8 | `yum install crash` | man |
| rhel9 | `dnf install crash drgn` | man |
| rhel10 | `dnf install crash drgn` | man |
| sles15sp6 | `zypper install crash python3-drgn` | man |
| sles15sp7 | `zypper install crash python3-drgn` | man |
| sles16 | `zypper install crash python313-drgn` | man |
| debian | `apt install crash python3-drgn` | man |

## Interpret
- if `crash --build-id` fails or the option is unknown -> crash is older than 9.0.2 or the kernel is older than 5.9; compare `crash --osrelease` with the debuginfo package version instead.
- if crash or drgn reports that symbols do not match the dump -> install the exact `<KVER>` package with `kernel-debuginfo-install`.
- if the `drgn` command is not found -> run `python3 -m drgn` with the same options.
- if drgn cannot read a compressed vmcore -> libkdumpfile support is missing; use `crash` on ubuntu2204, where `python3-drgn` is not in the archive.
- if the dump came from another host -> copy the dump, kernel image and debug file into one directory first; the architecture must match.
- if the dump is a Debian or Ubuntu `dump.<TS>` file -> pass it as `<VMCORE>` unchanged.

## Next
- kernel-debuginfo-install: symbols are missing or mismatched
- kdump-vmcore-locate: find the right dump file

## Guardrails
- Keep the original dump read-only and analyze a copy.
- Keep `drgn` and `crash` versions in the notes you hand to the next engineer.
