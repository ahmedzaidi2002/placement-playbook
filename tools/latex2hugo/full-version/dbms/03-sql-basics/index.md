---
title: "3 · SQL I: definitions, joins and NULL"
linkTitle: "3 SQL I: definitions, joins and NULL"
weight: 3
math: true
---
Most SQL questions in online assessments are not about clever queries. They are about three things that people get wrong under time pressure: how many rows a join returns, what `NULL` does to a predicate, and which dialect accepts which syntax. This chapter is about those three; [Chapter 4](../04-sql-advanced/) covers grouping, subqueries, windows and the rest.

## 3.1 Tables, constraints and changing data {#sec-dbms-ddl}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a company database: `departments` and `employees`, with a manager column that points back into `employees`.</em>

</div>

### 3.1.i The running schema {#s3-1-i}

```sql {filename="schema-company.sql"}
CREATE TABLE departments (
    dept_id    INTEGER PRIMARY KEY,
    dept_name  VARCHAR(20) NOT NULL UNIQUE,
    city       VARCHAR(20)
);
CREATE TABLE employees (
    emp_id     INTEGER PRIMARY KEY,
    name       VARCHAR(20) NOT NULL,
    dept_id    INTEGER REFERENCES departments,
    manager_id INTEGER REFERENCES employees,
    salary     INTEGER CHECK (salary > 0),
    hire_date  DATE
);
INSERT INTO departments VALUES (10, 'Engineering', 'Chennai'),
  (20, 'Sales', 'Mumbai'), (30, 'HR', 'Pune'),
  (40, 'Research', 'Bengaluru');
INSERT INTO employees VALUES
  (1, 'Asha',   10, NULL, 150000, '2018-03-01'),
  (2, 'Ravi',   10, 1,    120000, '2019-07-15'),
  (3, 'Meera',  10, 2,    120000, '2021-01-10'),
  (4, 'Kiran',  20, 1,     90000, '2020-02-01'),
  (5, 'Neha',   20, 4,     75000, '2022-05-20'),
  (6, 'Arjun',  30, 1,     60000, '2023-08-01'),
  (7, 'Farah',  NULL, 4,   55000, '2024-01-15'),
  (8, 'Vikram', 20, 4,     NULL,  '2025-06-01');
```

Three details are deliberate and used throughout: Farah has no department, Vikram’s salary is unknown, and the Research department has nobody.

### 3.1.ii Constraints are checked by the database {#s3-1-ii}

```sql {filename="c03-constraints.sql"}
-- CHECK: salary must be positive
INSERT INTO employees VALUES (9, 'Zoya', 10, 1, -5, '2026-01-01');

-- NOT NULL: every employee has a name
INSERT INTO employees VALUES (9, NULL, 10, 1, 50000, '2026-01-01');

-- PRIMARY KEY: emp_id 1 exists
INSERT INTO employees VALUES (1, 'Zoya', 10, 1, 50000, '2026-01-01');

-- UNIQUE: two departments with one name
INSERT INTO departments VALUES (50, 'Sales', 'Delhi');

-- a string in an INTEGER column
INSERT INTO employees VALUES (9, 'Zoya', 10, 1, 'lots', '2026-01-01');
SELECT emp_id, name, salary FROM employees WHERE emp_id = 9;

-- deleting a referenced parent row (no ON DELETE action = reject)
DELETE FROM departments WHERE dept_id = 30;
```

```text {filename="Result on SQLite 3.45.1"}
-- CHECK: salary must be positive
ERROR: CHECK constraint failed: salary > 0

-- NOT NULL: every employee has a name
ERROR: NOT NULL constraint failed: employees.name

-- PRIMARY KEY: emp_id 1 exists
ERROR: UNIQUE constraint failed: employees.emp_id

-- UNIQUE: two departments with one name
ERROR: UNIQUE constraint failed: departments.dept_name

 emp_id | name | salary
--------+------+--------
      9 | Zoya | lots
(1 row)

-- deleting a referenced parent row (no ON DELETE action = reject)
ERROR: FOREIGN KEY constraint failed
```

```text {filename="Result on PostgreSQL 16.14"}
-- CHECK: salary must be positive
ERROR: new row for relation "employees" violates check constraint
  "employees_salary_check"

-- NOT NULL: every employee has a name
ERROR: null value in column "name" of relation "employees" violates not-null
  constraint

-- PRIMARY KEY: emp_id 1 exists
ERROR: duplicate key value violates unique constraint "employees_pkey"

-- UNIQUE: two departments with one name
ERROR: duplicate key value violates unique constraint
  "departments_dept_name_key"

-- a string in an INTEGER column
ERROR: invalid input syntax for type integer: "lots"

 emp_id | name | salary
--------+------+--------
(0 rows)

-- deleting a referenced parent row (no ON DELETE action = reject)
ERROR: update or delete on table "departments" violates foreign key constraint
  "employees_dept_id_fkey" on table "employees"
```

<div class="nb nb-remark" id="remark-3-1-1">

<strong>Remark 3.1.1</strong> (SQLite’s type affinity) — Every constraint fired on both engines except the type check. SQLite stores the string `'lots'` in an `INTEGER` column: its columns have a type <em>affinity</em>, not a type, and a value that cannot be converted is stored as it is. The `CHECK` passed too, because in SQLite any text compares greater than any number. PostgreSQL rejects the value at parse time. SQLite 3.37+ offers `CREATE TABLE ... STRICT` for real type checking. MySQL (non-strict mode) would silently store $0$; in strict mode it errors.

</div>

<div class="nb nb-definition" id="fact-3-1-2">

<strong>Fact 3.1.2</strong> (Changing a table and its rows). Four statements remove or reshape things, and interviewers love to compare them.

- `ALTER TABLE t ADD COLUMN c INT DEFAULT 0`, `DROP COLUMN`, `ADD CONSTRAINT`, `RENAME`: change the schema (DDL).
- `DELETE FROM t WHERE ...`: DML, row by row, fires row triggers, can be rolled back, leaves the table and its structure.
- `TRUNCATE t`: DDL in most systems; removes all rows by deallocating pages, no `WHERE`, much faster, does not fire row-level delete triggers, resets identity counters (with `RESTART IDENTITY` in PostgreSQL). In PostgreSQL it is transactional and can be rolled back; in Oracle and MySQL it commits implicitly. SQLite has no `TRUNCATE`; an unqualified `DELETE` uses a fast path.
- `DROP TABLE t`: removes data, structure, indexes, constraints and privileges; with `CASCADE` also dependent views and foreign keys.

</div>

```sql {filename="c03-dml.sql"}
-- INSERT ... SELECT: copy Sales into an archive table
CREATE TABLE sales_archive (emp_id INTEGER PRIMARY KEY, name VARCHAR(20));
INSERT INTO sales_archive
  SELECT emp_id, name FROM employees WHERE dept_id = 20;

-- correlated UPDATE: 10% raise for anyone below the dept average
UPDATE employees SET salary = salary * 11 / 10
WHERE salary < (SELECT AVG(salary) FROM employees x
                WHERE x.dept_id = employees.dept_id);

-- UPSERT (SQLite 3.24+, PostgreSQL 9.5+): insert, or update on key clash
INSERT INTO sales_archive VALUES (4, 'Kiran K')
ON CONFLICT (emp_id) DO UPDATE SET name = excluded.name;

SELECT a.emp_id, a.name, e.salary
FROM sales_archive a JOIN employees e ON a.emp_id = e.emp_id
ORDER BY a.emp_id;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 emp_id |   name  | salary
--------+---------+--------
      4 | Kiran K |  90000
      5 | Neha    |  82500
      8 | Vikram  |   NULL
(3 rows)
```

The correlated `UPDATE` compares each row with the average of <em>its own</em> department; by the standard’s semantics the subquery sees the table as it was before the statement started changing it, so the order in which rows are updated cannot matter. Neha got the raise and nobody else did. `excluded` is the row that failed to insert.

<div class="nb nb-moral">

Constraints are the cheapest correctness you can buy; know which engine actually checks which one.

</div>

## 3.2 The anatomy of a query {#sec-dbms-select}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> why `WHERE k > 100` cannot see the alias `k` defined in `SELECT`.</em>

</div>

<div class="nb nb-definition" id="fact-3-2-1">

<strong>Fact 3.2.1</strong> (Logical evaluation order). `FROM` (with joins) $\to$ `WHERE` $\to$ `GROUP BY` $\to$ `HAVING` $\to$ window functions $\to$ `SELECT` (expressions, aliases) $\to$ `DISTINCT` $\to$ set operations $\to$ `ORDER BY` $\to$ `LIMIT`/`OFFSET`.

</div>

This is the order in which clauses are <em>defined</em> to take effect, not the order the engine runs them (the optimizer reorders freely). It explains most “why is this an error” questions: `WHERE` runs before `SELECT`, so it cannot use a select-list alias or an aggregate; `ORDER BY` runs after, so it can use both.

<div class="nb nb-definition" id="fact-3-2-2">

<strong>Fact 3.2.2</strong> (Operators of the `WHERE` clause). Comparison `= <> != < <= > >=`; `BETWEEN a AND b` (inclusive on both ends); `IN (list)` and `IN (subquery)`; `LIKE` with `%` (any string) and `_` (one character); `IS [NOT] NULL`; `EXISTS`; `ANY`/`SOME`/`ALL`; the connectives `AND`, `OR`, `NOT`. Not operators of the `WHERE` clause: aggregates (`SUM`, `COUNT` belong in `HAVING`), and clauses such as `GROUP BY`, `HAVING`, `ORDER BY`.

</div>

The standard is strict about the above; engines are not. Four small queries, four dialect differences:

```sql {filename="c03-dialect.sql"}
-- Q1 alias in WHERE
SELECT name, salary / 1000 AS k FROM employees WHERE k > 100;

-- Q2 NULLs in ORDER BY ... ASC
SELECT name, salary FROM employees WHERE dept_id = 20 ORDER BY salary;

-- Q3 is LIKE case-sensitive?
SELECT COUNT(*) AS n FROM employees WHERE name LIKE 'a%';

-- Q4 integer division, NULL in ||
SELECT 7 / 2 AS q, 7 % 2 AS r, 'x' || NULL AS s;
```

```text {filename="Result on SQLite 3.45.1"}
-- Q1 alias in WHERE
  name |  k
-------+-----
 Asha  | 150
 Ravi  | 120
 Meera | 120
(3 rows)

-- Q2 NULLs in ORDER BY ... ASC
  name  | salary
--------+--------
 Vikram |   NULL
 Neha   |  75000
 Kiran  |  90000
(3 rows)

-- Q3 is LIKE case-sensitive?
 n
---
 2
(1 row)

-- Q4 integer division, NULL in ||
 q | r |  s
---+---+------
 3 | 1 | NULL
(1 row)
```

```text {filename="Result on PostgreSQL 16.14"}
-- Q1 alias in WHERE
ERROR: column "k" does not exist

-- Q2 NULLs in ORDER BY ... ASC
  name  | salary
--------+--------
 Neha   |  75000
 Kiran  |  90000
 Vikram |   NULL
(3 rows)

-- Q3 is LIKE case-sensitive?
 n
---
 0
(1 row)

-- Q4 integer division, NULL in ||
 q | r |  s
---+---+------
 3 | 1 | NULL
(1 row)
```

<div class="nb nb-remark" id="remark-3-2-3">

<strong>Remark 3.2.3</strong> (What the two boxes show) — (Q1) SQLite lets `WHERE` use a select-list alias; PostgreSQL follows the standard. (Q2) `NULL` sorts <em>first</em> in ascending order in SQLite (and MySQL, SQL Server) and <em>last</em> in PostgreSQL (and Oracle); write `NULLS FIRST` or `NULLS LAST` when it matters, which both engines here accept. (Q3) SQLite’s `LIKE` ignores ASCII case, PostgreSQL’s does not (it has `ILIKE`). (Q4) Integer division truncates everywhere here; anything concatenated with `NULL` is `NULL` (Oracle is the exception: its `||` skips `NULL`s, and it treats `''` as `NULL`).

</div>

<div class="nb nb-moral">

Read a query in logical order, `FROM` first; and never rely on an engine’s default for `NULL` ordering or case sensitivity.

</div>

## 3.3 Joins and how many rows they return {#sec-dbms-joins}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> 8 employees and 4 departments: $7$, $8$, $8$, $9$ or $32$ rows, depending on the join.</em>

</div>

### 3.3.i The join family {#s3-3-i}

<div class="nb nb-definition" id="definition-3-3-1">

<strong>Definition 3.3.1</strong>. `A [INNER] JOIN B ON p`: pairs satisfying `p`. `A LEFT [OUTER] JOIN B`: the inner join plus each unmatched row of `A` padded with `NULL`s; `RIGHT` pads unmatched `B` rows; `FULL` both. `A CROSS JOIN B` (or `FROM A, B` with no condition): every pair. A <strong>self-join</strong> joins a table with itself under two aliases. `NATURAL JOIN` equates <em>all</em> same-named columns; `JOIN ... USING (c)` equates only the listed ones and outputs `c` once.

</div>

```sql {filename="c03-join-counts.sql"}
-- 8 employees (Farah: no department), 4 departments (Research: nobody)
SELECT
  (SELECT COUNT(*) FROM employees e JOIN departments d
     ON e.dept_id = d.dept_id)                            AS inner_j,
  (SELECT COUNT(*) FROM employees e LEFT JOIN departments d
     ON e.dept_id = d.dept_id)                            AS left_j,
  (SELECT COUNT(*) FROM employees e RIGHT JOIN departments d
     ON e.dept_id = d.dept_id)                            AS right_j,
  (SELECT COUNT(*) FROM employees e FULL JOIN departments d
     ON e.dept_id = d.dept_id)                            AS full_j,
  (SELECT COUNT(*) FROM employees e CROSS JOIN departments d) AS cross_j;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 inner_j | left_j | right_j | full_j | cross_j
---------+--------+---------+--------+---------
       7 |      8 |       8 |      9 |      32
(1 row)
```

<div class="nb nb-theorem nb-block" id="theorem-3-3-2">

<strong>Theorem 3.3.2</strong> (Row counts)

Let $m$ = matched pairs, $u_A$ = rows of `A` with no partner, $u_B$ = rows of `B` with no partner. Then inner $= m$, left $= m + u_A$, right $= m + u_B$, full $= m + u_A + u_B$, cross $= |A|\cdot|B|$.

</div>

Here $m=7$ (everyone except Farah, whose `NULL` department matches nothing), $u_A=1$ (Farah), $u_B=1$ (Research), and $8\times4=32$. The full join lists all of them:

```sql {filename="c03-full-join.sql"}
SELECT e.name, d.dept_name
FROM employees e FULL OUTER JOIN departments d ON e.dept_id = d.dept_id
ORDER BY d.dept_name NULLS LAST, e.name NULLS LAST;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
  name  |  dept_name
--------+-------------
 Asha   | Engineering
 Meera  | Engineering
 Ravi   | Engineering
 Arjun  | HR
 NULL   | Research
 Kiran  | Sales
 Neha   | Sales
 Vikram | Sales
 Farah  | NULL
(9 rows)
```

<div class="nb nb-example nb-block" id="example-3-3-3">

<strong>Example 3.3.3</strong> (Cross join)

`students` has $100$ rows and `course` has $5$. `SELECT * FROM students, course` has no join condition, so it returns $100\times5=500$ rows:

```sql {filename="c03-cross.sql"}
-- 100 students and 5 courses, generated with a recursive CTE
CREATE TABLE students (id INTEGER PRIMARY KEY);
CREATE TABLE course (cid INTEGER PRIMARY KEY);
INSERT INTO students
  WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL
                          SELECT i + 1 FROM n WHERE i < 100)
  SELECT i FROM n;
INSERT INTO course VALUES (1), (2), (3), (4), (5);

SELECT COUNT(*) AS rows_returned FROM students, course;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 rows_returned
---------------
           500
(1 row)
```

(The recursive CTE that generates $1..100$ is explained in [Chapter 4](../04-sql-advanced/).)

</div>

### 3.3.ii Duplicates multiply {#s3-3-ii}

When the join column is a key on one side, each row of the other side matches at most once. When it is a key on <em>neither</em> side, a value $v$ appearing $a_v$ times on the left and $b_v$ times on the right contributes $a_v b_v$ rows:

$$
|A\bowtie B| \;=\; \sum_v a_v\, b_v .
$$

<div class="nb nb-example nb-block" id="example-3-3-4">

<strong>Example 3.3.4</strong> (RIGHT JOIN with a repeated course)

`teacher` has two rows for `MA-101`, so Isha appears twice; `BI-104` has no student and survives only because it is on the preserved (right) side; `CH-103` has no teacher and disappears:

```sql {filename="c03-right-join.sql"}
CREATE TABLE student (course VARCHAR(8), name VARCHAR(10),
                      credits INTEGER);
CREATE TABLE teacher (course VARCHAR(8), tid INTEGER);
INSERT INTO student VALUES ('MA-101', 'Isha', 4), ('PH-102', 'Rohan', 3),
                           ('CH-103', 'Tara', 2);
INSERT INTO teacher VALUES ('MA-101', 501), ('PH-102', 502),
                           ('BI-104', 504), ('MA-101', 505);

SELECT s.name, s.credits, t.course, t.tid
FROM student s RIGHT JOIN teacher t ON s.course = t.course
ORDER BY t.tid;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
  name | credits | course | tid
-------+---------+--------+-----
 Isha  |       4 | MA-101 | 501
 Rohan |       3 | PH-102 | 502
 NULL  |    NULL | BI-104 | 504
 Isha  |       4 | MA-101 | 505
(4 rows)
```

</div>

<div class="nb nb-example nb-block" id="example-3-3-5">

<strong>Example 3.3.5</strong> (Fan-out)

Orders and stores joined on the city, which is a key of neither table:

```sql {filename="c03-fanout.sql"}
-- Joining on a column that is a key on NEITHER side multiplies rows.
CREATE TABLE orders (city VARCHAR(10), order_id INTEGER);
CREATE TABLE stores (city VARCHAR(10), store_id INTEGER);
INSERT INTO orders VALUES ('Pune', 1), ('Pune', 2), ('Pune', 3),
                          ('Delhi', 4), ('Delhi', 5), ('Goa', 6),
                          (NULL, 7);
INSERT INTO stores VALUES ('Pune', 10), ('Pune', 11), ('Delhi', 12),
                          ('Agra', 13), (NULL, 14);

-- Pune 3 x 2 + Delhi 2 x 1 = 8; Goa, Agra and the NULLs match nothing
SELECT COUNT(*) AS inner_rows
FROM orders o JOIN stores s ON o.city = s.city;
SELECT COUNT(*) AS left_rows
FROM orders o LEFT JOIN stores s ON o.city = s.city;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Pune 3 x 2 + Delhi 2 x 1 = 8; Goa, Agra and the NULLs match nothing
 inner_rows
------------
          8
(1 row)

 left_rows
-----------
        10
(1 row)
```

Inner: $3\cdot2+2\cdot1=8$. Left: those $8$ plus the $2$ unmatched orders (Goa and the `NULL` city) $=10$. The `NULL` cities on both sides do not match each other.

</div>

<div class="nb nb-remark" id="remark-3-3-6">

<strong>Remark 3.3.6</strong> (Why join Venn diagrams mislead) — The familiar two-circle pictures suggest a join returns at most $|A|+|B|$ rows. Fan-out breaks that: a join on a non-key can return up to $|A|\cdot|B|$ rows. A sudden jump in a report’s totals after adding a join is almost always fan-out; aggregate before joining or join on a key.

</div>

### 3.3.iii Self-joins and the NATURAL JOIN trap {#s3-3-iii}

```sql {filename="c03-self-natural.sql"}
-- self-join: each employee with the manager's name (LEFT keeps Asha)
SELECT e.name AS employee, m.name AS manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.emp_id
ORDER BY e.emp_id;

-- NATURAL JOIN joins on EVERY common column name
CREATE TABLE projects (dept_id INTEGER, name VARCHAR(20));
INSERT INTO projects VALUES (10, 'Search'), (20, 'Kiran');
SELECT COUNT(*) AS natural_rows FROM employees NATURAL JOIN projects;
SELECT COUNT(*) AS using_rows FROM employees JOIN projects USING (dept_id);
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- self-join: each employee with the manager's name (LEFT keeps Asha)
 employee | manager
----------+---------
 Asha     | NULL
 Ravi     | Asha
 Meera    | Ravi
 Kiran    | Asha
 Neha     | Kiran
 Arjun    | Asha
 Farah    | Kiran
 Vikram   | Kiran
(8 rows)

 natural_rows
--------------
            1
(1 row)

 using_rows
------------
          6
(1 row)
```

The self-join needs `LEFT` to keep Asha, who has no manager. The natural join returned $1$ row instead of $6$: both tables have a column called `name`, so it also required the employee’s name to equal the project’s name, and only (20, Kiran) matched. Natural joins silently change meaning when someone adds a column; use `USING` or `ON`.

<div class="nb nb-moral">

Count joins with $m+u_A+u_B$ and $\sum_v a_v b_v$; `NULL` keys never match, and `NATURAL JOIN` matches more columns than you think.

</div>

## 3.4 NULL and three-valued logic {#sec-dbms-null}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `NOT IN` returning nothing because one employee has no department.</em>

</div>

### 3.4.i UNKNOWN {#s3-4-i}

<div class="nb nb-definition" id="definition-3-4-1">

<strong>Definition 3.4.1</strong>. `NULL` means “value unknown or not applicable”. Any comparison with `NULL` (including `NULL = NULL`) evaluates to <strong>UNKNOWN</strong>, a third truth value. `WHERE`, `HAVING`, `JOIN ... ON` and `CASE WHEN` keep a row only when the condition is `TRUE`; `CHECK` constraints reject only `FALSE` (so `CHECK (salary > 0)` accepts `NULL`).

</div>

```sql {filename="c03-3vl.sql"}
-- Truth tables of AND, OR, NOT with UNKNOWN (NULL), printed as T / F / U
CREATE TABLE v (x BOOLEAN);
INSERT INTO v VALUES (TRUE), (FALSE), (NULL);
SELECT CASE WHEN a.x THEN 'T' WHEN NOT a.x THEN 'F' ELSE 'U' END AS p,
       CASE WHEN b.x THEN 'T' WHEN NOT b.x THEN 'F' ELSE 'U' END AS q,
       CASE WHEN a.x AND b.x THEN 'T' WHEN NOT (a.x AND b.x) THEN 'F'
            ELSE 'U' END AS p_and_q,
       CASE WHEN a.x OR b.x THEN 'T' WHEN NOT (a.x OR b.x) THEN 'F'
            ELSE 'U' END AS p_or_q,
       CASE WHEN NOT a.x THEN 'T' WHEN a.x THEN 'F' ELSE 'U' END AS not_p
FROM v a, v b
ORDER BY 1 DESC, 2 DESC;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 p | q | p_and_q | p_or_q | not_p
---+---+---------+--------+-------
 U | U | U       | U      | U
 U | T | U       | T      | U
 U | F | F       | U      | U
 T | U | U       | T      | F
 T | T | T       | T      | F
 T | F | F       | T      | F
 F | U | F       | U      | T
 F | T | F       | T      | T
 F | F | F       | F      | T
(9 rows)
```

<div class="nb nb-definition" id="fact-3-4-2">

<strong>Fact 3.4.2</strong>. $\text{F}\wedge \text{U}=\text{F}$ and $\text{T}\vee \text{U}=\text{T}$ (the known operand decides); otherwise anything combined with U is U, and $\neg \text{U}=\text{U}$. This is Kleene’s three-valued logic.

</div>

### 3.4.ii The traps {#s3-4-ii}

```sql {filename="c03-null-where.sql"}
-- Q1 = NULL is never true, even for NULL
SELECT COUNT(*) AS eq_null FROM employees WHERE salary = NULL;

-- Q2 IS NULL is the test
SELECT COUNT(*) AS is_null FROM employees WHERE salary IS NULL;

-- Q3 a predicate and its negation do not cover all rows
SELECT (SELECT COUNT(*) FROM employees WHERE salary > 80000) AS gt,
       (SELECT COUNT(*) FROM employees
        WHERE NOT (salary > 80000))                         AS not_gt,
       (SELECT COUNT(*) FROM employees)                     AS total;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Q1 = NULL is never true, even for NULL
 eq_null
---------
       0
(1 row)

-- Q2 IS NULL is the test
 is_null
---------
       1
(1 row)

-- Q3 a predicate and its negation do not cover all rows
 gt | not_gt | total
----+--------+-------
  4 |      3 |     8
(1 row)
```

Vikram’s salary is unknown, so he satisfies neither `salary > 80000` nor its negation: $4+3\ne8$.

```sql {filename="c03-null-notin.sql"}
-- Q4 NOT IN against a list containing NULL returns nothing
SELECT COUNT(*) AS not_in FROM departments
WHERE dept_id NOT IN (SELECT dept_id FROM employees);

-- Q5 NOT EXISTS does what was meant
SELECT dept_name AS no_employees FROM departments d
WHERE NOT EXISTS (SELECT * FROM employees e WHERE e.dept_id = d.dept_id);
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Q4 NOT IN against a list containing NULL returns nothing
 not_in
--------
      0
(1 row)

-- Q5 NOT EXISTS does what was meant
 no_employees
--------------
 Research
(1 row)
```

<div class="nb nb-theorem nb-block" id="theorem-3-4-3">

<strong>Theorem 3.4.3</strong> (NOT IN with a NULL)

`x NOT IN (a, b, NULL)` means $x\ne a\wedge x\ne b\wedge x\ne \text{NULL}$; the last conjunct is UNKNOWN, so the whole condition is never TRUE. One `NULL` in the subquery empties the result. `NOT EXISTS` has no such problem, because `EXISTS` is always TRUE or FALSE. `IN` with a `NULL` in the list is safe for the rows that match.

</div>

```sql {filename="c03-null-agg.sql"}
-- Q6 the four counts
SELECT COUNT(*) AS star, COUNT(salary) AS col,
       COUNT(DISTINCT salary) AS dist,
       COUNT(manager_id) AS mgr
FROM employees;

-- Q7 AVG skips NULLs: it is not SUM / COUNT(*)
SELECT SUM(salary) AS total, ROUND(AVG(salary), 2) AS avg_sal,
       SUM(salary) / COUNT(*) AS sum_over_rows
FROM employees;

-- Q8 aggregates over no rows: COUNT is 0, the others are NULL
SELECT COUNT(*) AS n, SUM(salary) AS s, MAX(salary) AS mx
FROM employees WHERE dept_id = 40;

-- Q9 COALESCE gives a default
SELECT name, COALESCE(salary, 0) AS salary_or_0 FROM employees
WHERE dept_id = 20 ORDER BY name;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Q6 the four counts
 star | col | dist | mgr
------+-----+------+-----
    8 |   7 |    6 |   7
(1 row)

-- Q7 AVG skips NULLs: it is not SUM / COUNT(*)
 total  | avg_sal  | sum_over_rows
--------+----------+---------------
 670000 | 95714.29 |         83750
(1 row)

-- Q8 aggregates over no rows: COUNT is 0, the others are NULL
 n |  s   |  mx
---+------+------
 0 | NULL | NULL
(1 row)

-- Q9 COALESCE gives a default
  name  | salary_or_0
--------+-------------
 Kiran  |       90000
 Neha   |       75000
 Vikram |           0
(3 rows)
```

<div class="nb nb-definition" id="fact-3-4-4">

<strong>Fact 3.4.4</strong> (Aggregates and NULL). `COUNT(*)` counts rows; `COUNT(col)` counts non-`NULL` values; `COUNT(DISTINCT col)` counts distinct non-`NULL` values. `SUM`, `AVG`, `MIN`, `MAX` ignore `NULL`s, so `AVG(salary)` divides by $7$, not $8$. Over zero rows (or only `NULL`s) `COUNT` is $0$ and the others are `NULL`. `GROUP BY` puts all `NULL`s in one group, and `DISTINCT` keeps one `NULL`: for grouping, `NULL`s are “not distinct”.

</div>

<div class="nb nb-remark" id="remark-3-4-5">

<strong>Remark 3.4.5</strong> (UNIQUE and NULL) — A `UNIQUE` column accepts any number of `NULL`s in PostgreSQL, SQLite, MySQL and Oracle (for single-column keys), because `NULL`s are not equal to each other. SQL Server allows only one `NULL` in a unique index. PostgreSQL 15+ can make `NULL`s collide with `UNIQUE NULLS NOT DISTINCT`. To compare null-safely use `a IS NOT DISTINCT FROM b` (both engines here; MySQL spells it `a <=> b`).

</div>

### 3.4.iii ALL and ANY over an empty set {#s3-4-iii}

```sql {filename="c03-all-empty.sql"}
CREATE TABLE r (a INTEGER, b INTEGER, c INTEGER);
INSERT INTO r VALUES (8, 5, 6), (4, 5, 6), (3, 4, 5), (7, 2, 9);

-- > ALL over an EMPTY subquery is TRUE for every row
SELECT COUNT(*) AS n FROM r WHERE a > ALL (SELECT a FROM r WHERE b > 100);

-- > ANY over an empty subquery is FALSE for every row
SELECT COUNT(*) AS n FROM r WHERE a > ANY (SELECT a FROM r WHERE b > 100);

-- MAX over no rows is NULL, so this is NOT the same as > ALL
SELECT COUNT(*) AS n FROM r WHERE a > (SELECT MAX(a) FROM r WHERE b > 100);

INSERT INTO r VALUES (NULL, 1, 1);
-- > ALL when the subquery contains a NULL: never TRUE
SELECT COUNT(*) AS n FROM r WHERE a > ALL (SELECT a FROM r WHERE b < 3);
```

```text {filename="Result on SQLite 3.45.1"}
-- > ALL over an EMPTY subquery is TRUE for every row
ERROR: near "ALL": syntax error

-- > ANY over an empty subquery is FALSE for every row
ERROR: near "SELECT": syntax error

-- MAX over no rows is NULL, so this is NOT the same as > ALL
 n
---
 0
(1 row)

-- > ALL when the subquery contains a NULL: never TRUE
ERROR: near "ALL": syntax error
```

```text {filename="Result on PostgreSQL 16.14"}
-- > ALL over an EMPTY subquery is TRUE for every row
 n
---
 4
(1 row)

-- > ANY over an empty subquery is FALSE for every row
 n
---
 0
(1 row)

-- MAX over no rows is NULL, so this is NOT the same as > ALL
 n
---
 0
(1 row)

-- > ALL when the subquery contains a NULL: never TRUE
 n
---
 0
(1 row)
```

<div class="nb nb-theorem nb-block" id="theorem-3-4-6">

<strong>Theorem 3.4.6</strong> (Quantified comparisons)

`x > ALL (S)` is $\forall s\in S: x>s$, so it is TRUE when $S$ is empty and never TRUE when $S$ contains a `NULL` (the best it can be is UNKNOWN). `x > ANY (S)` is $\exists s\in S: x>s$, FALSE when $S$ is empty. `x > (SELECT MAX(...))` is <em>not</em> the same as `> ALL`: `MAX` of no rows is `NULL`, so it returns nothing where `> ALL` returns everything.

</div>

So with the four rows of `r` the first query returns all $4$. SQLite has no `ALL`/`ANY`/`SOME` at all (hence the syntax errors); rewrite `x > ALL (S)` as `NOT EXISTS (SELECT * FROM S WHERE s >= x)`, which also matches the empty-set behaviour.

<div class="nb nb-moral">

`WHERE` keeps only TRUE. Prefer `NOT EXISTS` to `NOT IN`, `IS NULL` to `= NULL`, and remember that `ALL` over nothing is true.

</div>

## 3.5 DISTINCT {#sec-dbms-distinct}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “which command lists the unique values of a column?”: `SELECT DISTINCT address FROM student`.</em>

</div>

```sql {filename="c03-distinct.sql"}
CREATE TABLE student (roll INTEGER PRIMARY KEY, address VARCHAR(20),
                      hostel VARCHAR(10));
INSERT INTO student VALUES (1, 'Chennai', 'Ganga'), (2, 'Mumbai', NULL),
  (3, 'Kochi', 'Ganga'), (4, 'Jaipur', NULL), (5, 'Chennai', 'Tapti'),
  (6, 'Mumbai', 'Ganga');

-- Q1 distinct addresses, counted through a derived table (no alias needed
--    in PostgreSQL 16 or SQLite; MySQL and older PostgreSQL require one)
SELECT COUNT(*) AS n FROM (SELECT DISTINCT address FROM student);

-- Q2 COUNT(DISTINCT ...) ignores NULL, DISTINCT keeps one NULL
SELECT COUNT(DISTINCT hostel) AS count_distinct,
       (SELECT COUNT(*) FROM (SELECT DISTINCT hostel FROM student) t)
         AS rows_distinct
FROM student;

-- Q3 DISTINCT applies to the whole row, not to the first column
SELECT DISTINCT address, hostel FROM student
ORDER BY address, hostel NULLS FIRST;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Q1 distinct addresses, counted through a derived table (no alias needed
 n
---
 4
(1 row)

-- Q2 COUNT(DISTINCT ...) ignores NULL, DISTINCT keeps one NULL
 count_distinct | rows_distinct
----------------+---------------
              2 |             3
(1 row)

-- Q3 DISTINCT applies to the whole row, not to the first column
 address | hostel
---------+--------
 Chennai | Ganga
 Chennai | Tapti
 Jaipur  | NULL
 Kochi   | Ganga
 Mumbai  | NULL
 Mumbai  | Ganga
(6 rows)
```

<div class="nb nb-definition" id="fact-3-5-1">

<strong>Fact 3.5.1</strong>. `DISTINCT` applies to the whole select list, not to the column after it (`SELECT DISTINCT a, b` removes duplicate $(a,b)$ pairs; Chennai appears twice). `DISTINCT` keeps one `NULL`; `COUNT(DISTINCT c)` ignores `NULL`s, so the two counts in Q2 differ ($2$ vs $3$). `SELECT DISTINCT a` and `SELECT a ... GROUP BY a` return the same rows. A query that projects a key never needs `DISTINCT`.

</div>

<div class="nb nb-remark" id="remark-3-5-2">

<strong>Remark 3.5.2</strong> (Derived tables and aliases) — Q1 omits the alias of the subquery in `FROM`. PostgreSQL accepts that only since version 16, SQLite always did, and MySQL and SQL Server insist on one (`(SELECT ...) AS t`). In an exam answer, always write the alias. `SELECT UNIQUE` is Oracle’s old synonym for `DISTINCT`; it is not standard.

</div>

<div class="nb nb-moral">

`DISTINCT` is about rows; `COUNT(DISTINCT)` is about non-`NULL` values.

</div>
