@@ or-nosql-criteria
**Answer: (d) you need to store a very small amount of data**

**Why.** The usual reasons to choose NoSQL are very low latency, unstructured or loosely related data, simple storage of serialised objects (JSON, XML), and **massive** data volumes that need horizontal scaling. A tiny dataset is not a reason; any database handles it.

**Concept: SQL vs NoSQL.** Relational databases give schemas, joins and ACID transactions. NoSQL stores (key-value, document, wide-column, graph) relax some of that to gain flexible schemas and easy scaling across many machines.

@@ or-nosql-kv
**Answer: (c) Redis**

**Why.** Redis stores values under keys (in memory, with optional persistence). HBase and Accumulo are wide-column stores; MongoDB is a document store.

**Concept: NoSQL families.** Key-value (Redis, DynamoDB): get/put by key. Document (MongoDB): JSON-like documents with queries on fields. Wide-column (Cassandra, HBase): rows with dynamic column families. Graph (Neo4j): nodes and edges.

@@ or-oracle-release
**Answer: (a) 23ai** (at the time of the test, 2024–25)

**Why.** Oracle Database 23ai (first announced as 23c) is the long-term-support release after 19c. There was no 22ai or 24ai, and 19 is named "19c", not "19ai". Check current names before an interview; this changes over time.

**Concept: long-term releases.** Vendors mark some versions for long support (years of patches); companies standardise on those. Oracle's recent LTS line: 12.2 → 19c → 23ai.

@@ mw-iisc-25
**Answer: (b) 12**

**Why.** A super key is any set containing a candidate key. Supersets of AB: the other 3 attributes (C, D, E) are free, 2³ = 8. Supersets of BC: likewise 8. Supersets of both (containing ABC): D and E free, 2² = 4, counted twice. 8 + 8 − 4 = 12.

**Concept: keys.** Super key: uniquely identifies a row. Candidate key: a minimal super key. Primary key: the candidate key chosen. Count super keys with inclusion–exclusion over the candidate keys.

@@ dpworld-normalisation
**Answer.** Normalisation splits tables into smaller ones, guided by functional dependencies, so that every fact is stored once. It removes redundancy and the anomalies it causes:
- **Update anomaly:** a fact stored in many rows; changing only some leaves the data inconsistent.
- **Insertion anomaly:** a fact cannot be stored without an unrelated one.
- **Deletion anomaly:** deleting one fact loses another.

**The normal forms (each stricter).**
- 1NF: every value is atomic (no lists in a cell).
- 2NF: no non-key attribute depends on only part of a candidate key.
- 3NF: no non-key attribute depends on the key through another non-key attribute (no transitive dependency).
- BCNF: the left side of every non-trivial dependency is a super key.

**Concept: the trade-off.** A good decomposition is lossless (joining the parts gives back exactly the original) and ideally preserves dependencies. Normalised schemas need more joins, so read-heavy systems sometimes denormalise on purpose.

@@ mw-iiitd-7
**Answer: (c) every relation in BCNF is also in 3NF**

**Why.** BCNF is stricter than 3NF: every BCNF relation satisfies 3NF, but not the other way round (b is false, d is false). (a) describes 2NF ("fully functionally dependent"), not 3NF.

**Concept: 3NF vs BCNF.** For every dependency X → A: BCNF requires X to be a super key. 3NF also allows A to be a prime attribute (part of some candidate key). That small exception is why 3NF can always preserve dependencies and BCNF sometimes cannot.

@@ or-acid
**Answer: (d) dependency**

**Why.** The transaction properties are ACID: Atomicity, Consistency, Isolation, Durability. "Dependency" is not one of them.

**Concept: ACID.**
- Atomicity: all of a transaction happens or none of it (rollback on failure).
- Consistency: it takes the database from one valid state to another (constraints hold).
- Isolation: concurrent transactions don't see each other's partial work.
- Durability: once committed, changes survive crashes (write-ahead log).

@@ exl-filegroups
**Answer: (a) query 1** (`sys.filegroups`)

**Why.** The catalog view `sys.filegroups` has one row per filegroup with `name`, `type` ('FG' for a row filegroup) and `is_read_only`. `sys.data_spaces` has no `is_read_only` column; `sys.groups` and `sys.sysfile` are not the right views.

**Concept: SQL Server catalog views.** The `sys.*` views describe the database's own metadata (tables, columns, files, filegroups). A filegroup is a named set of data files that tables and indexes can be placed on.

@@ exl-max-diff
**Answer: option 2, `SELECT MAX(NO_OF_BOYS - NO_OF_GIRLS) AS DIFF FROM CLASS`** (or `MAX(ABS(...))` if girls may outnumber boys)

**Why.** The difference must be computed per row (per section) and then maximised. Option 1 subtracts the minimum girls of one section from the maximum boys of possibly another section, which is not a difference within any section.

**Concept: row expression inside an aggregate.** `MAX(a − b)` computes a − b for each row and then takes the maximum. `MAX(a) − MIN(b)` aggregates each column separately, mixing rows.

@@ exl-right-join
**Answer: (a) option 1**

**Why.** A right join keeps every Teacher row. Bio-101 and Phy-104 match students; Mas-103 has no student, so its Student columns are NULL. `SELECT *` returns both `Course` columns. Che-102 (a student with no teacher) is dropped.

**Concept: joins.** Inner join: only matching pairs. Left join: all rows of the left table, NULLs where the right has no match. Right join: the mirror. Full outer join: all rows of both.

@@ exl-third-salary
**Answer: (b) query 2**

**Why.** The inner query keeps the three largest salaries (500000, 300000, 90000). Ordering them ascending and taking the top one gives the smallest of those: 90000, the third-highest. Query 3 returns the third-lowest (85000); queries 1 and 4 keep only one row inside.

**Concept: N-th highest value.** Take the top N in descending order, then the smallest of them. Other ways: `ORDER BY salary DESC LIMIT 1 OFFSET 2` (MySQL), or `DENSE_RANK()` to handle ties.

@@ ion-q17
**Answer: (a) and (d)** (in MySQL, which HackerRank uses)

**Why.**
- (a) Fine: HAVING can test an aggregate; MySQL treats non-zero as true.
- (b) Selects `is_active` without aggregating or grouping by it; rejected under ONLY_FULL_GROUP_BY (MySQL's default) and standard SQL.
- (c) Syntax error: DISTINCT can only come right after SELECT.
- (d) Valid in MySQL, which lets HAVING refer to a select-list alias.

**Concept: GROUP BY rule.** Every selected column must either be in GROUP BY or inside an aggregate function, because each group produces one row and the database must know which single value to show.

@@ ie-q39
**Answer: (c) `select distinct data1 from MY_TABLE;`**

**Why.** DISTINCT removes duplicate rows from the result. (Oracle also accepts UNIQUE as a synonym, but DISTINCT is standard.)

**Concept: DISTINCT applies to the whole selected row.** `SELECT DISTINCT a, b` removes rows where both a and b repeat together.

@@ maq-exists
**Answer: (a) Bob Mary Mike Tara**

**Why.** EXISTS is true for customers with at least one order: 7000 Bob, 5000 Tara, 8000 Mary, 4000 Mike. Sorted by name: Bob, Mary, Mike, Tara. (Strictly, ORDER is a reserved word and the table would need quoting; the test intends the logical result.)

**Concept: correlated EXISTS.** The subquery runs for each outer row (it refers to CUSTOMER.CUSTID). EXISTS only checks whether any row comes back, not what it contains, so `SELECT *` or `SELECT 1` inside makes no difference.

@@ maq-q33
**Answer: (b) query (2)**

**Why.** Both join conditions are needed: S.sid = R.sid links sailors to their reservations, and R.bid = B.bid links reservations to boats. Without R.bid = B.bid, any sailor with any reservation qualifies when some red boat exists; without S.sid = R.sid, every sailor qualifies.

**Concept: joins in the WHERE clause.** Listing tables with commas makes a Cartesian product; the WHERE conditions keep only the matching combinations. With k tables you usually need k − 1 join conditions.

@@ maq-q34
**Answer: (a) 4**

**Why.** The distinct addresses are Chicago, New York, Boston, Seattle: 4. (Caveat for interviews: MySQL and SQL Server require an alias on a derived table, `(...) AS t`, and would reject this as written; SQLite, PostgreSQL 16+ and Oracle accept it.)

**Concept: counting distinct values.** `SELECT COUNT(DISTINCT address) FROM student;` does the same in one step.

@@ maq-q35
**Answer: (b) IN BETWEEN**

**Why.** IN and BETWEEN are two separate operators: `x IN (1, 2, 3)` and `x BETWEEN 1 AND 3`. There is no combined "IN BETWEEN".

**Concept: WHERE operators.** Comparison (=, !=, <>, <, >=), BETWEEN ... AND, IN (...), LIKE with % and _, IS NULL / IS NOT NULL, combined with AND, OR, NOT.

@@ maq-q36
**Answer: (a) 500**

**Why.** Listing two tables without a join condition gives the Cartesian product: every student paired with every course, 100 × 5 = 500 rows.

**Concept: cross join.** Rows multiply. A forgotten join condition is a common bug that produces huge results.

@@ mw-iitb-9
**Answer: (c) 4** (all the rows, assuming no row has A > 10)

**Why.** If the subquery returns no rows, `C = ALL (empty set)` is true for every row, so every row is returned. With the four visible rows, that is 4. (The candidate's 0 is the usual trap.)

**Concept: ALL and ANY on empty sets.** `x = ALL (S)` means "x equals every element of S", which is vacuously true when S is empty. `x = ANY (S)` means "x equals some element", which is false when S is empty.

@@ or-having
**Answer: (b) HAVING**

**Why.** HAVING filters groups after GROUP BY (e.g. `HAVING COUNT(*) > 5`). WHERE filters individual rows before grouping and cannot use aggregates.

**Concept: logical order of a query.** FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.

@@ or-partition
**Answer: (c)**

**Why.** Oracle's syntax is `PARTITION BY RANGE (col) (PARTITION p VALUES LESS THAN (...) TABLESPACE t, ...)`. `RANGE COLUMNS` is MySQL syntax; a primary-key clause cannot follow the partition list; a table has one partitioning clause (two levels use SUBPARTITION BY).

**Concept: table partitioning.** A big table is split into pieces by a key (range of dates, list of regions, hash). Queries that filter on the key read only the relevant partitions ("partition pruning"), and old partitions can be dropped quickly.

@@ paytm-sql
**Answer.**

```sql
SELECT 'customer' AS category, c.id, c.customer_name AS name
FROM customer c
WHERE NOT EXISTS (SELECT 1 FROM invoice i WHERE i.customer_id = c.id)
UNION
SELECT 'product', p.id, p.product_name
FROM product p
WHERE NOT EXISTS (SELECT 1 FROM invoice_item ii WHERE ii.product_id = p.id);
```

**Why.** Each branch finds rows with no matching row in another table. The two branches must have the same number of columns, which is why a constant string labels each row. `NOT EXISTS` (or `LEFT JOIN ... WHERE i.id IS NULL`) is safe with NULLs, unlike `NOT IN` over a column that may contain NULL.

**Concept: anti-join and UNION.** An anti-join returns rows of A with no match in B. UNION stacks two result sets (removing duplicates); UNION ALL keeps duplicates and is faster.

@@ protium-sql
**Answer.** It returns every Electronics sale whose amount equals the largest one, with the seller's id and name (ties all share rank 1). For the largest **total** per employee, aggregate first and then rank:

```sql
SELECT emp_id, name, total
FROM (SELECT e.emp_id, e.name, SUM(s.amount) AS total,
             RANK() OVER (ORDER BY SUM(s.amount) DESC) AS rnk
      FROM sales s JOIN employees e ON e.emp_id = s.emp_id
      WHERE e.department = 'Electronics'
      GROUP BY e.emp_id, e.name) t
WHERE rnk = 1;
```

**Why.** The window function can't be filtered in the same query's WHERE (WHERE runs before window functions), so the rank is computed in a subquery and filtered outside. RANK keeps ties; ROW_NUMBER would pick one arbitrarily.

**Concept: window functions.** `RANK() OVER (ORDER BY ...)` numbers rows without collapsing them like GROUP BY does. RANK leaves gaps after ties (1, 1, 3); DENSE_RANK doesn't (1, 1, 2); ROW_NUMBER is always unique.

@@ mw-iisc-23
**Answer: (a), (b) and (d)** define it incorrectly

**Why.** The correct definition is (c): a transaction is one or more DML statements, or a single DDL/DCL statement, forming a logical unit of work in one session. COMMIT and ROLLBACK **end** a transaction (they are not one), and a transaction never spans sessions.

**Concept: transaction boundaries.** A transaction starts with the first DML statement and ends with COMMIT (save) or ROLLBACK (undo). In Oracle, a DDL statement commits implicitly, so it forms its own transaction.
