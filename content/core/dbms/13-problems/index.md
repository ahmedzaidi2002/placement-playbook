---
title: "13 · Practice problems"
linkTitle: "13 Practice"
weight: 13
math: true
---
Fourteen OA-style problems on new examples. Try, then open the solution.

<div class="nb nb-problem nb-block" id="problem-db-1">

<strong>Problem 1</strong> (Super keys)

(a) $R(A, B, C, D, E, F)$ with candidate key $AB$: how many super keys? (b) $R(A, B, C, D)$ with candidate keys $A$ and $BC$?

<details class="nb-sol">
<summary>Solution</summary>

(a) $2^{6-2} = $ **16**. (b) $2^{3} + 2^{2} - 2^{4-3} = 8 + 4 - 2 = $ **10** (the 2 subtracted are supersets of $ABC$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-2">

<strong>Problem 2</strong> (Keys and normal form)

$R(A, B, C, D)$ with $AB \to C$, $C \to D$, $D \to A$. Find all candidate keys and the highest normal form.

<details class="nb-sol">
<summary>Solution</summary>

$B$ is on no right side, so every key contains $B$. $(AB)^+ = ABCD$, $(BC)^+ = BCDA$, $(BD)^+ = BDA \to$ with $AB \to C$ all. Keys: **AB, BC, BD**. All attributes are prime → **3NF**. Not BCNF: $C \to D$ and $C$ is not a super key.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-3">

<strong>Problem 3</strong> (Partial dependency)

$R(A, B, C, D)$, key $AB$, FDs $AB \to C$, $B \to D$. Normal form?

<details class="nb-sol">
<summary>Solution</summary>

$B \to D$: non-prime $D$ depends on part of the key → partial dependency → **1NF** only. Fix: split into $(A, B, C)$ and $(B, D)$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-4">

<strong>Problem 4</strong> (Lossless decomposition)

$R(A, B, C, D)$ with $A \to B$, $C \to D$. Is $\{(A, B), (C, D)\}$ lossless? Is $\{(A, B), (A, C, D)\}$?

<details class="nb-sol">
<summary>Solution</summary>

First: no common attribute → **lossy** (the join is a cross product). Second: common $A$, and $A \to B$ makes $A$ a key of $(A, B)$ → **lossless**, and both FDs are inside one piece → dependency preserving.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-5">

<strong>Problem 5</strong> (ER to tables)

Entities A, B, C. A–B is M:N, B–C is 1:N. Minimum number of tables?

<details class="nb-sol">
<summary>Solution</summary>

**4**: A, B, C, plus one table for the M:N relationship. The 1:N relationship becomes a foreign key in C (the N side).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-6">

<strong>Problem 6</strong> (NULLs and aggregates)

A column holds 10, NULL, 30, NULL. Values of `COUNT(*)`, `COUNT(col)`, `SUM(col)`, `AVG(col)`?

<details class="nb-sol">
<summary>Solution</summary>

4, 2, 40, **20** (average over the 2 non-NULL values, not 4).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-7">

<strong>Problem 7</strong> (Serializability)

(a) $r_1(X)\ r_2(X)\ w_3(X)$. (b) $w_1(A)\ r_2(A)\ w_2(B)\ r_1(B)$. Conflict serializable?

<details class="nb-sol">
<summary>Solution</summary>

(a) Edges $T_1 \to T_3$, $T_2 \to T_3$; no cycle → **yes**, equivalent to $T_1 T_2 T_3$ or $T_2 T_1 T_3$. (b) $w_1(A)$ before $r_2(A)$ → $T_1 \to T_2$; $w_2(B)$ before $r_1(B)$ → $T_2 \to T_1$. **Cycle → no.**

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-8">

<strong>Problem 8</strong> (Counting schedules)

$T_1$ and $T_2$ have 3 operations each. How many schedules, and how many are serial?

<details class="nb-sol">
<summary>Solution</summary>

$\binom{6}{3} = $ **20** schedules; **2** serial.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-9">

<strong>Problem 9</strong> (Recoverability)

$w_1(A)\ r_2(A)\ c_2\ c_1$: recoverable? What if $c_1$ comes before $c_2$?

<details class="nb-sol">
<summary>Solution</summary>

$T_2$ read $T_1$'s uncommitted value and committed first → **not recoverable**. With $c_1$ first → recoverable, but **not cascadeless** ($T_2$ still read uncommitted data).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-10">

<strong>Problem 10</strong> (Wait-die and wound-wait)

$T_5$ (timestamp 5) and $T_{10}$ (timestamp 10). What happens when (a) $T_5$ requests a lock held by $T_{10}$, (b) $T_{10}$ requests a lock held by $T_5$, under each scheme?

<details class="nb-sol">
<summary>Solution</summary>

$T_5$ is older. **Wait-die:** (a) $T_5$ waits; (b) $T_{10}$ dies. **Wound-wait:** (a) $T_5$ wounds $T_{10}$ (it aborts); (b) $T_{10}$ waits.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-11">

<strong>Problem 11</strong> (B+ tree order)

Block 1024 B, key 10 B, pointer 6 B. Maximum pointers in an internal node? Maximum keys in a leaf (with one next-leaf pointer)?

<details class="nb-sol">
<summary>Solution</summary>

Internal: $6p + 10(p - 1) \le 1024$ → $16p \le 1034$ → **$p = 64$**. Leaf: $16k + 6 \le 1024$ → **$k = 63$**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-12">

<strong>Problem 12</strong> (Index access cost)

100,000 records of 200 B, block 4096 B, sorted on the key. Block reads for binary search on the file, and with a primary index of 16-byte entries?

<details class="nb-sol">
<summary>Solution</summary>

$bfr = 20$ → 5,000 blocks → binary search $\lceil \log_2 5000 \rceil = $ **13**. Index: 256 entries per block, 5,000 entries → 20 index blocks → $\lceil \log_2 20 \rceil = 5$, plus 1 data block = **6**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-13">

<strong>Problem 13</strong> (Recovery)

Log at crash, no checkpoint: `<T1 start>` `<T1, X, 5, 7>` `<T2 start>` `<T2, Y, 1, 2>` `<T1 commit>` `<T3 start>` `<T3, Z, 8, 9>`. What is redone and undone?

<details class="nb-sol">
<summary>Solution</summary>

**Redo T1** (X = 7). **Undo T2 and T3** (Y = 1, Z = 8), scanning the log backwards.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-db-14">

<strong>Problem 14</strong> (Isolation level)

Which is the weakest isolation level that prevents non-repeatable reads? Which anomaly does it still allow (in the SQL standard)?

<details class="nb-sol">
<summary>Solution</summary>

**Repeatable read**; it still allows **phantom reads**.

</details>

</div>
