---
title: "Transactions, concurrency and recovery"
weight: 5
---

1 question asked by MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q23, what a transaction is

*Asked by: MathWorks (IISc 2024)*

Which of the following define a transaction INCORRECTLY? (more than one answer)

- **(a)** DDL statements on a schema
- **(b)** A COMMIT or ROLLBACK in a session
- **(c)** Either a collection of DML statements or a single DDL, DCL or TCL statement that forms a logical unit of work in a session
- **(d)** A collection of DML and DDL statements in different sessions

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a), (b) and (d)** define it incorrectly

**Why.** The correct definition is (c): a transaction is one or more DML statements, or a single DDL/DCL statement, forming a logical unit of work in one session. COMMIT and ROLLBACK **end** a transaction (they are not one), and a transaction never spans sessions.

**Concept: transaction boundaries.** A transaction starts with the first DML statement and ends with COMMIT (save) or ROLLBACK (undo). In Oracle, a DDL statement commits implicitly, so it forms its own transaction.

{{< /details >}}
