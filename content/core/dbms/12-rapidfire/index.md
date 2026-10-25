---
title: "12 · Interview rapid-fire"
linkTitle: "12 Rapid-fire"
weight: 12
math: true
---
## 12.1 Modelling and keys {#db-12-1}

1. **DBMS vs file system?** A DBMS adds integrity, concurrency control, recovery, security and a query language; files give none of these.
2. **Schema vs instance?** Structure vs the data at a moment.
3. **Physical vs logical data independence?** Change storage without changing the schema / change the schema without breaking applications.
4. **Super key vs candidate key vs primary key?** Any unique set / a minimal unique set / the chosen candidate key (not NULL).
5. **Foreign key?** A column that must match a primary key in another table (or be NULL).
6. **Weak entity?** Cannot be identified alone; uses its owner's key plus a partial key.
7. **How is an M:N relationship stored?** As a separate table holding both keys.
8. **DELETE vs TRUNCATE vs DROP?** Remove chosen rows (rollback-able) / remove all rows fast / remove the table.

## 12.2 SQL {#db-12-2}

9. **WHERE vs HAVING?** WHERE filters rows before grouping; HAVING filters groups after.
10. **Inner vs left join?** Only matches vs all left rows with NULLs for missing matches.
11. **UNION vs UNION ALL?** UNION removes duplicates; UNION ALL keeps them and is faster.
12. **Why is `NULL = NULL` not true?** NULL is unknown; comparisons give UNKNOWN. Use IS NULL.
13. **COUNT(*) vs COUNT(col)?** All rows vs non-NULL values.
14. **Second-highest salary?** `MAX(salary)` where `salary < MAX(salary)`, or `DENSE_RANK() = 2`.
15. **RANK vs DENSE_RANK?** Ties share a rank; RANK then skips numbers, DENSE_RANK does not.
16. **Correlated subquery?** A subquery that refers to the outer row and runs once per outer row.
17. **View vs materialized view?** A stored query vs a stored result that must be refreshed.
18. **What is a trigger?** Code that runs automatically on INSERT, UPDATE or DELETE.

## 12.3 Normalization {#db-12-3}

19. **Why normalize?** To remove redundancy and update/insert/delete anomalies.
20. **1NF, 2NF, 3NF, BCNF in one line each?** Atomic values; no partial dependency on a key; no transitive dependency (unless the dependent attribute is prime); every determinant is a super key.
21. **3NF vs BCNF?** BCNF is stricter; 3NF allows $X \to A$ when $A$ is prime. 3NF can always preserve dependencies; BCNF sometimes cannot.
22. **Lossless join?** Joining the pieces gives back exactly the original; true if the common attributes are a key of one piece.
23. **What is denormalization?** Adding redundancy on purpose to speed up reads.

## 12.4 Transactions and concurrency {#db-12-4}

24. **ACID?** Atomicity, consistency, isolation, durability.
25. **Conflicting operations?** Same item, different transactions, at least one write.
26. **How to test conflict serializability?** Precedence graph has no cycle.
27. **What is 2PL?** Acquire all locks before releasing any; guarantees serializability.
28. **Strict 2PL?** Hold exclusive locks until commit; prevents cascading rollbacks.
29. **Wait-die vs wound-wait?** Older waits / younger dies, vs older wounds younger / younger waits.
30. **Dirty, non-repeatable, phantom read?** Read uncommitted data / same row changes between reads / new rows appear on re-query.
31. **Isolation levels?** Read uncommitted, read committed, repeatable read, serializable.
32. **What is MVCC?** Keeping multiple versions so readers see a snapshot and never block writers.
33. **Write-ahead logging?** Log records reach disk before the data they describe, and before commit.
34. **What does a checkpoint do?** Flushes dirty pages and limits how much log must be scanned after a crash.

## 12.5 Indexing and beyond {#db-12-5}

35. **What is an index and its cost?** A structure for fast lookups; costs space and slows writes.
36. **Clustered vs non-clustered index?** Rows stored in index order (one per table) vs a separate pointer structure (many).
37. **Why B+ trees?** Shallow (high fan-out), balanced, and linked leaves make range scans fast.
38. **Hash vs B+ tree index?** Hash: fast equality, no ranges. B+ tree: both.
39. **SQL vs NoSQL?** Fixed schema, joins, ACID vs flexible schema, horizontal scaling, often eventual consistency.
40. **CAP theorem?** During a partition, choose consistency or availability.
41. **Sharding vs replication?** Split data across machines vs copy the same data to several.

<div class="nb nb-moral">

Forty-one answers, each under twenty seconds: that covers the DBMS theory part of most interviews. Chapter 13 has the numericals.

</div>
