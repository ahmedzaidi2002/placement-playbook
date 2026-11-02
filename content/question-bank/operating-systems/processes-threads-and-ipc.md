---
title: "Processes, threads and IPC"
weight: 1
---

16 questions asked by DP World, MAQ Software, MathWorks, Oracle, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · process versus thread

*Asked by: DP World (Interview rounds)*

Explain the difference between a process and a thread.

{{< details title="Answer and explanation" closed="true" >}}

**Answer.** A **process** is a program in execution with its own address space (code, data, heap, stack), open files and other resources, described by a process control block. A **thread** is a unit of execution inside a process: threads of one process share the address space, heap, globals and open files, but each has its own stack, registers and program counter.

**Key differences.**
- Creating and switching threads is cheaper: no new address space or TLB flush.
- Threads communicate through shared memory directly (needs mutexes); processes need IPC (pipes, sockets, shared memory segments).
- A crash in one thread can bring down the whole process; processes are isolated.

**Concept: isolation vs sharing.** Processes trade efficiency for safety; threads trade safety for efficiency. Use processes for isolation (browser tabs), threads for cheap parallelism inside one task.

{{< /details >}}

### 2 · Q31, reducing context-switch time

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

In an operating system, which of the following reduces the context-switch time?
(1) Minimise the amount of memory of a process to be swapped. (2) Increase the speed of the
disk used for swapped-out processes. (3) Overlap swapping and program execution.
(4) Maximise the amount of memory of a process to be swapped.

- **(a)** 1 and 3
- **(b)** 1, 2, and 3
- **(c)** 2 and 4
- **(d)** 2, 3, and 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1, 2 and 3**

**Why.** When a switch involves swapping, its cost is dominated by the transfer. Less memory to move (1), a faster disk (2) and overlapping the transfer with execution (3) all reduce it; (4) makes it worse. (Some keys give (a), treating faster hardware as outside the question.)

**Concept: context-switch cost.** Saving and loading registers is quick; the expensive parts are cache/TLB disruption and, if memory must be swapped, disk transfer.

{{< /details >}}

### 3 · Q10, fork and printf

*Asked by: MathWorks (IIIT Delhi 2024); MathWorks (NIT Delhi 2024)*

How many times will `*` be printed?

```c
main() {
    if (fork() >= 0) {
        printf("*");
        if (fork() == 0) {
            printf("*");
        }
    } else {
        // do nothing
    }
    printf("*");
}
```

- **(a)** 7
- **(b)** 5
- **(c)** 8
- **(d)** 10

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 8 printf calls** (the intended count; in practice 10 stars may appear, see below)

**Why.** The first fork gives 2 processes; each prints one star (2). The second fork doubles them to 4; the 2 new children print one star each (2). All 4 print the final star (4). 2 + 2 + 4 = 8. On a real system the first star is still in the unflushed stdout buffer when the second fork copies the process, so the copied buffer prints it again and 10 stars appear.

**Concept: fork duplicates everything.** After `fork()`, parent and child continue from the same point with copies of all memory, including stdio buffers. n sequential forks give 2ⁿ processes. Call `fflush(stdout)` before forking to avoid duplicated output.

{{< /details >}}

### 4 · Q11, system()

*Asked by: MathWorks (IISc 2024)*

How many times is `fork` called inside `system()`?

- **(a)** 1
- **(b)** 2
- **(c)** It is not called
- **(d)** 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) once**

**Why.** `system()` forks one child, which `exec`s `/bin/sh -c "command"`, and the parent waits for it.

**Concept: fork + exec.** Unix creates new programs in two steps: fork copies the current process, exec replaces the copy's program with a new one.

{{< /details >}}

### 5 · Q12, zombies

*Asked by: MathWorks (IISc 2024)*

Which are true of zombie processes? (1) They are killed by SIGKILL. (2) They are removed
by `wait()`. (3) One is created when a child terminates before its parent waits for it.

- **(a)** All
- **(b)** 2 and 3
- **(c)** 1 and 2
- **(d)** 1 and 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 2 and 3**

**Why.** A zombie is a process that has already terminated but whose parent has not yet collected its exit status with `wait()` (3). It is already dead, so no signal, not even SIGKILL, can kill it (1 false). The parent's `wait()` removes it (2), or, if the parent dies, init adopts and reaps it.

**Concept: zombie vs orphan.** Zombie: child dead, parent alive but not waiting; only a process-table entry remains. Orphan: parent dead, child still running; init/systemd adopts it.

{{< /details >}}

### 6 · Q8, terminating signals

*Asked by: MathWorks (IISc 2024)*

Which signals are best suited to terminate a process? (more than one answer)

- **(a)** SIGTERM
- **(b)** SIGKILL
- **(c)** SIGSEGV
- **(d)** SIGINT

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) and (b)** (SIGTERM and SIGKILL)

**Why.** SIGTERM politely asks a process to terminate (it can clean up or handle it). SIGKILL cannot be caught or ignored. SIGSEGV reports a memory fault and SIGINT is Ctrl-C; both end a process by default but are not the tools for terminating one deliberately.

**Concept: signals.** Asynchronous notifications to a process. Most can be handled or ignored; SIGKILL and SIGSTOP cannot. Good practice: send SIGTERM first, SIGKILL only if it doesn't exit.

{{< /details >}}

### 7 · process information

*Asked by: Oracle (HackerRank MCQ test)*

The operating system maintains the information about a process in which of the following?

- **(a)** Heap
- **(b)** Process Control Block
- **(c)** Stack
- **(d)** TLB Cache

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) process control block**

**Why.** The PCB holds everything the OS needs about a process: PID, state, saved registers and program counter, scheduling info, memory-management info, open files and I/O status.

**Concept: the PCB and context switches.** On a switch, the OS saves the running process's CPU state into its PCB and loads the next process's state from its PCB.

{{< /details >}}

### 8 · OS Fundamentals

*Asked by: Qualcomm (60-question online assessment)*

Which of the program given in options helps in converting the assembly language programs to an object program?

- **(a)** Macroprocessor
- **(b)** Linker
- **(c)** Assembler
- **(d)** Compiler

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) assembler**

**Why.** An assembler translates assembly language into machine-code object files. A compiler works on high-level languages; a linker combines object files; a macro processor expands macros.

**Concept: the build chain.** Source → (preprocessor) → compiler → assembly → assembler → object file → linker → executable → loader puts it in memory.

{{< /details >}}

### 9 · Processes

*Asked by: Qualcomm (NIT Durgapur, Q39)*

In which of the process states given in the options are process instructions executed?

- **(a)** Running state
- **(b)** Terminated state
- **(c)** Waiting state
- **(d)** Ready state

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) running state**

**Why.** Only the process holding the CPU executes instructions. Ready processes wait for the CPU; waiting (blocked) processes wait for an event such as I/O.

**Concept: process states.** New → Ready → Running → (Waiting → Ready) → Terminated. Running → Ready happens on preemption; Running → Waiting on I/O or a lock.

{{< /details >}}

### 10 · Processes

*Asked by: Qualcomm (NIT Durgapur, Q30)*

If a process has finished its execution, what is the state of that process?

- **(a)** Waiting
- **(b)** Ready
- **(c)** Terminated
- **(d)** Running

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) terminated**

**Why.** After its last instruction or `exit()`, a process enters the terminated state, where it stays until the parent collects its exit status.

**Concept: process lifecycle** (see the state diagram above).

{{< /details >}}

### 11 · Processes

*Asked by: Qualcomm (BITS Goa 2024, Q39)*

Which section of the process memory layout is also called the **bss** segment?

- **(a)** Stack
- **(b)** Uninitialized data segment
- **(c)** Initialized data segment
- **(d)** Code segment

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) uninitialised data segment**

**Why.** The bss (block started by symbol) holds globals and statics with no explicit initialiser. The loader fills it with zeros, so it takes no space in the executable file. Initialised globals go in the data segment.

**Concept: why bss saves space.** The file only records the bss size, not its contents, because all of it is zero.

{{< /details >}}

### 12 · Processes

*Asked by: Qualcomm (BITS Hyderabad 2024, Q33)*

During a context switch, which of the following information is stored for later use?

I. Accounting information  
II. I/O status information

- **(a)** Only (II)
- **(b)** Neither (I) nor (II)
- **(c)** Both (I) and (II)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) both (I) and (II)**

**Why.** Accounting information (CPU time used, limits) and I/O status (open files, devices) both live in the PCB, which is preserved across a context switch along with the registers, program counter, scheduling and memory information.

**Concept: PCB contents.** State, PC, registers, scheduling info, memory-management info, accounting info, I/O status.

{{< /details >}}

### 13 · Processes

*Asked by: Qualcomm (BITS Hyderabad 2025, Q39)*

Let *st1* be the time to switch between user mode and kernel mode, and *st2* the time to switch between two user processes. Which is true?

- **(a)** Indeterminate
- **(b)** st1 > st2
- **(c)** st1 < st2
- **(d)** st1 = st2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) st1 < st2**

**Why.** A mode switch only changes the privilege level and stack within the same process. A process switch includes a mode switch **and** saving one PCB, restoring another, changing the address space, and losing TLB and cache warmth, so it always costs more.

**Concept: mode switch vs context switch.** A system call is a mode switch (user → kernel → user), not necessarily a context switch. Context switches are much more expensive.

{{< /details >}}

### 14 · Inter-process communication

*Asked by: Qualcomm (IIIT Delhi 2025, Q34)*

Consider the IPC models I) Message passing and II) Shared memory. Which model(s) use map-memory system calls to access memory?

- **(a)** Neither (I) nor (II)
- **(b)** Only (I)
- **(c)** Only (II)
- **(d)** Both (I) and (II)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) only (II)**

**Why.** Shared memory is set up with calls such as `shmget`/`shmat` or `mmap`, which map a common region into each process's address space; after that, plain loads and stores are used. Message passing goes through `send`/`receive` system calls instead.

**Concept: two IPC models.** Shared memory: fast (no kernel involvement per access) but needs synchronisation. Message passing: simpler and safer, works across machines, but each message costs a system call.

{{< /details >}}

### 15 · Inter-process communication

*Asked by: Qualcomm (NIT Durgapur)*

Which of the following statements about sockets is/are true?

I. Sockets do not create connections between machines or processes to facilitate communication over a network.  
II. In a distributed application, sockets offer dependable, asynchronous communication between parts operating on various machines.

- **(a)** None
- **(b)** Only ii
- **(c)** Both i and ii
- **(d)** Only i

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) only (II)**

**Why.** (I) is false: a socket is exactly the endpoint through which two processes, possibly on different machines, communicate. (II) describes their use in distributed applications (loosely worded, but intended as true).

**Concept: sockets.** An endpoint identified by (IP address, port, protocol). TCP sockets give reliable ordered byte streams; UDP sockets give unreliable datagrams.

{{< /details >}}

### 16 · process states

*Asked by: Texas Instruments (IISc, second set)*

Which transition is not possible?

- **(a)** Blocked to Running
- **(b)** Ready to Running
- **(c)** Blocked to Ready
- **(d)** Running to Blocked

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) blocked to running**

**Why.** When the awaited event happens, a blocked process becomes ready; it must then be picked by the scheduler to run. It never goes straight from blocked to running.

**Concept: legal transitions.** Ready ↔ Running (dispatch / preempt), Running → Blocked (wait), Blocked → Ready (event done), Running → Terminated.

{{< /details >}}
