---
title: "CPU scheduling"
weight: 3
---

11 questions asked by MathWorks, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q21, starvation

*Asked by: MathWorks (IISc 2024)*

Which scheduling algorithms can cause starvation? (more than one answer)

- **(a)** Shortest job next
- **(b)** Shortest remaining time first
- **(c)** Round robin

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) and (b)** (shortest job next and shortest remaining time first)

**Why.** Both always pick the shortest job. If short jobs keep arriving, a long job can be postponed forever. Round robin gives every process a time slice in turn, so nobody waits forever.

**Concept: starvation and aging.** Starvation = a ready process never gets the CPU. Priority-style schedulers (SJF, SRTF, priority) can starve; the fix is aging: slowly raise the priority of processes that have waited long.

{{< /details >}}

### 2 · Q32, round robin with a large quantum

*Asked by: Qualcomm (IISc)*

As the time quantum of round-robin scheduling increases, the algorithm behaves like which one?

- **(a)** Shortest Job First
- **(b)** Optimal Algorithm
- **(c)** First Come First Serve
- **(d)** Priority Scheduling

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) FCFS**

**Why.** Once the time quantum is longer than every burst, no process is ever preempted; each runs to completion in arrival order, which is first-come-first-served.

**Concept: choosing the quantum.** Too large → behaves like FCFS (poor response time). Too small → too many context switches (overhead). A rule of thumb: about 80% of CPU bursts should finish within one quantum.

{{< /details >}}

### 3 · Q57, scheduling statements

*Asked by: Qualcomm (Nov 2024); Qualcomm (NIT Durgapur, Q22)*

Which statement(s) are correct for CPU scheduling algorithms? (I) The throughput of Shortest
Process Next (SPN) is on the higher side compared to FCFS. (II) The overhead of Round Robin is
lower than that of SPN. (III) Starvation of processes is possible in FCFS.

- **(a)** Only (I) and (III)
- **(b)** Only (II) and (III)
- **(c)** Only (II)
- **(d)** Only (I) and (II)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only (I) and (II)**

**Why.** (I) Shortest process next finishes many short jobs quickly, so its throughput is high (higher than FCFS). (II) Round robin's overhead is low (just a queue), while SPN needs burst-time estimates and sorting, which can be costly. (III) FCFS never starves anyone: everyone is served in arrival order. (Stallings' comparison table.)

**Concept: scheduling criteria.** Throughput (jobs per unit time), turnaround time, waiting time, response time, fairness/starvation, and overhead. No single algorithm wins on all of them.

{{< /details >}}

### 4 · Q31, release time of a process

*Asked by: Qualcomm (HirePro, Aug 2025); Qualcomm (IIIT Delhi 2025, Q40)*

Which one of the given options is also called the release time of a CPU scheduling
process?

- **(a)** Start time
- **(b)** Completion time
- **(c)** Release time
- **(d)** Response time

{{< details title="Answer and explanation" closed="true" >}}

**Answer: most likely (b) completion time** (the question is ambiguous)

**Why.** In real-time scheduling, "release time" means when a job becomes ready to run (its arrival), which is not an option. Question banks for this test treat "release" as the time the process leaves the system, i.e. completion time.

**Concept: scheduling times.** Arrival (release) time: enters the ready queue. Burst time: CPU time needed. Completion time: finishes. Turnaround = completion − arrival. Waiting = turnaround − burst. Response = first run − arrival.

{{< /details >}}

### 5 · OS Fundamentals

*Asked by: Qualcomm (60-question online assessment)*

Priority scheduling; a **lower** number means **higher** priority. All processes arrive at time 0.

| Process | Burst time | Priority |
|---|---|---|
| P0 | 7 | 3 |
| P1 | 7 | 2 |
| P2 | 4 | 5 |
| P3 | 9 | 8 |

What is the turnaround time of P2?

- **(a)** 9.75
- **(b)** 18
- **(c)** 14
- **(d)** 7

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 18**

**Why.** Lower number = higher priority, all arrive at 0. Order: P1 (priority 2, 7), P0 (3, 7), P2 (5, 4), P3 (8, 9). P2 finishes at 7 + 7 + 4 = 18. Turnaround = completion − arrival = 18 − 0 = 18.

**Concept: non-preemptive priority scheduling.** Sort by priority; each process runs to completion. Draw a Gantt chart (a timeline) and read completion times off it.

{{< /details >}}

### 6 · Operating Systems

*Asked by: Qualcomm (60-question online assessment)*

Which one of the given options is the responsibility of a secondary scheduler?

- **(a)** Runs threads with higher priority.
- **(b)** Assigns priorities to all threads.
- **(c)** Maintains states of executed, executing and non - executing threads.
- **(d)** Increases the priority of non - executing threads.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) maintains the states of executed, executing and non-executing threads**

**Why.** In this question bank's terms, the primary scheduler picks which high-priority thread runs and assigns priorities; the secondary scheduler keeps track of thread states (the bookkeeping).

**Concept: levels of scheduling.** Long-term (job) scheduler: admits jobs into memory. Medium-term: swaps processes out and in. Short-term (CPU) scheduler: picks the next ready process to run, very frequently.

{{< /details >}}

### 7 · Scheduling

*Asked by: Qualcomm (BITS Hyderabad 2024, Q27)*

Which scheduler is also called the **job scheduler**?

- **(a)** Intermediate-term
- **(b)** Long-term
- **(c)** Short-term
- **(d)** Medium-term

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) long-term**

**Why.** The long-term scheduler picks jobs from the job pool on disk and admits them into memory, which controls how many programs are in memory at once (the degree of multiprogramming).

**Concept: three schedulers.** Long-term (how many processes), medium-term (who is swapped out), short-term (who runs next on the CPU).

{{< /details >}}

### 8 · Scheduling

*Asked by: Qualcomm (Delhi campus 2024, Q40)*

Which of the CPU scheduling algorithms given in the options suffers from the **convoy effect**?

- **(a)** Multilevel queue
- **(b)** Shortest remaining time first
- **(c)** Round robin
- **(d)** First come first serve

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) first come first serve**

**Why.** In FCFS one long CPU-bound job holds the CPU while short I/O-bound jobs pile up behind it, like cars stuck behind a slow truck. Both CPU and device utilisation drop.

**Concept: convoy effect.** Non-preemptive, arrival-order scheduling lets one long job delay many short ones. Preemption (round robin) or shortest-job-first avoids it.

{{< /details >}}

### 9 · Scheduling

*Asked by: Qualcomm (2025 paper (campus not named), Q31)*

Round robin with time quantum 1. Five processes arrive at time 0 in the order A, B, C, D, E with burst times A = 4, B = 1, C = 8, D = 1, E = 2. What is the completion time of A?

- **(a)** 11
- **(b)** 4
- **(c)** 10
- **(d)** 12

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 11**

**Why.** Quantum 1; each round gives every unfinished process one unit, in order A, B, C, D, E.

| Time | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Runs | A | B | C | D | E | A | C | E | A | C | A |

B finishes at 2, D at 4, E at 8, A at 11; C runs alone afterwards and finishes at 16.

**Concept: round robin by hand.** Keep a queue. Run the front process for one quantum; if it is not finished, put it at the back. Write the timeline cell by cell.

{{< /details >}}

### 10 · Scheduling

*Asked by: Qualcomm (BITS Goa 2024, Q30)*

What is the average waiting time of a process if the scheduling queue holds on average 34 processes and 9 processes arrive every second?

- **(a)** 3.7 units
- **(b)** 2.9 units
- **(c)** 9 units
- **(d)** 4 units

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 3.7 units**

**Why.** Little's law: n = λ × W, where n is the average number in the queue (34), λ the arrival rate (9 per second), W the average wait. W = 34/9 ≈ 3.78, closest to 3.7.

**Concept: Little's law.** In any stable queue, average number in the system = arrival rate × average time spent. It holds regardless of the scheduling order or arrival pattern.

{{< /details >}}

### 11 · CPU and I/O busy together

*Asked by: Texas Instruments (BITS Pilani)*

Which keeps the CPU and I/O devices busy at the same time?

- **(a)** Preemptive scheduling
- **(b)** Multiprogramming
- **(c)** Spooling
- **(d)** All of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) all of these** (per the key; multiprogramming and spooling are the classic answers)

**Why.** Multiprogramming keeps several jobs in memory so the CPU runs one while another waits for I/O. Spooling buffers I/O on disk so devices work while the CPU computes. Preemptive scheduling helps by switching away from a process waiting on I/O.

**Concept: overlapping CPU and I/O.** I/O is slow, so a good OS always has some other work for the CPU while a device is busy.

{{< /details >}}
