---
title: "13 · Practice problems"
linkTitle: "13 Practice"
weight: 13
math: true
---
Fifteen OA-style numericals, each on a new example. Try it, then open the solution.

<div class="nb nb-problem nb-block" id="problem-os-1">

<strong>Problem 1</strong> (Four schedulers)

Processes (arrival, burst): P1 (0, 5), P2 (1, 3), P3 (2, 1), P4 (3, 2). Average waiting time under FCFS, SJF (non-preemptive), SRTF and RR with $q = 2$?

<details class="nb-sol">
<summary>Solution</summary>

- **FCFS:** P1 0–5, P2 5–8, P3 8–9, P4 9–11. Waiting 0, 4, 6, 6 → **4.0**.
- **SJF:** P1 0–5; then shortest first: P3 5–6, P4 6–8, P2 8–11. Waiting 0, 7, 3, 3 → **3.25**.
- **SRTF:** P1 0–1, P2 1–2, P3 2–3 (shortest), P2 3–5 (tie with P4 broken by arrival), P4 5–7, P1 7–11. Waiting 6, 1, 0, 2 → **2.25**.
- **RR q=2:** P1 0–2, P2 2–4, P3 4–5, P1 5–7, P4 7–9, P2 9–10, P1 10–11. Completion 11, 10, 5, 9 → waiting 6, 6, 2, 4 → **4.5**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-2">

<strong>Problem 2</strong> (Round-robin overhead)

Quantum 10 ms, context switch 2 ms, all processes CPU-bound. CPU utilisation?

<details class="nb-sol">
<summary>Solution</summary>

Each 12 ms does 10 ms of work: $10/12 = $ **83.3%**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-3">

<strong>Problem 3</strong> (RMS vs EDF)

Tasks (C, T): (2, 5) and (4, 7). Schedulable by RMS? By EDF?

<details class="nb-sol">
<summary>Solution</summary>

$U = 0.4 + 0.571 = 0.971$. Above the RMS bound 0.828, and in fact RMS fails: task 1 runs 0–2, task 2 runs 2–5, task 1 runs 5–7, so task 2 has had only 3 of its 4 units by its deadline 7. EDF works since $U \le 1$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-4">

<strong>Problem 4</strong> (fork)

How many processes exist after `for (i = 0; i < 4; i++) fork();`, and how many times does a `printf("x\n")` placed after the loop print?

<details class="nb-sol">
<summary>Solution</summary>

$2^4 = $ **16** processes (15 created); "x" prints **16** times.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-5">

<strong>Problem 5</strong> (Semaphore)

A counting semaphore starts at 5. 12 `wait` and 9 `signal` operations are performed. Final value?

<details class="nb-sol">
<summary>Solution</summary>

$5 - 12 + 9 = $ **2**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-6">

<strong>Problem 6</strong> (Deadlock-free resources)

4 processes each need up to 3 units of a resource. Minimum units that guarantee no deadlock?

<details class="nb-sol">
<summary>Solution</summary>

$4 \times (3 - 1) + 1 = $ **9**. With 8, each could hold 2 and wait for a third.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-7">

<strong>Problem 7</strong> (Banker's)

Resources (A, B) total (6, 4). Allocation: P0 (1, 1), P1 (2, 1), P2 (1, 1). Max: P0 (3, 2), P1 (4, 3), P2 (2, 2). Is the state safe? Should P1's request (1, 1) be granted?

<details class="nb-sol">
<summary>Solution</summary>

Available $= (6, 4) - (4, 3) = (2, 1)$. Need: P0 (2, 1), P1 (2, 2), P2 (1, 1). Safety: P0 fits → work (3, 2) → P1 → (5, 3) → P2 → (6, 4). **Safe** ⟨P0, P1, P2⟩.

Request (1, 1): within P1's need and available, so pretend: Available (1, 0), P1 need (1, 1). Now no process's need fits in (1, 0) → **unsafe → deny** (P1 waits).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-8">

<strong>Problem 8</strong> (Fit policies)

Holes: 200, 50, 400, 150 KB. Requests: 120, 300, 180 KB. First fit vs best fit?

<details class="nb-sol">
<summary>Solution</summary>

**First fit:** 120 → 200 (80 left), 300 → 400 (100 left), 180 → no hole ≥ 180 → **waits**. **Best fit:** 120 → 150, 300 → 400, 180 → 200: **all fit**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-9">

<strong>Problem 9</strong> (Address translation)

Page size 1 KB. Logical address 5000. Page 4 is in frame 7. Page number, offset, physical address?

<details class="nb-sol">
<summary>Solution</summary>

Page $\lfloor 5000/1024 \rfloor = 4$, offset $5000 - 4096 = 904$, physical $7 \times 1024 + 904 = $ **8072**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-10">

<strong>Problem 10</strong> (EAT, two-level page table)

TLB 10 ns, memory 80 ns, hit ratio 0.9, two-level page table. Effective access time?

<details class="nb-sol">
<summary>Solution</summary>

Hit: $10 + 80 = 90$. Miss: $10 + 2 \times 80$ (table) $+ 80$ (data) $= 250$. EAT $= 0.9 \times 90 + 0.1 \times 250 = $ **106 ns**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-11">

<strong>Problem 11</strong> (Page faults)

Reference string 7 0 1 2 0 3 0 4 2 3, 3 frames, initially empty. Faults under FIFO, LRU and OPT?

<details class="nb-sol">
<summary>Solution</summary>

- **FIFO:** faults on 7, 0, 1, 2, 3, 0, 4, 2, 3 → **9**.
- **LRU:** 7, 0, 1, 2 fault; 0 hit; 3 faults (evicts 1); 0 hit; 4 faults (evicts 2); 2 faults (evicts 3); 3 faults (evicts 0) → **8**.
- **OPT:** 7, 0, 1 fault; 2 evicts 7 (never used again); 0 hit; 3 evicts 1; 0 hit; 4 evicts 0; 2, 3 hit → **6**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-12">

<strong>Problem 12</strong> (Page-fault rate)

Memory access 100 ns, page-fault service 10 ms. What fault rate keeps the effective access time at most 200 ns?

<details class="nb-sol">
<summary>Solution</summary>

$(1-p)\,100 + p \times 10^7 \le 200$ → $p \le 100/(10^7 - 100) \approx$ **$10^{-5}$**: at most one fault per 100,000 accesses.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-13">

<strong>Problem 13</strong> (Inode)

Block 1 KB, pointer 4 bytes, 10 direct pointers plus single, double and triple indirect. Maximum file size?

<details class="nb-sol">
<summary>Solution</summary>

$k = 1024/4 = 256$. $(10 + 256 + 256^2 + 256^3) \times 1$ KB $= 10$ KB $+ 256$ KB $+ 64$ MB $+ 16$ GB ≈ **16 GB**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-14">

<strong>Problem 14</strong> (Disk scheduling)

Cylinders 0–199, head at 50 moving up. Requests: 82, 170, 43, 140, 24, 16, 190. Total head movement under FCFS, SSTF, SCAN and LOOK?

<details class="nb-sol">
<summary>Solution</summary>

- **FCFS:** 32 + 88 + 127 + 97 + 116 + 8 + 174 = **642**.
- **SSTF:** 50 → 43 → 24 → 16 → 82 → 140 → 170 → 190: 7 + 19 + 8 + 66 + 58 + 30 + 20 = **208**.
- **SCAN:** up to 199 then down to 16: $(199 - 50) + (199 - 16) = $ **332**.
- **LOOK:** up to 190 then down to 16: $140 + 174 = $ **314**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-os-15">

<strong>Problem 15</strong> (TLB reach and page-table size)

(a) A TLB has 64 entries and pages are 4 KB: how much memory does it cover? (b) 32-bit addresses, 8 KB pages, 4-byte entries: page-table size?

<details class="nb-sol">
<summary>Solution</summary>

(a) $64 \times 4$ KB = **256 KB**. (b) Offset 13 bits, so $2^{19}$ pages × 4 B = **2 MB**.

</details>

</div>
