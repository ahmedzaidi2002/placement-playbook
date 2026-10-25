---
title: "7 · Transactions and serializability"
linkTitle: "7 Transactions"
weight: 7
math: true
---
## 7.1 Transactions and ACID {#db-7-1}

<div class="nb nb-definition">

<strong>Definition</strong> — A **transaction** is a unit of work that must happen completely or not at all, e.g. moving ₹100 from account A to B (debit A, credit B).

</div>

| Property | Meaning | Ensured by |
|---|---|---|
| **Atomicity** | all or nothing | recovery (undo using the log) |
| **Consistency** | moves the database from one valid state to another (constraints hold) | the application + constraints |
| **Isolation** | concurrent transactions do not see each other's partial work | concurrency control (locks, MVCC) |
| **Durability** | once committed, survives crashes | recovery (redo, write-ahead log) |

**Transaction states:** active → partially committed (last statement done) → **committed**; or active → failed → **aborted** (rolled back; then restart or kill).

## 7.2 Why concurrency causes problems {#db-7-2}

| Anomaly | What happens |
|---|---|
| **Lost update** | T1 and T2 both read A = 100; T1 writes 150, T2 writes 120; T1's update is lost |
| **Dirty read** | T2 reads a value T1 wrote but has not committed; T1 then aborts |
| **Non-repeatable read** | T1 reads A twice and gets different values because T2 updated and committed in between |
| **Phantom read** | T1 runs the same `WHERE` query twice and gets new rows inserted by T2 |

## 7.3 Schedules and conflict serializability {#db-7-3}

A **schedule** interleaves the operations of several transactions. A **serial** schedule runs them one after another (always correct). A schedule is **serializable** if it gives the same result as some serial schedule.

Two operations **conflict** if they are from different transactions, touch the same item, and **at least one is a write**: read–write, write–read, write–write. (Read–read never conflicts.)

<div class="nb nb-theorem nb-block">

<strong>Precedence-graph test</strong>

Draw a node per transaction; for each conflicting pair where $T_i$'s operation comes first, add an edge $T_i \to T_j$. The schedule is **conflict serializable iff the graph has no cycle**; any topological order of the graph is an equivalent serial order.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Serializable)

$S$: $r_1(A)\ w_2(A)\ r_3(A)\ w_1(B)\ w_3(B)$. Conflicts: $r_1(A)$ before $w_2(A)$ → $T_1 \to T_2$; $w_2(A)$ before $r_3(A)$ → $T_2 \to T_3$; $w_1(B)$ before $w_3(B)$ → $T_1 \to T_3$. No cycle → serializable, equivalent to **$T_1, T_2, T_3$**.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Not serializable: the lost update)

$S$: $r_1(A)\ r_2(A)\ w_1(A)\ w_2(A)$. $r_1(A)$ before $w_2(A)$ → $T_1 \to T_2$; $r_2(A)$ before $w_1(A)$ → $T_2 \to T_1$. **Cycle** → not conflict serializable.

</div>

**View serializability** is weaker: same initial reads, same reads-from, same final writes as some serial schedule. Every conflict-serializable schedule is view serializable; the extra view-serializable ones have **blind writes** (a write without a read). Example: $r_1(A)\ w_2(A)\ w_1(A)\ w_3(A)$ is not conflict serializable but is view-equivalent to $T_1, T_2, T_3$. Testing view serializability is NP-complete, so systems use conflict serializability.

<div class="nb nb-example">

<strong>Example</strong> (Counting schedules)

$T_1$ has 2 operations and $T_2$ has 3, each keeping its own order: $\binom{5}{2} = $ **10** possible schedules, of which 2 are serial. With $k$ transactions there are $k!$ serial schedules.

</div>

## 7.4 Recoverability {#db-7-4}

If $T_2$ reads a value written by $T_1$:

| Class | Rule | Why |
|---|---|---|
| **Recoverable** | $T_1$ commits before $T_2$ commits | otherwise $T_1$ could abort after $T_2$ committed a value that never existed |
| **Cascadeless** | $T_2$ reads only **committed** data | avoids **cascading rollback** (one abort forcing others to abort) |
| **Strict** | no read **or write** of an item until its last writer commits/aborts | makes undo simple (restore the old value) |

Strict ⊂ cascadeless ⊂ recoverable.

<div class="nb nb-moral">

Conflicts are pairs with at least one write on the same item. Draw the precedence graph: no cycle means conflict serializable. Recoverable = readers commit after writers; cascadeless = read only committed data.

</div>
