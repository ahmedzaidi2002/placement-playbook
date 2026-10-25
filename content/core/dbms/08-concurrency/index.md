---
title: "8 · Concurrency control"
linkTitle: "8 Concurrency control"
weight: 8
math: true
---
## 8.1 Locks {#db-8-1}

- **Shared (S) lock:** for reading; many transactions can hold it together.
- **Exclusive (X) lock:** for writing; nobody else can hold any lock on the item.

| Held \ Requested | S | X |
|---|---|---|
| **S** | ✓ | ✗ |
| **X** | ✗ | ✗ |

## 8.2 Two-phase locking (2PL) {#db-8-2}

<div class="nb nb-definition">

<strong>Definition</strong> — **2PL:** a transaction first acquires locks (**growing phase**) and then releases them (**shrinking phase**); once it releases any lock, it may not acquire a new one.

</div>

- **2PL guarantees conflict serializability** (order transactions by their lock point).
- It does **not** prevent **deadlocks**, and basic 2PL allows **cascading rollbacks**.
- **Strict 2PL:** hold all **X locks** until commit/abort → no cascading rollback (strict schedules). What most databases use.
- **Rigorous 2PL:** hold **all** locks until commit.

## 8.3 Deadlocks in databases {#db-8-3}

Detected with a **wait-for graph** (cycle → deadlock → abort a victim, usually the youngest or the cheapest). Or prevented with timestamps (older = smaller timestamp = higher priority):

| Scheme | Older wants a lock held by younger | Younger wants a lock held by older |
|---|---|---|
| **Wait-die** (non-preemptive) | older **waits** | younger **dies** (aborts, restarts with the same timestamp) |
| **Wound-wait** (preemptive) | older **wounds** (aborts) the younger | younger **waits** |

In both, only younger transactions are aborted, and a restarted transaction keeps its original timestamp, so it eventually becomes the oldest: **no starvation**.

## 8.4 Timestamp ordering {#db-8-4}

Each transaction gets a timestamp when it starts; the schedule must be equivalent to running them in timestamp order. Each item keeps the largest read-timestamp and write-timestamp seen.

- $T$ reads $X$: if a **younger** transaction already wrote $X$ → abort $T$.
- $T$ writes $X$: if a younger transaction already read or wrote $X$ → abort $T$.
- **Thomas write rule:** if a younger transaction already *wrote* $X$, just **ignore** $T$'s obsolete write instead of aborting.

No locks, so **no deadlocks**, but more aborts.

## 8.5 Optimistic and multiversion control {#db-8-5}

- **Optimistic (validation-based):** run without locks, then at commit check whether anything you read was changed by others; if so, abort and retry. Good when conflicts are rare.
- **MVCC (multiversion):** writers create new versions; each reader sees a consistent **snapshot** as of its start time. **Readers never block writers and writers never block readers.** Used by PostgreSQL, Oracle, MySQL InnoDB.
- **Snapshot isolation** prevents dirty, non-repeatable and phantom reads but allows **write skew** (two transactions read the same data, update different rows, and together break a rule, e.g. both doctors go off call).

## 8.6 Isolation levels {#db-8-6}

| Level | Dirty read | Non-repeatable read | Phantom |
|---|---|---|---|
| **Read uncommitted** | possible | possible | possible |
| **Read committed** | prevented | possible | possible |
| **Repeatable read** | prevented | prevented | possible (standard) |
| **Serializable** | prevented | prevented | prevented |

Defaults: **PostgreSQL, Oracle, SQL Server → Read Committed; MySQL InnoDB → Repeatable Read**. Higher isolation = fewer anomalies but less concurrency.

## 8.7 Lock granularity {#db-8-7}

Locks can be on a database, table, page or row. Fine (row) locks → more concurrency, more overhead; coarse (table) locks → the reverse. **Intention locks** (IS, IX, SIX) on a table say "I hold or will take S/X locks on some rows inside", so a request for a whole-table lock can be checked without scanning every row lock. **Lock escalation:** many row locks turn into one table lock.

<div class="nb nb-moral">

2PL (grow, then shrink) guarantees serializability but not freedom from deadlock; strict 2PL also prevents cascading aborts. Wait-die: old waits, young dies. Wound-wait: old wounds, young waits. MVCC lets readers and writers not block each other.

</div>
