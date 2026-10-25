---
title: "4 · SQL II: grouping, subqueries, windows and the rest"
linkTitle: "4 SQL II: grouping, subqueries, windows and the rest"
weight: 4
math: true
---
## 4.1 Aggregation, GROUP BY and HAVING {#sec-dbms-groupby}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “average salary per department, only for departments with at least two people”: `WHERE` filters rows, `HAVING` filters groups.</em>

</div>

```sql {filename="c04-groupby.sql"}
-- departments with at least 2 employees hired before 2025, by average pay
SELECT dept_id, COUNT(*) AS n, MIN(salary) AS lo, MAX(salary) AS hi,
       ROUND(AVG(salary), 0) AS avg_sal
FROM employees
WHERE hire_date < '2025-01-01'        -- filters ROWS, before grouping
GROUP BY dept_id
HAVING COUNT(*) >= 2                  -- filters GROUPS, after grouping
ORDER BY avg_sal DESC;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 dept_id | n |   lo   |   hi   | avg_sal
---------+---+--------+--------+---------
      10 | 3 | 120000 | 150000 |  130000
      20 | 2 |  75000 |  90000 |   82500
(2 rows)
```

<div class="nb nb-definition" id="definition-4-1-1">

<strong>Definition 4.1.1</strong>. `GROUP BY g` partitions the rows that survived `WHERE` into groups with equal `g` (all `NULL`s together) and produces <em>one output row per group</em>. After grouping, only three kinds of expressions make sense in `SELECT`, `HAVING` and `ORDER BY`: the grouping columns, aggregates, and constants (plus, in PostgreSQL and the SQL:1999 standard, columns <strong>functionally dependent</strong> on the grouping columns, such as any column of a table whose primary key is grouped). `HAVING` is a `WHERE` for groups and may contain aggregates; `WHERE` may not, because it runs before groups exist.

</div>

### 4.1.i Which statements are valid? {#s4-1-i}

Twelve statements in the style of a “select every valid expression” question, run on both engines (one line per statement: `ok` with the row count, or the error):

```sql {filename="c04-groupby-valid.sql"}
-- V1 grouped column plus an aggregate
SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id;
-- V2 a column that is neither grouped nor aggregated
SELECT dept_id, name, COUNT(*) FROM employees GROUP BY dept_id;
-- V3 grouping column not in the select list
SELECT COUNT(*) FROM employees GROUP BY dept_id;
-- V4 aggregate in WHERE
SELECT dept_id FROM employees WHERE COUNT(*) > 1 GROUP BY dept_id;
-- V5 aggregate condition in HAVING
SELECT dept_id, AVG(salary) FROM employees
GROUP BY dept_id HAVING AVG(salary) > 80000;
-- V6 a plain (ungrouped) column in HAVING
SELECT dept_id FROM employees GROUP BY dept_id HAVING salary > 80000;
-- V7 HAVING without GROUP BY: the whole table is one group
SELECT COUNT(*) FROM employees HAVING COUNT(*) > 5;
-- V8 nested aggregates
SELECT MAX(AVG(salary)) FROM employees GROUP BY dept_id;
-- V9 dept_name is functionally dependent on the grouped primary key
SELECT d.dept_id, d.dept_name, COUNT(*)
FROM departments d JOIN employees e ON e.dept_id = d.dept_id
GROUP BY d.dept_id;
-- V10 a select-list alias in HAVING
SELECT dept_id, COUNT(*) AS n FROM employees GROUP BY dept_id HAVING n > 1;
-- V11 positions in GROUP BY and ORDER BY
SELECT dept_id, COUNT(*) FROM employees GROUP BY 1 ORDER BY 2 DESC;
-- V12 COUNT(DISTINCT *)
SELECT COUNT(DISTINCT *) FROM employees;
```

```text {filename="Result on SQLite 3.45.1"}
V1: ok, 4 rows
V2: ok, 4 rows
V3: ok, 4 rows
V4: ERROR: misuse of aggregate: COUNT()
V5: ok, 2 rows
V6: ok, 2 rows
V7: ok, 1 row
V8: ERROR: misuse of aggregate function AVG()
V9: ok, 3 rows
V10: ok, 2 rows
V11: ok, 4 rows
V12: ERROR: near "*": syntax error
```

```text {filename="Result on PostgreSQL 16.14"}
V1: ok, 4 rows
V2: ERROR: column "employees.name" must appear in the GROUP BY clause or be
    used in an aggregate function
V3: ok, 4 rows
V4: ERROR: aggregate functions are not allowed in WHERE
V5: ok, 2 rows
V6: ERROR: column "employees.salary" must appear in the GROUP BY clause or be
    used in an aggregate function
V7: ok, 1 row
V8: ERROR: aggregate function calls cannot be nested
V9: ok, 3 rows
V10: ERROR: column "n" does not exist
V11: ok, 4 rows
V12: ERROR: syntax error at or near "*"
```

|  | Standard | SQLite | Why |
|:--|:-:|:-:|:--|
| V1, V3, V5, V7, V11 | valid | ok | V3: selecting fewer columns than you group by is legal; V7: no `GROUP BY` means one group |
| V2, V6 | invalid | ok | `name`/`salary` are neither grouped nor aggregated; SQLite returns a value from an arbitrary row of the group |
| V4 | invalid | error | aggregates cannot appear in `WHERE` |
| V8 | invalid | error | aggregates cannot nest (Oracle alone accepts `MAX(AVG(x)) ... GROUP BY`) |
| V9 | valid (FD) | ok | `dept_name` depends on the grouped key `dept_id` |
| V10 | invalid | ok | aliases are not visible in `HAVING` (MySQL and SQLite allow it) |
| V12 | invalid | error | `COUNT(DISTINCT *)` does not exist; write `COUNT(DISTINCT col)` |

<div class="nb nb-remark" id="remark-4-1-2">

<strong>Remark 4.1.2</strong> (MySQL’s ONLY\_FULL\_GROUP\_BY) — MySQL behaves like SQLite (V2 runs and picks an arbitrary `name`) unless the SQL mode `ONLY_FULL_GROUP_BY` is on, which it is by default since MySQL 5.7.5; then it rejects V2 like PostgreSQL, and still accepts V9 because it also detects functional dependence. On an OA, answer by the standard: a column in `SELECT` must be grouped, aggregated or functionally dependent on the grouping columns.

</div>

<div class="nb nb-moral">

`WHERE` before grouping, `HAVING` after; after `GROUP BY` every selected column is a group key or an aggregate.

</div>

## 4.2 Subqueries {#sec-dbms-subq}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “employees who earn more than their department’s average”: a correlated subquery.</em>

</div>

<div class="nb nb-definition" id="definition-4-2-1">

<strong>Definition 4.2.1</strong>. A <strong>scalar subquery</strong> returns one row and one column and can stand wherever a value can. `IN (subquery)` tests membership in a one-column result. `EXISTS (subquery)` is TRUE iff the subquery returns at least one row (what it selects is irrelevant, hence `SELECT 1` or `SELECT *`). A <strong>correlated</strong> subquery refers to a column of the outer query and is (logically) re-evaluated for each outer row; an uncorrelated one is evaluated once.

</div>

```sql {filename="c04-subq.sql"}
-- Q1 scalar subquery: compare with the overall average
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC, name;

-- Q2 correlated: earns more than the average of their OWN department
SELECT e.name, e.dept_id, e.salary FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x
                  WHERE x.dept_id = e.dept_id)
ORDER BY e.dept_id;

-- Q3 IN with a subquery: departments in Chennai or Mumbai
SELECT name FROM employees
WHERE dept_id IN (SELECT dept_id FROM departments
                  WHERE city IN ('Chennai', 'Mumbai'))
ORDER BY name;

-- Q4 EXISTS: managers (someone reports to them)
SELECT m.name FROM employees m
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.manager_id = m.emp_id)
ORDER BY m.name;

-- Q5 scalar subquery in SELECT: head count per department
SELECT d.dept_name,
       (SELECT COUNT(*) FROM employees e WHERE e.dept_id = d.dept_id) AS n
FROM departments d ORDER BY d.dept_id;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Q1 scalar subquery: compare with the overall average
  name | salary
-------+--------
 Asha  | 150000
 Meera | 120000
 Ravi  | 120000
(3 rows)

-- Q2 correlated: earns more than the average of their OWN department
  name | dept_id | salary
-------+---------+--------
 Asha  |      10 | 150000
 Kiran |      20 |  90000
(2 rows)

-- Q3 IN with a subquery: departments in Chennai or Mumbai
 name
--------
 Asha
 Kiran
 Meera
 Neha
 Ravi
 Vikram
(6 rows)

-- Q4 EXISTS: managers (someone reports to them)
 name
-------
 Asha
 Kiran
 Ravi
(3 rows)

-- Q5 scalar subquery in SELECT: head count per department
  dept_name  | n
-------------+---
 Engineering | 3
 Sales       | 3
 HR          | 1
 Research    | 0
(4 rows)
```

Q2 compares each employee with the average of their own department (Engineering $130000$, Sales $82500$): only Asha and Kiran beat it. Farah’s department is `NULL`, so her subquery averages nothing and returns `NULL`; the comparison is UNKNOWN and she is dropped. Q5 is the subquery form of a left join plus `COUNT`: Research shows $0$.

<div class="nb nb-example nb-block" id="example-4-2-2">

<strong>Example 4.2.2</strong> (EXISTS with ORDER BY)

Customers and their orders; which customers are listed, in which order?

```sql {filename="c04-exists-order.sql"}
CREATE TABLE customer (custid INTEGER PRIMARY KEY, name VARCHAR(10));
CREATE TABLE orders (orderid INTEGER PRIMARY KEY, custid INTEGER);
INSERT INTO customer VALUES (1100, 'Leela'), (1200, 'Sameer'),
  (1300, 'Anil'), (1400, 'Gita'), (1500, 'Mohan'), (1600, 'Zara');
INSERT INTO orders VALUES (1, 1400), (2, 1200), (3, 1500), (4, 1100),
  (5, 1400);

-- Q1 customers with at least one order, by name
SELECT c.custid, c.name FROM customer c
WHERE EXISTS (SELECT * FROM orders o WHERE o.custid = c.custid)
ORDER BY c.name;

-- Q2 the uncorrelated version: EXISTS is true for every row
SELECT COUNT(*) AS n FROM customer c
WHERE EXISTS (SELECT * FROM orders o WHERE o.custid = 1400);

-- Q3 EXISTS over an aggregate is always true (COUNT returns a row)
SELECT COUNT(*) AS n FROM customer c
WHERE EXISTS (SELECT COUNT(*) FROM orders o WHERE o.custid = c.custid);
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Q1 customers with at least one order, by name
 custid |  name
--------+--------
   1400 | Gita
   1100 | Leela
   1500 | Mohan
   1200 | Sameer
(4 rows)

-- Q2 the uncorrelated version: EXISTS is true for every row
 n
---
 6
(1 row)

-- Q3 EXISTS over an aggregate is always true (COUNT returns a row)
 n
---
 6
(1 row)
```

Q1 lists exactly the customers with an order, each once (`EXISTS` never duplicates outer rows, unlike a join: Gita has two orders), in the order of `ORDER BY`, which applies to the outer query only. Q2 is uncorrelated, so it is the same TRUE for every row. Q3 is the classic broken query: `SELECT COUNT(*)` returns a row even when it counts zero, so the `EXISTS` is always TRUE.

</div>

<div class="nb nb-remark" id="remark-4-2-3">

<strong>Remark 4.2.3</strong> (A scalar subquery that returns several rows) — Engineering has three salaries, so the subquery below is not scalar:

```sql {filename="c04-scalar-many.sql"}
-- a "scalar" subquery that returns 3 rows
SELECT name FROM employees
WHERE salary = (SELECT salary FROM employees WHERE dept_id = 10);
```

```text {filename="Result on SQLite 3.45.1"}
 name
------
 Asha
(1 row)
```

```text {filename="Result on PostgreSQL 16.14"}
ERROR: more than one row returned by a subquery used as an expression
```

PostgreSQL (and the standard, Oracle, SQL Server, MySQL) raise an error. SQLite silently uses the first row the subquery happens to produce. Use `IN` or `= ANY` when several rows are possible.

</div>

<div class="nb nb-definition" id="fact-4-2-4">

<strong>Fact 4.2.4</strong> (Rewrites the optimizer does, and you can do). `IN (subquery)` and `EXISTS` become a <strong>semi-join</strong>; `NOT EXISTS` becomes an <strong>anti-join</strong>; a correlated aggregate subquery can become a join with a grouped derived table (`JOIN (SELECT dept_id, AVG(salary) ... GROUP BY dept_id)`). `NOT IN` cannot be turned into an anti-join unless both sides are known to be non-`NULL` ([Section 3.4](../03-sql-basics/#sec-dbms-null)), which is one more reason to prefer `NOT EXISTS`.

</div>

<div class="nb nb-moral">

`EXISTS` asks “is there a row?”, never “how many”; correlate it or it is a constant.

</div>

## 4.3 Set operations {#sec-dbms-setops}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `UNION` vs `UNION ALL`: $5$ rows or $10$.</em>

</div>

```sql {filename="c04-setops.sql"}
CREATE TABLE a (x INTEGER);
CREATE TABLE b (x INTEGER);
INSERT INTO a VALUES (1), (1), (2), (3), (NULL);
INSERT INTO b VALUES (1), (3), (3), (4), (NULL);

-- Q1 row counts (a and b have 5 rows each)
SELECT (SELECT COUNT(*) FROM (SELECT x FROM a UNION     SELECT x FROM b) t)
         AS union_n,
       (SELECT COUNT(*) FROM (SELECT x FROM a UNION ALL SELECT x FROM b) t)
         AS union_all_n,
       (SELECT COUNT(*) FROM (SELECT x FROM a INTERSECT SELECT x FROM b) t)
         AS intersect_n,
       (SELECT COUNT(*) FROM (SELECT x FROM a EXCEPT    SELECT x FROM b) t)
         AS except_n;

-- Q2 EXCEPT ALL subtracts counts
SELECT x FROM a EXCEPT ALL SELECT x FROM b ORDER BY x;
```

```text {filename="Result on SQLite 3.45.1"}
-- Q1 row counts (a and b have 5 rows each)
 union_n | union_all_n | intersect_n | except_n
---------+-------------+-------------+----------
       5 |          10 |           3 |        1
(1 row)

-- Q2 EXCEPT ALL subtracts counts
ERROR: near "ALL": syntax error
```

```text {filename="Result on PostgreSQL 16.14"}
-- Q1 row counts (a and b have 5 rows each)
 union_n | union_all_n | intersect_n | except_n
---------+-------------+-------------+----------
       5 |          10 |           3 |        1
(1 row)

-- Q2 EXCEPT ALL subtracts counts
 x
---
 1
 2
(2 rows)
```

<div class="nb nb-definition" id="fact-4-3-1">

<strong>Fact 4.3.1</strong>. `UNION`, `INTERSECT`, `EXCEPT` (Oracle: `MINUS`) need the same number of columns with compatible types, take the column names of the first query, and <em>remove duplicates</em>, treating `NULL`s as equal (both `NULL`s merged into one row above). The `ALL` versions keep multiplicities: `UNION ALL` adds counts, `INTERSECT ALL` takes the minimum, `EXCEPT ALL` subtracts (two $1$s minus one $1$ leaves one $1$). SQLite has only `UNION ALL`. `UNION ALL` is cheaper (no sort or hash to deduplicate): use it whenever duplicates are impossible or wanted. One `ORDER BY` at the end sorts the combined result.

</div>

<div class="nb nb-moral">

Set operators are set-based (deduplicate) unless you write `ALL`.

</div>

## 4.4 CASE, NULL functions, strings and dates {#sec-dbms-case}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> counting high and low earners in one pass with `COUNT(CASE ... END)`.</em>

</div>

```sql {filename="c04-case.sql"}
-- Q1 searched CASE: the first true branch wins; no ELSE means NULL
SELECT name,
       CASE WHEN salary >= 120000 THEN 'band A'
            WHEN salary >= 70000  THEN 'band B'
            WHEN salary IS NULL   THEN 'unknown'
            ELSE 'band C' END AS band
FROM employees ORDER BY emp_id;

-- Q2 CASE inside an aggregate: a pivot by hand
SELECT COUNT(CASE WHEN salary >= 100000 THEN 1 END) AS high,
       COUNT(CASE WHEN salary <  100000 THEN 1 END) AS low,
       SUM(CASE WHEN dept_id = 20 THEN 1 ELSE 0 END) AS in_sales
FROM employees;

-- Q3 NULLIF avoids division by zero (x / NULL is NULL)
SELECT dept_name, 100 / NULLIF(COUNT(e.emp_id), 0) AS pct_each
FROM departments d LEFT JOIN employees e ON e.dept_id = d.dept_id
GROUP BY d.dept_id, dept_name ORDER BY d.dept_id;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Q1 searched CASE: the first true branch wins; no ELSE means NULL
  name  |   band
--------+---------
 Asha   | band A
 Ravi   | band A
 Meera  | band A
 Kiran  | band B
 Neha   | band B
 Arjun  | band C
 Farah  | band C
 Vikram | unknown
(8 rows)

-- Q2 CASE inside an aggregate: a pivot by hand
 high | low | in_sales
------+-----+----------
    3 |   4 |        3
(1 row)

-- Q3 NULLIF avoids division by zero (x / NULL is NULL)
  dept_name  | pct_each
-------------+----------
 Engineering |       33
 Sales       |       33
 HR          |      100
 Research    |     NULL
(4 rows)
```

<div class="nb nb-definition" id="fact-4-4-1">

<strong>Fact 4.4.1</strong>. A searched `CASE` returns the result of the first `WHEN` that is TRUE (UNKNOWN counts as not true, so test `IS NULL` explicitly) and `NULL` if none matches and there is no `ELSE`. `COUNT(CASE WHEN p THEN 1 END)` counts rows satisfying `p`, because the missing `ELSE` gives `NULL`, which `COUNT` skips; with `ELSE 0` you must use `SUM`. `COALESCE(a, b, ...)` returns the first non-`NULL` argument; `NULLIF(a, b)` returns `NULL` if $a=b$, else $a$, the standard guard against division by zero.

</div>

String and date functions are where dialects differ most; the common subset is small:

```sql {filename="c04-functions.sql"}
-- Q1 string functions common to both engines
SELECT UPPER('ganga') AS up, LENGTH('Tapti') AS len,
       SUBSTR('Kaveri', 2, 3) AS sub, TRIM('  x  ') AS trimmed,
       REPLACE('a-b-c', '-', '+') AS repl;

-- Q2 position of a substring: INSTR (SQLite) vs POSITION (PostgreSQL)
SELECT INSTR('database', 'base') AS pos;
SELECT POSITION('base' IN 'database') AS pos;

-- Q3 date arithmetic on a fixed date
SELECT DATE('2026-02-27', '+3 days') AS d;
SELECT DATE '2026-02-27' + 3 AS d;

-- Q4 year of a date
SELECT STRFTIME('%Y', '2026-08-15') AS y;
SELECT EXTRACT(YEAR FROM DATE '2026-08-15') AS y;
```

```text {filename="Result on SQLite 3.45.1"}
-- Q1 string functions common to both engines
   up  | len | sub | trimmed |  repl
-------+-----+-----+---------+-------
 GANGA |   5 | ave | x       | a+b+c
(1 row)

-- Q2 position of a substring: INSTR (SQLite) vs POSITION (PostgreSQL)
 pos
-----
   5
(1 row)

ERROR: no such table: database

-- Q3 date arithmetic on a fixed date
 d
------------
 2026-03-02
(1 row)

ERROR: near "+": syntax error

-- Q4 year of a date
 y
------
 2026
(1 row)

ERROR: near "FROM": syntax error
```

```text {filename="Result on PostgreSQL 16.14"}
-- Q1 string functions common to both engines
   up  | len | sub | trimmed |  repl
-------+-----+-----+---------+-------
 GANGA |   5 | ave | x       | a+b+c
(1 row)

-- Q2 position of a substring: INSTR (SQLite) vs POSITION (PostgreSQL)
ERROR: function instr(unknown, unknown) does not exist

 pos
-----
   5
(1 row)

-- Q3 date arithmetic on a fixed date
ERROR: function date(unknown, unknown) does not exist

 d
------------
 2026-03-02
(1 row)

-- Q4 year of a date
ERROR: function strftime(unknown, unknown) does not exist

 y
------
 2026
(1 row)
```

| Task | PostgreSQL (standard-ish) | SQLite / others |
|:--|:--|:--|
| concatenate | `a \|\| b`, `concat(a, b)` | `a \|\| b`; MySQL `CONCAT`; SQL Server `+` |
| find substring | `POSITION(s IN t)`, `strpos` | `INSTR(t, s)` (also Oracle, MySQL) |
| today | `CURRENT_DATE` | `DATE('now')`; SQL Server `GETDATE()`; Oracle `SYSDATE` |
| add days | `d + 3`, `d + INTERVAL '3 days'` | `DATE(d, '+3 days')`; MySQL `DATE_ADD` |
| part of a date | `EXTRACT(YEAR FROM d)` | `STRFTIME('%Y', d)` (a string) |

<div class="nb nb-moral">

`CASE` inside an aggregate is the portable pivot; dates and strings need the dialect’s manual.

</div>

## 4.5 Window functions {#sec-dbms-window}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> rank employees by salary without collapsing rows, the thing `GROUP BY` cannot do.</em>

</div>

<div class="nb nb-definition" id="definition-4-5-1">

<strong>Definition 4.5.1</strong>. A <strong>window function</strong> computes a value for each row from a set of related rows (its <strong>window</strong>) without merging them: `f(...) OVER (PARTITION BY p ORDER BY o frame)`. `PARTITION BY` splits the rows into independent groups, `ORDER BY` orders each partition, and the <strong>frame</strong> (`ROWS` or `RANGE BETWEEN ... AND ...`) chooses which rows of the partition an aggregate sees. Window functions run after `WHERE`, `GROUP BY` and `HAVING`, so they cannot be used in `WHERE`: filter on them from an outer query or CTE.

</div>

```sql {filename="c04-rank.sql"}
SELECT name, dept_id, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC, name) AS rn,
       RANK()       OVER (ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS drnk,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS in_dept
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC, name;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
  name | dept_id | salary | rn | rnk | drnk | in_dept
-------+---------+--------+----+-----+------+---------
 Asha  |      10 | 150000 |  1 |   1 |    1 |       1
 Meera |      10 | 120000 |  2 |   2 |    2 |       2
 Ravi  |      10 | 120000 |  3 |   2 |    2 |       2
 Kiran |      20 |  90000 |  4 |   4 |    3 |       1
 Neha  |      20 |  75000 |  5 |   5 |    4 |       2
 Arjun |      30 |  60000 |  6 |   6 |    5 |       1
 Farah |    NULL |  55000 |  7 |   7 |    6 |       1
(7 rows)
```

<div class="nb nb-definition" id="fact-4-5-2">

<strong>Fact 4.5.2</strong> (ROW\_NUMBER, RANK, DENSE\_RANK). On the tie at $120000$: `ROW_NUMBER` gives distinct numbers, breaking ties by whatever else is in `ORDER BY` (here the name; without a tiebreaker the order is arbitrary); `RANK` gives both $2$ and then <em>skips</em> to $4$; `DENSE_RANK` gives both $2$ and continues with $3$. So “$n$-th highest <em>distinct</em> salary” is `DENSE_RANK` $=n$, and “top $n$ rows” is `ROW_NUMBER` $\le n$. `PARTITION BY dept_id` restarts the ranking per department.

</div>

```sql {filename="c04-lag-frames.sql"}
CREATE TABLE sales (day INTEGER, amount INTEGER);
INSERT INTO sales VALUES (1, 100), (2, 40), (2, 60), (3, 80), (4, 50);

SELECT day, amount,
       LAG(amount)  OVER (ORDER BY day, amount) AS prev,
       LEAD(amount) OVER (ORDER BY day, amount) AS next,
       SUM(amount) OVER (ORDER BY day, amount
                         ROWS BETWEEN UNBOUNDED PRECEDING
                         AND CURRENT ROW)     AS run_rows,
       SUM(amount) OVER (ORDER BY day)        AS run_range,
       ROUND(AVG(amount) OVER (ORDER BY day, amount
                         ROWS BETWEEN 1 PRECEDING
                         AND 1 FOLLOWING), 2) AS avg3,
       SUM(amount) OVER ()                    AS total
FROM sales
ORDER BY day, amount;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 day | amount | prev | next | run_rows | run_range |  avg3 | total
-----+--------+------+------+----------+-----------+-------+-------
   1 |    100 | NULL |   40 |      100 |       100 |    70 |   330
   2 |     40 |  100 |   60 |      140 |       200 | 66.67 |   330
   2 |     60 |   40 |   80 |      200 |       200 |    60 |   330
   3 |     80 |   60 |   50 |      280 |       280 | 63.33 |   330
   4 |     50 |   80 | NULL |      330 |       330 |    65 |   330
(5 rows)
```

<div class="nb nb-definition" id="fact-4-5-3">

<strong>Fact 4.5.3</strong> (Offsets and frames). `LAG(x)`/`LEAD(x)` read the previous/next row in window order (`NULL` at the edges; `LAG(x, k, default)` for other offsets). With `ORDER BY` and no frame, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which includes all <em>peers</em> (rows with an equal sort key): both day-2 rows get the running total $200$. `ROWS` counts physical rows, giving $140$ then $200$. With no `ORDER BY` at all the frame is the whole partition (`total`). `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` is a centered moving average. `NTILE(k)` splits into $k$ buckets; `FIRST_VALUE`, `LAST_VALUE` (mind the frame) and `NTH_VALUE` read specific rows.

</div>

<div class="nb nb-remark" id="remark-4-5-4">

<strong>Remark 4.5.4</strong> (The running-total trap) — A “running total” with `SUM(x) OVER (ORDER BY day)` jumps by the whole day when several rows share a day. Interviewers ask for running totals precisely to see whether you know the default frame; write `ROWS` (and a unique `ORDER BY`) when you mean row by row.

</div>

<div class="nb nb-moral">

`GROUP BY` collapses, windows annotate; `RANK` skips, `DENSE_RANK` does not, and the default frame is `RANGE`.

</div>

## 4.6 Common table expressions and recursion {#sec-dbms-cte}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the whole reporting chain under the CEO, at any depth.</em>

</div>

```sql {filename="c04-recursive.sql"}
-- Q1 a plain CTE names a subquery so it can be used twice
WITH dept_avg AS (
  SELECT dept_id, AVG(salary) AS a FROM employees GROUP BY dept_id
)
SELECT d.dept_id, ROUND(d.a, 0) AS avg_sal FROM dept_avg d
WHERE d.a = (SELECT MAX(a) FROM dept_avg);

-- Q2 the reporting chain under Asha, with depth and path
WITH RECURSIVE chain(emp_id, name, depth, path) AS (
  SELECT emp_id, name, 0, CAST(name AS VARCHAR(200))
  FROM employees WHERE manager_id IS NULL          -- anchor
  UNION ALL
  SELECT e.emp_id, e.name, c.depth + 1,
         CAST(c.path || ' > ' || e.name AS VARCHAR(200))
  FROM employees e JOIN chain c ON e.manager_id = c.emp_id  -- step
)
SELECT depth, path FROM chain ORDER BY path;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Q1 a plain CTE names a subquery so it can be used twice
 dept_id | avg_sal
---------+---------
      10 |  130000
(1 row)

-- Q2 the reporting chain under Asha, with depth and path
 depth |          path
-------+-----------------------
     0 | Asha
     1 | Asha > Arjun
     1 | Asha > Kiran
     2 | Asha > Kiran > Farah
     2 | Asha > Kiran > Neha
     2 | Asha > Kiran > Vikram
     1 | Asha > Ravi
     2 | Asha > Ravi > Meera
(8 rows)
```

<div class="nb nb-definition" id="definition-4-6-1">

<strong>Definition 4.6.1</strong>. `WITH name AS (query)` defines a <strong>common table expression</strong>: a named subquery visible to the rest of the statement, usable several times (Q1 uses `dept_avg` twice). `WITH RECURSIVE` allows a CTE to refer to itself: an <strong>anchor</strong> member, `UNION [ALL]`, and a <strong>recursive</strong> member that joins the CTE’s <em>previous iteration</em> with base tables. Evaluation iterates until an iteration adds no rows.

</div>

<div class="nb nb-remark" id="remark-4-6-2">

<strong>Remark 4.6.2</strong> (Termination) — Recursion stops only when a step produces nothing. A cycle in the data (`manager_id` loops) with `UNION ALL` never terminates; `UNION` stops when no <em>new</em> rows appear, or carry a path and test it (PostgreSQL 14+ also has a `CYCLE` clause). Number generators need an explicit bound (`WHERE i < 100`). Recursive CTEs are how SQL gets transitive closure ([Section 2.6](../02-algebra/#sec-dbms-calculus)); MySQL has them since 8.0.

</div>

<div class="nb nb-moral">

A recursive CTE is BFS over a table: anchor = start set, recursive member = one hop.

</div>

## 4.7 Views {#sec-dbms-views}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a `sales_staff` view that HR can query without seeing other departments.</em>

</div>

```sql {filename="c04-views.sql"}
CREATE VIEW sales_staff AS
  SELECT emp_id, name, salary FROM employees WHERE dept_id = 20;
-- V0 a view that may not be used to move rows out of itself
CREATE VIEW checked_sales AS
  SELECT emp_id, name, dept_id FROM employees WHERE dept_id = 20
  WITH CHECK OPTION;

UPDATE employees SET salary = 80000 WHERE name = 'Neha';
-- Q1 a view is a stored query: it sees the change to the base table
SELECT name, salary FROM sales_staff ORDER BY name;

UPDATE sales_staff SET salary = 95000 WHERE name = 'Kiran';
-- Q2 did the update through the view reach the table?
SELECT salary FROM employees WHERE name = 'Kiran';

-- Q3 WITH CHECK OPTION rejects a row that would leave the view
UPDATE checked_sales SET dept_id = 30 WHERE name = 'Neha';
```

```text {filename="Result on SQLite 3.45.1"}
-- V0 a view that may not be used to move rows out of itself
ERROR: near "WITH": syntax error

-- Q1 a view is a stored query: it sees the change to the base table
  name  | salary
--------+--------
 Kiran  |  90000
 Neha   |  80000
 Vikram |   NULL
(3 rows)

ERROR: cannot modify sales_staff because it is a view

-- Q2 did the update through the view reach the table?
 salary
--------
  90000
(1 row)

-- Q3 WITH CHECK OPTION rejects a row that would leave the view
ERROR: no such table: checked_sales
```

```text {filename="Result on PostgreSQL 16.14"}
-- Q1 a view is a stored query: it sees the change to the base table
  name  | salary
--------+--------
 Kiran  |  90000
 Neha   |  80000
 Vikram |   NULL
(3 rows)

-- Q2 did the update through the view reach the table?
 salary
--------
  95000
(1 row)

-- Q3 WITH CHECK OPTION rejects a row that would leave the view
ERROR: new row violates check option for view "checked_sales"
```

<div class="nb nb-definition" id="fact-4-7-1">

<strong>Fact 4.7.1</strong>. A <strong>view</strong> is a named, stored query; querying it runs the query, so it always reflects the base tables. Views give logical data independence and security (grant access to the view, not the table). A view is <strong>updatable</strong> in PostgreSQL (and the standard) when it selects from one table without `DISTINCT`, `GROUP BY`, aggregates, set operations or window functions; `WITH CHECK OPTION` rejects changes that would make the row invisible through the view. SQLite views are read-only (an `INSTEAD OF` trigger can make them writable) and SQLite has no `WITH CHECK OPTION`. A <strong>materialized view</strong> (PostgreSQL, Oracle) stores the result and must be refreshed (`REFRESH MATERIALIZED VIEW`); it trades freshness for speed.

</div>

<div class="nb nb-moral">

A view is a query with a name; a materialized view is a table with a refresh schedule.

</div>

## 4.8 Indexes in SQL {#sec-dbms-sql-index}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `CREATE INDEX idx_emp_dept ON employees (dept_id)`.</em>

</div>

```sql {filename="c04-index.sql"}
CREATE INDEX idx_emp_dept ON employees (dept_id);            -- plain
CREATE UNIQUE INDEX idx_dept_city ON departments (city);      -- unique
CREATE INDEX idx_emp_dept_sal ON employees (dept_id, salary); -- composite
CREATE INDEX idx_emp_lower ON employees (LOWER(name));        -- expression
CREATE INDEX idx_emp_paid ON employees (salary)
  WHERE salary IS NOT NULL;                                   -- partial

-- Q1 a unique index is a constraint: a second Pune is rejected
INSERT INTO departments VALUES (50, 'Legal', 'Pune');

-- Q2 the catalog lists the indexes (spelled differently per engine)
SELECT name FROM sqlite_master WHERE type = 'index' AND name LIKE 'idx%'
ORDER BY name;
SELECT indexname AS name FROM pg_indexes WHERE indexname LIKE 'idx%'
ORDER BY name;
```

```text {filename="Result on SQLite 3.45.1"}
-- Q1 a unique index is a constraint: a second Pune is rejected
ERROR: UNIQUE constraint failed: departments.city

-- Q2 the catalog lists the indexes (spelled differently per engine)
 name
------------------
 idx_dept_city
 idx_emp_dept
 idx_emp_dept_sal
 idx_emp_lower
 idx_emp_paid
(5 rows)

ERROR: no such table: pg_indexes
```

```text {filename="Result on PostgreSQL 16.14"}
-- Q1 a unique index is a constraint: a second Pune is rejected
ERROR: duplicate key value violates unique constraint "idx_dept_city"

-- Q2 the catalog lists the indexes (spelled differently per engine)
ERROR: relation "sqlite_master" does not exist

 name
------------------
 idx_dept_city
 idx_emp_dept
 idx_emp_dept_sal
 idx_emp_lower
 idx_emp_paid
(5 rows)
```

<div class="nb nb-definition" id="fact-4-8-1">

<strong>Fact 4.8.1</strong>. Indexes are not part of the relational model or of the SQL standard, but every engine has the same vocabulary: plain, `UNIQUE` (also enforces a constraint; primary keys and `UNIQUE` constraints create one automatically), composite (column order matters), expression (`LOWER(name)`; only queries using the same expression benefit) and partial (`WHERE ...`; both engines here). Indexes speed up reads and slow down every `INSERT`, `DELETE` and indexed-column `UPDATE`. Foreign keys are <em>not</em> indexed automatically in PostgreSQL or SQLite. How the optimizer chooses, and the left-prefix rule for composite indexes, are in [Section 10.5](../10-storage/#sec-dbms-index-sql).

</div>

## 4.9 Triggers and stored procedures {#sec-dbms-triggers}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> an audit table that records every salary change, whoever makes it.</em>

</div>

<div class="nb nb-definition" id="definition-4-9-1">

<strong>Definition 4.9.1</strong>. A <strong>trigger</strong> is code the database runs automatically on an event (`INSERT`, `UPDATE [OF col]`, `DELETE`) on a table, `BEFORE` or `AFTER` it (or `INSTEAD OF` it, on views), once per affected row (`FOR EACH ROW`, with the `OLD` and `NEW` row values) or once per statement.

</div>

In PostgreSQL the body is a separate function returning `trigger`:

```sql {filename="c04-trigger-plpgsql.sql"}
CREATE TABLE salary_audit (emp_id INTEGER, old_salary INTEGER,
                           new_salary INTEGER);

CREATE FUNCTION log_raise() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.salary IS DISTINCT FROM OLD.salary THEN
    INSERT INTO salary_audit VALUES (OLD.emp_id, OLD.salary, NEW.salary);
  END IF;
  RETURN NEW;          -- the row to store (NULL would skip the update)
END $$;

CREATE TRIGGER audit_salary AFTER UPDATE OF salary ON employees
FOR EACH ROW EXECUTE FUNCTION log_raise();

UPDATE employees SET salary = salary + 5000 WHERE dept_id = 20;
SELECT * FROM salary_audit ORDER BY emp_id;
```

```text {filename="Result on PostgreSQL 16.14"}
 emp_id | old_salary | new_salary
--------+------------+------------
      4 |      90000 |      95000
      5 |      75000 |      80000
(2 rows)
```

SQLite writes the body inline; same effect:

```sql {filename="c04-trigger-inline.sql"}
CREATE TABLE salary_audit (emp_id INTEGER, old_salary INTEGER,
                           new_salary INTEGER);

-- SQLite: the trigger body is SQL statements, no separate function
CREATE TRIGGER audit_salary AFTER UPDATE OF salary ON employees
FOR EACH ROW WHEN NEW.salary IS NOT OLD.salary
BEGIN
  INSERT INTO salary_audit VALUES (OLD.emp_id, OLD.salary, NEW.salary);
END;

UPDATE employees SET salary = salary + 5000 WHERE dept_id = 20;
SELECT * FROM salary_audit ORDER BY emp_id;
```

```text {filename="Result on SQLite 3.45.1"}
 emp_id | old_salary | new_salary
--------+------------+------------
      4 |      90000 |      95000
      5 |      75000 |      80000
(2 rows)
```

<div class="nb nb-definition" id="definition-4-9-2">

<strong>Definition 4.9.2</strong>. A <strong>stored procedure</strong> is named code stored in the database and run with `CALL`; it returns no value (only `OUT` parameters) and, in PostgreSQL 11+, may `COMMIT` inside. A <strong>stored function</strong> returns a value and can be used inside a query. PL/pgSQL (PostgreSQL), PL/SQL (Oracle) and T-SQL (SQL Server) are the procedural languages; SQLite has no stored procedures (the application is the procedure).

</div>

```sql {filename="c04-proc.sql"}
CREATE TABLE account (id INTEGER PRIMARY KEY,
                      balance INTEGER CHECK (balance >= 0));
INSERT INTO account VALUES (1, 500), (2, 100);

-- a procedure: does work, may COMMIT inside, called with CALL
CREATE PROCEDURE transfer(src INTEGER, dst INTEGER, amt INTEGER)
LANGUAGE plpgsql AS $$
BEGIN
  UPDATE account SET balance = balance - amt WHERE id = src;
  UPDATE account SET balance = balance + amt WHERE id = dst;
END $$;

-- a function: returns a value, usable inside a query
CREATE FUNCTION total_balance() RETURNS INTEGER LANGUAGE sql AS $$
  SELECT SUM(balance)::INTEGER FROM account
$$;

CALL transfer(1, 2, 200);
-- Q1 after a valid transfer
SELECT id, balance, total_balance() AS total FROM account ORDER BY id;

-- Q2 overdraft: the CHECK fails inside the procedure, nothing changes
CALL transfer(2, 1, 1000);
SELECT id, balance FROM account ORDER BY id;
```

```text {filename="Result on PostgreSQL 16.14"}
-- Q1 after a valid transfer
 id | balance | total
----+---------+-------
  1 |     300 |   600
  2 |     300 |   600
(2 rows)

-- Q2 overdraft: the CHECK fails inside the procedure, nothing changes
ERROR: new row for relation "account" violates check constraint
  "account_balance_check"

 id | balance
----+---------
  1 |     300
  2 |     300
(2 rows)
```

The second transfer failed in its first `UPDATE`; the `CALL` is one statement, so the error rolled back all its effects and the balances are unchanged.

<div class="nb nb-remark" id="remark-4-9-3">

<strong>Remark 4.9.3</strong> (When to use them) — Triggers enforce rules no matter which application writes (audit, denormalized counters, complex constraints); their cost is hidden work and surprising cascades. Procedures cut round trips and centralize logic, at the price of logic living in the database, which is harder to version, test and scale out. Many teams keep business logic in the application and use the database only for constraints.

</div>

## 4.10 Partitioning {#sec-dbms-partition}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> an `orders` table split by year of `order_date`.</em>

</div>

<div class="nb nb-definition" id="definition-4-10-1">

<strong>Definition 4.10.1</strong>. <strong>Partitioning</strong> stores one logical table as several physical pieces, chosen by a <strong>partition key</strong>: <strong>range</strong> (date ranges), <strong>list</strong> (region in {north, south}) or <strong>hash</strong> (spread evenly). Queries that filter on the key touch only the relevant partitions (<strong>partition pruning</strong>); old data can be dropped by dropping a partition instead of a huge `DELETE`. It is a single-server technique; splitting across servers is sharding ([Chapter 12](../12-beyond/)).

</div>

```sql {filename="c04-partition.sql"}
CREATE TABLE orders (
    order_id     INTEGER,
    customer_id  INTEGER,
    order_date   DATE NOT NULL,
    total_amount NUMERIC(10,2),
    PRIMARY KEY (order_id, order_date)  -- must include the partition key
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');  -- TO is exclusive
CREATE TABLE orders_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
CREATE TABLE orders_rest PARTITION OF orders DEFAULT;

INSERT INTO orders VALUES (1, 7, '2024-03-10', 999),
  (2, 8, '2024-12-31', 50), (3, 7, '2025-01-01', 120),
  (4, 9, '2026-02-02', 75);

-- Q1 where did each row go?
SELECT tableoid::regclass AS partition, order_id, order_date
FROM orders ORDER BY order_id;

-- Q2 partition pruning: only one partition is scanned
EXPLAIN (COSTS OFF)
SELECT * FROM orders WHERE order_date = '2025-03-01';
```

```text {filename="Result on PostgreSQL 16.14"}
-- Q1 where did each row go?
  partition  | order_id | order_date
-------------+----------+------------
 orders_2024 |        1 | 2024-03-10
 orders_2024 |        2 | 2024-12-31
 orders_2025 |        3 | 2025-01-01
 orders_rest |        4 | 2026-02-02
(4 rows)

-- Q2 partition pruning: only one partition is scanned
 query plan
---------------------------------------------
 Seq Scan on orders_2025 orders
   Filter: (order_date = '2025-03-01'::date)
(2 rows)
```

<div class="nb nb-remark" id="remark-4-10-2">

<strong>Remark 4.10.2</strong> (The same table in Oracle (not run here)) — Oracle names partitions inline and uses exclusive upper bounds with `VALUES LESS THAN`:

```sql
CREATE TABLE orders (
  order_id NUMBER PRIMARY KEY, customer_id NUMBER,
  order_date DATE, total_amount NUMBER(10,2))
PARTITION BY RANGE (order_date) (
  PARTITION p2024 VALUES LESS THAN (DATE '2025-01-01'),
  PARTITION p2025 VALUES LESS THAN (DATE '2026-01-01'),
  PARTITION pmax  VALUES LESS THAN (MAXVALUE));
```

MySQL is similar: `PARTITION BY RANGE (YEAR(order_date)) (PARTITION p2024 VALUES LESS THAN (2025), ...)`. The OA trap options put the `PARTITION BY` clause inside the column list, use `VALUES FROM`/`TO` (PostgreSQL’s spelling) in an Oracle statement, or partition by a column that is not in the table. PostgreSQL also requires the primary key to include the partition key, which is why `order_date` is in it.

</div>

<div class="nb nb-moral">

Partition by the column your big queries filter on; pruning is the whole benefit.

</div>

## 4.11 Dialect corner: TOP, LIMIT, FETCH, catalogs {#sec-dbms-dialects}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the third-highest salary written three ways.</em>

</div>

```sql {filename="c04-limit.sql"}
CREATE TABLE emp_pos (emp_id INTEGER, salary INTEGER);
INSERT INTO emp_pos VALUES (1, 500000), (2, 75000), (3, 90000),
                           (4, 85000), (5, 300000);

-- Q1 third-highest salary with LIMIT/OFFSET (SQLite, PostgreSQL, MySQL)
SELECT salary FROM emp_pos ORDER BY salary DESC LIMIT 1 OFFSET 2;

-- Q2 the standard spelling (PostgreSQL, Oracle 12c+, SQL Server 2012+)
SELECT salary FROM emp_pos ORDER BY salary DESC
OFFSET 2 ROWS FETCH FIRST 1 ROW ONLY;

-- Q3 portable: count how many distinct salaries are higher
SELECT salary FROM emp_pos e
WHERE 2 = (SELECT COUNT(DISTINCT salary) FROM emp_pos x
           WHERE x.salary > e.salary);
```

```text {filename="Result on SQLite 3.45.1"}
-- Q1 third-highest salary with LIMIT/OFFSET (SQLite, PostgreSQL, MySQL)
 salary
--------
  90000
(1 row)

-- Q2 the standard spelling (PostgreSQL, Oracle 12c+, SQL Server 2012+)
ERROR: near "OFFSET": syntax error

-- Q3 portable: count how many distinct salaries are higher
 salary
--------
  90000
(1 row)
```

```text {filename="Result on PostgreSQL 16.14"}
-- Q1 third-highest salary with LIMIT/OFFSET (SQLite, PostgreSQL, MySQL)
 salary
--------
  90000
(1 row)

-- Q2 the standard spelling (PostgreSQL, Oracle 12c+, SQL Server 2012+)
 salary
--------
  90000
(1 row)

-- Q3 portable: count how many distinct salaries are higher
 salary
--------
  90000
(1 row)
```

<div class="nb nb-definition" id="fact-4-11-1">

<strong>Fact 4.11.1</strong> (Limiting rows). `LIMIT n OFFSET k`: MySQL, PostgreSQL, SQLite. `OFFSET k ROWS FETCH FIRST n ROWS ONLY`: the SQL standard, PostgreSQL, Oracle 12c+, SQL Server 2012+ (with `ORDER BY`), not SQLite. `SELECT TOP n`: SQL Server only, and it has no offset, so the third-highest salary there is written by nesting: `SELECT TOP 1 salary FROM (SELECT DISTINCT TOP 3 salary FROM emp ORDER BY salary DESC) t ORDER BY salary ASC`. Oracle before 12c used `ROWNUM`, which is assigned <em>before</em> `ORDER BY`, so the sort must be in a subquery. Without `ORDER BY`, “first $n$ rows” is any $n$ rows.

</div>

<div class="nb nb-definition" id="fact-4-11-2">

<strong>Fact 4.11.2</strong> (Where the catalog lives). The standard catalog is `information_schema` (`tables`, `columns`, `table_constraints`), present in PostgreSQL, MySQL and SQL Server. Each engine also has its own: PostgreSQL’s `pg_catalog` (`pg_indexes`, `pg_class`), SQLite’s `sqlite_schema` table and `PRAGMA table_info(t)`, Oracle’s `USER_TABLES`/`ALL_TAB_COLUMNS`, and SQL Server’s `sys` views such as `sys.tables`, `sys.indexes` and `sys.filegroups` (one row per filegroup, with columns including `name`, `type_desc` and `is_read_only`), so “list the filegroups with their type and read-only flag” is `SELECT name, type_desc, is_read_only FROM sys.filegroups`.

</div>

<div class="nb nb-definition" id="fact-4-11-3">

<strong>Fact 4.11.3</strong> (DCL). `GRANT SELECT, INSERT ON employees TO hr_role`; `REVOKE INSERT ON employees FROM hr_role`; `GRANT ... WITH GRANT OPTION` lets the grantee grant further, and revoking it cascades. Roles group privileges. SQLite has no users or privileges.

</div>

<div class="nb nb-remark" id="remark-4-11-4">

<strong>Remark 4.11.4</strong> (Vendor versions) — OAs sometimes ask which release of a commercial database is the current long-term release. Such answers change every year or two and cannot be derived; check the vendor’s release-support page shortly before the test rather than memorising a number.

</div>

<div class="nb nb-moral">

Know `LIMIT`, `FETCH FIRST` and `TOP`, and solve “$n$-th highest” with `DENSE_RANK` or a correlated count, which work everywhere.

</div>
