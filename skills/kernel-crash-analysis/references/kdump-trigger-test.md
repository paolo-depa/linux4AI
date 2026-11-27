---
id: kdump-trigger-test
title: Prove kdump works by forcing a test crash
area: kernel
symptoms: [verify kdump end to end, test crash dump capture]
families: [rhel, sles, debian]
releases: [rhel8, rhel9, rhel10, sles15sp6, sles15sp7, sles16, debian12, debian13, ubuntu2204, ubuntu2404]
mode: live
risk: disruptive
requires_root: true
vendor: none
verified: man
sources: [https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html-single/managing_monitoring_and_updating_the_kernel/index, https://documentation.suse.com/sles/15-SP6/single-html/SLES-tuning/, https://documentation.suse.com/sles/16.1/html/SLES-kdump-capturing-crash-dumps/, https://documentation.ubuntu.com/server/how-to/software/kernel-crash-dump/, https://docs.kernel.org/admin-guide/kdump/kdump.html]
updated: 2026-11-27
---

# Prove kdump works by forcing a test crash

## When to use
`kdump-enable-verify` shows an armed crash kernel and you need proof that a vmcore is really written. The test panics the host as a real crash would.

## Check first

### S1 Is magic SysRq enabled?
The trigger writes to `/proc/sysrq-trigger`. Sources [S4] [S5].

| Family | Command | Verified |
| - | - | - |
| all | `cat /proc/sys/kernel/sysrq` | man |

### S2 Is free space available for the dump?
Sources [S2].

| Family | Command | Verified |
| - | - | - |
| all | `df -h /var/crash` | man |

## Act

### S3 Trigger the crash
CONFIRM WITH HUMAN: panics and reboots this host, drops sessions, may lose unsaved data; run only on an idle host with console access in a maintenance window.
Sources [S1] [S2] [S3] [S4].

| Family | Command | Verified |
| - | - | - |
| rhel | `kdumpctl restart` then `kdumpctl status` then `echo c > /proc/sysrq-trigger` | man |
| sles15sp6 | `systemctl isolate rescue.target` then `systemctl start kdump` then `umount -a` then `mount -o remount,ro /` then `echo c > /proc/sysrq-trigger` | man |
| sles15sp7 | `systemctl isolate rescue.target` then `systemctl start kdump` then `umount -a` then `mount -o remount,ro /` then `echo c > /proc/sysrq-trigger` | man |
| sles16 | `echo s > /proc/sysrq-trigger` then `echo u > /proc/sysrq-trigger` then `echo c > /proc/sysrq-trigger` | man |
| debian | `echo c > /proc/sysrq-trigger` | man |

Run the debian command from a real root shell; `sudo echo c > ...` applies the redirect as the unprivileged user.

## Interpret
- if sysrq prints `0` in S1 -> run `sysctl -w kernel.sysrq=1`, then S3.
- if the host reboots and a dump exists -> go to `kdump-vmcore-locate`.
- if the host hangs without rebooting -> read the BMC or serial console for the capture-kernel log; suspect firmware or a missing driver in the capture initramfs.
- if the capture kernel reports out of memory -> roughly double the reservation and rerun `kdump-enable-verify`.
- if the host reboots with no dump -> read the dump directory settings and `journalctl -b -1` for kdump errors.

## Next
- kdump-vmcore-locate: find and identify the dump
- kdump-enable-verify: adjust the reservation

## Guardrails
- Keep this test off production hosts that carry load.
- Keep the first test on one host before repeating it fleet-wide.
