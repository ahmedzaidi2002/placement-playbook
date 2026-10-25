---
title: "2 · Processes"
linkTitle: "2 Processes"
weight: 2
math: true
---
## 2.1 Program, process, PCB {#os-2-1}

<div class="nb nb-definition">

<strong>Definition</strong> — A **program** is a passive file on disk. A **process** is a program in execution: its own address space (code, data, heap, stack), its CPU state (registers, program counter) and the resources it holds (open files). One program run twice = two processes.

</div>

**Memory layout of a process** (low to high address): **text** (code) → **data** (initialised globals/statics) → **BSS** (uninitialised globals) → **heap** (grows up; `malloc`/`new`) → … → **stack** (grows down; local variables, return addresses).

<div class="nb nb-remark">

<strong>OA</strong> — "The area used as a pool for dynamic memory allocation" is the **heap**. Local variables live on the **stack**; globals and statics in the **data** segment.

</div>

The kernel keeps everything about a process in its **process control block (PCB)**: PID and parent PID, state, saved registers and program counter, scheduling info (priority, CPU time used), memory-management info (page-table pointer), open-file table, and accounting data.

## 2.2 Process states {#os-2-2}

**New → Ready → Running → (Blocked/Waiting → Ready) → Terminated.**

- **Running → Ready:** preempted (timer expired).
- **Running → Blocked:** waits for an event (I/O, lock).
- **Blocked → Ready:** the event happened.
- **Ready → Running:** the scheduler dispatched it.

<div class="nb nb-remark">

<strong>Trap: impossible transitions</strong> — **Blocked → Running** (it must go through Ready first), **Ready → Blocked** (only a running process can make the call that blocks it), and **New → Running**.

</div>

**Schedulers:** the **long-term** scheduler admits jobs into memory (controls the *degree of multiprogramming*); the **medium-term** scheduler swaps processes out to disk and back (suspended states); the **short-term** (CPU) scheduler picks the next ready process every few milliseconds. The **dispatcher** does the actual switch; the time it takes is the **dispatch latency**.

## 2.3 Context switch {#os-2-3}

Switching from process A to B: save A's registers and program counter in A's PCB, load B's from B's PCB, switch the page table (memory map), and resume B. It is pure overhead.

The hidden cost is bigger than the copying: B's data is not in the caches and the TLB is flushed. Things that **reduce** context-switch time: multiple hardware register sets, using **threads** instead of processes (no address-space switch), and tagged TLBs.

## 2.4 `fork`, `exec`, `wait` {#os-2-4}

- `fork()` creates a **child** that is a copy of the parent. It **returns twice**: 0 in the child, the child's PID in the parent (−1 on failure).
- `exec()` replaces the process's program with a new one (same PID); it returns only on failure.
- `wait()` makes the parent block until a child finishes and collects its exit status.

A shell runs a command with exactly this: `fork`, then `exec` in the child, `wait` in the parent.

<div class="nb nb-theorem nb-block">

<strong>Counting rule</strong>

If every process runs the same $n$ `fork()` calls, there are $2^n$ processes at the end, $2^n - 1$ of them newly created. A statement after the $k$-th fork runs $2^k$ times.

</div>

<div class="nb nb-example">

<strong>Example</strong> (fork counting)

- `fork(); fork(); fork(); printf("hi\n");` → 8 processes, "hi" printed **8** times, 7 children created.
- `for (i = 0; i < 3; i++) { fork(); printf("x\n"); }` → after iteration $i$ there are $2^{i+1}$ processes, each printing once: $2 + 4 + 8 = $ **14** prints.
- `if (fork() && fork()) fork();` → draw the tree: the parent's first fork makes child A (A gets 0, so `&&` stops). The parent's second fork makes B (B gets 0, stops). The parent (both non-zero) runs the third fork, making C. Total **4** processes.

</div>

<div class="nb nb-remark">

<strong>Trap: buffered output</strong> — `printf("*")` **without** `\n` stays in the stdio buffer, and `fork` copies the buffer, so the star can be printed more times than the number of `printf` calls. If every `printf` ends with `\n` (and output is to a terminal), count calls.

</div>

## 2.5 Zombies and orphans {#os-2-5}

- **Zombie:** a child that has **terminated** but whose parent has not called `wait` yet. Its memory is freed; only its PCB entry (PID, exit status) remains. Fix: the parent calls `wait`/`waitpid` (or handles `SIGCHLD`). `kill -9` does nothing to a zombie: it is already dead.
- **Orphan:** a child that is **still running** after its parent died. It is adopted by `init` (PID 1), which reaps it later. Orphans are normal; un-reaped zombies are the bug (they use up PIDs).

## 2.6 Signals, in brief {#os-2-6}

A **signal** is an asynchronous notification to a process: `SIGINT` (Ctrl-C), `SIGTERM` (polite "please terminate", catchable; the default of `kill PID`), `SIGKILL` (9, cannot be caught or ignored), `SIGSEGV` (bad memory access), `SIGCHLD` (a child stopped or died). The right way to stop a process: `SIGTERM` first, `SIGKILL` if it does not exit.

## 2.7 Inter-process communication {#os-2-7}

Processes are isolated, so they talk through the kernel:

| Model | How | Pros / cons |
|---|---|---|
| **Shared memory** | the kernel maps the same memory into both processes; then plain reads/writes | **fastest** (no system call per message); needs explicit synchronisation |
| **Message passing** | each message goes through a system call: **pipes**, FIFOs (named pipes), message queues, **sockets** | slower; synchronisation built in; works across machines (sockets) |

A **pipe** (`ls | wc -l`) is a one-way byte stream with a kernel buffer: the reader blocks when it is empty, the writer when it is full; the reader sees end-of-file only when every write end is closed.

<div class="nb nb-moral">

Zombie = dead but not reaped (fix: `wait`); orphan = alive but parent dead (adopted by `init`). Count forks with $2^n$ only when every process runs every fork; otherwise draw the tree.

</div>
