---
title: "6 · Deadlocks"
linkTitle: "6 Deadlocks"
weight: 6
math: true
---
## 6.1 Definition and the four conditions {#os-6-1}

<div class="nb nb-definition">

<strong>Definition</strong> — A set of processes is **deadlocked** if each one waits for something only another process in the set can provide, so none can ever proceed. Classic case: thread 1 holds lock A and wants B; thread 2 holds B and wants A.

</div>

<div class="nb nb-theorem nb-block">

<strong>Coffman conditions</strong> (all four are needed)

1. **Mutual exclusion:** at least one resource can be used by only one process at a time.
2. **Hold and wait:** a process holds a resource while waiting for another.
3. **No preemption:** resources are released only voluntarily.
4. **Circular wait:** a cycle $P_0 \to P_1 \to \dots \to P_0$, each waiting for the next.

</div>

**Resource-allocation graph (RAG):** processes (circles), resources (boxes with one dot per instance), request edges $P \to R$, assignment edges $R \to P$.

- **No cycle → no deadlock.**
- **Single instance** per resource: cycle ⟺ deadlock.
- **Multiple instances:** a cycle is necessary but **not sufficient**.

<div class="nb nb-remark">

<strong>Trap</strong> — "Circular wait is a necessary condition": true. "Circular wait is sufficient": false in general (only with single-instance resources).

</div>

<div class="nb nb-theorem nb-block">

<strong>How many resources make deadlock impossible?</strong>

$n$ processes share $R$ identical units; process $i$ needs at most $S_i$. Deadlock is impossible iff

$$R \ \ge\ \sum_{i=1}^{n} (S_i - 1) + 1.$$

</div>

<div class="nb nb-example">

<strong>Example</strong> (Minimum resources)

3 processes, each needs 2 tape drives. Worst case: each holds 1 and waits. With $3 \times (2-1) + 1 = $ **4** drives, one process can always finish. With 3 drives, deadlock is possible. (Asked the other way: with 4 drives and processes needing 2 each, at most 3 processes are deadlock-free.)

</div>

## 6.2 Four ways to handle deadlock {#os-6-2}

1. **Prevention:** make one Coffman condition impossible.
   - Hold and wait: request all resources at once (poor utilisation, starvation).
   - No preemption: take resources away (only for things like CPU or memory, not a printer mid-page).
   - Circular wait: **number the resources and always acquire them in increasing order**. This is what real code does with locks.
2. **Avoidance:** grant a request only if the system stays in a **safe state** (Banker's algorithm). Needs maximum demands in advance.
3. **Detection and recovery:** let deadlocks happen, detect cycles, then kill a process or preempt resources (what databases do).
4. **Ignore it** (the "ostrich" approach): what general-purpose OSs like Linux and Windows do for most resources.

## 6.3 Banker's algorithm {#os-6-3}

A state is **safe** if there is an order (a **safe sequence**) in which every process can get its remaining need from what is available plus what earlier processes release. Safe → no deadlock. **Unsafe does not mean deadlocked**; it only means the OS can no longer guarantee to avoid one.

**Need = Max − Allocation.** Safety check: start with Work = Available; repeatedly find a process with Need ≤ Work, pretend it finishes (Work += its Allocation); safe if all finish.

<div class="nb nb-example">

<strong>Example</strong> (Banker's, resources A B C, total 10 5 7)

| | Allocation | Max | Need |
|---|---|---|---|
| P0 | 0 1 0 | 7 5 3 | 7 4 3 |
| P1 | 2 0 0 | 3 2 2 | 1 2 2 |
| P2 | 3 0 2 | 9 0 2 | 6 0 0 |
| P3 | 2 1 1 | 2 2 2 | 0 1 1 |
| P4 | 0 0 2 | 4 3 3 | 4 3 1 |

Available = 10 5 7 − (sum of allocations 7 2 5) = **3 3 2**.

Safety: Work 3 3 2 → P1 (need 1 2 2 fits) → Work 5 3 2 → P3 → 7 4 3 → P4 → 7 4 5 → P2 → 10 4 7 → P0 → 10 5 7. **Safe sequence ⟨P1, P3, P4, P2, P0⟩.**

Request: P1 asks for (1, 0, 2). It is ≤ its Need (1 2 2) and ≤ Available (3 3 2). Pretend: Available 2 3 0, P1's Need 0 2 0. Safety: P1 → 5 3 2 → P3 → 7 4 3 → P4 → 7 4 5 → P0 → 7 5 5 → P2 → 10 5 7. Still safe → **grant**.

</div>

## 6.4 Detection {#os-6-4}

- **Single instance:** build a **wait-for graph** ($P_i \to P_j$ if $P_i$ waits for something $P_j$ holds) and look for a cycle.
- **Multiple instances:** run the Banker's safety loop using each process's current *request* instead of *need*; the processes that can never be marked finished are the deadlocked ones.
- **Recovery:** abort processes (all, or one at a time until the cycle breaks), or preempt resources and roll a victim back.

## 6.5 Livelock and starvation {#os-6-5}

- **Deadlock:** everyone waits, nobody runs.
- **Livelock:** everyone keeps running (retrying, backing off) but nobody progresses, like two people stepping aside the same way in a corridor. Fix: random back-off.
- **Starvation:** one process waits forever while others progress (low priority without aging). Deadlock implies starvation; starvation does not imply deadlock.

<div class="nb nb-moral">

All four Coffman conditions are needed; break any one to prevent deadlock (in practice: acquire locks in a fixed order). Safe means a safe sequence exists; unsafe is not the same as deadlocked.

</div>
