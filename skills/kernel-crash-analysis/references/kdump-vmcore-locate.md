---
id: kdump-vmcore-locate
title: Locate and identify the dump a crash left behind
area: kernel
symptoms: [where is the vmcore, vmcore file name differs, dump directory empty]
families: [rhel, sles, debian]
releases: [rhel8, rhel9, rhel10, sles15sp6, sles15sp7, sles16, debian12, debian13, ubuntu2204, ubuntu2404]
mode: both
risk: read-only
requires_root: true
vendor: none
verified: man
sources: [https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html-single/managing_monitoring_and_updating_the_kernel/index, https://documentation.suse.com/sles/15-SP6/single-html/SLES-tuning/, https://documentation.suse.com/sles/16.1/html/SLES-kdump-capturing-crash-dumps/, https://documentation.ubuntu.com/server/how-to/software/kernel-crash-dump/, https://manpages.debian.org/bookworm/kdump-tools/kdump-tools.5.en.html]
updated: 2026-11-27
---

# Locate and identify the dump a crash left behind

## When to use
A host panicked and rebooted, or a customer sent a dump directory, and you need the right files. The file names differ by family.

## Check first

### S1 List dumps in the default directory
Sources [S1] [S2] [S4].

| Family | Command | Verified |
| - | - | - |
| all | `ls -lt /var/crash` | man |

### S2 Find the configured dump directory
The default is `/var/crash`; a dump target or `path` can move it. Sources [S1] [S2] [S5].

| Family | Command | Verified |
| - | - | - |
| rhel | `grep -v "^#" /etc/kdump.conf` | man |
| sles | `grep KDUMP_SAVEDIR /etc/sysconfig/kdump` | man |
| debian | `grep KDUMP_COREDIR /etc/default/kdump-tools` | man |

## Act
n/a

## Interpret
- if rhel -> expect `/var/crash/<HOST-OR-127.0.0.1>-<YYYY-MM-DD-HH:MM:SS>/` holding `vmcore`, `vmcore-dmesg.txt` and `kexec-dmesg.log`.
- if sles15 -> expect `/var/crash/<YYYY-MM-DD-HH:MM>/vmcore`; the directory name contains a colon.
- if sles16 -> expect `/var/crash/<YYYY-MM-DD-HH-MM>/` holding `vmcore`, `dmesg` and `README.txt` with kernel version and dump level.
- if debian or ubuntu -> expect `/var/crash/<YYYYMMDDHHMM>/` holding `dump.<TS>` and `dmesg.<TS>`; the file is not named `vmcore`, and a file named `dump-incomplete` means the save did not finish.
- if the directory is empty -> run `kdump-enable-verify`, then `kdump-trigger-test`.

## Next
- kernel-debuginfo-install: a dump was found and needs symbols
- kernel-vmcore-open: symbols are installed, open the dump
- kdump-enable-verify: nothing was captured
- kdump-trigger-test: prove capture works

## Guardrails
- Keep dumps on access-controlled storage; they contain kernel and process memory.
- Keep the original dump untouched and analyze a copy.
