---
title: "3 · SQL basics: tables, joins, NULL"
linkTitle: "3 SQL basics"
weight: 3
math: true
---
Running schema: `Employee(id, name, salary, dept_id, manager_id)`, `Department(id, dname)`.

## 3.1 Creating tables and constraints {#db-3-1}

```sql
CREATE TABLE Employee (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  salary INT CHECK (salary > 0),
  dept_id INT REFERENCES Department(id) ON DELETE SET NULL
);
```

Constraints: `PRIMARY KEY` (unique + not null), `UNIQUE` (allows one or more NULLs, depending on the DBMS), `NOT NULL`, `CHECK`, `FOREIGN KEY ... REFERENCES`, `DEFAULT`.

Changing data: `INSERT INTO t VALUES (...)`, `UPDATE t SET col = v WHERE ...`, `DELETE FROM t WHERE ...`. **Forgetting `WHERE` updates or deletes every row.**

## 3.2 The order a query is evaluated {#db-3-2}

Written: `SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT`.
**Evaluated:** `FROM` (and joins) → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `DISTINCT` → `ORDER BY` → `LIMIT`.

That is why a column alias from `SELECT` cannot be used in `WHERE`, but can be used in `ORDER BY`; and why aggregates are not allowed in `WHERE` (use `HAVING`).

## 3.3 Joins {#db-3-3}

| Join | Returns |
|---|---|
| `INNER JOIN` | only rows with a match in both tables |
| `LEFT JOIN` | all rows of the left table; NULLs where the right has no match |
| `RIGHT JOIN` | all rows of the right table |
| `FULL OUTER JOIN` | all rows of both (not in MySQL: use `LEFT … UNION … RIGHT`) |
| `CROSS JOIN` | every pair: $m \times n$ rows |
| Self join | a table joined with itself (employee with their manager) |
| `NATURAL JOIN` | equality on **all** columns with the same name (risky) |

```sql
SELECT e.name, d.dname
FROM Employee e LEFT JOIN Department d ON e.dept_id = d.id;
```

<div class="nb nb-example">

<strong>Example</strong> (Row counts)

`Students` has 100 rows, `Course` has 5. `SELECT * FROM Students, Course` has no join condition → $100 \times 5 = $ **500** rows. Joining on a column that is a key of neither table multiplies duplicates: 3 orders from Pune × 2 stores in Pune = 6 rows for Pune alone.

</div>

**Self join** (each employee with their manager's name):

```sql
SELECT e.name, m.name AS manager
FROM Employee e LEFT JOIN Employee m ON e.manager_id = m.id;
```

<div class="nb nb-remark">

<strong>Trap: NATURAL JOIN</strong> — it joins on every column with a matching name, so a shared column like `name` or `created_at` silently becomes part of the condition and rows vanish. Prefer explicit `JOIN … ON`.

</div>

## 3.4 NULL and three-valued logic {#db-3-4}

NULL means "unknown". Any comparison with NULL gives **UNKNOWN** (not TRUE, not FALSE), and `WHERE` keeps only TRUE rows.

- `NULL = NULL` is UNKNOWN → test with `IS NULL` / `IS NOT NULL`.
- `x NOT IN (1, 2, NULL)` is **never TRUE** → returns no rows. A subquery returning a NULL silently empties a `NOT IN` query; use `NOT EXISTS`.
- Aggregates **ignore NULLs**: `COUNT(col)` skips them, `COUNT(*)` counts all rows, `AVG(col)` divides by the non-NULL count.
- `NULL + 5` is NULL. Use `COALESCE(col, 0)` to replace NULLs.

<div class="nb nb-example">

<strong>Example</strong> (COUNT and AVG with NULL)

Salaries: 100, 200, NULL. `COUNT(*) = 3`, `COUNT(salary) = 2`, `SUM = 300`, `AVG(salary) = 150` (not 100).

</div>

## 3.5 DISTINCT, ORDER BY, LIMIT, LIKE {#db-3-5}

- `SELECT DISTINCT dept_id` removes duplicate rows. `COUNT(DISTINCT dept_id)` counts distinct values.
- `ORDER BY salary DESC, name` sorts; NULLs come first or last depending on the DBMS.
- `LIMIT 5 OFFSET 10` (MySQL/PostgreSQL) = `TOP 5` (SQL Server) = `FETCH FIRST 5 ROWS ONLY` (standard/Oracle).
- `LIKE 'A%'` (starts with A), `'%a'` (ends with a), `'_b%'` (second letter b). `BETWEEN 10 AND 20` is inclusive. `IN (…)` tests membership.

<div class="nb nb-moral">

Evaluation order is FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY. Comparisons with NULL are UNKNOWN, so use IS NULL, and never NOT IN over a column that can be NULL.

</div>
