---
title: "Synchronization (semaphores, mutex, monitors)"
weight: 5
---

6 questions asked by NVIDIA, Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q12, initial semaphore value

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

After 10 wait operations and 7 signal operations on a counting semaphore, its final
value was 6. What was its initial value?

- **(a)** 3
- **(b)** 9
- **(c)** 4
- **(d)** 11

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 9**

**Why.** Each wait (P) decrements and each signal (V) increments: S − 10 + 7 = 6 → S = 9.

**Concept: counting semaphores.** The value counts available resources (or, if negative in some implementations, waiting processes). wait: S−−, block if no resource; signal: S++, wake a waiter.

{{< /details >}}

### 2 · Q17, signal operations

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

A counting semaphore has value 7. After 20 wait operations and some signal operations,
its value becomes 5. How many signal operations were performed?

- **(a)** 18
- **(b)** 22
- **(c)** 10
- **(d)** 20

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 18**

**Why.** 7 − 20 + s = 5 → s = 18.

**Concept: semaphore arithmetic.** Final value = initial − waits + signals (assuming the waits eventually completed).

{{< /details >}}

### 3 · Q35, negative synchronisation in RTOS

*Asked by: Qualcomm (IISc)*

Which method is used to handle negative synchronisation in an RTOS?

- **(a)** Semaphores
- **(b)** Event Flags
- **(c)** Signals
- **(d)** Message Pipes

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) semaphores** (the ticked answer; "negative synchronisation" is not standard terminology)

**Why.** Read it as "make a task wait until another task signals it". A semaphore's wait/signal pair does exactly that: the waiting task blocks until the signal arrives.

**Concept: RTOS synchronisation tools.** Semaphores (signalling and counting), mutexes (mutual exclusion with priority inheritance), event flags (wait for combinations of events), message queues (pass data).

{{< /details >}}

### 4 · Q55, hardware critical-section solutions

*Asked by: Qualcomm (Nov 2024); Qualcomm (Delhi campus 2024, Q48)*

Which of these is/are hardware-based solutions to the critical-section problem?
(I) Test_and_set() (II) Compare_and_swap() (III) Peterson's solution

- **(a)** Only (I) and (II)
- **(b)** Only (I) and (III)
- **(c)** All (I), (II) and (III)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) only (I) and (II)**

**Why.** Test-and-set and compare-and-swap are atomic hardware instructions. Peterson's solution uses only ordinary loads and stores, so it is a software solution.

**Concept: atomic instructions.** The hardware guarantees the read-modify-write happens as one indivisible step, which makes simple spinlocks possible: `while (test_and_set(&lock)) ;`.

{{< /details >}}

### 5 · Synchronisation

*Asked by: Qualcomm (Delhi campus 2024, Q37)*

Which of the following is a case of the concurrency-control problem?

- **(a)** Block allocation
- **(b)** Bounded buffer
- **(c)** I/O interlock
- **(d)** Low page hit ratio

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) bounded buffer**

**Why.** The bounded-buffer (producer–consumer) problem is a classic concurrency-control problem: producers wait when the buffer is full, consumers when it is empty, and the buffer needs mutual exclusion.

**Concept: producer–consumer with semaphores.** `empty` (counts free slots, starts at n), `full` (counts filled slots, starts at 0) and `mutex` (starts at 1). Producer: wait(empty), wait(mutex), add, signal(mutex), signal(full). Consumer does the mirror.

{{< /details >}}

### 6 · Synchronisation

*Asked by: Qualcomm (Delhi campus 2024, Q43)*

The `test_and_set()` algorithm below will satisfy which of the critical-section requirements? (The options were not captured in the photo.)

```c
do {
    waiting[i] = true;
    key = true;
    while (waiting[i] && key)
        key = test_and_set(&lock);
    waiting[i] = false;

    /* critical section */

    j = (i + 1) % n;
    while ((j != i) && !waiting[j])
        j = (j + 1) % n;
    if (j == i)
        lock = false;
    else
        waiting[j] = false;

    /* remainder section */
} while (true);
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: it satisfies all three requirements**: mutual exclusion, progress and bounded waiting.

**Why.**
- Mutual exclusion: a process enters only when `key` becomes false (it won the lock) or when the leaving process sets its `waiting[i]` to false, and only one of those can happen at a time.
- Progress: a leaving process either hands entry to a waiting process or releases the lock.
- Bounded waiting: the leaving process scans `waiting[]` in cyclic order from i + 1, so any waiting process gets in within n − 1 turns.

**Concept: the three critical-section requirements.** Mutual exclusion (one at a time), progress (if nobody is inside, someone who wants in gets in), bounded waiting (no one waits forever). Plain test-and-set gives only the first two; this version adds bounded waiting.

{{< /details >}}
