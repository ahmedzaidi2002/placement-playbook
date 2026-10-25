---
title: "Database Management Systems"
weight: 4
math: true
sidebar:
  open: false
---

The DBMS topics that placement OAs and interviews ask, cut down to what matters: definitions, the idea behind each, short SQL, and a worked example wherever there is a numerical (super-key counting, candidate keys, normal forms, serializability, B+ tree order, join cost).

## Contents

**Part: Modelling and SQL**

- [1 · ER model, relational model and keys](01-er-relational/)
- [2 · Relational algebra and calculus](02-algebra/)
- [3 · SQL basics: tables, joins, NULL](03-sql-basics/)
- [4 · SQL advanced: grouping, subqueries, windows](04-sql-advanced/)
- [5 · SQL queries interviewers ask](05-sql-patterns/)
- [6 · Functional dependencies and normalization](06-normalization/)

**Part: Transactions**

- [7 · Transactions and serializability](07-transactions/)
- [8 · Concurrency control](08-concurrency/)
- [9 · Recovery](09-recovery/)

**Part: Storage and beyond**

- [10 · Indexing and query processing](10-indexing-query/)
- [11 · NoSQL, CAP and distributed databases](11-beyond/)

**Part: Revision**

- [12 · Interview rapid-fire](12-rapidfire/)
- [13 · Practice problems](13-problems/)

<div class="nb nb-moral">

Highest-yield: keys and normalization (chapters 1, 6), SQL joins / GROUP BY / nth-highest salary (chapters 3–5), ACID, serializability and isolation levels (chapters 7–8), indexes and B+ trees (chapter 10).

</div>

The full-length version, with every query run on SQLite and PostgreSQL, is kept in `tools/latex2hugo/full-version/dbms/` and in the PDF.
