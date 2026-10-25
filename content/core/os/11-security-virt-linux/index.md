---
title: "11 · Security, virtualization and Linux"
linkTitle: "11 Security, VMs, Linux"
weight: 11
math: true
---
## 11.1 Protection and security {#os-11-1}

- **Protection** is the mechanism controlling which process can access which resource; **security** defends against attackers trying to break it.
- **Access matrix:** rows = users/domains, columns = objects, entries = rights. Stored by column it is an **access control list (ACL)** (each file lists who may do what; UNIX `rwx` bits). Stored by row it is a **capability list** (each process holds tokens for what it may access; file descriptors are capabilities).
- **UNIX permissions:** `rwxr-x---` = owner read/write/execute, group read/execute, others nothing. **setuid**: a program runs with its owner's rights (`passwd` runs as root to update `/etc/shadow`).
- Passwords are stored as **salted, slow hashes**, never as plain text.

**Common attacks:** **buffer overflow** (writing past a buffer to overwrite the return address; defences: stack canaries, non-executable stack, ASLR), **TOCTOU** (time-of-check to time-of-use: the file changes between checking and opening it), privilege escalation, viruses (attach to programs), worms (spread by themselves), trojans (pretend to be useful).

## 11.2 Virtual machines {#os-11-2}

A **hypervisor** (virtual machine monitor) runs several guest operating systems, each thinking it owns the machine.

- **Type 1 (bare metal):** runs directly on hardware: VMware ESXi, Xen, Hyper-V, KVM.
- **Type 2 (hosted):** an application on a host OS: VirtualBox, VMware Workstation.

Techniques: trap-and-emulate (privileged guest instructions trap to the hypervisor), binary translation, **paravirtualisation** (the guest OS is modified to call the hypervisor directly), and **hardware support** (Intel VT-x, AMD-V, nested page tables).

## 11.3 Containers {#os-11-3}

A **container** is a group of ordinary processes isolated by two kernel features: **namespaces** (a private view: own PIDs, file system, network, hostname) and **cgroups** (limits on CPU, memory, I/O). All containers share the host kernel.

| | Virtual machine | Container |
|---|---|---|
| Kernel | own guest kernel | shares the host kernel |
| Start-up | seconds to minutes | milliseconds |
| Size | GBs | MBs |
| Isolation | stronger | weaker |
| Example | VirtualBox VM | Docker container |

## 11.4 Linux in practice {#os-11-4}

**What happens when you type `./a.out`:** the shell `fork`s; the child `exec`s the program (the kernel loads the executable, maps its code and data, and starts the dynamic loader, which loads shared libraries and calls `main`); the parent `wait`s; on exit the child's status goes back to the shell.

**Pipes and redirection** are done by the shell with `dup2` before `exec`: `ls | grep x` creates a pipe, forks twice, connects `ls`'s stdout to the pipe's write end and `grep`'s stdin to the read end. `cmd > f 2>&1` sends both stdout and stderr to `f`.

**Everyday tools:** `ps` (process states: R running, S sleeping, D uninterruptible disk wait, T stopped, Z zombie), `top`/`htop` (live CPU/memory, load average), `kill`, `/proc/<pid>/` (process information as files), `nice` (lower priority), `nohup` (survive logout), `lsof` (open files).

**Daemon:** a background service with no controlling terminal (sshd, cron).

**`/etc/hosts`:** a local table of name → IP, checked before DNS (per `/etc/nsswitch.conf`).

<div class="nb nb-moral">

ACLs answer "who can touch this file"; capabilities answer "what can this process touch". A VM virtualises the hardware and runs its own kernel; a container isolates ordinary processes on the shared kernel.

</div>
