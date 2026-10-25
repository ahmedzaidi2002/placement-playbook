---
title: "14 · Interview rapid-fire"
linkTitle: "14 Interview rapid-fire"
weight: 14
math: true
---
## 14.1 Short answers to the questions that keep coming {#sec-os-rapid}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “What is the difference between a process and a thread?”, answered in two lines.</em>

</div>

Each answer is what a strong candidate says out loud in the first thirty seconds; the chapter in brackets has the depth for the follow-ups.

### 14.1.i Kernel, system calls, processes {#s14-1-i}

1. <strong>What is a system call, and how is it different from a function call?</strong><br>A controlled entry into the kernel: number in a register, a trap instruction, a kernel-chosen entry point, validated arguments. It switches privilege mode and costs about 100 ns here versus about 1 ns for a call ([Section 1.3](../01-kernel/#sec-os-syscalls)).
2. <strong>Is `printf` a system call? `malloc`?</strong><br>No and no: library functions. `printf` eventually calls `write`; `malloc` calls `brk`/`mmap` only when its pool runs out.
3. <strong>User mode vs kernel mode?</strong><br>A CPU privilege bit. Privileged instructions (I/O, page-table base, interrupt masking, timer) work only in kernel mode; user code enters the kernel only through traps, exceptions and interrupts.
4. <strong>Interrupt vs trap vs exception?</strong><br>Interrupts are asynchronous, from devices. Exceptions are synchronous, caused by the instruction: faults (page fault, re-executed), traps (`int3`, `syscall`, continue after) and aborts.
5. <strong>Monolithic vs microkernel?</strong><br>Monolithic runs all services in kernel space with function calls (Linux): fast, large trusted base. Microkernel keeps IPC, scheduling and address spaces in the kernel and the rest in user-space servers (QNX, seL4): isolation at IPC cost.
6. <strong>What happens at boot?</strong><br>Firmware (BIOS/UEFI) self-test, boot loader (GRUB) loads kernel and initramfs, kernel initialises and mounts root, starts PID 1 (systemd), which starts everything else.
7. <strong>Program vs process?</strong><br>A program is a file; a process is a running instance with an address space, registers, open files and a PCB.
8. <strong>What is in a PCB?</strong><br>PID, state, saved registers and PC, scheduling info, page-table root and memory regions, open files, signal state, credentials, accounting.
9. <strong>Which state transitions are impossible?</strong><br>Blocked $\to$ running and ready $\to$ blocked (and anything out of terminated): a woken process always goes through ready.
10. <strong>What does a context switch save, and what makes it expensive?</strong><br>Registers, PC, stack pointer and, between processes, the address space (CR3). The real cost is indirect: TLB and cache misses afterwards.
11. <strong>What does `fork` return?</strong><br>0 in the child, the child’s PID in the parent, $-1$ on failure. Memory is copied lazily (copy-on-write); file descriptors share offsets.
12. <strong>How many processes does `fork(); fork(); fork();` create?</strong><br>8 in total (7 new): $2^n$ when every process executes every fork.
13. <strong>Why can `printf("x"); fork();` print x twice?</strong><br>The text is still in the stdio buffer, which `fork` copies; both processes flush it at exit. Newline-terminated output to a terminal is flushed before the fork; to a pipe or file it is not.
14. <strong>`fork` vs `exec`?</strong><br>`fork` creates a new process running the same program; `exec` replaces the program in the current process (same PID, same open files).
15. <strong>How many forks does `system()` do?</strong><br>It creates one child, which runs `/bin/sh -c cmd`; glibc makes it with `posix_spawn`, i.e. a `clone(CLONE_VM|CLONE_VFORK)`. The shell may fork again for the command (dash does for external commands).
16. <strong>Zombie vs orphan?</strong><br>Zombie: dead, but its exit status has not been collected by `wait`; only its entry in the process table remains, and `SIGKILL` does nothing. Orphan: alive, parent dead; adopted and later reaped by `init` or a subreaper.
17. <strong>How do you avoid zombies?</strong><br>`wait`/`waitpid`, a `SIGCHLD` handler that loops on `waitpid(-1, ..., WNOHANG)`, or `SIGCHLD` set to `SIG_IGN`.
18. <strong>Which signals cannot be caught?</strong><br>`SIGKILL` and `SIGSTOP`.
19. <strong>`SIGTERM` vs `SIGKILL`?</strong><br>`SIGTERM` asks politely and can be handled for cleanup; `SIGKILL` cannot be caught and kills at once. Send TERM, wait, then KILL.
20. <strong>What is async-signal-safe?</strong><br>Safe to call from a handler that may interrupt anything: `write`, `_exit`, `waitpid`…, not `printf` or `malloc`, which hold locks.
21. <strong>Fastest IPC?</strong><br>Shared memory: after set-up there are no system calls; but you must synchronise yourself. Pipes, message queues and sockets copy through the kernel.
22. <strong>Pipe vs FIFO vs message queue?</strong><br>Pipe: anonymous byte stream between related processes. FIFO: a pipe with a file-system name. Message queue: discrete messages with priorities.

### 14.1.ii Threads and scheduling {#s14-1-ii}

23. <strong>Process vs thread?</strong><br>A process is an isolated address space with resources; a thread is an execution context inside it. Threads share memory and files, have their own stack, registers and TLS; cheaper to create and switch, but one crash kills all.
24. <strong>User-level vs kernel-level threads?</strong><br>User-level: fast, invisible to the kernel, one blocking call blocks all, no parallelism. Kernel-level: scheduled by the kernel, parallel, costlier. Linux is one-to-one.
25. <strong>What is thread-local storage?</strong><br>One instance of a variable per thread (`_Thread_local`); `errno` is the famous example.
26. <strong>Concurrency vs parallelism?</strong><br>Concurrency: overlapping lifetimes, possibly interleaved on one core. Parallelism: simultaneous execution on several cores.
27. <strong>Turnaround, waiting and response time?</strong><br>TAT = completion $-$ arrival; WT = TAT $-$ burst; RT = first run $-$ arrival.
28. <strong>What is the “release time” of a process?</strong><br>Its arrival time (the real-time term for when a job becomes ready).
29. <strong>Which algorithm minimises average waiting time?</strong><br>SJF for jobs available together; SRTF in general. Both need burst predictions (exponential averaging).
30. <strong>What happens to round robin as the quantum grows?</strong><br>It becomes FCFS. As it shrinks, it approaches processor sharing but drowns in context switches.
31. <strong>Which algorithms can starve?</strong><br>SJF, SRTF, priority without aging, multilevel queues, MLFQ without boosting. FCFS, RR and HRRN cannot.
32. <strong>What is aging?</strong><br>Raising a process’s priority the longer it waits; HRRN’s ratio $(w+s)/s$ is aging built in.
33. <strong>What is the convoy effect?</strong><br>Short jobs stuck behind a long one in FCFS.
34. <strong>How does MLFQ approximate SJF without knowing bursts?</strong><br>New jobs start at top priority; using a full quantum demotes them; interactive jobs that block stay high; periodic boosts prevent starvation.
35. <strong>How does Linux’s fair scheduler work?</strong><br>Each task’s virtual runtime grows at $1024/\text{weight}$; it always runs the smallest. Nice 0 has weight 1024, each nice step about 1.25$\times$ (about 10% CPU). Since 6.6 the pick rule is EEVDF.
36. <strong>RMS vs EDF?</strong><br>RMS: static priority by period, schedulable if $U\le n(2^{1/n}-1)$ (sufficient). EDF: dynamic, nearest deadline first, schedulable iff $U\le1$.
37. <strong>What is processor affinity?</strong><br>Preference (soft) or restriction (hard, `taskset`) to run on particular CPUs, to keep caches warm.

### 14.1.iii Synchronization and deadlock {#s14-1-iii}

38. <strong>What is a race condition?</strong><br>An outcome that depends on timing of unsynchronised accesses to shared data, at least one a write. `count++` is load-add-store.
39. <strong>The three critical-section requirements?</strong><br>Mutual exclusion, progress (no deadlock, no interference from non-contenders), bounded waiting (no starvation).
40. <strong>Does Peterson’s algorithm work on a modern CPU?</strong><br>Not without a fence: stores can be delayed past later loads (store buffer), and both processes enter. With `seq_cst` fences it works.
41. <strong>Hardware solutions to the critical section?</strong><br>Test-and-set, compare-and-swap, fetch-and-add, LL/SC; disabling interrupts on a uniprocessor. Peterson is software.
42. <strong>Mutex vs semaphore?</strong><br>A mutex has an owner and protects a critical section; a semaphore is a counter for resources or signalling that any thread may post.
43. <strong>Spinlock vs mutex?</strong><br>Spin when the wait is shorter than a context switch and the holder runs on another CPU; sleep otherwise.
44. <strong>Why `while` and not `if` around `pthread_cond_wait`?</strong><br>Mesa semantics and spurious wake-ups: the condition may be false again when the thread runs.
45. <strong>A semaphore starts at $S$, has $W$ waits and $V$ signals; final value?</strong><br>$S - W + V$ (negative means that many blocked).
46. <strong>Producer–consumer with semaphores?</strong><br>`empty`$=n$, `full`$=0$, `mutex`$=1$; wait on the counting semaphore before the mutex, or it deadlocks.
47. <strong>Readers–writers problem?</strong><br>Many readers or one writer. Reader preference starves writers; writer preference starves readers; a turnstile makes it fair.
48. <strong>Dining philosophers deadlock fix?</strong><br>Break circular wait (one philosopher picks right first), allow at most $n-1$ at the table, or pick up both chopsticks atomically.
49. <strong>What is priority inversion?</strong><br>High waits for a lock held by low, and medium preempts low. Fix: priority inheritance (Mars Pathfinder, 1997) or priority ceiling.
50. <strong>What is the ABA problem?</strong><br>CAS sees the same value though it changed in between (A to B to A); fix with version counters, LL/SC or safe memory reclamation.
51. <strong>Four conditions for deadlock?</strong><br>Mutual exclusion, hold and wait, no preemption, circular wait. All four necessary.
52. <strong>Is a cycle in the RAG a deadlock?</strong><br>With single-instance resources yes; with multiple instances it is necessary but not sufficient.
53. <strong>Prevention vs avoidance vs detection?</strong><br>Prevention breaks a condition by design (lock ordering); avoidance refuses unsafe requests (Banker’s); detection finds cycles later and recovers by killing or rolling back.
54. <strong>Safe vs unsafe state?</strong><br>Safe: some order lets everyone finish. Unsafe is not deadlock, only no guarantee.
55. <strong>Minimum resources so $n$ processes needing $S_i$ each can never deadlock?</strong><br>$\sum(S_i-1)+1$.
56. <strong>Deadlock vs livelock vs starvation?</strong><br>Deadlock: all wait. Livelock: all run, none progresses. Starvation: one waits while others progress.

### 14.1.iv Memory {#s14-1-iv}

57. <strong>Logical vs physical address?</strong><br>The CPU issues logical (virtual) addresses; the MMU translates each into a physical one.
58. <strong>Internal vs external fragmentation?</strong><br>Internal: unused space inside an allocated unit (paging, fixed partitions). External: free memory split into holes too small to use (variable partitions, segmentation).
59. <strong>First, best, worst fit?</strong><br>First: first hole that fits (fast). Best: smallest that fits. Worst: largest. First and best beat worst in practice.
60. <strong>Why paging?</strong><br>No external fragmentation, easy allocation and sharing, and it enables demand paging.
61. <strong>Page-table size for 32-bit addresses, 4 KiB pages, 4-byte PTEs?</strong><br>$2^{20}$ entries $\times$ 4 B = 4 MiB per process; hence multi-level tables.
62. <strong>Why multi-level page tables?</strong><br>Only the parts of the table covering used regions are allocated; the cost is one memory access per level on a TLB miss.
63. <strong>What is the TLB?</strong><br>A small associative cache of translations. EAT $=h(t+m)+(1-h)(t+(k+1)m)$ for a $k$-level table.
64. <strong>Inverted page table?</strong><br>One entry per physical frame (PID, VPN); size scales with RAM; looked up by hashing.
65. <strong>Paging vs segmentation?</strong><br>Fixed-size invisible pages vs variable-size logical segments; internal vs external fragmentation. x86-64 is effectively pure paging.
66. <strong>The heap vs the stack?</strong><br>Heap: dynamic allocation by `malloc`/`new`, any lifetime. Stack: locals and return addresses, LIFO, one per thread.

### 14.1.v Virtual memory {#s14-1-v}

67. <strong>Why is virtual memory called “virtual”?</strong><br>Its addresses do not name physical locations: each process sees a private address space that the OS maps, partly, onto frames or disk.
68. <strong>What happens on a page fault?</strong><br>Trap; check the address is valid (else `SIGSEGV`); find a frame (evict a victim, write it back if dirty); read the page; update the PTE; restart the instruction.
69. <strong>FIFO vs LRU vs OPT vs Clock?</strong><br>OPT evicts the page used furthest in the future (bound); LRU the least recently used; Clock approximates LRU with reference bits; FIFO the oldest.
70. <strong>What is Belady’s anomaly?</strong><br>More frames giving more faults, possible with FIFO, impossible with stack algorithms (LRU, OPT).
71. <strong>What is thrashing and how do you fix it?</strong><br>More time paging than executing because the working sets do not fit. Reduce multiprogramming, add RAM, use working-set or PFF allocation and local replacement.
72. <strong>What is page stealing?</strong><br>Taking frames from other processes’ working sets (global replacement), done by the page daemon (`kswapd`).
73. <strong>Proportional frame allocation?</strong><br>$a_i = \lfloor s_i m / S\rfloor$.
74. <strong>What is copy-on-write?</strong><br>Shared read-only pages after `fork`; the first write faults and copies just that page.
75. <strong>What does `mmap` do?</strong><br>Maps a file or anonymous memory into the address space; `MAP_SHARED` writes reach the file, `MAP_PRIVATE` writes are COW copies.
76. <strong>Buddy vs slab allocator?</strong><br>Buddy: power-of-two page blocks that split and merge. Slab: per-object-type caches of preformatted objects on top of it.
77. <strong>Why does `malloc` rarely return `NULL` on Linux?</strong><br>Over-commit: memory is reserved, not backed, until touched; real exhaustion triggers the OOM killer instead.

### 14.1.vi Files, I/O, security, virtualization, Linux {#s14-1-vi}

78. <strong>What is an inode?</strong><br>The file’s metadata and block pointers, everything except its name; directories map names to inode numbers.
79. <strong>Hard link vs soft link?</strong><br>Hard: another name for the same inode, same file system, not for directories, survives deletion of the original. Soft: a file holding a path; can dangle.
80. <strong>Maximum file size with 12 direct, single, double, triple indirect, 4 KiB blocks, 4 B pointers?</strong><br>$(12 + 1024 + 1024^2 + 1024^3)\times4$ KiB, just over 4 TiB.
81. <strong>Does `write` put data on disk?</strong><br>No, into the page cache. `fsync` forces it to stable storage.
82. <strong>What is journaling?</strong><br>Write intended metadata updates to a log first, then in place; after a crash replay the log instead of scanning the disk.
83. <strong>Polling vs interrupts vs DMA?</strong><br>Polling burns CPU waiting; interrupts notify per operation; DMA moves whole blocks and interrupts once.
84. <strong>Character vs block device?</strong><br>Character: byte stream (terminal, keyboard, `/dev/null`). Block: random-access blocks via the page cache (disk, SSD).
85. <strong>Best disk-scheduling algorithm?</strong><br>SSTF minimises movement greedily but can starve; SCAN/LOOK bound waiting; C-SCAN/C-LOOK make it uniform; for SSDs none matters.
86. <strong>RAID 5 vs RAID 6 vs RAID 10?</strong><br>5: one parity, $n-1$ capacity, one failure. 6: two parities, two failures. 10: mirrored stripes, $n/2$ capacity, fast rebuild.
87. <strong>Why TRIM on SSDs?</strong><br>It tells the drive which blocks are free so garbage collection does not copy dead data.
88. <strong>ACL vs capability?</strong><br>ACL: per object, who may access it. Capability: per subject, unforgeable token naming what it may access.
89. <strong>What does setuid do?</strong><br>The program runs with its owner’s effective uid (`passwd`).
90. <strong>Stack canary, NX, ASLR?</strong><br>Detect overwritten return addresses; forbid executing data; randomise addresses. Each blocks one exploit step.
91. <strong>VM vs container?</strong><br>A VM runs its own kernel on virtual hardware; a container is a group of host processes isolated by namespaces and limited by cgroups.
92. <strong>Type 1 vs type 2 hypervisor?</strong><br>Bare metal (ESXi, Xen, KVM) vs hosted on an OS (VirtualBox).
93. <strong>What happens when you run `./a.out`?</strong><br>Shell forks, child execs; kernel maps the ELF and the dynamic loader; loader maps libc, relocates, jumps to `_start`; `main` runs; `exit` flushes and calls `exit_group`; parent’s `wait` returns.
94. <strong>How does the shell run `ls | grep x`?</strong><br>`pipe`, two `fork`s, `dup2` of the pipe ends onto stdout and stdin, close the unused ends, `exec`, parent waits for both.
95. <strong>What is `/etc/hosts`?</strong><br>A static name-to-IP table consulted before DNS when `/etc/nsswitch.conf` says `hosts: files dns`.
96. <strong>What is `/proc`?</strong><br>A pseudo file system exposing kernel data per process and system-wide; `ps` and `top` read it.
97. <strong>How do you stop a fork bomb?</strong><br>Limits: `ulimit -u` or a `pids` cgroup; then `kill -9` the process group from an existing shell.
98. <strong>What does `nohup` do?</strong><br>Runs a command immune to `SIGHUP`, so it survives the terminal closing.
