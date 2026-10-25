---
title: "9 · Recovery"
linkTitle: "9 Recovery"
weight: 9
math: true
---
## 9.1 Failures, storage and buffer policies {#sec-dbms-failures}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the power fails one millisecond after the database told the client “committed”.</em>

</div>

<div class="nb nb-definition" id="definition-9-1-1">

<strong>Definition 9.1.1</strong>. Failures: a <strong>transaction failure</strong> (logical error, deadlock victim, constraint violation), a <strong>system crash</strong> (power, OS, DBMS bug: main memory lost, disk intact), and a <strong>media failure</strong> (disk lost: restore from a backup and replay the archived log). Storage: <strong>volatile</strong> (RAM, the buffer pool), <strong>non-volatile</strong> (disk, SSD) and <strong>stable</strong> (survives everything; approximated by replication and mirrored logs).

</div>

The recovery manager must guarantee atomicity and durability no matter which pages the buffer manager happened to write before the crash. Two buffer-manager decisions determine how much work that is:

<div class="nb nb-definition" id="definition-9-1-2">

<strong>Definition 9.1.2</strong>. <strong>Steal</strong>: a page modified by an uncommitted transaction may be written to disk (to free a buffer frame). <strong>Force</strong>: all pages a transaction modified are written to disk at its commit.

</div>

|  | Force | No-force |
|:--|:--|:--|
| No-steal | no undo, no redo; slow commits, buffer pool pinned by long transactions | redo only (deferred update) |
| Steal | undo only | <strong>undo and redo</strong>: what real systems (ARIES) do, because it is the fastest at run time |

Steal means uncommitted data may be on disk at a crash, so the log must allow <em>undo</em>; no-force means committed data may be missing from disk, so the log must allow <em>redo</em>.

<div class="nb nb-moral">

Steal requires undo, no-force requires redo; the log provides both, so the buffer manager can do whatever is fastest.

</div>

## 9.2 Log-based recovery and write-ahead logging {#sec-dbms-wal}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `<T1, A, 500, 400>`: transaction $T_1$ changed $A$ from $500$ to $400$.</em>

</div>

<div class="nb nb-definition" id="definition-9-2-1">

<strong>Definition 9.2.1</strong>. The <strong>log</strong> is an append-only sequence of records on stable storage: `<T start>`, `<T, X, old, new>` (an update with before- and after-image), `<T commit>`, `<T abort>`. <strong>Write-ahead logging</strong> (WAL) has two rules: (1) the log record of an update reaches stable storage <em>before</em> the data page it describes (so undo is always possible), and (2) all log records of a transaction, including `<T commit>`, reach stable storage before the commit is acknowledged (so redo is always possible). A transaction is committed exactly when its commit record is on stable storage.

</div>

<div class="nb nb-definition" id="fact-9-2-2">

<strong>Fact 9.2.2</strong> (Deferred and immediate update). With <strong>deferred update</strong>, a transaction writes nothing to the database until it commits (no-steal); recovery only <em>redoes</em> committed transactions (“NO-UNDO/REDO”), and the log needs only new values. With <strong>immediate update</strong>, changes may reach the database before commit (steal); recovery must <em>undo</em> incomplete transactions and <em>redo</em> committed ones (“UNDO/REDO”), and the log needs both images.

</div>

<div class="nb nb-remark" id="algorithm-9-2-3">

<strong>Algorithm 9.2.3</strong> (Undo/redo recovery after a crash) — Scan the log. Every transaction with `<T start>` but no `<T commit>` or `<T abort>` is a <strong>loser</strong> and goes on the undo list. Then redo <em>every</em> update forward, in log order (<strong>repeating history</strong>, which also redoes losers’ updates, harmlessly), and finally undo the losers’ updates backward, newest first, writing a <strong>compensation log record</strong> (CLR, a redo-only record of the undo) for each, and then `<T abort>`. Redo and undo must be <strong>idempotent</strong>: a crash during recovery just restarts it.

</div>

```python {filename="c09-recovery.py, lines 1–27",linenos=table,linenostart=1}
# Undo/redo recovery with immediate update: after a crash, redo every logged
# update forward (repeating history), then undo the transactions that have
# no <commit>/<abort>, backward, writing compensation records.
LOG = [("start", "T1"),
       ("upd", "T1", "A", 500, 400),        # <T1, A, old 500, new 400>
       ("upd", "T1", "B", 300, 400),
       ("commit", "T1"),
       ("start", "T2"),
       ("upd", "T2", "C", 900, 700),
       ("start", "T3"),
       ("upd", "T3", "A", 400, 450),
       ("commit", "T2"),
       ("upd", "T3", "B", 400, 380)]


def recover(log):
    db = {"A": 500, "B": 300, "C": 900}   # disk may hold any mix of old/new
    finished = {r[1] for r in log if r[0] in ("commit", "abort")}
    started = [r[1] for r in log if r[0] == "start"]
    for r in log:                          # redo phase: forward
        if r[0] == "upd":
            db[r[2]] = r[4]
    undo = [t for t in started if t not in finished]
    for r in reversed(log):                # undo phase: backward
        if r[0] == "upd" and r[1] in undo:
            db[r[2]] = r[3]                # (and log <T, X, old> as a CLR)
    return finished, undo, db
```

```text {filename="Output (Python 3.11)"}
crash after record  3 (upd T1 B 300 400)
   committed: -        undo: T1       final A=500 B=300 C=900
crash after record  6 (upd T2 C 900 700)
   committed: T1       undo: T2       final A=400 B=400 C=900
crash after record  9 (commit T2)
   committed: T1, T2   undo: T3       final A=400 B=400 C=700
crash after record 10 (upd T3 B 400 380)
   committed: T1, T2   undo: T3       final A=400 B=400 C=700
```

Crash after record $3$: $T_1$ had not committed, so its changes are undone and $A$, $B$ return to $500$, $300$. After record $9$, $T_1$ and $T_2$ are winners and $T_3$ is undone, so $A$ ends at $400$ (not $T_3$’s $450$). Undo must run newest first and redo oldest first: the last value written wins in redo, the oldest before-image wins in undo.

<div class="nb nb-remark" id="remark-9-2-4">

<strong>Remark 9.2.4</strong> (Why redo winners’ changes at all?) — With no-force, a committed transaction’s pages may never have reached the disk; the log is the only copy of its effects. Repeating all of history (rather than redoing only the winners) is simpler and is what ARIES does: it restores the exact pre-crash state, after which undoing the losers is an ordinary rollback.

</div>

### 9.2.i Checkpoints {#s9-2-i}

Without help, recovery would scan the whole log since the database was created. A <strong>checkpoint</strong> bounds the work: (1) write all log records in memory to stable storage, (2) write all modified buffer pages to disk, (3) write `<checkpoint L>`, where $L$ lists the transactions active at that moment. Recovery then only considers transactions in $L$ and those that started after the checkpoint.

<figure class="nb-fig"><img src="fig-1.svg" alt="Figure 1" loading="lazy"></figure>

A dot marks a commit; lines that reach the crash were still active. $T_1$ committed before the checkpoint, so its pages are on disk: ignore it. $T_2$ and $T_4$ committed after it: redo. $T_3$ and $T_5$ were active at the crash: undo, including $T_3$’s updates from before the checkpoint (the log is scanned back past the checkpoint for them). A simple checkpoint stops all updates while it runs; a <strong>fuzzy checkpoint</strong> records the dirty-page list and lets work continue, which is what ARIES uses.

<div class="nb nb-moral">

WAL: log before data, log before commit. Recovery: redo forward, undo losers backward, and a checkpoint tells you where to start.

</div>

## 9.3 ARIES at overview depth {#sec-dbms-aries}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> three passes over the log: analysis, redo, undo.</em>

</div>

<div class="nb nb-definition" id="definition-9-3-1">

<strong>Definition 9.3.1</strong>. ARIES (Mohan et al., IBM; the design behind DB2, SQL Server and many others) uses steal and no-force with WAL and adds: a <strong>log sequence number</strong> (LSN) on every record; a <strong>pageLSN</strong> in every page (the LSN of the last update applied to it); a <strong>transaction table</strong> (active transactions and their last LSN) and a <strong>dirty page table</strong> (DPT: each dirty page and its recLSN, the first log record that dirtied it), both saved in fuzzy checkpoints; and CLRs, which make undo itself redoable and never undone twice.

</div>

<div class="nb nb-remark" id="algorithm-9-3-2">

<strong>Algorithm 9.3.2</strong> (ARIES restart) — <strong>Analysis</strong>: from the last checkpoint, rebuild the transaction table (the losers) and the dirty page table. <strong>Redo</strong>: from the smallest recLSN in the DPT, reapply every update unless the page is not in the DPT, the record is older than the page’s recLSN, or the page’s pageLSN shows the update is already there. <strong>Undo</strong>: roll the losers back, newest record first, writing a CLR for each undone update.

</div>

```python {filename="c09-aries.py, lines 1–16",linenos=table,linenostart=1}
# ARIES in miniature: analysis, redo (repeating history), undo with CLRs.
LOG = {  # LSN: record
    10: ("begin", "T1"),
    20: ("update", "T1", "P1", "A", 100, 150),
    30: ("begin", "T2"),
    40: ("update", "T2", "P2", "B", 200, 250),
    50: ("commit", "T1"),
    60: ("checkpoint", {"T2": 40}, {"P1": 20, "P2": 40}),  # ATT, DPT
    70: ("begin", "T3"),
    80: ("update", "T3", "P3", "C", 300, 350),
    90: ("update", "T2", "P1", "A", 150, 175),
    100: ("commit", "T3"),
    110: ("update", "T2", "P4", "D", 400, 450),
}
# what reached the disk before the crash: page -> (pageLSN, value)
DISK = {"P1": (20, 150), "P2": (0, 200), "P3": (80, 350), "P4": (0, 400)}
```

The three passes are straightforward loops over this log (the rest of `c09-aries.py`):

```text {filename="Output (Python 3.11)"}
analysis: losers (ATT) {'T2': 110}
          dirty pages (DPT) {'P1': 20, 'P2': 40, 'P3': 80, 'P4': 110}
redo  LSN  20: skip (P1 already has it)
redo  LSN  40: B = 250 on P2
redo  LSN  80: skip (P3 already has it)
redo  LSN  90: A = 175 on P1
redo  LSN 110: D = 450 on P4
undo  LSN 110: D = 400 on P4, CLR LSN 120
undo  LSN  90: A = 150 on P1, CLR LSN 130
undo  LSN  40: B = 200 on P2, CLR LSN 140
final: A=150, B=200, C=350, D=400
```

Analysis finds $T_2$ the only loser ($T_1$ and $T_3$ committed) and four dirty pages. Redo starts at LSN $20$ but skips it and LSN $80$, because the pageLSNs on disk show those updates arrived before the crash; it reapplies LSNs $40$, $90$ and $110$, including $T_2$’s updates. Undo then rolls $T_2$ back through LSNs $110$, $90$, $40$, so $A$ returns to the value $T_1$ committed ($150$) and $C$ keeps $T_3$’s committed $350$.

<div class="nb nb-remark" id="remark-9-3-3">

<strong>Remark 9.3.3</strong> (Interview follow-ups) — “Why not force pages at commit?” Random writes of every dirty page at each commit are far slower than one sequential log append; group commit amortizes even that. “Why log both images?” Before-images for undo (steal), after-images for redo (no-force). “What is `fsync` doing here?” Making the log write durable, which is what the OS book’s file-system chapter is about; PostgreSQL calls its log the WAL and `synchronous_commit` controls whether commit waits for it.

</div>

<div class="nb nb-moral">

ARIES: repeat history with redo, then undo the losers with CLRs; LSNs make every step idempotent.

</div>
