---
id: kernel-debuginfo-install
title: Install kernel debug symbols that match a kernel or vmcore
area: kernel
symptoms: [need vmlinux for vmcore, crash says namelist mismatch, kernel debuginfo package missing]
families: [rhel, sles, debian]
releases: [rhel8, rhel9, rhel10, sles15sp6, sles15sp7, sles16, debian12, debian13, ubuntu2204, ubuntu2404]
mode: both
risk: intrusive
requires_root: true
vendor: none
verified: unverified
sources: [https://access.redhat.com/solutions/9907, https://documentation.suse.com/sles/15-SP7/html/SLES-all/cha-tuning-kexec.html, https://documentation.ubuntu.com/server/how-to/debugging/debug-symbol-packages/, https://documentation.ubuntu.com/server/how-to/software/kernel-crash-dump/, https://drgn.readthedocs.io/en/latest/getting_debugging_symbols.html, https://raw.githubusercontent.com/crash-utility/crash/master/help.c]
updated: 2026-11-27
---

# Install kernel debug symbols that match a kernel or vmcore

## When to use
`crash` or `drgn` cannot open a vmcore or live kernel without matching symbols. The package must match `<KVER>` exactly, where `<KVER>` is the kernel release string. Debug packages are large (about 0.4 to 1.7 GB).

## Check first

### S1 Get `<KVER>`
Live system: `uname -r`. For a vmcore, read it from the dump header. Sources [S6].

| Family | Command | Verified |
| - | - | - |
| all | `uname -r` | man |
| all | `crash --osrelease <VMCORE>` | man |

### S2 Is the package already installed?
Sources [S1] [S4] [S5].

| Family | Command | Verified |
| - | - | - |
| rhel | `rpm -q kernel-debuginfo-<KVER>` | man |
| sles | `rpm -q kernel-default-debuginfo` | man |
| debian12 | `dpkg -s linux-image-<KVER>-dbg` | man |
| debian13 | `dpkg -s linux-image-<KVER>-dbg` | man |
| ubuntu | `dpkg -s linux-image-unsigned-<KVER>-dbgsym` | man |

## Act

### S3 Enable the debug repository
CONFIRM WITH HUMAN: adds a package source; needs a valid subscription or network access.
Sources [S1] [S2] [S3].

| Family | Command | Verified |
| - | - | - |
| rhel8 | `subscription-manager repos --enable=rhel-8-for-$(uname -m)-baseos-debug-rpms --enable=rhel-8-for-$(uname -m)-appstream-debug-rpms` | man |
| rhel9 | `subscription-manager repos --enable=rhel-9-for-$(uname -m)-baseos-debug-rpms` | man |
| rhel10 | `subscription-manager repos --enable=rhel-10-for-$(uname -m)-baseos-debug-rpms` | man |
| sles15sp6 | `yast2 repositories`, then enable the `*-Debuginfo-Updates` repository | man |
| sles15sp7 | `yast2 repositories`, then enable the `*-Debuginfo-Updates` repository | man |
| sles16 | n/a: SLES 16 debuginfo repo enablement is not documented; check SCC or the RMT repo list | unverified |
| debian | n/a: Debian ships kernel `-dbg` packages in the normal main archive | man |
| ubuntu | `apt install ubuntu-dbgsym-keyring`, create `/etc/apt/sources.list.d/ddebs.sources` as below, then `apt-get update` | man |

```text
Types: deb
URIs: http://ddebs.ubuntu.com/
Suites: <CODENAME> <CODENAME>-updates <CODENAME>-proposed
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-dbgsym-keyring.gpg
```

### S4 Install the matching package
CONFIRM WITH HUMAN: downloads and installs a large package.
Sources [S1] [S2] [S4] [S5].

| Family | Command | Verified |
| - | - | - |
| rhel8 | `yum install kernel-debuginfo-<KVER> kernel-debuginfo-common-$(uname -m)-<KVER>` | man |
| rhel9 | `dnf install kernel-debuginfo-<KVER>` | man |
| rhel10 | `dnf install kernel-debuginfo-<KVER>` | man |
| sles | `zypper search -s kernel-default-debuginfo` then `zypper install kernel-default-debuginfo-<VERSION>` | man |
| debian | `apt install linux-image-<KVER>-dbg` | man |
| ubuntu | `apt-get install linux-image-<KVER>-dbgsym` | man |

`<VERSION>`: the package version from the search list that corresponds to `<KVER>`.

## Interpret
- if the package is not found for an old kernel -> download the RPM or deb by hand (Red Hat Customer Portal Packages tab, `ddebs.ubuntu.com/pool/main/l/linux/`, Debian pool) and install with `rpm -i` or `dpkg -i`.
- if the dump came from another host -> install the exact `<KVER>` package there too; a newer or older build does not match.
- if the host is air-gapped -> mirror the repos with RMT (`rmt-cli export` and `rmt-cli import`) on SUSE, or copy the packages in.
- if you expect debuginfod to supply the kernel -> do not rely on it; no official source confirms it serves kernel vmlinux.

## Next
- kernel-vmcore-open: open the dump with crash or drgn

## Guardrails
- Keep the package version identical to the crashed kernel, not the newest one.
- Keep downloads inside approved repositories and subscriptions.
