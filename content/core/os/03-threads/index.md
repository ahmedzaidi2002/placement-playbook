---
title: "3 · Threads"
linkTitle: "3 Threads"
weight: 3
math: true
---
## 3.1 Thread vs process {#os-3-1}

<div class="nb nb-definition">

<strong>Definition</strong> — A **thread** is one flow of execution inside a process: its own program counter, registers and **stack**. Threads of a process **share** its code, global data, heap and open files. The process is the unit of resource ownership; the thread is the unit of scheduling.

</div>

| | Process | Thread |
|---|---|---|
| Memory | own address space | shares the process's |
| Creation / switch cost | high | low (no address-space switch, no TLB flush) |
| Communication | IPC through the kernel | ordinary shared variables |
| Failure | isolated | one crash kills all threads |
| Needs locks? | only for shared IPC | yes, for any shared data |

<div class="nb nb-remark">

<strong>Interview answer in four sentences</strong> — A process is an isolated address space plus resources; a thread is an execution context inside one. Threads share memory, so they communicate cheaply but need locks, and one bad pointer crashes them all. Creating and switching threads is cheaper. That is why a browser runs each site in its own *process* (isolation) while a web server uses *threads* per request (cheap sharing).

</div>

**Concurrency** = several tasks in progress at once (can interleave on one core). **Parallelism** = several tasks running at the same instant (needs several cores). One core can be concurrent but not parallel.

## 3.2 User-level vs kernel-level threads {#os-3-2}

- **User-level threads:** managed by a library; the kernel sees one process. Very fast to create and switch, but **one blocking system call blocks all of them**, and they cannot run on two cores at once.
- **Kernel-level threads:** created and scheduled by the kernel. Can run in parallel; a blocking call blocks only that thread; switching costs a bit more.

**Mapping models:**

| Model | Meaning | Example |
|---|---|---|
| Many-to-one | many user threads on one kernel thread | old "green threads" |
| **One-to-one** | each user thread is a kernel thread | **Linux, Windows** |
| Many-to-many | $M$ user threads on $N \le M$ kernel threads | Go goroutines |

## 3.3 Common thread bugs and facts {#os-3-3}

- Each thread has its own stack, so **local variables are private**; globals and heap data are **shared**.
- If `main` returns, the whole process (all threads) ends: join the threads first.
- **Thread-local storage** gives each thread its own copy of a variable (that is how `errno` works per thread).
- **Thread pool:** create a fixed set of threads once and give them tasks from a queue, instead of creating a thread per request.

<div class="nb nb-moral">

Threads share everything except their stack and registers: cheaper to create and switch, easier to share data, harder to keep correct.

</div>
