---
title: "5 · SQL puzzles"
linkTitle: "5 SQL puzzles"
weight: 5
math: true
---
Thirty-one classic interview queries, grouped by the idea that solves them. Each listing was run on both engines; puzzles are numbered P1–P31 in the comments. Most use the company schema of [Section 3.1](../03-sql-basics/#sec-dbms-ddl); the shop puzzles use this one (customer 4 and 5 never ordered, the lamp never sold):

```sql {filename="schema-shop.sql"}
CREATE TABLE customers (cust_id INTEGER PRIMARY KEY, name VARCHAR(10),
                        city VARCHAR(10));
CREATE TABLE products (prod_id INTEGER PRIMARY KEY, pname VARCHAR(10),
                       category VARCHAR(12));
CREATE TABLE orders (order_id INTEGER PRIMARY KEY,
                     cust_id INTEGER REFERENCES customers,
                     prod_id INTEGER REFERENCES products,
                     order_date DATE, amount INTEGER);
CREATE TABLE logins (user_id INTEGER, day INTEGER);  -- day number
INSERT INTO customers VALUES (1, 'Aarav', 'Pune'), (2, 'Diya', 'Delhi'),
  (3, 'Kabir', 'Pune'), (4, 'Myra', 'Chennai'), (5, 'Vihaan', 'Delhi');
INSERT INTO products VALUES (1, 'Phone', 'Electronics'),
  (2, 'Laptop', 'Electronics'), (3, 'Kettle', 'Home'),
  (4, 'Lamp', 'Home'), (5, 'Headset', 'Electronics');
INSERT INTO orders VALUES
  (101, 1, 1, '2026-01-05', 20000), (102, 1, 3, '2026-01-20', 1500),
  (103, 2, 2, '2026-02-02', 60000), (104, 3, 1, '2026-02-14', 21000),
  (105, 1, 2, '2026-03-01', 58000), (106, 2, 3, '2026-03-03', 1500),
  (107, 3, 5, '2026-03-10', 3000),  (108, 1, 5, '2026-03-15', 2800),
  (109, 2, 1, '2026-03-20', 19500);
INSERT INTO logins VALUES (1, 1), (1, 2), (1, 3), (1, 5), (1, 6), (1, 9),
  (2, 2), (2, 3), (2, 4), (2, 5), (3, 7);
```

## 5.1 Ranking: $n$-th highest, top per group {#sec-dbms-pz-rank}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “find the third-highest salary”: three answers, one for every dialect.</em>

</div>

```sql {filename="c05-nth.sql"}
-- P1a 3rd highest DISTINCT salary: DENSE_RANK
SELECT DISTINCT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS r
  FROM employees WHERE salary IS NOT NULL) t
WHERE r = 3;

-- P1b the same with DISTINCT + LIMIT/OFFSET
SELECT DISTINCT salary FROM employees WHERE salary IS NOT NULL
ORDER BY salary DESC LIMIT 1 OFFSET 2;

-- P1c the same with a correlated count (any SQL dialect)
SELECT DISTINCT salary FROM employees e
WHERE 2 = (SELECT COUNT(DISTINCT x.salary) FROM employees x
           WHERE x.salary > e.salary);

-- P2 second highest, or NULL if there is none (HR has one salary)
SELECT (SELECT MAX(salary) FROM employees
        WHERE dept_id = 30 AND salary < (SELECT MAX(salary)
                       FROM employees WHERE dept_id = 30)) AS second_hr;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P1a 3rd highest DISTINCT salary: DENSE_RANK
 salary
--------
  90000
(1 row)

-- P1b the same with DISTINCT + LIMIT/OFFSET
 salary
--------
  90000
(1 row)

-- P1c the same with a correlated count (any SQL dialect)
 salary
--------
  90000
(1 row)

-- P2 second highest, or NULL if there is none (HR has one salary)
 second_hr
-----------
      NULL
(1 row)
```

<div class="nb nb-remark" id="remark-5-1-1">

<strong>Remark 5.1.1</strong> (What “third highest” means) — Salaries are $150000, 120000, 120000, 90000, \dots$ Ranking <em>distinct</em> values gives $90000$; ranking <em>rows</em> (`ROW_NUMBER`, or `LIMIT 1 OFFSET 2` without `DISTINCT`) gives $120000$. Ask which one is wanted. P1c works in any SQL: a salary is the $n$-th highest distinct one iff exactly $n-1$ distinct salaries exceed it. P2 wraps the query in an outer `SELECT (...)` so that “no such salary” comes out as one row containing `NULL` rather than zero rows, which is what most online judges expect.

</div>

```sql {filename="c05-dept-max.sql"}
-- P3 highest-paid employee(s) of each department, ties included
SELECT e.dept_id, e.name, e.salary FROM employees e
WHERE e.salary = (SELECT MAX(x.salary) FROM employees x
                  WHERE x.dept_id = e.dept_id)
ORDER BY e.dept_id;

-- P4 top 2 per department: ROW_NUMBER cuts ties, DENSE_RANK keeps them
SELECT dept_id, name, salary, rn, dr FROM (
  SELECT dept_id, name, salary,
         ROW_NUMBER() OVER w AS rn, DENSE_RANK() OVER w AS dr
  FROM employees WHERE dept_id IS NOT NULL AND salary IS NOT NULL
  WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC, name)) t
WHERE dr <= 2
ORDER BY dept_id, salary DESC, name;

-- P5 the department with the highest average salary
SELECT d.dept_name, ROUND(AVG(e.salary), 0) AS avg_sal
FROM employees e JOIN departments d ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY AVG(e.salary) DESC LIMIT 1;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P3 highest-paid employee(s) of each department, ties included
 dept_id |  name | salary
---------+-------+--------
      10 | Asha  | 150000
      20 | Kiran |  90000
      30 | Arjun |  60000
(3 rows)

-- P4 top 2 per department: ROW_NUMBER cuts ties, DENSE_RANK keeps them
 dept_id |  name | salary | rn | dr
---------+-------+--------+----+----
      10 | Asha  | 150000 |  1 |  1
      10 | Meera | 120000 |  2 |  2
      20 | Kiran |  90000 |  1 |  1
      20 | Neha  |  75000 |  2 |  2
      30 | Arjun |  60000 |  1 |  1
(5 rows)

-- P5 the department with the highest average salary
  dept_name  | avg_sal
-------------+---------
 Engineering |  130000
(1 row)
```

P3 keeps ties (two people at the maximum both appear); `GROUP BY dept_id` with `MAX(salary)` alone cannot say <em>who</em> has it, and adding `name` to that `GROUP BY` is the classic invalid answer ([Section 4.1](../04-sql-advanced/#sec-dbms-groupby)). P4 filters on `DENSE_RANK` so that ties at the cut stay in; with `ROW_NUMBER` $\le2$ exactly two rows per department survive. The window must be computed in a subquery: `WHERE` cannot see it. P5 uses `ORDER BY ... LIMIT 1`, which drops a tie for first place; the `= (SELECT MAX(...))` form of P3 keeps it.

<div class="nb nb-moral">

Distinct values: `DENSE_RANK`. Rows: `ROW_NUMBER`. Ties at the top: compare with a `MAX` subquery or use `RANK`.

</div>

## 5.2 Duplicates and self-joins {#sec-dbms-pz-dups}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a sign-up table where the same phone number registered three times.</em>

</div>

```sql {filename="c05-dups.sql"}
CREATE TABLE signups (id INTEGER PRIMARY KEY, phone VARCHAR(10),
                      name VARCHAR(10));
INSERT INTO signups VALUES (1, '98001', 'Asha'), (2, '98002', 'Ravi'),
  (3, '98001', 'Asha'), (4, '98003', 'Neha'), (5, '98002', 'Ravi K'),
  (6, '98001', 'A. Rao');

-- P6 phone numbers that occur more than once
SELECT phone, COUNT(*) AS n FROM signups
GROUP BY phone HAVING COUNT(*) > 1 ORDER BY phone;

-- P7 delete duplicates, keeping the row with the smallest id per phone
DELETE FROM signups
WHERE id NOT IN (SELECT MIN(id) FROM signups GROUP BY phone);
SELECT id, phone, name FROM signups ORDER BY id;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P6 phone numbers that occur more than once
 phone | n
-------+---
 98001 | 3
 98002 | 2
(2 rows)

 id | phone | name
----+-------+------
  1 | 98001 | Asha
  2 | 98002 | Ravi
  4 | 98003 | Neha
(3 rows)
```

<div class="nb nb-remark" id="remark-5-2-1">

<strong>Remark 5.2.1</strong> (Deleting duplicates elsewhere) — MySQL refuses to read the table it is deleting from in a subquery (error 1093); wrap it in a derived table, `WHERE id NOT IN (SELECT id FROM (SELECT MIN(id) AS id ...) t)`, or use a self-join delete: `DELETE a FROM signups a JOIN signups b ON a.phone = b.phone AND a.id > b.id`. With window functions: delete the rows whose `ROW_NUMBER() OVER (PARTITION BY phone ORDER BY id)` is greater than $1$. PostgreSQL also has the physical row id `ctid` for tables without a key.

</div>

```sql {filename="c05-self.sql"}
-- P8 employees who earn at least as much as their manager
SELECT e.name, e.salary, m.name AS manager, m.salary AS mgr_salary
FROM employees e JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary >= m.salary;

-- P9 number of direct reports per manager (only managers)
SELECT m.name, COUNT(*) AS reports
FROM employees e JOIN employees m ON e.manager_id = m.emp_id
GROUP BY m.emp_id, m.name ORDER BY reports DESC, m.name;

-- P10 pairs of colleagues in the same department, each pair once
SELECT a.name AS first, b.name AS second
FROM employees a JOIN employees b
  ON a.dept_id = b.dept_id AND a.emp_id < b.emp_id
ORDER BY a.emp_id, b.emp_id;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P8 employees who earn at least as much as their manager
  name | salary | manager | mgr_salary
-------+--------+---------+------------
 Meera | 120000 | Ravi    |     120000
(1 row)

-- P9 number of direct reports per manager (only managers)
  name | reports
-------+---------
 Asha  |       3
 Kiran |       3
 Ravi  |       1
(3 rows)

-- P10 pairs of colleagues in the same department, each pair once
 first | second
-------+--------
 Asha  | Ravi
 Asha  | Meera
 Ravi  | Meera
 Kiran | Neha
 Kiran | Vikram
 Neha  | Vikram
(6 rows)
```

P8 joins each employee to their manager row (two aliases of one table). P9 counts reports per manager; using an inner join it lists only managers, a `LEFT JOIN` from the manager side would add zeros. P10 uses `a.emp_id < b.emp_id` to list each unordered pair once and never pair a row with itself: a department of $n$ people gives $\binom n2$ pairs ($3+3$ here); with `<>` instead you get every pair twice.

<div class="nb nb-moral">

Duplicates: `GROUP BY ... HAVING COUNT(*) > 1`. Pairs: a self-join with a strict inequality.

</div>

## 5.3 Anti-joins: what is missing {#sec-dbms-pz-anti}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> customers who never placed an order, and products that never sold.</em>

</div>

```sql {filename="c05-anti.sql"}
-- P11a customers with no order: LEFT JOIN ... IS NULL
SELECT c.name FROM customers c
LEFT JOIN orders o ON o.cust_id = c.cust_id
WHERE o.order_id IS NULL ORDER BY c.name;

-- P11b the same with NOT EXISTS
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.cust_id)
ORDER BY c.name;

-- P12 customers and products that never appear in a sale, in one list
SELECT 'customer' AS kind, name FROM customers
WHERE cust_id NOT IN (SELECT cust_id FROM orders)
UNION ALL
SELECT 'product', pname FROM products
WHERE prod_id NOT IN (SELECT prod_id FROM orders)
ORDER BY kind, name;

-- P13 orders per customer INCLUDING zero: COUNT(o.order_id), not COUNT(*)
SELECT c.name, COUNT(o.order_id) AS right_way, COUNT(*) AS wrong_way
FROM customers c LEFT JOIN orders o ON o.cust_id = c.cust_id
GROUP BY c.cust_id, c.name ORDER BY c.cust_id;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P11a customers with no order: LEFT JOIN ... IS NULL
 name
--------
 Myra
 Vihaan
(2 rows)

-- P11b the same with NOT EXISTS
 name
--------
 Myra
 Vihaan
(2 rows)

-- P12 customers and products that never appear in a sale, in one list
   kind   |  name
----------+--------
 customer | Myra
 customer | Vihaan
 product  | Lamp
(3 rows)

-- P13 orders per customer INCLUDING zero: COUNT(o.order_id), not COUNT(*)
  name  | right_way | wrong_way
--------+-----------+-----------
 Aarav  |         4 |         4
 Diya   |         3 |         3
 Kabir  |         2 |         2
 Myra   |         0 |         1
 Vihaan |         0 |         1
(5 rows)
```

<div class="nb nb-definition" id="fact-5-3-1">

<strong>Fact 5.3.1</strong> (Three ways to find what is missing). `LEFT JOIN ... WHERE right.key IS NULL` (test a column that cannot be `NULL` in a real match, such as the primary key); `NOT EXISTS` (correlated, `NULL`-safe, usually the fastest plan); `NOT IN` (correct here only because `orders.cust_id` contains no `NULL`, [Section 3.4](../03-sql-basics/#sec-dbms-null)); also `EXCEPT` on keys. P13 is the counting version of the same trap: after a `LEFT JOIN`, `COUNT(*)` counts the padded row, so customers with no orders get $1$; `COUNT(o.order_id)` counts only real matches and gives $0$.

</div>

<div class="nb nb-moral">

“Never”, “no”, “without”: `NOT EXISTS`. After a left join, count a column of the right table.

</div>

## 5.4 Running totals, shares and changes {#sec-dbms-pz-running}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a customer’s cumulative spend after each order.</em>

</div>

```sql {filename="c05-running.sql"}
-- P14 running total of each customer's spending, in date order
-- P15 each order's share of its customer's total, in percent
SELECT cust_id, order_date, amount,
       SUM(amount) OVER (PARTITION BY cust_id ORDER BY order_date
                         ROWS UNBOUNDED PRECEDING) AS running,
       ROUND(100.0 * amount / SUM(amount) OVER (PARTITION BY cust_id), 1)
         AS pct
FROM orders WHERE cust_id IN (1, 2)
ORDER BY cust_id, order_date;

-- P16 month-over-month revenue change with LAG
SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS change
FROM (SELECT SUBSTR(CAST(order_date AS VARCHAR(10)), 1, 7) AS month,
             SUM(amount) AS revenue
      FROM orders GROUP BY 1) m
ORDER BY month;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P14 running total of each customer's spending, in date order
 cust_id | order_date | amount | running | pct
---------+------------+--------+---------+------
       1 | 2026-01-05 |  20000 |   20000 | 24.3
       1 | 2026-01-20 |   1500 |   21500 |  1.8
       1 | 2026-03-01 |  58000 |   79500 | 70.5
       1 | 2026-03-15 |   2800 |   82300 |  3.4
       2 | 2026-02-02 |  60000 |   60000 | 74.1
       2 | 2026-03-03 |   1500 |   61500 |  1.9
       2 | 2026-03-20 |  19500 |   81000 | 24.1
(7 rows)

-- P16 month-over-month revenue change with LAG
  month  | revenue | change
---------+---------+--------
 2026-01 |   21500 |   NULL
 2026-02 |   81000 |  59500
 2026-03 |   84800 |   3800
(3 rows)
```

P14 partitions by customer and uses an explicit `ROWS` frame ([Section 4.5](../04-sql-advanced/#sec-dbms-window)); P15 divides by a window `SUM` with no `ORDER BY`, i.e. the customer’s total (multiply by `100.0`, not `100`, or integer division gives $0$). P16 first aggregates per month in a derived table, then compares each month with the previous one using `LAG`; the first month has no predecessor and gets `NULL`.

<div class="nb nb-moral">

Cumulative: window `SUM` with `ROWS UNBOUNDED PRECEDING`. Change: `LAG`. Share: divide by a window total.

</div>

## 5.5 Gaps and islands {#sec-dbms-pz-islands}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> login streaks: user 1 logged in on days 1, 2, 3, 5, 6, 9.</em>

</div>

```sql {filename="c05-islands.sql"}
-- P17 islands: consecutive login streaks (day - row_number is constant)
SELECT user_id, MIN(day) AS start_day, MAX(day) AS end_day,
       COUNT(*) AS streak
FROM (SELECT user_id, day,
             day - ROW_NUMBER() OVER (PARTITION BY user_id
                                      ORDER BY day) AS grp
      FROM logins) t
GROUP BY user_id, grp
ORDER BY user_id, start_day;

-- P18 users who logged in on at least 3 consecutive days
SELECT DISTINCT a.user_id FROM logins a
JOIN logins b ON b.user_id = a.user_id AND b.day = a.day + 1
JOIN logins c ON c.user_id = a.user_id AND c.day = a.day + 2
ORDER BY a.user_id;

-- P19 gaps: missing day ranges inside each user's activity
SELECT user_id, day + 1 AS gap_from, next_day - 1 AS gap_to
FROM (SELECT user_id, day,
             LEAD(day) OVER (PARTITION BY user_id ORDER BY day) AS next_day
      FROM logins) t
WHERE next_day - day > 1
ORDER BY user_id, gap_from;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P17 islands: consecutive login streaks (day - row_number is constant)
 user_id | start_day | end_day | streak
---------+-----------+---------+--------
       1 |         1 |       3 |      3
       1 |         5 |       6 |      2
       1 |         9 |       9 |      1
       2 |         2 |       5 |      4
       3 |         7 |       7 |      1
(5 rows)

-- P18 users who logged in on at least 3 consecutive days
 user_id
---------
       1
       2
(2 rows)

-- P19 gaps: missing day ranges inside each user's activity
 user_id | gap_from | gap_to
---------+----------+--------
       1 |        4 |      4
       1 |        7 |      8
(2 rows)
```

<div class="nb nb-theorem nb-block" id="theorem-5-5-1">

<strong>Theorem 5.5.1</strong> (The island trick)

Within one user, sort the days and number them $1,2,3,\dots$. For consecutive days, $\text{day}-\text{row\_number}$ is constant; it jumps when a day is skipped. Grouping by that difference groups each streak: days $1,2,3,5,6,9$ minus $1..6$ give $0,0,0,1,1,3$, three islands.

</div>

P18 is the self-join version for a fixed length (three rows on days $d$, $d+1$, $d+2$); P19 finds the holes with `LEAD`. With real dates the same works with date arithmetic (`d - ROW_NUMBER() ...` in PostgreSQL gives a date per island; SQLite needs `julianday(d)`); this book stores day numbers to keep the query portable.

<div class="nb nb-moral">

Consecutive runs: group by value minus `ROW_NUMBER`. Holes: `LEAD` minus the current value greater than $1$.

</div>

## 5.6 Arithmetic across columns, top sale, median, pivot {#sec-dbms-pz-misc}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the class section with the largest difference between boys and girls.</em>

</div>

```sql {filename="c05-misc.sql"}
CREATE TABLE class (section VARCHAR(4), boys INTEGER, girls INTEGER,
                    total INTEGER);
INSERT INTO class VALUES ('A', 22, 18, 40), ('B', 15, 27, 42),
  ('C', 20, 21, 41), ('D', 30, 19, 49);

-- P20 the largest gap between boys and girls in any section
SELECT MAX(ABS(boys - girls)) AS max_diff FROM class;

-- P21 ... and which section has it (ties kept)
SELECT section, boys, girls FROM class
WHERE ABS(boys - girls) = (SELECT MAX(ABS(boys - girls)) FROM class);
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P20 the largest gap between boys and girls in any section
 max_diff
----------
       12
(1 row)

-- P21 ... and which section has it (ties kept)
 section | boys | girls
---------+------+-------
 B       |   15 |    27
(1 row)
```

Functions of several columns of the same row are ordinary expressions; aggregates then work on them (`MAX(ABS(boys - girls))`). `ORDER BY ABS(boys - girls) DESC LIMIT 1` also finds the section, but hides ties, which the subquery form keeps.

```sql {filename="c05-topsale.sql"}
CREATE TABLE staff (emp_id INTEGER PRIMARY KEY, name VARCHAR(10),
                    department VARCHAR(12));
CREATE TABLE sales (emp_id INTEGER REFERENCES staff, amount INTEGER,
                    sale_date DATE);
INSERT INTO staff VALUES (1, 'Ishaan', 'Electronics'),
  (2, 'Pooja', 'Electronics'), (3, 'Rehan', 'Grocery'),
  (4, 'Sana', 'Electronics');
INSERT INTO sales VALUES (1, 4000, '2026-05-01'), (2, 9000, '2026-05-02'),
  (1, 9000, '2026-05-03'), (3, 12000, '2026-05-03'),
  (4, 2500, '2026-05-04');

-- P22 the top sale in Electronics, with the seller (ties kept)
SELECT s.name, x.amount, x.sale_date
FROM sales x JOIN staff s ON s.emp_id = x.emp_id
WHERE s.department = 'Electronics'
  AND x.amount = (SELECT MAX(y.amount) FROM sales y
                  JOIN staff t ON t.emp_id = y.emp_id
                  WHERE t.department = 'Electronics')
ORDER BY s.name;

-- P23 the top seller per department by total sales
SELECT department, name, total FROM (
  SELECT s.department, s.name, SUM(x.amount) AS total,
         RANK() OVER (PARTITION BY s.department
                      ORDER BY SUM(x.amount) DESC) AS r
  FROM staff s JOIN sales x ON x.emp_id = s.emp_id
  GROUP BY s.department, s.emp_id, s.name) t
WHERE r = 1 ORDER BY department;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P22 the top sale in Electronics, with the seller (ties kept)
  name  | amount | sale_date
--------+--------+------------
 Ishaan |   9000 | 2026-05-03
 Pooja  |   9000 | 2026-05-02
(2 rows)

-- P23 the top seller per department by total sales
  department |  name  | total
-------------+--------+-------
 Electronics | Ishaan | 13000
 Grocery     | Rehan  | 12000
(2 rows)
```

P22 keeps both $9000$ sales in Electronics; P23 ranks sellers by <em>total</em> sales per department: the window is computed over the grouped rows, so `SUM(x.amount)` can appear inside `OVER (... ORDER BY ...)`.

```sql {filename="c05-median.sql"}
-- P24 median salary, portable: average of the middle one or two values
SELECT AVG(salary) AS median FROM (
  SELECT salary,
         ROW_NUMBER() OVER (ORDER BY salary) AS rn,
         COUNT(*) OVER () AS n
  FROM employees WHERE salary IS NOT NULL) t
WHERE rn IN ((n + 1) / 2, (n + 2) / 2);
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 median
--------
  90000
(1 row)
```

The middle row numbers are $(n+1)/2$ and $(n+2)/2$ in integer arithmetic: for $n=7$ both are $4$; for even $n$ they are the two middle rows and `AVG` averages them. PostgreSQL has the standard ordered-set aggregates (SQLite has neither):

```sql {filename="c05-median-ordered.sql"}
-- P24 in PostgreSQL: ordered-set aggregates (NULLs are ignored)
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_cont,
       PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY salary) AS median_disc
FROM employees;
```

```text {filename="Result on PostgreSQL 16.14"}
 median_cont | median_disc
-------------+-------------
       90000 |       90000
(1 row)
```

`PERCENTILE_CONT` interpolates between the middle values for even $n$; `PERCENTILE_DISC` returns an actual value from the data.

```sql {filename="c05-pivot.sql"}
-- P25 pivot: revenue by city (rows) and category (columns)
SELECT c.city,
       SUM(CASE WHEN p.category = 'Electronics' THEN o.amount ELSE 0 END)
         AS electronics,
       SUM(CASE WHEN p.category = 'Home' THEN o.amount ELSE 0 END) AS home,
       SUM(o.amount) AS total
FROM orders o JOIN customers c ON c.cust_id = o.cust_id
              JOIN products p ON p.prod_id = o.prod_id
GROUP BY c.city ORDER BY c.city;

-- P26 each customer's second most recent order
SELECT cust_id, order_id, order_date FROM (
  SELECT cust_id, order_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY cust_id
                            ORDER BY order_date DESC) AS rn
  FROM orders) t
WHERE rn = 2 ORDER BY cust_id;

-- P27 first and last purchase per customer
SELECT cust_id, MIN(order_date) AS first_order,
       MAX(order_date) AS last_order, COUNT(*) AS n
FROM orders GROUP BY cust_id ORDER BY cust_id;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P25 pivot: revenue by city (rows) and category (columns)
  city | electronics | home | total
-------+-------------+------+--------
 Delhi |       79500 | 1500 |  81000
 Pune  |      104800 | 1500 | 106300
(2 rows)

-- P26 each customer's second most recent order
 cust_id | order_id | order_date
---------+----------+------------
       1 |      105 | 2026-03-01
       2 |      106 | 2026-03-03
       3 |      104 | 2026-02-14
(3 rows)

-- P27 first and last purchase per customer
 cust_id | first_order | last_order | n
---------+-------------+------------+---
       1 | 2026-01-05  | 2026-03-15 | 4
       2 | 2026-02-02  | 2026-03-20 | 3
       3 | 2026-02-14  | 2026-03-10 | 2
(3 rows)
```

P25 turns category values into columns with `SUM(CASE ...)` (SQL Server and Oracle also have a `PIVOT` operator; PostgreSQL has `crosstab` in an extension and the standard `FILTER (WHERE ...)` clause on aggregates). P26 is “top-$k$ per group” with $k=2$ and only the second row kept. P27 shows that `MIN`/`MAX` work on dates.

<div class="nb nb-moral">

Row arithmetic first, aggregate second; the median is the average of the middle one or two rows; a pivot is `SUM(CASE)`.

</div>

## 5.7 Sailors, hierarchies and swaps {#sec-dbms-pz-sailors}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “names of sailors who reserved a red boat” (the instance of [Chapter 2](../02-algebra/)).</em>

</div>

```sql {filename="c05-sailors.sql"}
-- P28 names of sailors who reserved a red boat: join (DISTINCT needed)
SELECT DISTINCT s.sname FROM sailors s
JOIN reserves r ON r.sid = s.sid
JOIN boats b ON b.bid = r.bid
WHERE b.color = 'red' ORDER BY s.sname;

-- P28' the same with nested IN (no duplicates by construction)
SELECT s.sname FROM sailors s
WHERE s.sid IN (SELECT r.sid FROM reserves r
                WHERE r.bid IN (SELECT bid FROM boats WHERE color = 'red'))
ORDER BY s.sname;

-- P29 sailors who reserved every red boat (division by counting)
SELECT s.sname FROM sailors s JOIN reserves r ON r.sid = s.sid
JOIN boats b ON b.bid = r.bid AND b.color = 'red'
GROUP BY s.sid, s.sname
HAVING COUNT(DISTINCT b.bid) = (SELECT COUNT(*) FROM boats
                                WHERE color = 'red')
ORDER BY s.sname;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P28 names of sailors who reserved a red boat: join (DISTINCT needed)
 sname
-------
 Arjun
 Bina
 Divya
(3 rows)

-- P28' the same with nested IN (no duplicates by construction)
 sname
-------
 Arjun
 Bina
 Divya
(3 rows)

-- P29 sailors who reserved every red boat (division by counting)
 sname
-------
 Arjun
 Divya
(2 rows)
```

<div class="nb nb-remark" id="remark-5-7-1">

<strong>Remark 5.7.1</strong> (Join or IN?) — The join in P28 produces one row per (sailor, red reservation): Arjun reserved two red boats, so without `DISTINCT` he would appear twice. The `IN` form never duplicates the outer row. Neither confuses the two Binas, because both work on `sid`; only `DISTINCT` on `sname` merges different sailors who share a name, which here is harmless since only Bina 2 reserved a red boat. P29 is division by counting ([Section 2.3](../02-algebra/#sec-dbms-ra-div)); it relies on `(sid, bid)` pairs being counted with `DISTINCT`.

</div>

```sql {filename="c05-hier-swap.sql"}
-- P30 everyone below Asha, at any depth
WITH RECURSIVE below(emp_id, name, lvl) AS (
  SELECT emp_id, name, 1 FROM employees
  WHERE manager_id = (SELECT emp_id FROM employees WHERE name = 'Asha')
  UNION ALL
  SELECT e.emp_id, e.name, b.lvl + 1
  FROM employees e JOIN below b ON e.manager_id = b.emp_id
)
SELECT name, lvl FROM below ORDER BY lvl, name;

-- P31 swap two values in one UPDATE (all Sales <-> HR)
UPDATE employees
SET dept_id = CASE dept_id WHEN 20 THEN 30 WHEN 30 THEN 20 END
WHERE dept_id IN (20, 30);
SELECT dept_id, COUNT(*) AS n FROM employees
GROUP BY dept_id ORDER BY dept_id NULLS LAST;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- P30 everyone below Asha, at any depth
  name  | lvl
--------+-----
 Arjun  |   1
 Kiran  |   1
 Ravi   |   1
 Farah  |   2
 Meera  |   2
 Neha   |   2
 Vikram |   2
(7 rows)

 dept_id | n
---------+---
      10 | 3
      20 | 1
      30 | 3
    NULL | 1
(4 rows)
```

P30 is the recursive CTE of [Section 4.6](../04-sql-advanced/#sec-dbms-cte) started from Asha’s direct reports. P31 swaps two values in a single statement: the `CASE` is evaluated on the old values for every row, so there is no “temporary value” problem (two separate `UPDATE`s would merge both departments into one).

<div class="nb nb-moral">

Join for columns from both sides, `IN`/`EXISTS` for filtering; a hierarchy of unknown depth needs `WITH RECURSIVE`.

</div>
