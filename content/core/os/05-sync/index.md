---
title: "5 · Synchronization"
linkTitle: "5 Synchronization"
weight: 5
math: true
---
## 5.1 Race conditions and the critical section {#os-5-1}

<div class="nb nb-definition">

<strong>Definition</strong> — A **race condition** is when the result depends on the timing of operations on shared data, and at least one of them writes. The **critical section (CS)** is the code that touches the shared data.

</div>

Why `count++` races: it is three steps (load, add, store). Two threads can both load 5, both add 1, both store 6: one increment is lost.

A correct solution must give:

1. **Mutual exclusion:** at most one process in its CS at a time.
2. **Progress:** if nobody is in the CS, a process that wants to enter is not kept out forever (and processes not trying to enter do not get a vote).
3. **Bounded waiting:** there is a limit on how many times others can enter before a waiting process gets its turn (no starvation).

<div class="nb nb-example">

<strong>Example</strong> (Which values are possible?)

$x = 10$. Thread A does `x = x + 5`, thread B does `x = x * 2`, with no lock. Serial orders give **25** (A then B) and **30** (B then A). Lost updates give **15** (both read 10; A writes last) and **20** (both read 10; B writes last). So $x \in \{15, 20, 25, 30\}$.

</div>

## 5.2 Software and hardware solutions {#os-5-2}

**Peterson's algorithm** (two processes, software only): `flag[i] = true; turn = j; while (flag[j] && turn == j);` → CS → `flag[i] = false;`. It satisfies all three requirements on paper, but fails on modern multicore CPUs, which reorder memory operations, unless memory fences are added.

**Hardware:** atomic instructions that read and write in one indivisible step:

- **Test-and-set** (TSL): return the old value and set it to 1. Lock: `while (test_and_set(&lock));` unlock: `lock = 0`.
- **Compare-and-swap** (CAS): set the value to *new* only if it still equals *expected*.
- **Disabling interrupts:** works only on a single CPU.

<div class="nb nb-remark">

<strong>OA</strong> — Hardware solutions: test-and-set, compare-and-swap, disabling interrupts. Software solutions: Peterson, Dekker, Bakery. A simple TSL spinlock gives mutual exclusion and progress but **not bounded waiting** (the same thread can win every time).

</div>

## 5.3 Locks, semaphores, monitors {#os-5-3}

| Tool | What it is | Use |
|---|---|---|
| **Spinlock** | busy-waits in a loop | very short waits on multi-core (no context switch) |
| **Mutex** | sleeping lock with an **owner**; only the locker unlocks | mutual exclusion |
| **Semaphore** | an integer $S$ with atomic `wait`/P (decrement, block if it goes below 0) and `signal`/V (increment, wake a waiter) | counting resources, signalling between threads |
| **Condition variable** | wait until a condition is true, used together with a mutex | "wait until the buffer is non-empty" |
| **Monitor** | a class whose methods run one at a time, with condition variables | Java `synchronized` |

- **Binary semaphore:** values 0/1, acts like a lock. **Counting semaphore:** initialised to the number of available resources.
- **Mutex vs binary semaphore:** a mutex has an owner (only the locker may unlock); a semaphore is a signal any thread can post. Use a mutex to protect data, a semaphore to say "something happened".
- Always wait on a condition variable inside a `while` loop, not an `if`: another thread may change the condition before you run.

<div class="nb nb-theorem nb-block">

<strong>Semaphore arithmetic</strong>

$$S_{\text{final}} = S_{\text{initial}} - (\text{number of waits}) + (\text{number of signals}).$$

If $S_{\text{final}} = -k$ (in the textbook version that allows negatives), $k$ processes are blocked.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Semaphore count)

A counting semaphore starts at 7. Then 20 `wait` and 15 `signal` operations happen. Final value $= 7 - 20 + 15 = $ **2**. If it started at 3 with the same operations, the value would be $-2$: two processes blocked.

</div>

## 5.4 The classical problems {#os-5-4}

**Producer–consumer (bounded buffer of size $N$):** semaphores `empty = N`, `full = 0`, `mutex = 1`.

- Producer: `wait(empty); wait(mutex);` add item `signal(mutex); signal(full);`
- Consumer: `wait(full); wait(mutex);` remove item `signal(mutex); signal(empty);`

<div class="nb nb-remark">

<strong>Trap</strong> — Swap the producer's two waits (`wait(mutex)` before `wait(empty)`) and it **deadlocks** when the buffer is full: the producer sleeps holding the mutex and the consumer can never get in to free a slot. The counting wait comes first, the mutex second.

</div>

- **Readers–writers:** many readers may read together; a writer needs exclusive access. The simple solution lets readers starve writers (or the reverse); fair versions alternate.
- **Dining philosophers:** 5 philosophers, 5 forks, each needs both neighbours' forks. If all pick up the left fork at once → **deadlock**. Fixes: at most 4 at the table, pick up both forks at once, or one philosopher picks right-then-left (breaks the circular wait).
- **Sleeping barber:** customers wait in $N$ chairs; the barber sleeps when nobody is waiting; classic semaphore exercise.

## 5.5 Priority inversion {#os-5-5}

A high-priority task H waits for a lock held by a low-priority task L, and a medium-priority task M (which needs no lock) preempts L. Now H effectively waits for M, for an unbounded time. This reset the **Mars Pathfinder** lander repeatedly in 1997.

Fix: **priority inheritance**: while L holds a lock that H wants, L runs at H's priority, so M cannot preempt it. (Or **priority ceiling**: a lock carries the priority of its highest user.)

## 5.6 Lock-free, briefly {#os-5-6}

**Lock-free** algorithms use CAS retry loops instead of locks, so some thread always makes progress. The classic pitfall is the **ABA problem**: a value changes A → B → A, and CAS cannot tell anything happened. Fix: a version counter next to the pointer.

<div class="nb nb-moral">

Spin when the wait is shorter than a context switch, sleep otherwise. Mutex for exclusion, semaphore for counting and signalling, condition variable in a `while`. Final semaphore value = initial − waits + signals.

</div>
