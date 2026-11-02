@@ mw-iisc-21
**Answer: (a) and (b)** (shortest job next and shortest remaining time first)

**Why.** Both always pick the shortest job. If short jobs keep arriving, a long job can be postponed forever. Round robin gives every process a time slice in turn, so nobody waits forever.

**Concept: starvation and aging.** Starvation = a ready process never gets the CPU. Priority-style schedulers (SJF, SRTF, priority) can starve; the fix is aging: slowly raise the priority of processes that have waited long.

@@ qc-iisc-rr
**Answer: (c) FCFS**

**Why.** Once the time quantum is longer than every burst, no process is ever preempted; each runs to completion in arrival order, which is first-come-first-served.

**Concept: choosing the quantum.** Too large → behaves like FCFS (poor response time). Too small → too many context switches (overhead). A rule of thumb: about 80% of CPU bursts should finish within one quantum.

@@ qc-n-sched
**Answer: (d) only (I) and (II)**

**Why.** (I) Shortest process next finishes many short jobs quickly, so its throughput is high (higher than FCFS). (II) Round robin's overhead is low (just a queue), while SPN needs burst-time estimates and sorting, which can be costly. (III) FCFS never starves anyone: everyone is served in arrival order. (Stallings' comparison table.)

**Concept: scheduling criteria.** Throughput (jobs per unit time), turnaround time, waiting time, response time, fairness/starvation, and overhead. No single algorithm wins on all of them.

@@ qc25-release
**Answer: most likely (b) completion time** (the question is ambiguous)

**Why.** In real-time scheduling, "release time" means when a job becomes ready to run (its arrival), which is not an option. Question banks for this test treat "release" as the time the process leaves the system, i.e. completion time.

**Concept: scheduling times.** Arrival (release) time: enters the ready queue. Burst time: CPU time needed. Completion time: finishes. Turnaround = completion − arrival. Waiting = turnaround − burst. Response = first run − arrival.

@@ qc60-28
**Answer: (b) 18**

**Why.** Lower number = higher priority, all arrive at 0. Order: P1 (priority 2, 7), P0 (3, 7), P2 (5, 4), P3 (8, 9). P2 finishes at 7 + 7 + 4 = 18. Turnaround = completion − arrival = 18 − 0 = 18.

**Concept: non-preemptive priority scheduling.** Sort by priority; each process runs to completion. Draw a Gantt chart (a timeline) and read completion times off it.

@@ qc60-58
**Answer: (c) maintains the states of executed, executing and non-executing threads**

**Why.** In this question bank's terms, the primary scheduler picks which high-priority thread runs and assigns priorities; the secondary scheduler keeps track of thread states (the bookkeeping).

**Concept: levels of scheduling.** Long-term (job) scheduler: admits jobs into memory. Medium-term: swaps processes out and in. Short-term (CPU) scheduler: picks the next ready process to run, very frequently.

@@ qcc-os-06
**Answer: (b) long-term**

**Why.** The long-term scheduler picks jobs from the job pool on disk and admits them into memory, which controls how many programs are in memory at once (the degree of multiprogramming).

**Concept: three schedulers.** Long-term (how many processes), medium-term (who is swapped out), short-term (who runs next on the CPU).

@@ qcc-os-07
**Answer: (d) first come first serve**

**Why.** In FCFS one long CPU-bound job holds the CPU while short I/O-bound jobs pile up behind it, like cars stuck behind a slow truck. Both CPU and device utilisation drop.

**Concept: convoy effect.** Non-preemptive, arrival-order scheduling lets one long job delay many short ones. Preemption (round robin) or shortest-job-first avoids it.

@@ qcc-os-08
**Answer: (a) 11**

**Why.** Quantum 1; each round gives every unfinished process one unit, in order A, B, C, D, E.

| Time | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Runs | A | B | C | D | E | A | C | E | A | C | A |

B finishes at 2, D at 4, E at 8, A at 11; C runs alone afterwards and finishes at 16.

**Concept: round robin by hand.** Keep a queue. Run the front process for one quantum; if it is not finished, put it at the back. Write the timeline cell by cell.

@@ qcc-os-09
**Answer: (a) 3.7 units**

**Why.** Little's law: n = λ × W, where n is the average number in the queue (34), λ the arrival rate (9 per second), W the average wait. W = 34/9 ≈ 3.78, closest to 3.7.

**Concept: Little's law.** In any stable queue, average number in the system = arrival rate × average time spent. It holds regardless of the scheduling order or arrival pattern.

@@ ti-busy
**Answer: (d) all of these** (per the key; multiprogramming and spooling are the classic answers)

**Why.** Multiprogramming keeps several jobs in memory so the CPU runs one while another waits for I/O. Spooling buffers I/O on disk so devices work while the CPU computes. Preemptive scheduling helps by switching away from a process waiting on I/O.

**Concept: overlapping CPU and I/O.** I/O is slow, so a good OS always has some other work for the CPU while a device is busy.

@@ qc-iisc-livelock
**Answer: (d) livelock**

**Why.** In a livelock the processes are not blocked; they keep reacting to each other (like two people stepping aside the same way in a corridor) but make no progress.

**Concept: deadlock vs livelock vs starvation.** Deadlock: processes wait forever for each other, doing nothing. Livelock: processes keep changing state but achieve nothing. Starvation: one process never gets a resource while others proceed.

@@ qc60-55
**Answer: (d) (I), (II), (IV), (III), (V)**

**Why.** Detection starts by initialising the work (temporary) vector to the available resources. Then repeatedly find an unmarked process whose request can be met; if found, add its allocation back to work (it can finish and release resources); if none is found, stop. Processes left unmarked are deadlocked. Only option (d) starts with initialisation.

**Concept: deadlock detection.** Like the banker's safety check, but with current requests instead of maximum needs: pretend each satisfiable process finishes and returns its resources; whoever can never finish is deadlocked.

@@ qcc-os-22
**Answer: (c) all three**

**Why.** The textbook strategies: prevent or avoid deadlocks (I), let them happen then detect and recover (II), or ignore them (III, the "ostrich algorithm"), which most general-purpose systems such as Linux and Windows do.

**Concept: deadlock strategies.** Prevention breaks a necessary condition; avoidance checks each request (banker's algorithm); detection finds cycles and kills or rolls back processes; ignoring is cheap when deadlocks are rare.

@@ qcc-os-23
**Answer: (a) only (I)**

**Why.** Avoidance (e.g. the banker's algorithm) grants a request only if the resulting state is safe. Otherwise the process waits, even though the resource is free right now.

**Concept: safe state.** A state is safe if there is some order in which every process can get its maximum need and finish. Unsafe does not mean deadlocked yet, but deadlock becomes possible, so avoidance never enters it.

@@ qcc-os-24
**Answer: (d) a deadlock may arise**

**Why.** Without prevention or avoidance nothing rules deadlock out, but it is not guaranteed either. If one happens, the system needs detection and recovery.

**Concept: necessary conditions are not certainty.** Deadlock needs all four Coffman conditions; their being possible does not mean they will line up.

@@ qcc-os-25
**Answer: (d) the OS can decide whether the process should wait for each request**

**Why.** Knowing future requests in advance is exactly what deadlock avoidance needs: for each request, the OS checks whether granting it keeps the system safe, and makes the process wait if not.

**Concept: avoidance needs advance information.** The banker's algorithm requires each process to declare its maximum need up front.

@@ ti-circular-wait
**Answer: A true, B false**

**Why.** Circular wait is one of the four conditions that must all hold for deadlock, so it is necessary. It is not sufficient alone: if a resource has several instances, or can be preempted, a cycle in the wait graph need not be a deadlock.

**Concept: the Coffman conditions.** Mutual exclusion, hold and wait, no preemption, circular wait. Deadlock is possible only if all four hold; breaking any one prevents it.

@@ ti-deadlock
**Answer: (a) both true** (many keys say "A false, B true", because preemption is impractical for resources like printers)

**Why.** Deadlock needs all four Coffman conditions, so removing any one of them, including "no preemption" (A) or "circular wait" (B), prevents deadlock in principle.

**Concept: prevention techniques.** Break hold-and-wait (request everything at once), allow preemption (take resources away), or break circular wait (number resources and request them in increasing order, the most practical).

@@ qcc-os-12
**Answer: no reliable pick** (the time per cylinder and the disk size are cut off in the photo)

**Why.** The service order is clear. Moving up from 30, C-SCAN serves 45, 55, 66, 67, 69, 77, 95, 112, 180, then jumps back to the low end and serves 10 and 22.
- Counting only cylinders crossed while serving: 30 → 180 = 150, wrap 180 → 10 = 170, 10 → 22 = 12, total 332; at 3 ms per cylinder that is 996 ms (option (c)).
- If the head runs to the last cylinder (199) and the return to 0 counts: 169 + 199 + 22 = 390 cylinders.

**Concept: C-SCAN disk scheduling.** The head sweeps in one direction serving requests, then returns to the other end without serving on the way back, and sweeps again. It gives more uniform waiting times than SCAN, which serves in both directions.

@@ devrev-q3
**Answer: (b) heap**

**Why.** `malloc`/`new` carve blocks out of the heap. The stack holds call frames and local variables; the data segment holds initialised globals and statics; virtual memory is the whole address-space mechanism.

**Concept: process memory layout.** From low to high addresses: text (code), data (initialised globals), bss (zero-initialised globals), heap (grows up), ..., stack (grows down).

@@ mw-iisc-22
**Answer: (a) and (b)**

**Why.** Thrashing happens when processes don't have enough frames for their working sets and spend their time paging. Running fewer processes (a) or adding RAM (b) gives each process room. Smaller pages do not fix a shortage of memory.

**Concept: thrashing.** CPU utilisation collapses because the CPU waits on page faults. The OS sees low CPU use and admits more processes, making it worse. Cure: reduce multiprogramming, using the working-set model or page-fault-frequency control.

@@ or-virtual
**Answer: (a) the address does not map directly to the physical memory cell with that number**

**Why.** A virtual address is translated by the MMU through page tables to some physical frame, which can be anywhere, or the page may not be in RAM at all (it may be on disk).

**Concept: virtual memory.** Each process sees its own large, private address space. The OS and hardware map pages of it to physical frames on demand. Benefits: isolation, programs larger than RAM, easy sharing.

@@ qc-n-frames
**Answer: (a) 19 frames for P1 and 36 for P2** (most likely; P2's page count is cut off)

**Why.** Proportional allocation gives each process frames in proportion to its size: aᵢ = (sᵢ / S) × m. Option (a) fits P2 having 32 pages: 55 × 17/49 ≈ 19.1 and 55 × 32/49 ≈ 35.9. (b) does not use all 55 frames.

**Concept: frame allocation.** Equal allocation splits frames evenly; proportional allocation gives bigger processes more. Priority-based allocation weights by priority instead of size.

@@ qc25-page-stealing
**Answer: (c) it takes page frames away to make space for newer pages**

**Why.** Page stealing takes frames (often from other processes) when memory is needed. Frequent stealing is a sign of memory pressure, not efficiency.

**Concept: page replacement.** When no frame is free, the OS picks a victim page (by LRU, clock, etc.), writes it to disk if dirty, and reuses its frame.

@@ qc60-22
**Answer: no reliable pick** (the key cannot be derived; the nearest listed option is (a) 136K)

**Why.** A buddy allocator rounds each request up to a power of two: P2 99K → 128K (29K wasted), P4 119K → 128K (9K), P1 201K → 256K (55K), P5 91K → 128K (37K). Total internal fragmentation before P1 leaves is 130K; after P1 leaves, 75K. Neither matches an option.

**Concept: buddy system.** Memory is split into halves repeatedly until a block just big enough (a power of two) is found. Freed blocks merge with their "buddy" if it is also free. Rounding up causes internal fragmentation.

@@ qc60-60
**Answer: (a) segmentation fault for both addresses**

**Why.** A segment's offset must be smaller than its length. (I) segment 0: offset 402 ≥ length 245 → fault. (II) segment 2: offset 25 ≥ length 23 → fault. (Otherwise the physical address would be base + offset.)

**Concept: segmentation.** A logical address is (segment, offset). The hardware checks offset < limit (length); if it passes, physical = base + offset; if not, it traps (segmentation fault).

@@ qcc-os-13
**Answer: (d) only (II) and (III)**

**Why.** Dynamic (variable) partitioning gives each process exactly the size it needs, so partitions differ in size and number (III). As processes leave, free gaps ("holes") appear between allocated blocks (II): external fragmentation. Fixed-length partitions (I) describe static partitioning.

**Concept: fixed vs variable partitions.** Fixed partitions waste space inside blocks (internal fragmentation). Variable partitions waste space between blocks (external fragmentation), fixed by compaction or paging.

@@ qcc-os-14
**Answer: (d) they can be caused by repeated allocation and deallocation**

**Why.** Allocating and freeing blocks of different sizes over time leaves scattered gaps that are too small to use. It is not limited to the heap (physical memory fragments too), and malloc vs calloc only differ in zero-filling.

**Concept: fragmentation.** External: free memory is split into small pieces. Internal: allocated blocks are larger than requested. Pools of fixed-size blocks avoid external fragmentation.

@@ qcc-os-15
**Answer: (b) only (II)** is not true

**Why.** In OS terms, "memory management" means managing main (primary) memory: allocation, protection, paging, swapping. Secondary storage is handled by file-system and disk management. (Swapping moves pages to disk, but what is managed is still main memory.)

**Concept: OS subsystems.** Process management, memory management (RAM), file systems and storage management (disks), I/O management (devices).

@@ qcc-os-16
**Answer: (c) high**

**Why.** A high page-fault rate means the process has too few frames for its working set, so the OS should give it more. A very low rate means some frames can be taken away.

**Concept: page-fault-frequency control.** Set an upper and lower bound on the fault rate: above the upper bound add frames; below the lower bound remove frames.

@@ ti-ext-frag
**Answer: external fragmentation**

**Why.** The free memory exists (50 + 150 + 250 = 450) but is split into separate holes between partitions; a request larger than 250 cannot be met even though the total is enough.

**Concept: external fragmentation.** Free space is outside allocated blocks but scattered. Compaction (moving blocks together) or paging solves it.

@@ ti-first-fit
**Answer: both internal and external fragmentation**

**Why.** First fit: 70 → 120 (50 wasted inside), 90 → 200 (110 wasted), 50 → 80 (30 wasted): internal fragmentation. 130 cannot be placed, although 60 + 50 + 110 + 30 free space exists in total, just not in one block: external fragmentation.

**Concept: first fit.** Put each request in the first block large enough. Fast, but leaves leftovers in fixed blocks (internal) and can strand total free space in pieces (external).

@@ ti-partitions
**Answer: no option matches the textbook definitions** (the candidate chose 1:1)

**Why.** First fit places the three 200 processes in the 600, 200 and 500 partitions, wasting 400 + 0 + 300 = 700 inside them (internal). The 100 partition stays free; whether it counts as "external" fragmentation depends on the definition, and no ratio in the options follows cleanly.

**Concept: fixed-partition fragmentation.** With fixed partitions, unused space inside an allocated partition is internal fragmentation; a whole free partition too small for any waiting process is usually called external.

@@ dpworld-process-thread
**Answer.** A **process** is a program in execution with its own address space (code, data, heap, stack), open files and other resources, described by a process control block. A **thread** is a unit of execution inside a process: threads of one process share the address space, heap, globals and open files, but each has its own stack, registers and program counter.

**Key differences.**
- Creating and switching threads is cheaper: no new address space or TLB flush.
- Threads communicate through shared memory directly (needs mutexes); processes need IPC (pipes, sockets, shared memory segments).
- A crash in one thread can bring down the whole process; processes are isolated.

**Concept: isolation vs sharing.** Processes trade efficiency for safety; threads trade safety for efficiency. Use processes for isolation (browser tabs), threads for cheap parallelism inside one task.

@@ maq-q31
**Answer: (b) 1, 2 and 3**

**Why.** When a switch involves swapping, its cost is dominated by the transfer. Less memory to move (1), a faster disk (2) and overlapping the transfer with execution (3) all reduce it; (4) makes it worse. (Some keys give (a), treating faster hardware as outside the question.)

**Concept: context-switch cost.** Saving and loading registers is quick; the expensive parts are cache/TLB disruption and, if memory must be swapped, disk transfer.

@@ mw-iiitd-10
**Answer: (c) 8 printf calls** (the intended count; in practice 10 stars may appear, see below)

**Why.** The first fork gives 2 processes; each prints one star (2). The second fork doubles them to 4; the 2 new children print one star each (2). All 4 print the final star (4). 2 + 2 + 4 = 8. On a real system the first star is still in the unflushed stdout buffer when the second fork copies the process, so the copied buffer prints it again and 10 stars appear.

**Concept: fork duplicates everything.** After `fork()`, parent and child continue from the same point with copies of all memory, including stdio buffers. n sequential forks give 2ⁿ processes. Call `fflush(stdout)` before forking to avoid duplicated output.

@@ mw-iisc-11
**Answer: (a) once**

**Why.** `system()` forks one child, which `exec`s `/bin/sh -c "command"`, and the parent waits for it.

**Concept: fork + exec.** Unix creates new programs in two steps: fork copies the current process, exec replaces the copy's program with a new one.

@@ mw-iisc-12
**Answer: (b) 2 and 3**

**Why.** A zombie is a process that has already terminated but whose parent has not yet collected its exit status with `wait()` (3). It is already dead, so no signal, not even SIGKILL, can kill it (1 false). The parent's `wait()` removes it (2), or, if the parent dies, init adopts and reaps it.

**Concept: zombie vs orphan.** Zombie: child dead, parent alive but not waiting; only a process-table entry remains. Orphan: parent dead, child still running; init/systemd adopts it.

@@ mw-iisc-8
**Answer: (a) and (b)** (SIGTERM and SIGKILL)

**Why.** SIGTERM politely asks a process to terminate (it can clean up or handle it). SIGKILL cannot be caught or ignored. SIGSEGV reports a memory fault and SIGINT is Ctrl-C; both end a process by default but are not the tools for terminating one deliberately.

**Concept: signals.** Asynchronous notifications to a process. Most can be handled or ignored; SIGKILL and SIGSTOP cannot. Good practice: send SIGTERM first, SIGKILL only if it doesn't exit.

@@ or-pcb
**Answer: (b) process control block**

**Why.** The PCB holds everything the OS needs about a process: PID, state, saved registers and program counter, scheduling info, memory-management info, open files and I/O status.

**Concept: the PCB and context switches.** On a switch, the OS saves the running process's CPU state into its PCB and loads the next process's state from its PCB.

@@ qc60-32
**Answer: (c) assembler**

**Why.** An assembler translates assembly language into machine-code object files. A compiler works on high-level languages; a linker combines object files; a macro processor expands macros.

**Concept: the build chain.** Source → (preprocessor) → compiler → assembly → assembler → object file → linker → executable → loader puts it in memory.

@@ qcc-os-01
**Answer: (a) running state**

**Why.** Only the process holding the CPU executes instructions. Ready processes wait for the CPU; waiting (blocked) processes wait for an event such as I/O.

**Concept: process states.** New → Ready → Running → (Waiting → Ready) → Terminated. Running → Ready happens on preemption; Running → Waiting on I/O or a lock.

@@ qcc-os-02
**Answer: (c) terminated**

**Why.** After its last instruction or `exit()`, a process enters the terminated state, where it stays until the parent collects its exit status.

**Concept: process lifecycle** (see the state diagram above).

@@ qcc-os-03
**Answer: (b) uninitialised data segment**

**Why.** The bss (block started by symbol) holds globals and statics with no explicit initialiser. The loader fills it with zeros, so it takes no space in the executable file. Initialised globals go in the data segment.

**Concept: why bss saves space.** The file only records the bss size, not its contents, because all of it is zero.

@@ qcc-os-04
**Answer: (c) both (I) and (II)**

**Why.** Accounting information (CPU time used, limits) and I/O status (open files, devices) both live in the PCB, which is preserved across a context switch along with the registers, program counter, scheduling and memory information.

**Concept: PCB contents.** State, PC, registers, scheduling info, memory-management info, accounting info, I/O status.

@@ qcc-os-05
**Answer: (c) st1 < st2**

**Why.** A mode switch only changes the privilege level and stack within the same process. A process switch includes a mode switch **and** saving one PCB, restoring another, changing the address space, and losing TLB and cache warmth, so it always costs more.

**Concept: mode switch vs context switch.** A system call is a mode switch (user → kernel → user), not necessarily a context switch. Context switches are much more expensive.

@@ qcc-os-17
**Answer: (c) only (II)**

**Why.** Shared memory is set up with calls such as `shmget`/`shmat` or `mmap`, which map a common region into each process's address space; after that, plain loads and stores are used. Message passing goes through `send`/`receive` system calls instead.

**Concept: two IPC models.** Shared memory: fast (no kernel involvement per access) but needs synchronisation. Message passing: simpler and safer, works across machines, but each message costs a system call.

@@ qcc-os-18
**Answer: (b) only (II)**

**Why.** (I) is false: a socket is exactly the endpoint through which two processes, possibly on different machines, communicate. (II) describes their use in distributed applications (loosely worded, but intended as true).

**Concept: sockets.** An endpoint identified by (IP address, port, protocol). TCP sockets give reliable ordered byte streams; UDP sockets give unreliable datagrams.

@@ ti-process-state
**Answer: (a) blocked to running**

**Why.** When the awaited event happens, a blocked process becomes ready; it must then be picked by the scheduler to run. It never goes straight from blocked to running.

**Concept: legal transitions.** Ready ↔ Running (dispatch / preempt), Running → Blocked (wait), Blocked → Ready (event done), Running → Terminated.

@@ nv-12
**Answer: (b) 9**

**Why.** Each wait (P) decrements and each signal (V) increments: S − 10 + 7 = 6 → S = 9.

**Concept: counting semaphores.** The value counts available resources (or, if negative in some implementations, waiting processes). wait: S−−, block if no resource; signal: S++, wake a waiter.

@@ nv-17
**Answer: (a) 18**

**Why.** 7 − 20 + s = 5 → s = 18.

**Concept: semaphore arithmetic.** Final value = initial − waits + signals (assuming the waits eventually completed).

@@ qc-iisc-rtos
**Answer: (a) semaphores** (the ticked answer; "negative synchronisation" is not standard terminology)

**Why.** Read it as "make a task wait until another task signals it". A semaphore's wait/signal pair does exactly that: the waiting task blocks until the signal arrives.

**Concept: RTOS synchronisation tools.** Semaphores (signalling and counting), mutexes (mutual exclusion with priority inheritance), event flags (wait for combinations of events), message queues (pass data).

@@ qc-n-hwcs
**Answer: (a) only (I) and (II)**

**Why.** Test-and-set and compare-and-swap are atomic hardware instructions. Peterson's solution uses only ordinary loads and stores, so it is a software solution.

**Concept: atomic instructions.** The hardware guarantees the read-modify-write happens as one indivisible step, which makes simple spinlocks possible: `while (test_and_set(&lock)) ;`.

@@ qcc-os-19
**Answer: (b) bounded buffer**

**Why.** The bounded-buffer (producer–consumer) problem is a classic concurrency-control problem: producers wait when the buffer is full, consumers when it is empty, and the buffer needs mutual exclusion.

**Concept: producer–consumer with semaphores.** `empty` (counts free slots, starts at n), `full` (counts filled slots, starts at 0) and `mutex` (starts at 1). Producer: wait(empty), wait(mutex), add, signal(mutex), signal(full). Consumer does the mirror.

@@ qcc-os-21
**Answer: it satisfies all three requirements**: mutual exclusion, progress and bounded waiting.

**Why.**
- Mutual exclusion: a process enters only when `key` becomes false (it won the lock) or when the leaving process sets its `waiting[i]` to false, and only one of those can happen at a time.
- Progress: a leaving process either hands entry to a waiting process or releases the lock.
- Bounded waiting: the leaving process scans `waiting[]` in cyclic order from i + 1, so any waiting process gets in within n − 1 turns.

**Concept: the three critical-section requirements.** Mutual exclusion (one at a time), progress (if nobody is inside, someone who wants in gets in), bounded waiting (no one waits forever). Plain test-and-set gives only the first two; this version adds bounded waiting.

@@ mw-iisc-14
**Answer: (d) terminals**

**Why.** A terminal transfers a stream of characters with no seeking. Hard disks and USB flash drives are block devices (fixed-size blocks, random access). (A webcam is also exposed as a character device on Linux, but the textbook answer is the terminal.)

**Concept: character vs block devices.** Character devices: byte streams, no buffering cache (keyboards, serial ports, terminals). Block devices: addressable blocks, cached, hold file systems (disks, SSDs).

@@ or-hosts
**Answer: (d) it holds hostname (FQDN) to IP address mappings**

**Why.** `/etc/hosts` gives static name-to-address mappings, checked before (or instead of) DNS. Users are in `/etc/passwd`.

**Concept: name resolution order.** Linux consults `/etc/nsswitch.conf`, usually "files dns": first `/etc/hosts`, then DNS servers from `/etc/resolv.conf`.

@@ qcc-os-26
**Answer: (d) all of (I), (II) and (III)**

**Why.** A distribution ("distro") bundles the Linux kernel with a collection of software (GNU tools, libraries, desktop) and a package manager such as apt, dnf or pacman.

**Concept: kernel vs distribution.** Linux strictly is the kernel. Ubuntu, Fedora, Arch are distributions: the kernel plus everything needed to make a usable system.
