---
id: kdump-enable-verify
title: Enable kdump and verify a crash kernel is armed
area: kernel
symptoms: [no vmcore after panic, kdump not operational, crashkernel not reserved, set up kdump]
families: [rhel, sles, debian]
releases: [rhel8, rhel9, rhel10, sles15sp6, sles15sp7, sles16, debian12, debian13, ubuntu2204, ubuntu2404]
mode: live
risk: intrusive
requires_root: true
vendor: none
verified: man
sources: [https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html-single/managing_monitoring_and_updating_the_kernel/index, https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/, https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/managing_monitoring_and_updating_the_kernel/index, https://documentation.suse.com/sles/15-SP6/single-html/SLES-tuning/, https://documentation.suse.com/sles/16.1/html/SLES-kdump-capturing-crash-dumps/, https://documentation.ubuntu.com/server/how-to/software/kernel-crash-dump/, https://manpages.debian.org/trixie/kdump-tools/kdump-config.8.en.html]
updated: 2026-11-27
---

# Enable kdump and verify a crash kernel is armed

## When to use
A panic or hang left no vmcore, or a new host needs crash capture. Needs root on the live system. S1 and S2 only read; the Act steps change packages and boot arguments and need a reboot.

## Check first

### S1 Is memory reserved for the crash kernel?
Look for `crashkernel=` on the running kernel. Sources [S1] [S4] [S6].

| Family | Command | Verified |
| - | - | - |
| all | `cat /proc/cmdline` | man |
| all | `journalctl -k -g crashkernel` | man |

### S2 Is the capture kernel armed?
Sources [S1] [S4] [S5] [S7].

| Family | Command | Verified |
| - | - | - |
| rhel | `kdumpctl status` | man |
| sles | `systemctl status kdump.service` | man |
| debian | `kdump-config show` | man |

## Act

### S3 Install and enable the service
CONFIRM WITH HUMAN: installs packages and starts a service on a live host.
Sources [S1] [S2] [S4] [S5] [S6].

| Family | Command | Verified |
| - | - | - |
| rhel8 | `dnf install kexec-tools` then `systemctl enable --now kdump.service` | man |
| rhel9 | `dnf install kexec-tools` then `systemctl enable --now kdump.service` | man |
| rhel10 | `dnf install kexec-tools kdump-utils makedumpfile` then `systemctl enable --now kdump.service` | man |
| rhel | `rpm -q kexec-tools` | man |
| sles15sp6 | `zypper install kexec-tools makedumpfile` then `systemctl enable kdump` then `systemctl start kdump` | man |
| sles15sp7 | `zypper install kexec-tools makedumpfile` then `systemctl enable kdump` then `systemctl start kdump` | man |
| sles16 | `zypper install kdump` then `systemctl enable --now kdump` | man |
| sles | `rpm -q kexec-tools` | man |
| debian | `apt install kdump-tools` then `dpkg-reconfigure kdump-tools` | man |

### S4 Set the memory reservation
CONFIRM WITH HUMAN: changes boot arguments; the reservation only takes effect after a reboot.
Sources [S1] [S2] [S3] [S4] [S5] [S6].

| Family | Command | Verified |
| - | - | - |
| rhel8 | `grubby --update-kernel=ALL --args="crashkernel=<SIZE>"` | man |
| rhel9 | `kdumpctl reset-crashkernel --kernel=ALL` | man |
| rhel10 | `kdumpctl reset-crashkernel --kernel=ALL` | man |
| rhel | `kdumpctl estimate` | man |
| sles15sp6 | `kdumptool calibrate` then set the printed High and Low values in the boot loader | man |
| sles15sp7 | `kdumptool calibrate` then set the printed High and Low values in the boot loader | man |
| sles16 | `journalctl -u kdump-commandline.service` | man |
| debian | `update-grub` | man |

`<SIZE>`: memory in MB or a range string, for example `512M-2G:64M,2G-:128M`. Then reboot with `systemctl reboot` after the human agrees.

## Interpret
- if `/proc/cmdline` lacks `crashkernel=` -> run S3 and S4, reboot, repeat S1 and S2.
- if rhel `kdumpctl status` is not operational -> read `journalctl -u kdump.service -b`; if the dump `path` in `/etc/kdump.conf` does not exist, create it, because RHEL 8/9/10 do not create it.
- if rhel8 -> `crashkernel=auto` is valid there; on rhel9 and rhel10 use `kdumpctl reset-crashkernel` instead.
- if sles16 journal says `No crashkernel memory reserved, Kdump cannot start` -> reboot after `kdump-commandline.service` rewrote the boot loader; keep manual `crashkernel=` out of `GRUB_CMDLINE_LINUX`.
- if debian `kdump-config show` says `Not ready to kdump` -> check `USE_KDUMP` in `/etc/default/kdump-tools` and that `crashkernel=` was reserved at boot.
- if ubuntu2404 reserves nothing -> host has under 2 GB RAM; the packaged ranges start at 2G.

## Next
- kdump-trigger-test: prove the whole path with a real crash
- kdump-vmcore-locate: find the dump after a crash

## Guardrails
- Keep a maintenance window and console access before any reboot.
- Keep free space in the dump directory at least equal to RAM when dumps are uncompressed.
