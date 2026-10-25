---
title: "12 · Virtualization and containers"
linkTitle: "12 Virtualization and containers"
weight: 12
math: true
---
## 12.1 Virtual machines {#sec-os-vm}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> this book was built inside a Linux VM (the CPU reports a hypervisor) on a host the guest never sees.</em>

</div>

<div class="nb nb-definition" id="definition-12-1-1">

<strong>Definition 12.1.1</strong>. A <strong>virtual machine monitor</strong> (VMM, <strong>hypervisor</strong>) runs several guest operating systems, each believing it owns a whole machine. A <strong>type 1</strong> (bare-metal) hypervisor runs directly on the hardware (Xen, VMware ESXi, Hyper-V; KVM turns Linux itself into one). A <strong>type 2</strong> (hosted) hypervisor is an application on a host OS (VirtualBox, VMware Workstation, QEMU without KVM).

</div>

<div class="nb nb-definition" id="definition-12-1-2">

<strong>Definition 12.1.2</strong>. How the guest kernel is kept from touching real hardware:

- <strong>Trap-and-emulate</strong>: run the guest kernel in user mode; each privileged instruction it executes traps to the VMM, which emulates its effect on the <em>virtual</em> machine state. This works only if every sensitive instruction traps (Popek and Goldberg’s condition); classic x86 had sensitive instructions that silently behaved differently in user mode (`popf` dropping the interrupt flag), so it was not virtualisable this way.
- <strong>Binary translation</strong> (early VMware): rewrite the guest kernel’s problem instructions on the fly into safe sequences.
- <strong>Paravirtualisation</strong> (Xen): modify the guest kernel to call the hypervisor explicitly (<strong>hypercalls</strong>) instead of executing privileged instructions; today it survives mainly as paravirtual <em>devices</em> (virtio disks and NICs, like `/dev/vda` in [Chapter 10](../10-io/)), much faster than emulating real hardware.
- <strong>Hardware-assisted virtualisation</strong> (Intel VT-x, AMD-V): a new CPU mode for guests in which sensitive operations cause <strong>VM exits</strong> to the hypervisor, plus <strong>nested paging</strong> (EPT/NPT): the MMU walks guest page tables (guest virtual to guest physical) and the hypervisor’s tables (guest physical to host physical) in hardware, instead of the VMM maintaining <strong>shadow page tables</strong>.

</div>

<div class="nb nb-remark" id="remark-12-1-3">

<strong>Remark 12.1.3</strong> (Costs) — CPU-bound guest code runs at nearly native speed (it executes directly). Overheads come from VM exits (I/O, interrupts, some instructions) and from TLB misses, which with nested paging may need up to $24$ memory references instead of $4$ for a 4-level walk in each dimension ($(4+1)\times(4+1)-1$). Large pages and paravirtual devices reduce both.

</div>

## 12.2 Containers {#sec-os-containers}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `docker run` starts a process that sees itself as PID 1 with its own host name and file system, and it is still just a process of the host kernel.</em>

</div>

<div class="nb nb-definition" id="definition-12-2-1">

<strong>Definition 12.2.1</strong>. A <strong>container</strong> is a group of ordinary processes isolated by two kernel features:

- <strong>namespaces</strong> give it a private <em>view</em>: PID (its own PID 1), mount (its own root file system), network (its own interfaces, ports, routing), UTS (host name), IPC, user (uid 0 inside mapped to an unprivileged uid outside), cgroup, time;
- <strong>control groups</strong> (cgroups) limit and account its <em>resources</em>: CPU shares and quotas, memory (the OOM killer acts per cgroup), block I/O, number of processes.

A container image is a layered file system (overlay) mounted as its root. Seccomp filters and dropped capabilities narrow the system calls it may use.

</div>

```text {filename="Terminal session (bash, Linux 6.18)"}
## namespaces: a private view of PIDs, host name, mounts, ...
$ ls /proc/self/ns | tr '\n' ' '; echo
cgroup ipc mnt net pid pid_for_children time time_for_children user uts 
$ unshare --pid --fork --mount-proc ps -o pid,comm
    PID COMMAND
      1 ps
$ unshare --uts sh -c 'hostname box; hostname'
box
$ hostname
vm
## cgroups: limits on a group of processes (here: at most 5 tasks)
$ bash -c 'echo $$ > /sys/fs/cgroup/pids/os-book/cgroup.procs; exec ./forker 10'
fork() succeeded 4 times, failed 6 times: Resource temporarily unavailable
## are we in a VM? (the CPU announces a hypervisor)
$ grep -m1 -o hypervisor /proc/cpuinfo
hypervisor
```

`unshare` created new namespaces for one command: inside the PID namespace `ps` was PID 1; the host name changed only inside the UTS namespace. The `pids` cgroup with a limit of 5 tasks let the program (task 1) create 4 children and made the other 6 `fork`s fail with `EAGAIN`: the same mechanism stops a fork bomb inside a container.

|  | Virtual machine | Container |
|:--|:--|:--|
| Isolation boundary | hypervisor + hardware virtualisation | kernel namespaces and cgroups |
| Kernel | its own guest kernel (any OS) | the host’s kernel (Linux on Linux) |
| Start-up | seconds (boot an OS) | milliseconds (start a process) |
| Size | GBs (full OS image) | MBs (application and libraries) |
| Density | tens per host | hundreds to thousands |
| Security | strong: small hypervisor interface | weaker: the whole system-call interface is shared; a kernel bug escapes |

<div class="nb nb-remark" id="remark-12-2-2">

<strong>Remark 12.2.2</strong> — The two combine: cloud containers often run inside VMs, and “micro-VMs” (Firecracker, gVisor’s sandbox kernel, Kata Containers) aim at container start-up speed with VM-strength isolation.

</div>

<div class="nb nb-moral">

A VM virtualises the hardware and runs its own kernel; a container virtualises the kernel’s view (namespaces) and budget (cgroups) for ordinary processes.

</div>
