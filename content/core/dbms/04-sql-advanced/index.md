---
title: "4 · SQL advanced: grouping, subqueries, windows"
linkTitle: "4 SQL advanced"
weight: 4
math: true
---
## 4.1 GROUP BY and HAVING {#db-4-1}

`GROUP BY` collapses rows into one row per group; aggregates (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) summarise each group. `HAVING` filters **groups**, `WHERE` filters **rows** (before grouping).

```sql
SELECT dept_id, COUNT(*) AS n, AVG(salary) AS avg_sal
FROM Employee
WHERE salary > 0
GROUP BY dept_id
HAVING COUNT(*) > 5;
```

<div class="nb nb-remark">

<strong>Rule</strong> — Every column in `SELECT` must either be in `GROUP BY` or be inside an aggregate. `SELECT dept_id, name, MAX(salary) … GROUP BY dept_id` is invalid in standard SQL (which `name`?). MySQL with its default mode also rejects it.

</div>

## 4.2 Subqueries {#db-4-2}

- **Scalar subquery** (one value): `WHERE salary > (SELECT AVG(salary) FROM Employee)`.
- **`IN` / `EXISTS`**: `WHERE dept_id IN (SELECT id FROM Department WHERE dname = 'HR')`.
- **Correlated subquery** (refers to the outer row; runs once per outer row):

```sql
SELECT e.name FROM Employee e
WHERE e.salary > (SELECT AVG(salary) FROM Employee x WHERE x.dept_id = e.dept_id);
```

(Employees earning above their own department's average.)

- `EXISTS` is TRUE if the subquery returns any row; it never duplicates outer rows (a join can).
- `> ALL (subquery)`: greater than every value (TRUE if the subquery is empty). `> ANY`: greater than at least one (FALSE if empty).

## 4.3 Set operations {#db-4-3}

`UNION` (removes duplicates), `UNION ALL` (keeps them; faster), `INTERSECT`, `EXCEPT` (`MINUS` in Oracle). The two queries need the same number of compatible columns.

## 4.4 CASE and NULL functions {#db-4-4}

```sql
SELECT name,
  CASE WHEN salary >= 100000 THEN 'High'
       WHEN salary >= 50000  THEN 'Mid'
       ELSE 'Low' END AS band
FROM Employee;
```

`COALESCE(a, b, c)` returns the first non-NULL. `NULLIF(a, b)` returns NULL if a = b (handy to avoid division by zero: `x / NULLIF(y, 0)`).

## 4.5 Window functions {#db-4-5}

A window function computes over a set of related rows **without collapsing them** (unlike `GROUP BY`): `function() OVER (PARTITION BY … ORDER BY …)`.

| Function | Meaning |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3, 4 (unique even on ties) |
| `RANK()` | 1, 2, 2, **4** (ties share, then a gap) |
| `DENSE_RANK()` | 1, 2, 2, **3** (ties share, no gap) |
| `LAG(col)` / `LEAD(col)` | previous / next row's value |
| `SUM(col) OVER (ORDER BY …)` | running total |
| `NTILE(n)` | splits rows into $n$ buckets |

<div class="nb nb-example">

<strong>Example</strong> (Ranking ties)

Salaries 900, 800, 800, 700 (descending): `ROW_NUMBER` 1, 2, 3, 4; `RANK` 1, 2, 2, 4; `DENSE_RANK` 1, 2, 2, 3. "Second-highest distinct salary" = the row with `DENSE_RANK = 2` → 800.

</div>

## 4.6 CTEs, views, indexes, triggers {#db-4-6}

- **CTE** (common table expression): a named temporary result, `WITH t AS (SELECT …) SELECT … FROM t;`. **Recursive CTEs** walk hierarchies (an org chart).
- **View:** a stored query used like a table (`CREATE VIEW v AS SELECT …`). It stores no data (a **materialized view** does, and must be refreshed). Simple views can be updatable; views with joins/aggregates usually are not.
- **Index:** `CREATE INDEX idx ON Employee(dept_id);` speeds up searches and joins, slows down inserts/updates, takes space (chapter 10).
- **Trigger:** code that runs automatically `BEFORE`/`AFTER` an `INSERT`/`UPDATE`/`DELETE` (audit logs, derived columns).
- **Stored procedure:** named SQL code stored in the database, called with parameters.

<div class="nb nb-moral">

WHERE filters rows, HAVING filters groups; every selected column must be grouped or aggregated. Window functions keep the rows: RANK leaves gaps on ties, DENSE_RANK does not.

</div>
