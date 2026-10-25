---
title: "12 · Interview rapid-fire"
linkTitle: "12 Rapid-fire"
weight: 12
math: true
---
Answers you can say in under twenty seconds. Cover the answer, say yours, compare.

## 12.1 Processes, threads, scheduling {#os-12-1}

1. **Process vs thread?** A process is an isolated address space with resources; a thread is an execution context inside it, sharing that memory. Threads are cheaper to create and switch but need locks.
2. **What is in a PCB?** PID, state, saved registers and program counter, scheduling info, memory-management info (page table), open files, accounting.
3. **Mode switch vs context switch?** A mode switch is user ↔ kernel in the same process (a system call). A context switch changes which process runs.
4. **What is a system call?** A controlled entry into the kernel through a trap instruction, to ask for a privileged service.
5. **Zombie vs orphan?** Zombie: finished but not yet `wait`ed for. Orphan: still running after its parent died; adopted by `init`.
6. **What does `fork` return?** 0 in the child, the child's PID in the parent, −1 on failure.
7. **How many processes after 3 `fork()` calls?** $2^3 = 8$ (7 new).
8. **Preemptive vs non-preemptive scheduling?** Preemptive can take the CPU away (timer); non-preemptive waits until the process finishes or blocks.
9. **Which algorithm minimises average waiting time?** SRTF (SJF among non-preemptive).
10. **Convoy effect?** In FCFS, short jobs stuck behind one long job.
11. **RR with a huge quantum?** Becomes FCFS. Tiny quantum: too much switching overhead.
12. **Starvation and its fix?** A process never gets the CPU (low priority); fix with aging.
13. **Which algorithms can starve?** SJF, SRTF, priority, multilevel queue. Not FCFS, RR or HRRN.
14. **Why multilevel feedback queues?** They favour interactive jobs without knowing burst lengths: CPU-hungry jobs sink to lower queues.

## 12.2 Synchronization and deadlock {#os-12-2}

15. **Race condition?** The result depends on the timing of unsynchronised accesses to shared data.
16. **Three requirements of a critical-section solution?** Mutual exclusion, progress, bounded waiting.
17. **Mutex vs semaphore?** A mutex is a lock with an owner; a semaphore is a counter any thread can signal, used for counting resources and signalling.
18. **Spinlock vs mutex?** A spinlock busy-waits (good for very short waits on multi-core); a mutex sleeps.
19. **Why test-and-set?** It reads and sets a value atomically, which makes a lock possible.
20. **Producer–consumer semaphores?** `empty = N`, `full = 0`, `mutex = 1`; wait on the counting semaphore before the mutex.
21. **Priority inversion and fix?** A high-priority task waits on a lock held by a low one that a medium one keeps preempting; fix with priority inheritance.
22. **Four deadlock conditions?** Mutual exclusion, hold and wait, no preemption, circular wait.
23. **Prevention vs avoidance?** Prevention makes a condition impossible (e.g. lock ordering); avoidance grants requests only if the state stays safe (Banker's).
24. **Is an unsafe state a deadlock?** No; it only means deadlock can no longer be ruled out.
25. **Deadlock vs livelock vs starvation?** Nobody runs / everybody runs but no progress / one process never gets served.

## 12.3 Memory {#os-12-3}

26. **Internal vs external fragmentation?** Wasted space inside an allocated block vs free memory split into unusable holes.
27. **Why paging?** No external fragmentation; any free frame fits any page.
28. **Logical vs physical address?** The CPU generates logical addresses; the MMU translates them to physical ones.
29. **What is the TLB?** A small cache of page-to-frame translations that avoids a page-table lookup on most accesses.
30. **Paging vs segmentation?** Fixed-size pages (internal fragmentation) vs variable-size logical segments (external fragmentation).
31. **What is a page fault?** Access to a page not in memory; the OS loads it and restarts the instruction.
32. **Belady's anomaly?** With FIFO, more frames can cause more page faults. LRU and OPT do not have it.
33. **Why is OPT not used?** It needs to know future references; it is a benchmark.
34. **Thrashing and fix?** More time paging than working; reduce the number of processes, use working sets, add memory.
35. **Copy-on-write?** After `fork`, pages are shared read-only and copied only when written.
36. **Virtual memory benefit?** Programs larger than RAM, isolation between processes, and more processes in memory.

## 12.4 Files, I/O, other {#os-12-4}

37. **What is an inode?** The structure holding a file's metadata and block pointers (not its name).
38. **Hard vs soft link?** Hard link = another name for the same inode; soft link = a file holding a path (breaks if the target is deleted).
39. **DMA?** A controller copies blocks between device and memory without the CPU, interrupting once at the end.
40. **Best disk-scheduling algorithm?** SSTF gives the least movement but can starve; SCAN/LOOK are fair and widely used.
41. **What is journaling?** Writing changes to a log before applying them, so a crash can be recovered quickly.
42. **RAID 5?** Striping with rotated parity; $n-1$ disks of capacity; survives one disk failure.
43. **VM vs container?** A VM runs its own kernel on a hypervisor; a container is isolated processes sharing the host kernel.
44. **Monolithic vs microkernel?** All services in the kernel (fast) vs minimal kernel with services in user space (robust).

<div class="nb nb-moral">

If you can say these 44 aloud, the conceptual part of an OS interview is covered; chapter 13 covers the numericals.

</div>
