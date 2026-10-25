---
title: "8 · Concurrency control"
linkTitle: "8 Concurrency control"
weight: 8
math: true
---
[Chapter 7](../07-transactions/) judged finished schedules. A real DBMS cannot wait for a schedule to finish: its <strong>scheduler</strong> must decide, operation by operation, whether to run, delay or abort, so that only serializable (and recoverable) schedules are produced. The two families are <em>pessimistic</em> (locking: prevent conflicts) and <em>optimistic</em> or ordered (timestamps, validation, multiversioning: detect conflicts). The OS book covers the primitives (mutexes, semaphores); here they are applied to data items.

## 8.1 Locking and two-phase locking {#sec-dbms-2pl}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> strict 2PL turning the lost-update schedule into a deadlock instead of a wrong answer.</em>

</div>

### 8.1.i Shared and exclusive locks {#s8-1-i}

<div class="nb nb-definition" id="definition-8-1-1">

<strong>Definition 8.1.1</strong>. A transaction must hold a <strong>shared</strong> lock (S) on an item to read it and an <strong>exclusive</strong> lock (X) to write it. S is compatible with S; X is compatible with nothing. A request that is incompatible with a lock held by another transaction waits.

</div>

Locks alone are not enough. If $T_1$ unlocks $A$ as soon as it has written it, $T_2$ can then lock and update both $A$ and $B$, and $T_1$ later locks $B$: $T_1\to T_2$ on $A$ and $T_2\to T_1$ on $B$, a cycle, although every access was properly locked. What is missing is a rule about <em>when</em> locks may be released.

### 8.1.ii Two-phase locking {#s8-1-ii}

<div class="nb nb-definition" id="definition-8-1-2">

<strong>Definition 8.1.2</strong>. A transaction follows <strong>two-phase locking</strong> (2PL) if it acquires all its locks before it releases any: a <strong>growing</strong> phase (lock only) followed by a <strong>shrinking</strong> phase (unlock only). The moment of its last lock acquisition is its <strong>lock point</strong>. With <strong>lock conversion</strong>, upgrades (S$\to$X) are allowed only in the growing phase and downgrades (X$\to$S) only in the shrinking phase.

</div>

<div class="nb nb-theorem nb-block" id="theorem-8-1-3">

<strong>Theorem 8.1.3</strong>

If every transaction follows 2PL, every schedule produced is conflict serializable, and ordering the transactions by their lock points gives an equivalent serial order. The converse fails: some conflict-serializable schedules cannot be produced by 2PL.

</div>

<div class="nb nb-proof">

<em>Idea.</em> If $T_i\to T_j$ in the precedence graph, $T_j$ acquired a lock after $T_i$ released one on the same item, so $T_i$’s lock point is earlier than $T_j$’s. Edges therefore go from earlier to later lock points and cannot form a cycle.

</div>

| Variant | Rule | Serializable | Cascadeless | Deadlock-free |
|:--|:--|:-:|:-:|:-:|
| Basic 2PL | grow, then shrink | yes | no | no |
| Strict 2PL | \+ hold all X locks until commit/abort | yes | yes (strict) | no |
| Rigorous 2PL | \+ hold <em>all</em> locks until commit/abort; serial order = commit order | yes | yes (strict) | no |
| Conservative 2PL | lock everything needed before the first operation (or wait) | yes | no<sup>\*</sup> | yes |

<sup>\*</sup>Unless combined with strictness, which is what “conservative strict 2PL” means. Conservative 2PL needs the read and write sets in advance, so it is rare in general-purpose systems.

Basic 2PL allows cascading aborts: $T_1$ may unlock $A$ in its shrinking phase, $T_2$ reads it, and $T_1$ then aborts. Strict 2PL closes that hole and is what most lock-based systems implement (with locks taken implicitly by each statement and released at commit).

A small strict-2PL scheduler (`c08-2pl.py`; the part below grants or queues one request, the rest detects deadlocks and retries waiting transactions) shows what the lock manager does with two request sequences:

```python {filename="c08-2pl.py, lines 12–41",linenos=table,linenostart=12}
    def holders_blocking(t, op, x):
        held = locks.get(x, {})
        if op == "r":
            return [u for u, m in held.items() if u != t and m == "X"]
        return [u for u in held if u != t]

    def release(t):
        for x in list(locks):
            locks[x].pop(t, None)

    def step(t):
        op, x = txns[t][pc[t]]
        if op == "c":
            release(t)
            log.append(f"c{t} (unlock all)")
        else:
            block = holders_blocking(t, op, x)
            if block:
                waiting[t] = block
                log.append(f"T{t} waits for {'/'.join(f'T{u}' for u in block)}"
                           f" ({'S' if op == 'r' else 'X'} on {x})")
                return False
            mode = "X" if op == "w" else locks.get(x, {}).get(t, "S")
            locks.setdefault(x, {})[t] = mode
            log.append(f"{op}{t}({x})")
        waiting.pop(t, None)
        pc[t] += 1
        if pc[t] == len(txns[t]):
            done.add(t)
        return True
```

```text {filename="Output (Python 3.11)"}
lost update: requests in the order T1 T2 T1 T2 T1 T2
    r1(A)
    r2(A)
    T1 waits for T2 (X on A)
    T2 waits for T1 (X on A)
    deadlock T1 -> T2 -> T1: abort T2
    w1(A)
    c1 (unlock all)
transfer vs audit: requests in the order T1 T1 T2 T1 T1 T2 T1 T2
    r1(A)
    w1(A)
    T2 waits for T1 (S on A)
    r1(B)
    w1(B)
    c1 (unlock all)
    r2(A)
    r2(B)
    c2 (unlock all)
```

In the lost-update interleaving both transactions hold S on $A$ and each wants to upgrade to X: the classic <strong>upgrade deadlock</strong>. The scheduler breaks it by aborting $T_2$, so no update is lost; $T_2$ will be restarted. (`SELECT ... FOR UPDATE`, which takes the X lock at read time, avoids the upgrade.) In the second case the audit simply waits until the transfer commits: the result is the serial schedule $T_1T_2$.

<div class="nb nb-moral">

2PL gives serializability; holding locks to commit (strict 2PL) adds recoverability without cascades; neither prevents deadlock.

</div>

## 8.2 Deadlocks {#sec-dbms-deadlock}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> two transfers that lock the two accounts in opposite orders.</em>

</div>

<div class="nb nb-definition" id="definition-8-2-1">

<strong>Definition 8.2.1</strong>. A <strong>deadlock</strong> is a set of transactions each waiting for a lock held by another in the set. In the <strong>wait-for graph</strong> (an edge $T_i\to T_j$ when $T_i$ waits for $T_j$) a deadlock is exactly a cycle.

</div>

<div class="nb nb-definition" id="fact-8-2-2">

<strong>Fact 8.2.2</strong> (The three strategies). <strong>Prevention</strong> makes a cycle impossible: conservative 2PL (lock everything up front); a global order on items (always lock accounts in increasing id); or timestamp schemes that never let a younger transaction wait for an older one (or vice versa):

- <strong>wait-die</strong> (non-preemptive): an older requester waits, a younger requester dies (aborts and restarts);
- <strong>wound-wait</strong> (preemptive): an older requester wounds (aborts) the younger holder, a younger requester waits.

A restarted transaction keeps its <em>original</em> timestamp, so it eventually becomes the oldest and cannot starve. <strong>Avoidance</strong> checks each request against a model of future needs (Banker’s-style, <em>OS book</em>); databases rarely do it. <strong>Detection and recovery</strong> lets deadlocks happen, finds cycles in the wait-for graph (periodically or after a timeout) and aborts a <strong>victim</strong> (cheapest to roll back, fewest locks, youngest); this is what PostgreSQL, MySQL/InnoDB, Oracle and SQL Server do. Lock <strong>timeouts</strong> are the crudest version.

</div>

```text {filename="Output (Python 3.11)"}
requester holder | wait-die                        | wound-wait
   T5      T10  | T5 waits                        | T10 is wounded (aborted)
   T10     T5   | T10 dies (restarts, same TS)    | T10 waits
wait-for graph T1->T2, T2->T3, T3->T1, T4->T1
   cycle: T1 -> T2 -> T3 -> T1 (T4 waits but is not on it)
```

And a real one, on PostgreSQL: two sessions update rows 1 and 2 in opposite orders. The script runs the blocked statement in a thread and gives $T_2$ a shorter `deadlock_timeout`, so it is $T_2$ that runs the check, finds the cycle and is chosen as the victim:

```text {filename="Transcript of c08-pg-anomalies.py on PostgreSQL 16.14"}
8. Deadlock: opposite update order (T2 checks for deadlock first)
  T1: BEGIN
  T2: BEGIN
  T1: UPDATE acct SET bal = bal - 10 WHERE id = 1
  T2: UPDATE acct SET bal = bal - 10 WHERE id = 2
  T1: UPDATE acct SET bal = bal + 10 WHERE id = 2   ... waits (row lock)
  T2: UPDATE acct SET bal = bal + 10 WHERE id = 1 -> ERROR: deadlock detected
  T2: ROLLBACK
  T1: (resumes)
  T1: COMMIT
  T1: SELECT bal FROM acct ORDER BY id -> 90, 110
```

<div class="nb nb-moral">

Prevention orders the waiting (wait-die: old waits; wound-wait: old preempts); production systems detect cycles and abort a victim, and applications must retry.

</div>

## 8.3 Timestamp ordering {#sec-dbms-ts}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> an old transaction trying to write an item a younger one has already read.</em>

</div>

<div class="nb nb-definition" id="definition-8-3-1">

<strong>Definition 8.3.1</strong>. Each transaction gets a timestamp $TS(T)$ at start; the protocol forces the serial order to be timestamp order. Each item keeps $RTS(X)$ and $WTS(X)$, the largest timestamps that read and wrote it.

- $T$ reads $X$: if $WTS(X)>TS(T)$, a younger transaction already overwrote the value $T$ should have seen: abort $T$. Else read and set $RTS(X)=\max(RTS(X),TS(T))$.
- $T$ writes $X$: if $RTS(X)>TS(T)$, a younger transaction read the old value and would miss this write: abort $T$. If $WTS(X)>TS(T)$, abort $T$, or, under <strong>Thomas’ write rule</strong>, <em>ignore</em> the write: it is obsolete, since a younger write already superseded it and nobody read in between. Else write and set $WTS(X)=TS(T)$.

An aborted transaction restarts with a <em>new</em> timestamp.

</div>

```python {filename="c08-ts.py, lines 6–34",linenos=table,linenostart=6}
def timestamp_order(text, thomas=False):
    rts, wts, dead, log = {}, {}, set(), []
    for tok in text.split():
        op, t, x = re.fullmatch(r"([rw])(\d+)\((\w)\)", tok).groups()
        t = int(t)
        if t in dead:
            continue
        r, w = rts.get(x, 0), wts.get(x, 0)
        if op == "r":
            if w > t:
                verdict = f"reject, WTS({x})={w} > {t}: abort T{t}"
                dead.add(t)
            else:
                rts[x] = max(r, t)
                verdict = f"ok, RTS({x})={rts[x]}"
        else:
            if r > t:
                verdict = f"reject, RTS({x})={r} > {t}: abort T{t}"
                dead.add(t)
            elif w > t and thomas:
                verdict = f"ignore (obsolete write, WTS({x})={w})"
            elif w > t:
                verdict = f"reject, WTS({x})={w} > {t}: abort T{t}"
                dead.add(t)
            else:
                wts[x] = t
                verdict = f"ok, WTS({x})={t}"
        log.append(f"{tok:7} {verdict}")
    return log
```

```text {filename="Output (Python 3.11)"}
r1(A) w2(A) w1(A) w1(B)  basic TO
    r1(A)   ok, RTS(A)=1
    w2(A)   ok, WTS(A)=2
    w1(A)   reject, WTS(A)=2 > 1: abort T1
r1(A) w2(A) w1(A) w1(B)  Thomas write rule
    r1(A)   ok, RTS(A)=1
    w2(A)   ok, WTS(A)=2
    w1(A)   ignore (obsolete write, WTS(A)=2)
    w1(B)   ok, WTS(B)=1
r2(A) r1(B) w1(A) w2(B)  basic TO
    r2(A)   ok, RTS(A)=2
    r1(B)   ok, RTS(B)=1
    w1(A)   reject, RTS(A)=2 > 1: abort T1
    w2(B)   ok, WTS(B)=2
r2(A) r1(B) w1(A) w2(B)  Thomas write rule
    r2(A)   ok, RTS(A)=2
    r1(B)   ok, RTS(B)=1
    w1(A)   reject, RTS(A)=2 > 1: abort T1
    w2(B)   ok, WTS(B)=2
OCC: T2 passes | T3 fails against T1: wrote ['A']
OCC: T3 starting after T1 finished: passes
```

<div class="nb nb-definition" id="fact-8-3-2">

<strong>Fact 8.3.2</strong>. Basic timestamp ordering produces conflict-serializable schedules, has no waiting and hence no deadlock, but allows cascading aborts and non-recoverable schedules unless commits are also ordered (a “strict” variant delays reads of uncommitted writes), and a long transaction can starve by being restarted repeatedly. With Thomas’ write rule it accepts some view-serializable schedules that are not conflict serializable (the first example). 2PL and timestamp ordering are incomparable: each admits schedules the other rejects.

</div>

## 8.4 Validation (optimistic concurrency control) {#sec-dbms-occ}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a mostly-read workload where locks would only cost time.</em>

</div>

<div class="nb nb-definition" id="definition-8-4-1">

<strong>Definition 8.4.1</strong>. Each transaction runs in three phases: <strong>read</strong> (execute on private copies, recording the read set $RS$ and write set $WS$), <strong>validation</strong> (check for conflicts), and <strong>write</strong> (install the writes). Its timestamp is the time it enters validation. $T_j$ passes validation if, for every $T_i$ with an earlier timestamp, either $T_i$ finished before $T_j$ started, or $T_i$ finished its write phase before $T_j$ began validation and $WS(T_i)\cap RS(T_j)=\emptyset$.

</div>

The output above shows $T_3$ failing: $T_1$ wrote $A$ while $T_3$ (which read $A$) was running. Started after $T_1$ finished, it passes. Optimistic control has no locks and no deadlocks but wastes the work of every failed transaction, so it suits low-contention workloads; the same idea appears as version-number checks in application code (`UPDATE ... SET v = v + 1 WHERE id = ? AND v = ?`, retry if no row matched).

## 8.5 Multiversion concurrency control and snapshot isolation {#sec-dbms-mvcc}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a long report that reads a consistent snapshot while transfers keep committing.</em>

</div>

<div class="nb nb-definition" id="definition-8-5-1">

<strong>Definition 8.5.1</strong>. <strong>Multiversion concurrency control</strong> (MVCC) keeps several versions of each item. A write creates a new version stamped with the writer’s transaction id; a read sees the latest version committed before its <strong>snapshot</strong>. Readers never block writers and writers never block readers; only writers of the same item conflict. Old versions are removed when no snapshot can need them (PostgreSQL’s `VACUUM`, Oracle’s and MySQL’s undo segments).

</div>

In PostgreSQL every row version carries `xmin` (the creating transaction) and `xmax` (the deleting or updating one), and an `UPDATE` writes a whole new version:

```sql {filename="c08-mvcc.sql"}
-- PostgreSQL keeps old row versions; ctid = (page, slot) of the version
CREATE TABLE acct (id INTEGER PRIMARY KEY, bal INTEGER);
INSERT INTO acct VALUES (1, 100);
CREATE TABLE before AS SELECT ctid AS old_ctid, xmin AS old_xmin FROM acct;

UPDATE acct SET bal = 150 WHERE id = 1;
-- Q1 an UPDATE writes a NEW version: new ctid, new creating transaction
SELECT a.ctid AS new_ctid, b.old_ctid, a.xmin <> b.old_xmin AS new_xmin
FROM acct a, before b;
```

```text {filename="Result on PostgreSQL 16.14"}
 new_ctid | old_ctid | new_xmin
----------+----------+----------
 (0,2)    | (0,1)    | true
(1 row)
```

<div class="nb nb-definition" id="definition-8-5-2">

<strong>Definition 8.5.2</strong>. <strong>Snapshot isolation</strong> (SI): every transaction reads from a snapshot taken at its start (its own writes included), and it can commit only if no other transaction that committed after its snapshot wrote an item it also wrote (<strong>first-committer-wins</strong>; PostgreSQL checks at the moment of the second write, <strong>first-updater-wins</strong>).

</div>

SI prevents dirty reads, non-repeatable reads, phantoms and lost updates, but it is <em>not</em> serializable: two transactions that read overlapping data and write <em>different</em> items can both commit and break an invariant neither broke alone (<strong>write skew</strong>, demo 6 below). <strong>Serializable snapshot isolation</strong> (SSI, PostgreSQL’s `SERIALIZABLE` since 9.1) tracks read–write dependencies between concurrent transactions and aborts one when a dangerous cycle could form (demo 7).

<div class="nb nb-moral">

MVCC lets readers and writers pass each other; snapshot isolation is strong but allows write skew, which only true serializable isolation catches.

</div>

## 8.6 Isolation levels and anomalies {#sec-dbms-isolation}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the same two transactions run at four isolation levels on PostgreSQL.</em>

</div>

<div class="nb nb-definition" id="definition-8-6-1">

<strong>Definition 8.6.1</strong> (Anomalies). Five things that go wrong when transactions interleave:

- <strong>Dirty read</strong>: reading a value written by a transaction that has not committed (and may abort).
- <strong>Non-repeatable read</strong>: reading the same row twice and getting different values, because another transaction committed an update in between.
- <strong>Phantom</strong>: re-running a query with a condition and getting a different <em>set</em> of rows, because another transaction inserted or deleted matching rows.
- <strong>Lost update</strong>: two read–modify–write cycles on the same item; the second write overwrites the first.
- <strong>Write skew</strong>: two transactions read overlapping data, write disjoint items, and together violate a constraint.

</div>

| Level (SQL standard) | Dirty read | Non-repeatable | Phantom | In PostgreSQL 16.14 |
|:--|:-:|:-:|:-:|:--|
| `READ UNCOMMITTED` | possible | possible | possible | behaves as `READ COMMITTED` |
| `READ COMMITTED` | no | possible | possible | snapshot per statement; the default |
| `REPEATABLE READ` | no | no | possible | snapshot isolation: no phantoms, no lost update, write skew possible |
| `SERIALIZABLE` | no | no | no | SSI: serializable |

The standard defines the levels by the anomalies they forbid, so an implementation may give more. Defaults differ: `READ COMMITTED` in PostgreSQL, Oracle and SQL Server; `REPEATABLE READ` in MySQL/InnoDB; SQLite allows one writer at a time and is serializable. Oracle’s `SERIALIZABLE` is snapshot isolation.

The demos below are real: two connections to one PostgreSQL database, statements issued in the order shown (the full script is `c08-pg-anomalies.py`).

```text {filename="Transcript on PostgreSQL 16.14"}
1. Dirty read? T2 asks for READ UNCOMMITTED
  T1: BEGIN
  T1: UPDATE acct SET bal = 999 WHERE id = 1
  T2: BEGIN ISOLATION LEVEL READ UNCOMMITTED
  T2: SELECT bal FROM acct WHERE id = 1 -> 100
  T1: ROLLBACK
  T2: COMMIT
```

No dirty read is possible in PostgreSQL even when asked for: it reads the committed $100$.

```text {filename="Transcript on PostgreSQL 16.14"}
2. Non-repeatable read and phantom, T2 at READ COMMITTED
  T2: BEGIN ISOLATION LEVEL READ COMMITTED
  T2: SELECT bal FROM acct WHERE id = 1 -> 100
  T2: SELECT COUNT(*) FROM acct -> 2
  T1: UPDATE acct SET bal = 200 WHERE id = 1
  T1: INSERT INTO acct VALUES (3, 50)
  T2: SELECT bal FROM acct WHERE id = 1 -> 200
  T2: SELECT COUNT(*) FROM acct -> 3
  T2: COMMIT
```

```text {filename="Transcript on PostgreSQL 16.14"}
3. Non-repeatable read and phantom, T2 at REPEATABLE READ
  T2: BEGIN ISOLATION LEVEL REPEATABLE READ
  T2: SELECT bal FROM acct WHERE id = 1 -> 100
  T2: SELECT COUNT(*) FROM acct -> 2
  T1: UPDATE acct SET bal = 200 WHERE id = 1
  T1: INSERT INTO acct VALUES (3, 50)
  T2: SELECT bal FROM acct WHERE id = 1 -> 100
  T2: SELECT COUNT(*) FROM acct -> 2
  T2: COMMIT
```

At `READ COMMITTED` every statement takes a new snapshot, so $T_2$ sees $T_1$’s committed update (non-repeatable read) and insert (phantom). At `REPEATABLE READ` the snapshot is taken once, at the first query, and both reads repeat.

```text {filename="Transcript on PostgreSQL 16.14"}
4. Lost update (read, add 100 in the app, write); READ COMMITTED
  T1: BEGIN ISOLATION LEVEL READ COMMITTED
  T2: BEGIN ISOLATION LEVEL READ COMMITTED
  T1: SELECT bal FROM acct WHERE id = 1 -> 100
  T2: SELECT bal FROM acct WHERE id = 1 -> 100
  T1: UPDATE acct SET bal = 200 WHERE id = 1
  T2: UPDATE acct SET bal = 200 WHERE id = 1   ... waits (row lock)
  T1: COMMIT
  T2: (resumes)
  T2: COMMIT
  T1: SELECT bal FROM acct WHERE id = 1 -> 200
```

```text {filename="Transcript on PostgreSQL 16.14"}
5. Lost update (read, add 100 in the app, write); REPEATABLE READ
  T1: BEGIN ISOLATION LEVEL REPEATABLE READ
  T2: BEGIN ISOLATION LEVEL REPEATABLE READ
  T1: SELECT bal FROM acct WHERE id = 1 -> 100
  T2: SELECT bal FROM acct WHERE id = 1 -> 100
  T1: UPDATE acct SET bal = 200 WHERE id = 1
  T2: UPDATE acct SET bal = 200 WHERE id = 1   ... waits (row lock)
  T1: COMMIT
  T2: (resumes) -> ERROR: could not serialize access due to concurrent update
  T2: COMMIT
  T1: SELECT bal FROM acct WHERE id = 1 -> 200
```

Both clients read $100$ and write $100+100$. At `READ COMMITTED` $T_2$ waits for $T_1$’s row lock, then simply overwrites: the balance is $200$, not $300$; one deposit is lost. At `REPEATABLE READ` the second writer is aborted with a serialization error and must retry. The robust fixes at any level: compute in SQL (`SET bal = bal + 100`), lock on read (`SELECT ... FOR UPDATE`), or an optimistic version check.

```text {filename="Transcript on PostgreSQL 16.14"}
6. Write skew (go off call if someone else is on); REPEATABLE READ
  T1: BEGIN ISOLATION LEVEL REPEATABLE READ
  T2: BEGIN ISOLATION LEVEL REPEATABLE READ
  T1: SELECT COUNT(*) FROM doctors WHERE on_call -> 2
  T2: SELECT COUNT(*) FROM doctors WHERE on_call -> 2
  T1: UPDATE doctors SET on_call = false WHERE name = 'Alok'
  T2: UPDATE doctors SET on_call = false WHERE name = 'Bela'
  T1: COMMIT
  T2: COMMIT
  T1: SELECT COUNT(*) FROM doctors WHERE on_call -> 0
```

```text {filename="Transcript on PostgreSQL 16.14"}
7. Write skew (go off call if someone else is on); SERIALIZABLE
  T1: BEGIN ISOLATION LEVEL SERIALIZABLE
  T2: BEGIN ISOLATION LEVEL SERIALIZABLE
  T1: SELECT COUNT(*) FROM doctors WHERE on_call -> 2
  T2: SELECT COUNT(*) FROM doctors WHERE on_call -> 2
  T1: UPDATE doctors SET on_call = false WHERE name = 'Alok'
  T2: UPDATE doctors SET on_call = false WHERE name = 'Bela'
  T1: COMMIT
  T2: COMMIT -> ERROR: could not serialize access due to read/write
        dependencies among transactions
  T1: SELECT COUNT(*) FROM doctors WHERE on_call -> 1
```

The rule “at least one doctor on call” is checked by each transaction against its own snapshot, where two doctors are on call; they update different rows, so snapshot isolation sees no write–write conflict and both commit: nobody is on call. `SERIALIZABLE` detects the read–write dependency cycle and aborts the second committer.

<div class="nb nb-remark" id="remark-8-6-2">

<strong>Remark 8.6.2</strong> (Applications must retry) — Under `REPEATABLE READ` and `SERIALIZABLE` (and after any deadlock), a transaction can fail through no fault of its own with SQLSTATE `40001` (serialization failure) or `40P01` (deadlock); the correct response is to roll back and run the whole transaction again. Code that does not retry should not ask for these levels.

</div>

<div class="nb nb-moral">

Know the four anomalies of the standard plus lost update and write skew, which level stops each, and that PostgreSQL’s levels are stronger than the standard’s minimum.

</div>

## 8.7 Lock granularity and intention locks {#sec-dbms-granularity}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> one transaction updates a row while another wants to lock the whole table.</em>

</div>

Locking a whole table costs one lock but blocks everyone; locking rows maximizes concurrency but costs a lock per row. <strong>Multiple-granularity locking</strong> lets each transaction lock at the level it needs in a hierarchy (database $\to$ table $\to$ page $\to$ row). To lock a node in S or X, a transaction must first hold an <strong>intention</strong> lock on every ancestor: <strong>IS</strong> (will lock something below in S), <strong>IX</strong> (will lock something below in X), or <strong>SIX</strong> (S on this node plus IX: read all, update some). Locks are taken root to leaf and released leaf to root. Then a table-level X request conflicts with a row-level X immediately, at the table node, without scanning the rows.

| held $\backslash$ requested | IS | IX | S | SIX | X |
|:-:|:-:|:-:|:-:|:-:|:-:|
| IS | yes | yes | yes | yes | no |
| IX | yes | yes | no | no | no |
| S | yes | no | yes | no | no |
| SIX | yes | no | no | no | no |
| X | no | no | no | no | no |

When a transaction holds too many fine locks, the system may <strong>escalate</strong> them to one coarser lock (SQL Server does; PostgreSQL does not escalate row locks, which it stores in the rows themselves). Coarser granularity means less overhead and less concurrency.

<div class="nb nb-moral">

Intention locks let a coarse lock and fine locks check each other at the top of the hierarchy.

</div>
