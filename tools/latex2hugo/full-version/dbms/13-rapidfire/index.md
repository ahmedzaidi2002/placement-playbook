---
title: "13 · Interview rapid-fire"
linkTitle: "13 Interview rapid-fire"
weight: 13
math: true
---
Short answers to the questions that come up again and again, in the words a strong candidate would use out loud. Each points back to the section that explains it.

## 13.1 Modelling, keys and normalization {#s13-1}

1. <strong>What is a DBMS and why not just files?</strong><br>Software that stores data once under a schema and gives declarative queries, integrity constraints, concurrent access, crash recovery and security; files give none of these ([Section 1.1](../01-relational/#sec-dbms-why)).
2. <strong>Logical vs physical data independence?</strong><br>Physical: change storage (indexes, files) without changing the schema or queries. Logical: change the conceptual schema without breaking external views; harder ([Section 1.1](../01-relational/#sec-dbms-why)).
3. <strong>Schema vs instance?</strong><br>The schema is the description (rarely changes); the instance is the data at one moment.
4. <strong>Weak entity?</strong><br>An entity set without a key of its own, identified by its owner’s key plus a partial key; total participation in an identifying relationship ([Section 1.2](../01-relational/#sec-dbms-er)).
5. <strong>How do you map an M:N relationship? A 1:N one?</strong><br>M:N gets its own table with both keys as the primary key; 1:N puts the “one” side’s key as a foreign key in the “many” side ([Section 1.3](../01-relational/#sec-dbms-mapping)).
6. <strong>Super key vs candidate key vs primary key?</strong><br>Super key: identifies rows. Candidate key: a minimal super key. Primary key: the chosen candidate key, never `NULL`; the others are alternate keys ([Section 1.4](../01-relational/#sec-dbms-keys)).
7. <strong>Primary key vs unique constraint?</strong><br>One primary key per table, never `NULL`, often the clustering key; any number of `UNIQUE` constraints, which allow `NULL`s (any number of them in PostgreSQL, one in SQL Server). Both create an index.
8. <strong>Can a foreign key be `NULL`? Refer to its own table?</strong><br>Yes and yes (a manager column). It must reference a primary key or unique column set.
9. <strong>How many super keys does $R(A,B,C,D)$ have if $A$ is the only candidate key?</strong><br>$2^3=8$: any subset containing $A$.
10. <strong>What is a functional dependency?</strong><br>$X\to Y$: rows that agree on $X$ agree on $Y$, in every legal instance; a property of the schema, not of today’s data ([Section 6.2](../06-normalization/#sec-dbms-fd)).
11. <strong>What is normalization and why?</strong><br>Decomposing tables so each fact is stored once, removing redundancy and the update, insertion and deletion anomalies; the price is joins ([Section 6.1](../06-normalization/#sec-dbms-why-norm)).
12. <strong>2NF, 3NF, BCNF in one line each?</strong><br>2NF: no non-prime attribute depends on part of a key. 3NF: every non-trivial $X\to A$ has $X$ a super key or $A$ prime. BCNF: $X$ is always a super key ([Section 6.5](../06-normalization/#sec-dbms-nf)).
13. <strong>3NF vs BCNF: which is better?</strong><br>BCNF removes all FD redundancy but may lose a dependency; 3NF always has a lossless, dependency-preserving decomposition. Prefer BCNF, fall back to 3NF.
14. <strong>When is a relation in 3NF but not BCNF?</strong><br>Only with overlapping composite candidate keys, e.g. $SC\to T$, $T\to C$.
15. <strong>Lossless join?</strong><br>Joining the decomposed tables gives back exactly the original; for two pieces, iff the common attributes are a key of one piece ([Section 6.6](../06-normalization/#sec-dbms-decomp)).
16. <strong>What is denormalization and when is it right?</strong><br>Storing redundant or derived data to save joins on hot read paths, with a defined way to keep copies in sync; common in warehouses ([Section 12.6](../12-beyond/#sec-dbms-practical)).
17. <strong>4NF?</strong><br>No non-trivial multivalued dependency except from a super key; it separates independent multi-valued facts ([Section 6.7](../06-normalization/#sec-dbms-4nf)).

## 13.2 SQL {#s13-2}

18. <strong>`DELETE` vs `TRUNCATE` vs `DROP`?</strong><br>`DELETE`: DML, row by row, `WHERE` allowed, fires triggers, rollback-able. `TRUNCATE`: removes all rows by deallocating pages, much faster, can reset identity counters, usually DDL (transactional in PostgreSQL). `DROP`: removes the table itself ([Section 3.1](../03-sql-basics/#sec-dbms-ddl)).
19. <strong>`WHERE` vs `HAVING`?</strong><br>`WHERE` filters rows before grouping and cannot use aggregates; `HAVING` filters groups after grouping ([Section 4.1](../04-sql-advanced/#sec-dbms-groupby)).
20. <strong>`UNION` vs `UNION ALL`?</strong><br>`UNION` removes duplicates (a sort or hash); `UNION ALL` keeps them and is cheaper ([Section 4.3](../04-sql-advanced/#sec-dbms-setops)).
21. <strong>Order in which a `SELECT` is evaluated?</strong><br>`FROM`/`JOIN`, `WHERE`, `GROUP BY`, `HAVING`, windows, `SELECT`, `DISTINCT`, `ORDER BY`, `LIMIT` ([Section 3.2](../03-sql-basics/#sec-dbms-select)).
22. <strong>Inner vs left vs full join row counts?</strong><br>Inner $m$ matched pairs; left $m$ plus unmatched left rows; full adds unmatched right rows too; cross $|A||B|$ ([Section 3.3](../03-sql-basics/#sec-dbms-joins)).
23. <strong>Rows of `SELECT * FROM A, B` with $100$ and $5$ rows?</strong><br>$500$: a cross join.
24. <strong>`COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`?</strong><br>Rows; non-`NULL` values; distinct non-`NULL` values ([Section 3.4](../03-sql-basics/#sec-dbms-null)).
25. <strong>Why does `NOT IN` sometimes return nothing?</strong><br>If the subquery yields a `NULL`, `x <> NULL` is UNKNOWN for every `x`. Use `NOT EXISTS`.
26. <strong>What is `NULL = NULL`?</strong><br>UNKNOWN; use `IS NULL` or `IS NOT DISTINCT FROM`.
27. <strong>`x > ALL (empty set)`?</strong><br>TRUE (vacuous); `x > ANY (empty)` is FALSE.
28. <strong>`IN` vs `EXISTS`?</strong><br>Same result for non-null data; `EXISTS` is a semi-join on a correlated condition and is `NULL`-safe in its negated form; modern optimizers plan both as semi-joins ([Section 4.2](../04-sql-advanced/#sec-dbms-subq)).
29. <strong>Correlated subquery?</strong><br>A subquery that references the outer row and is logically re-evaluated per outer row.
30. <strong>`RANK` vs `DENSE_RANK` vs `ROW_NUMBER`?</strong><br>On a tie: same rank then a gap; same rank, no gap; distinct numbers ([Section 4.5](../04-sql-advanced/#sec-dbms-window)).
31. <strong>$N$-th highest salary?</strong><br>`DENSE_RANK() OVER (ORDER BY salary DESC) = N` in a subquery, or `DISTINCT ... ORDER BY ... LIMIT 1 OFFSET N-1`, or a correlated count of greater distinct salaries equal to $N-1$ ([Section 5.1](../05-sql-puzzles/#sec-dbms-pz-rank)).
32. <strong>`GROUP BY` vs window function?</strong><br>`GROUP BY` collapses rows to one per group; a window function keeps every row and adds a computed column.
33. <strong>View vs materialized view?</strong><br>A view is a stored query, always current; a materialized view stores the result and must be refreshed ([Section 4.7](../04-sql-advanced/#sec-dbms-views)).
34. <strong>CTE vs subquery vs temp table?</strong><br>A CTE names a subquery for one statement (and can be recursive); a temp table is materialized and lives for the session.
35. <strong>Stored procedure vs function?</strong><br>A procedure is called with `CALL`, returns nothing directly and may control transactions; a function returns a value and is usable in queries ([Section 4.9](../04-sql-advanced/#sec-dbms-triggers)).
36. <strong>What is a trigger? A danger?</strong><br>Code run automatically on insert/update/delete; hidden work, cascading effects, hard debugging.
37. <strong>`TOP` vs `LIMIT` vs `FETCH FIRST`?</strong><br>SQL Server; MySQL/PostgreSQL/SQLite; the standard (PostgreSQL, Oracle 12c+, SQL Server 2012+) ([Section 4.11](../04-sql-advanced/#sec-dbms-dialects)).
38. <strong>What is SQL injection and the fix?</strong><br>User input concatenated into SQL text changes the query; always use parameterized queries (placeholders), never string formatting.
39. <strong>`CHAR` vs `VARCHAR`?</strong><br>Fixed length, space-padded vs variable length up to a maximum.
40. <strong>What does `DISTINCT` apply to?</strong><br>The whole select list, not the first column.

## 13.3 Storage and indexes {#s13-3}

41. <strong>Why B$^+$-trees and not binary search trees?</strong><br>Disk reads whole blocks; a node per block with fan-out in the hundreds gives height 3–4 for millions of keys, versus height 20+ for a binary tree ([Section 10.3](../10-storage/#sec-dbms-btree)).
42. <strong>B-tree vs B$^+$-tree?</strong><br>B$^+$: all data in chained leaves, internal nodes are separators only (higher fan-out, efficient range scans); B-tree: each key once, anywhere, no leaf chain.
43. <strong>Clustered vs non-clustered index?</strong><br>Clustered: the rows are stored in index order (one per table, InnoDB’s primary key); non-clustered: a separate structure pointing to rows ([Section 10.5](../10-storage/#sec-dbms-index-sql)).
44. <strong>Dense vs sparse index?</strong><br>Dense: an entry per key value; sparse: one per block, needs the file sorted on the key ([Section 10.2](../10-storage/#sec-dbms-files)).
45. <strong>Primary vs secondary index?</strong><br>Primary: on the ordering key of a sorted file (sparse). Secondary: on any other field (dense). At most one primary or clustering index.
46. <strong>What is a covering index? An index-only scan?</strong><br>An index containing every column the query needs, so the table is not read.
47. <strong>Composite index on $(a,b)$: does `WHERE b = 5` use it?</strong><br>Not for a seek (no left prefix); the engine may scan the whole index or skip-scan if $a$ has few values.
48. <strong>When does an index not help?</strong><br>Low selectivity, small tables, functions on the column, leading wildcards, type mismatches; and every index slows writes.
49. <strong>Hash index vs B$^+$-tree?</strong><br>Hash: equality only, about one I/O; B$^+$-tree: equality, ranges, ordering, prefixes ([Section 10.4](../10-storage/#sec-dbms-hash)).
50. <strong>Why is a primary-key lookup fast?</strong><br>The key is indexed: $\approx$ tree height block reads, and the upper levels are almost always cached.
51. <strong>Extendible vs linear hashing?</strong><br>Extendible: a directory that doubles, split only the overflowing bucket. Linear: no directory, split buckets in round-robin order.
52. <strong>How many levels for $10^7$ keys with fan-out $128$?</strong><br>$\lceil \log_{128}10^7\rceil=4$ (the exact answer depends on leaf capacity; [Section 10.3](../10-storage/#sec-dbms-btree)).

## 13.4 Transactions, concurrency and recovery {#s13-4}

53. <strong>What is a transaction?</strong><br>A unit of work executed atomically: all its changes commit or none do ([Section 7.1](../07-transactions/#sec-dbms-acid)).
54. <strong>ACID?</strong><br>Atomicity (all or nothing, via undo log), consistency (constraints hold), isolation (as if serial, via concurrency control), durability (survives crashes, via the WAL).
55. <strong>Conflict serializable?</strong><br>Conflict equivalent to a serial schedule; test: the precedence graph is acyclic ([Section 7.2](../07-transactions/#sec-dbms-serial)).
56. <strong>View vs conflict serializability?</strong><br>View is weaker (more schedules), allows blind writes, and is NP-complete to test; conflict is polynomial and what schedulers enforce.
57. <strong>Recoverable vs cascadeless vs strict?</strong><br>Commit after those you read from; read only committed data; read or write only committed data ([Section 7.3](../07-transactions/#sec-dbms-recoverable)).
58. <strong>What is 2PL? Why strict 2PL?</strong><br>Acquire all locks before releasing any: guarantees conflict serializability. Strict 2PL holds write locks until commit, preventing dirty reads and cascading aborts ([Section 8.1](../08-concurrency/#sec-dbms-2pl)).
59. <strong>Does 2PL prevent deadlock?</strong><br>No; conservative 2PL does, at the cost of declaring all locks up front.
60. <strong>Wait-die vs wound-wait?</strong><br>Wait-die: older waits, younger dies. Wound-wait: older wounds (aborts) younger, younger waits. Both restart with the old timestamp ([Section 8.2](../08-concurrency/#sec-dbms-deadlock)).
61. <strong>How do real databases handle deadlocks?</strong><br>Detect a cycle in the wait-for graph and abort a victim, which the application retries.
62. <strong>Timestamp ordering and the Thomas write rule?</strong><br>Conflicts must follow timestamp order or the late transaction aborts; Thomas ignores an obsolete write instead of aborting ([Section 8.3](../08-concurrency/#sec-dbms-ts)).
63. <strong>Optimistic vs pessimistic concurrency control?</strong><br>Optimistic: run, then validate at commit (good for low contention); pessimistic: lock before access.
64. <strong>What is MVCC?</strong><br>Keep multiple versions; readers see a snapshot and never block writers ([Section 8.5](../08-concurrency/#sec-dbms-mvcc)).
65. <strong>Isolation levels and what each prevents?</strong><br>Read uncommitted (nothing), read committed (dirty reads), repeatable read (non-repeatable reads), serializable (phantoms and every other anomaly) ([Section 8.6](../08-concurrency/#sec-dbms-isolation)).
66. <strong>Dirty read, non-repeatable read, phantom?</strong><br>Reading uncommitted data; re-reading a row and seeing a change; re-running a query and seeing new or vanished rows.
67. <strong>Lost update and how to prevent it?</strong><br>Two read-modify-write cycles overwrite each other; use `UPDATE x = x + 1`, `SELECT ... FOR UPDATE`, a version check, or a higher isolation level.
68. <strong>Write skew?</strong><br>Two transactions read overlapping data and update different rows, jointly breaking a constraint; allowed by snapshot isolation, prevented by serializable.
69. <strong>Default isolation level?</strong><br>Read committed in PostgreSQL, Oracle and SQL Server; repeatable read in MySQL/InnoDB.
70. <strong>Intention locks?</strong><br>IS/IX/SIX on ancestors announce finer locks below, so table and row locks can be checked at the table level ([Section 8.7](../08-concurrency/#sec-dbms-granularity)).
71. <strong>What is the WAL rule?</strong><br>Log record before the data page, and all of a transaction’s log before its commit is acknowledged ([Section 9.2](../09-recovery/#sec-dbms-wal)).
72. <strong>Steal/no-force?</strong><br>Uncommitted pages may be written (needs undo); committed pages need not be (needs redo); the fastest policy, used with undo/redo logging ([Section 9.1](../09-recovery/#sec-dbms-failures)).
73. <strong>What is a checkpoint for?</strong><br>To bound how much log recovery must scan.
74. <strong>ARIES in one breath?</strong><br>Analysis rebuilds the losers and dirty pages; redo repeats history from the oldest dirty page; undo rolls back losers, logging CLRs ([Section 9.3](../09-recovery/#sec-dbms-aries)).

## 13.5 Query processing and distributed data {#s13-5}

75. <strong>Join algorithms?</strong><br>Nested loop (any condition), block nested loop, index nested loop, sort-merge and hash join (equijoins) ([Section 11.2](../11-query/#sec-dbms-joins-algo)).
76. <strong>Hash join vs sort-merge join?</strong><br>Hash: no ordering needed, about $3(b_r+b_s)$, equality only. Sort-merge: great when inputs are already sorted or the output must be.
77. <strong>What does the optimizer do?</strong><br>Rewrites the algebra (push selections), chooses access paths, join order and algorithms by estimated cost from statistics ([Section 11.3](../11-query/#sec-dbms-optimizer)).
78. <strong>Why is a query suddenly slow?</strong><br>Read `EXPLAIN ANALYZE`: stale statistics, a missing or unusable index, a bad join order from a misestimate, a spill to disk.
79. <strong>OLTP vs OLAP?</strong><br>Short transactions on normalized rows versus long scans and aggregates on a star schema in a column store ([Section 12.1](../12-beyond/#sec-dbms-olap)).
80. <strong>SQL vs NoSQL?</strong><br>Relational for relationships, ad hoc queries and transactions; NoSQL for simple access patterns at very large scale or schemaless data ([Section 12.2](../12-beyond/#sec-dbms-nosql)).
81. <strong>Examples of key-value stores?</strong><br>Redis, Memcached, Amazon DynamoDB, Riak, etcd.
82. <strong>CAP theorem?</strong><br>During a partition a replicated store must give up consistency (linearizability) or availability ([Section 12.4](../12-beyond/#sec-dbms-cap)).
83. <strong>BASE?</strong><br>Basically available, soft state, eventually consistent.
84. <strong>Replication vs sharding?</strong><br>Copies of the same data for availability and reads, versus splitting the data for size and write throughput ([Section 12.3](../12-beyond/#sec-dbms-scale)).
85. <strong>Why consistent hashing?</strong><br>Adding a node moves only about $1/n$ of the keys instead of nearly all.
86. <strong>2PC and its weakness?</strong><br>Prepare/vote then commit/abort; participants that voted yes block if the coordinator dies ([Section 12.5](../12-beyond/#sec-dbms-2pc)).
87. <strong>What is the N+1 problem?</strong><br>One query for a list plus one per item for a relation; fix with a join or a batched `IN` query ([Section 12.6](../12-beyond/#sec-dbms-practical)).
88. <strong>Why a connection pool?</strong><br>Connections are expensive to open and the database runs only so many queries concurrently; reuse a bounded set.
89. <strong>Partitioning vs sharding?</strong><br>Partitioning splits a table inside one server (pruning, maintenance); sharding spreads data across servers ([Section 4.10](../04-sql-advanced/#sec-dbms-partition)).
