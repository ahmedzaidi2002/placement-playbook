---
title: "9 · Recovery"
linkTitle: "9 Recovery"
weight: 9
math: true
---
## 9.1 Failures and storage {#db-9-1}

- **Transaction failure:** a logical error or a deadlock abort → roll that transaction back.
- **System crash:** power or OS failure; memory is lost, disk survives → use the log.
- **Disk failure:** use backups/replicas (and RAID).

Storage: **volatile** (RAM, lost on crash), **non-volatile** (disk), **stable** (replicated so that it effectively never loses data; where the log lives).

**Buffer policies:**

- **Steal:** a dirty page of an uncommitted transaction may be written to disk → recovery needs **UNDO**.
- **No-force:** committed changes need not be on disk at commit → recovery needs **REDO**.
- Real systems use **steal + no-force** (best performance), so they need both undo and redo.

## 9.2 Log-based recovery {#db-9-2}

The **log** records every change: `<T start>`, `<T, X, old value, new value>`, `<T commit>`, `<T abort>`.

<div class="nb nb-definition">

<strong>Write-ahead logging (WAL)</strong> — (1) a log record must reach stable storage **before** the data page it describes is written to disk; (2) all of a transaction's log records must be on stable storage **before** it commits.

</div>

After a crash:

- **Redo** every transaction that has `<T start>` **and** `<T commit>` in the log (reapply new values).
- **Undo** every transaction that has `<T start>` but **no** commit/abort (restore old values, scanning backwards).

**Deferred update:** changes go to the database only after commit → only REDO needed. **Immediate update:** changes may go before commit → both UNDO and REDO.

## 9.3 Checkpoints {#db-9-3}

Scanning the whole log is slow. A **checkpoint** writes all dirty pages to disk and logs `<checkpoint L>` (L = active transactions). After a crash, transactions that committed **before** the checkpoint need nothing.

<div class="nb nb-example">

<strong>Example</strong> (What to redo and undo)

Log at crash:
`<T1 start>` `<T1, A, 100, 50>` `<T2 start>` `<T1 commit>` `<checkpoint {T2}>` `<T2, B, 200, 300>` `<T3 start>` `<T3, C, 5, 10>` `<T3 commit>` — crash.

- **T1:** committed before the checkpoint → **nothing to do**.
- **T3:** started and committed after the checkpoint → **redo** (C = 10).
- **T2:** active at the checkpoint, never committed → **undo** (B back to 200).

</div>

## 9.4 ARIES, at overview depth {#db-9-4}

The standard algorithm (used by DB2, SQL Server) for steal/no-force: every log record has a **log sequence number (LSN)**, and each page stores the LSN of its last change. Recovery runs three passes:

1. **Analysis:** from the last checkpoint, find which transactions were active and which pages were dirty.
2. **Redo:** repeat history: reapply all changes (even of losers) to bring pages to their crash state.
3. **Undo:** roll back the losers, writing **compensation log records (CLRs)** so a crash during recovery does not undo twice.

<div class="nb nb-moral">

WAL: log first, data later, and the log is on disk before commit. After a crash, redo the committed, undo the uncommitted; checkpoints limit how far back to look.

</div>
