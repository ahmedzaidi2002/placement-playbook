---
title: "1 · OS basics: kernel, modes, system calls"
linkTitle: "1 OS basics"
weight: 1
math: true
---
## 1.1 What an OS does {#os-1-1}

An operating system does three jobs: it **virtualises** the hardware (every program thinks it has the whole CPU and memory), **protects** programs from each other, and **arbitrates** shared resources (CPU time, memory, disk, devices).

<div class="nb nb-definition">

<strong>Definition</strong> — The **kernel** is the part of the OS that runs in the CPU's privileged mode and is always in memory. Everything else (shell, libraries, utilities) is an ordinary program that asks the kernel for service through **system calls**.

</div>

| Term | Meaning |
|---|---|
| **Multiprogramming** | several jobs in memory; when one waits for I/O, the CPU runs another. Goal: keep the CPU busy |
| **Time-sharing (multitasking)** | multiprogramming + a timer that switches jobs every few ms. Goal: fast response for users |
| **Multiprocessing** | more than one CPU/core running at the same time |
| **Real-time OS** | correctness includes meeting deadlines. *Hard* (airbag: a miss is failure), *soft* (video: a miss lowers quality) |
| **Spooling** | putting a slow device's jobs in a disk queue (print spooler) so the CPU and the device work at the same time |

## 1.2 User mode and kernel mode {#os-1-2}

The CPU has (at least) two privilege levels, kept as a bit in a register:

- **Kernel mode** (ring 0): can run every instruction, including **privileged** ones (I/O, disable interrupts, set the timer, change page tables).
- **User mode** (ring 3): a privileged instruction here raises an exception and the process is usually killed.

The only ways from user mode into kernel mode are a **system call**, an **exception** or an **interrupt**, and each enters the kernel at an address the kernel chose.

<div class="nb nb-remark">

<strong>Why the timer matters</strong> — Without a periodic timer interrupt, a program in an infinite loop would keep the CPU forever, because the kernel only runs when something traps into it. The timer is what makes preemptive scheduling possible, which is why setting it is privileged.

</div>

## 1.3 System calls {#os-1-3}

A **system call** is a controlled entry into the kernel. For `write(fd, buf, n)`: the library puts the call number and arguments in registers, executes a trap instruction (`syscall`), the CPU switches to kernel mode and jumps to the kernel's entry point, the kernel checks the arguments and does the work, and returns the result (or −1 and `errno`) to user mode.

Classes: process control (`fork`, `exec`, `exit`, `wait`), file management (`open`, `read`, `write`, `close`), device management (`ioctl`), information (`getpid`, `time`), communication (`pipe`, `socket`, `shmget`).

<div class="nb nb-remark">

<strong>Trap</strong> — A **mode switch is not a context switch**. A system call switches user → kernel → user mode *inside the same process*. A **context switch** replaces the running process with another. A system call that blocks (a `read` with no data yet) leads to a context switch; a quick one like `getpid` does not.

</div>

## 1.4 Interrupts, exceptions and traps {#os-1-4}

All three jump to a kernel handler through the **interrupt vector table**.

| | Cause | Synchronous? | Example |
|---|---|---|---|
| **Interrupt** | a device | no (any time) | key press, timer, disk done |
| **Fault** (exception) | the current instruction, reported *before* it completes; the instruction is **re-run** | yes | page fault |
| **Trap** (exception) | the current instruction, reported *after*; execution **continues** after it | yes | system call, breakpoint |
| **Abort** | serious error, cannot continue | yes | hardware failure |

A page fault on a valid page that is just not in memory is **not an error**: the kernel loads the page and re-runs the instruction. Only an access to an unmapped address (or a write to a read-only page) becomes a segmentation fault.

## 1.5 Booting {#os-1-5}

Power on → firmware (BIOS/UEFI) runs self-tests → loads the **boot loader** (GRUB) → the boot loader loads the kernel → the kernel initialises memory, devices and drivers, mounts the root file system → starts the first user process, **`init`/`systemd` (PID 1)** → login.

## 1.6 Kernel designs {#os-1-6}

| Design | What runs in kernel mode | Pros / cons | Examples |
|---|---|---|---|
| **Monolithic** | all services (scheduler, memory, file systems, drivers, network) in one address space | fast (plain function calls); one buggy driver can crash everything | Linux, BSD |
| **Microkernel** | only the minimum (address spaces, threads, IPC); drivers and file systems are user-space servers | isolated and robust; slower (message passing) | Mach, L4, QNX, MINIX 3 |
| **Hybrid** | a microkernel-style design with many services moved back into the kernel | in between | Windows NT, macOS (XNU) |
| **Modular** | monolithic + **loadable kernel modules** added at run time | flexible | Linux |

<div class="nb nb-moral">

The kernel is the privileged core; user programs reach it only through system calls, exceptions and interrupts. The timer interrupt is what lets the OS take the CPU back.

</div>
