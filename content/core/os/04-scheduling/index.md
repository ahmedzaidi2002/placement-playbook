---
title: "4 · CPU scheduling"
linkTitle: "4 CPU scheduling"
weight: 4
math: true
---
The most-asked OS numerical. Learn the three formulas, then work each algorithm once on the same four processes.

## 4.1 The formulas {#os-4-1}

For a process with arrival time $A$, burst (CPU) time $B$, completion time $C$ and first time on the CPU $F$:

$$\text{Turnaround } T = C - A, \qquad \text{Waiting } W = T - B, \qquad \text{Response } R = F - A.$$

- **Throughput** = processes completed per unit time. **CPU utilisation** = fraction of time the CPU is busy.
- **Preemptive**: the OS can take the CPU away from a running process. **Non-preemptive**: a process keeps the CPU until it finishes or blocks.

**The workload used for every example below:**

| Process | Arrival | Burst |
|---|---|---|
| P1 | 0 | 8 |
| P2 | 1 | 4 |
| P3 | 2 | 9 |
| P4 | 3 | 5 |

Total burst = 26, so every schedule ends at time 26.

## 4.2 FCFS (first come, first served) {#os-4-2}

Run in arrival order, each to completion. Non-preemptive, simple, no starvation.

<div class="nb nb-example">

<strong>Example</strong> (FCFS)

Gantt: `P1 [0–8] | P2 [8–12] | P3 [12–21] | P4 [21–26]`

| | C | T = C − A | W = T − B |
|---|---|---|---|
| P1 | 8 | 8 | 0 |
| P2 | 12 | 11 | 7 |
| P3 | 21 | 19 | 10 |
| P4 | 26 | 23 | 18 |

Average turnaround **15.25**, average waiting **8.75**.

</div>

**Convoy effect:** short jobs wait behind one long job. Three jobs arriving together with bursts 24, 3, 3: FCFS average waiting $= (0 + 24 + 27)/3 = 17$; running the short ones first gives $(0 + 3 + 6)/3 = 3$.

## 4.3 SJF (shortest job first), non-preemptive {#os-4-3}

When the CPU is free, pick the ready process with the **smallest burst** and run it to completion.

<div class="nb nb-example">

<strong>Example</strong> (SJF)

At 0 only P1 is there, so it runs 0–8. At 8, P2 (4), P3 (9), P4 (5) are waiting: P2, then P4, then P3.

Gantt: `P1 [0–8] | P2 [8–12] | P4 [12–17] | P3 [17–26]`

Waiting: P1 0, P2 7, P3 15, P4 9 → average **7.75**. Turnaround average **14.25**.

</div>

## 4.4 SRTF (shortest remaining time first) = preemptive SJF {#os-4-4}

When a process arrives, compare its burst with the **remaining** time of the running one; switch if the newcomer is shorter.

<div class="nb nb-example">

<strong>Example</strong> (SRTF)

- 0: P1 starts (remaining 8).
- 1: P2 arrives with 4 < P1's remaining 7 → **P2 preempts** P1.
- 2: P3 (9) arrives, 3: P4 (5) arrives; neither is shorter than P2's remaining (3, then 2).
- 5: P2 done. Remaining: P1 7, P3 9, P4 5 → P4 runs 5–10, then P1 10–17, then P3 17–26.

Gantt: `P1 [0–1] | P2 [1–5] | P4 [5–10] | P1 [10–17] | P3 [17–26]`

Waiting: P1 $= 17 - 0 - 8 = 9$, P2 0, P3 15, P4 2 → average **6.5** (the lowest of all). Turnaround average **13**.

</div>

<div class="nb nb-theorem nb-block">

<strong>Optimality</strong>

SJF gives the minimum average waiting time among non-preemptive schedules (all jobs present at once); SRTF gives the minimum among all schedules. The catch: real burst lengths are unknown, so they are **predicted** by exponential averaging, $\tau_{n+1} = \alpha t_n + (1-\alpha)\tau_n$.

</div>

SJF and SRTF can **starve** long jobs if short ones keep arriving.

## 4.5 Priority scheduling {#os-4-5}

Each process has a priority; the highest-priority ready process runs (here: smaller number = higher priority). Can be preemptive or not. SJF is priority scheduling with priority = burst length.

<div class="nb nb-example">

<strong>Example</strong> (Preemptive priority)

Priorities: P1 = 2, P2 = 4, P3 = 1, P4 = 3.

- 0: P1 runs. 1: P2 (4) arrives, lower priority, P1 continues.
- 2: P3 (1) arrives → **preempts** P1 (remaining 6) and runs to 11.
- 11: ready are P1 (2), P4 (3), P2 (4) → P1 11–17, P4 17–22, P2 22–26.

Gantt: `P1 [0–2] | P3 [2–11] | P1 [11–17] | P4 [17–22] | P2 [22–26]`

Waiting: P1 9, P2 21, P3 0, P4 14 → average **11**. P2, the lowest priority, waits longest.

</div>

**Starvation** (indefinite blocking): a low-priority process may never run. Cure: **aging**, gradually raising the priority of processes that wait long.

## 4.6 Round robin (RR) {#os-4-6}

Ready processes in a FIFO queue; each runs for at most one **time quantum** $q$, then goes to the back of the queue. Designed for time-sharing: good **response time**.

<div class="nb nb-example">

<strong>Example</strong> (RR, $q = 3$)

Convention: a newly arrived process joins the queue **before** a process that was just preempted at the same moment.

- 0–3 P1 (left 5). Queue now: P2, P3, P4, P1.
- 3–6 P2 (left 1) → 6–9 P3 (left 6) → 9–12 P4 (left 2) → 12–15 P1 (left 2)
- 15–16 P2 **done** → 16–19 P3 (left 3) → 19–21 P4 **done** → 21–23 P1 **done** → 23–26 P3 **done**

Gantt: `P1 [0–3] | P2 [3–6] | P3 [6–9] | P4 [9–12] | P1 [12–15] | P2 [15–16] | P3 [16–19] | P4 [19–21] | P1 [21–23] | P3 [23–26]`

Completion: P1 23, P2 16, P3 26, P4 21. Waiting: P1 15, P2 11, P3 15, P4 13 → average **13.5**. Response: P1 0, P2 2, P3 4, P4 6 → average **3**, the best response here.

</div>

**Choosing the quantum:**

- $q$ very large → RR becomes **FCFS**.
- $q$ very small → too many context switches. With switch cost $s$, the useful CPU fraction is $q/(q+s)$: $q = 95$ ms, $s = 5$ ms gives 95%.
- Rule of thumb: about 80% of CPU bursts should finish within one quantum.

## 4.7 HRRN (highest response ratio next) {#os-4-7}

Non-preemptive. When the CPU is free, pick the largest

$$\text{Response ratio} = \frac{\text{waiting time} + \text{burst}}{\text{burst}}.$$

Short jobs start with a high ratio (like SJF), and a long job's ratio grows as it waits, so **no starvation**: aging is built into the formula.

<div class="nb nb-example">

<strong>Example</strong> (HRRN)

P1 runs 0–8. At 8: P2 $= (7+4)/4 = 2.75$, P3 $= (6+9)/9 = 1.67$, P4 $= (5+5)/5 = 2.0$ → **P2** (8–12). At 12: P3 $= (10+9)/9 = 2.11$, P4 $= (9+5)/5 = 2.8$ → **P4** (12–17), then P3 (17–26). Same order as SJF here; it differs when a long job has already waited a long time.

</div>

## 4.8 Comparison {#os-4-8}

| Algorithm | Preemptive? | Avg waiting (our workload) | Starvation? | Note |
|---|---|---|---|---|
| FCFS | no | 8.75 | no | convoy effect |
| SJF | no | 7.75 | yes | optimal among non-preemptive |
| SRTF | yes | **6.5** | yes | optimal overall |
| Priority (preemptive) | either | 11 | yes (fix: aging) | |
| RR ($q = 3$) | yes | 13.5 | no | best response (3) |
| HRRN | no | 7.75 | no | aging built in |

## 4.9 Multilevel queues {#os-4-9}

- **Multilevel queue (MLQ):** separate queues for different process types (system, interactive, batch), each with its own algorithm, scheduled by fixed priority between queues. A process never changes queue, so low queues can starve.
- **Multilevel feedback queue (MLFQ):** processes **move** between queues by behaviour. New processes start at the top (short quantum). A process that uses its whole quantum (CPU-bound) moves **down**; one that blocks early (interactive, I/O-bound) stays up. Lower queues get longer quanta. Periodically everyone is boosted to the top so nothing starves. It favours interactive jobs without knowing burst lengths in advance.

**Linux (CFS):** gives each task a CPU share proportional to its weight (from its `nice` value, −20 to 19); it always runs the task with the smallest "virtual runtime", kept in a red-black tree.

## 4.10 Real-time scheduling {#os-4-10}

Periodic task $i$ needs $C_i$ time every period $T_i$; utilisation $U = \sum C_i/T_i$.

- **Rate-monotonic (RMS):** fixed priorities, **shorter period = higher priority**. Guaranteed schedulable if $U \le n(2^{1/n} - 1)$: 1 for one task, **0.828** for two, 0.780 for three, → 0.693 for many. (Sufficient, not necessary.)
- **Earliest deadline first (EDF):** dynamic; run the job with the nearest deadline. Schedulable **iff** $U \le 1$.

<div class="nb nb-example">

<strong>Example</strong> (RMS test)

Tasks (C, T): (1, 4), (2, 6), (1, 8). $U = 0.25 + 0.333 + 0.125 = 0.708 \le 0.780$ → RMS guarantees all deadlines. Tasks (2, 4), (3, 6): $U = 0.5 + 0.5 = 1.0 > 0.828$, so RMS gives no guarantee, but EDF works since $U \le 1$.

</div>

<div class="nb nb-remark">

<strong>Statements OAs test</strong> — "RR with a very large quantum becomes FCFS": true. "SRTF has the minimum average waiting time": true. "HRRN can starve long jobs": false. "FCFS can starve": false. Can starve: SJF, SRTF, priority, MLQ.

</div>

<div class="nb nb-moral">

Shortest-first minimises waiting; round robin minimises response at the cost of turnaround and switches; priority needs aging; HRRN has aging built in.

</div>
