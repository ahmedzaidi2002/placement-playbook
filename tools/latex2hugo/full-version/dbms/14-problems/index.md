---
title: "14 · A few harder problems to think about"
linkTitle: "14 A few harder problems to think about"
weight: 14
math: true
---
Original problems in the patterns of real online assessments and interviews. Every SQL listing was run on SQLite 3.45.1 and PostgreSQL 16.14, and every number was computed by `code/p14-checks.py`; the real outputs are in the solutions (the <em>Solution</em> drop-down under each problem). Predict before you look.

## 14.1 Modelling and keys {#s14-1}

<div class="nb nb-problem nb-block" id="problem-14-1">

<strong>Problem 14.1</strong> 🌶 (Counting super keys)

$R(A,B,C,D,E,F)$. How many super keys does $R$ have if its candidate keys are (a) $AB$ and $CD$; (b) $AB$, $BC$ and $DE$; (c) $A$ and $BC$?

<details class="nb-hint">
<summary>Hint</summary>

Count supersets of each key and correct the overlaps by inclusion–exclusion; supersets of two keys are supersets of their union.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $2^4+2^4-2^2=28$. (b) Singles: $3\cdot2^4=48$. Pairs: $AB\cup BC=ABC$ ($2^3$), $AB\cup DE=ABDE$ ($2^2$), $BC\cup DE=BCDE$ ($2^2$). Triple: $ABCDE$ ($2^1$). Total $48-8-4-4+2=34$. (c) $2^5+2^4-2^3=40$.

```text {filename="Computed by p14-checks.py"}
R(ABCDEF), keys ['AB', 'CD']: 28 super keys
R(ABCDEF), keys ['AB', 'BC', 'DE']: 34 super keys
R(ABCDEF), keys ['A', 'BC']: 40 super keys
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-2">

<strong>Problem 14.2</strong> 🌶🌶 (As many keys as possible)

A relation has $6$ attributes. (a) What is the largest possible number of candidate keys? (b) The same, if $A_1A_2$ is known to be a candidate key.

<details class="nb-hint">
<summary>Hint</summary>

Candidate keys form an antichain. For (b), every other key must be incomparable with $A_1A_2$: which $3$-attribute sets are ruled out?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $\binom63=20$ (Sperner: all $3$-sets). (b) A key containing $A_1A_2$ is not minimal, so the $4$ three-sets $A_1A_2X$ are excluded; one cannot do better by mixing sizes, and adding $A_1A_2$ itself gives $20-4+1=17$. The exact maximum antichain (Dilworth, [Section 1.4](../01-relational/#sec-dbms-keys)) confirms it:

```text {filename="Computed by p14-checks.py"}
n = 6: at most 20 candidate keys (C(6,3) = 20)
n = 6, A1A2 a key: at most 17
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-3">

<strong>Problem 14.3</strong> (Minimum number of tables)

An ER diagram has entity sets $E_1(\underline{a},\{m\})$ with a multivalued attribute $m$, $E_2(\underline{b})$ and $E_3(\underline{c})$; relationship $R_1$ between $E_1$ and $E_2$ is 1:N ($E_2$ on the N side, partial participation on both sides), $R_2$ between $E_2$ and $E_3$ is M:N, and $R_3$ between $E_1$ and $E_3$ is 1:1 with total participation on both sides. What is the minimum number of tables in a good relational design?

<details class="nb-hint">
<summary>Hint</summary>

Which relationships need their own table, and which entity sets can be merged?

</details>

<details class="nb-sol">
<summary>Solution</summary>

$4$: one table for $E_1$, $E_3$ and $R_3$ merged (1:1, total on both sides); one for $m$; one for $E_2$ carrying $a$ as a nullable foreign key ($R_1$); one for $R_2$ ($b$, $c$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-4">

<strong>Problem 14.4</strong> (Cascades)

Predict the three counts.

```sql {filename="p14-fk.sql"}
CREATE TABLE team (tid INTEGER PRIMARY KEY);
CREATE TABLE player (pid INTEGER PRIMARY KEY,
                     tid INTEGER REFERENCES team ON DELETE CASCADE);
CREATE TABLE coach (cid INTEGER PRIMARY KEY,
                    tid INTEGER REFERENCES team ON DELETE SET NULL);
INSERT INTO team VALUES (1), (2), (3);
INSERT INTO player VALUES (10, 1), (11, 1), (12, 2), (13, 3), (14, NULL);
INSERT INTO coach VALUES (20, 1), (21, 2), (22, 1);

DELETE FROM team WHERE tid = 1;
SELECT (SELECT COUNT(*) FROM player) AS players,
       (SELECT COUNT(*) FROM coach) AS coaches,
       (SELECT COUNT(*) FROM coach WHERE tid IS NULL) AS coaches_without_team;
```

<details class="nb-hint">
<summary>Hint</summary>

`CASCADE` deletes the referencing rows; `SET NULL` keeps them. Player 14 never referenced a team.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Players 10 and 11 are deleted with team 1: $3$ players remain (12, 13, 14). Coaches 20 and 22 stay with `tid` set to `NULL`: $3$ coaches, $2$ without a team.

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 players | coaches | coaches_without_team
---------+---------+----------------------
       3 |       3 |                    2
(1 row)
```

</details>

</div>

## 14.2 Relational algebra {#s14-2}

<div class="nb nb-problem nb-block" id="problem-14-5">

<strong>Problem 14.5</strong> (Division)

$$
R(s,c)=\{(u,c_1),(u,c_2),(u,c_3),(v,c_1),(v,c_3),(w,c_2),(w,c_3),(w,c_1),(x,c_3)\}
$$

and $S(c)=\{c_1,c_3\}$. Compute $R\div S$ and the upper bound $\lfloor|R|/|S|\rfloor$.

<details class="nb-hint">
<summary>Hint</summary>

Which students appear with both $c_1$ and $c_3$?

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\{u,v,w\}$; $x$ lacks $c_1$. The bound is $\lfloor9/2\rfloor=4$.

```text {filename="Computed by p14-checks.py"}
R / S = ['u', 'v', 'w']
bound floor(|R|/|S|) = 4
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-6">

<strong>Problem 14.6</strong> (Join sizes)

$R(A,B)$ has $30$ tuples and $S(B,C)$ has $20$. Give the minimum and maximum of $|R\bowtie S|$ (a) in general; (b) if $B$ is the key of $S$; (c) if moreover $R.B$ is a non-null foreign key referencing $S$; (d) what is $|R\times S|$?

<details class="nb-hint">
<summary>Hint</summary>

A key on one side means each tuple of the other side matches at most once.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $0$ to $600$ (every tuple shares one $B$ value). (b) $0$ to $30$. (c) exactly $30$. (d) $600$. See [Section 2.2](../02-algebra/#sec-dbms-ra-joins).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-7">

<strong>Problem 14.7</strong> (Which equivalences hold?)

Select every identity that holds for all relations ($R,S$ union compatible): (a) $\sigma_c(R\cup S)=\sigma_c(R)\cup \sigma_c(S)$; (b) $\pi_A(R-S)=\pi_A(R)-\pi_A(S)$; (c) $\pi_A(R\cup S)=\pi_A(R)\cup \pi_A(S)$; (d) $\pi_A(R\cap S)=\pi_A(R)\cap \pi_A(S)$; (e) $\sigma_c(R-S)=\sigma_c(R)-S$.

<details class="nb-hint">
<summary>Hint</summary>

Look for two tuples that agree on $A$ but differ elsewhere.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (c), (e). (b) and (d) fail: $R=\{(0,0)\}$, $S=\{(0,1)\}$ project to the same $\{0\}$; the random search of [Section 2.5](../02-algebra/#sec-dbms-ra-equiv) found exactly these counterexamples.

</details>

</div>

## 14.3 SQL output and validity {#s14-3}

<div class="nb nb-problem nb-block" id="problem-14-8">

<strong>Problem 14.8</strong> (Cross joins)

`students` has $40$ rows with `batch` $=0,1,2,3$ ($10$ each) and `courses` has $6$ rows (`cid` $1..6$). Give `q1`, `q2`, `q3`.

```sql {filename="p14-cross.sql"}
CREATE TABLE students (id INTEGER PRIMARY KEY, batch INTEGER);
CREATE TABLE courses (cid INTEGER PRIMARY KEY);
INSERT INTO students
  WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL
                          SELECT i + 1 FROM n WHERE i < 40)
  SELECT i, i % 4 FROM n;
INSERT INTO courses VALUES (1), (2), (3), (4), (5), (6);

SELECT (SELECT COUNT(*) FROM students, courses) AS q1,
       (SELECT COUNT(*) FROM students s, courses c
        WHERE s.batch = 0) AS q2,
       (SELECT COUNT(*) FROM students s JOIN courses c
        ON s.batch = c.cid) AS q3;
```

<details class="nb-hint">
<summary>Hint</summary>

A condition that mentions only one table filters before the product multiplies.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$40\cdot6=240$; $10\cdot6=60$; batches $1,2,3$ match one course each: $30$.

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
  q1 | q2 | q3
-----+----+----
 240 | 60 | 30
(1 row)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-9">

<strong>Problem 14.9</strong> (RIGHT JOIN)

List the rows of the result, in order.

```sql {filename="p14-right-join.sql"}
CREATE TABLE enrol (course VARCHAR(6), name VARCHAR(8), credits INTEGER);
CREATE TABLE faculty (course VARCHAR(6), fid INTEGER);
INSERT INTO enrol VALUES ('EE-201', 'Aman', 3), ('ME-110', 'Bela', 4),
                         ('EE-201', 'Chirag', 3), ('CY-105', 'Dia', 2);
INSERT INTO faculty VALUES ('EE-201', 71), ('BT-300', 72), ('ME-110', 73);

SELECT e.name, f.course, f.fid
FROM enrol e RIGHT JOIN faculty f ON e.course = f.course
ORDER BY f.fid, e.name;
```

<details class="nb-hint">
<summary>Hint</summary>

Every faculty row survives; enrolments without a faculty row vanish; repeated courses multiply.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Four rows: Aman and Chirag with EE-201/71, a `NULL` name for BT-300/72, Bela with ME-110/73. Dia (CY-105) has no faculty row and disappears.

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
  name  | course | fid
--------+--------+-----
 Aman   | EE-201 |  71
 Chirag | EE-201 |  71
 NULL   | BT-300 |  72
 Bela   | ME-110 |  73
(4 rows)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-10">

<strong>Problem 14.10</strong> 🌶 (ALL, ANY and the empty set)

For the five rows of `r`, give the four counts.

```sql {filename="p14-quantified.sql"}
CREATE TABLE r (a INTEGER, b INTEGER, c INTEGER);
INSERT INTO r VALUES (6, 1, 4), (2, 7, 3), (9, 4, 4), (5, 5, 8), (1, 3, 6);

-- Q1
SELECT COUNT(*) AS q1 FROM r WHERE a > ALL (SELECT b FROM r WHERE c > 8);
-- Q2
SELECT COUNT(*) AS q2 FROM r WHERE a > ALL (SELECT b FROM r WHERE c = 4);
-- Q3
SELECT COUNT(*) AS q3 FROM r WHERE a < ANY (SELECT c FROM r WHERE b > 4);
-- Q4
SELECT COUNT(*) AS q4 FROM r WHERE a >= (SELECT MAX(b) FROM r WHERE c > 8);
```

<details class="nb-hint">
<summary>Hint</summary>

Which subqueries are empty? What is `MAX` of no rows?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Q1: no row has $c>8$, so `> ALL` of the empty set is TRUE: $5$. Q2: $b\in \{1,4\}$ for $c=4$, so $a>4$: $6, 9, 5$, i.e. $3$. Q3: $c$ values for $b>4$ are $\{3,8\}$, so $a<8$: $6,2,5,1$, i.e. $4$. Q4: `MAX` over no rows is `NULL`: $0$ rows.

```text {filename="Result on PostgreSQL 16.14"}
-- Q1
 q1
----
  5
(1 row)

-- Q2
 q2
----
  3
(1 row)

-- Q3
 q3
----
  4
(1 row)

-- Q4
 q4
----
  0
(1 row)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-11">

<strong>Problem 14.11</strong> 🌶 (NULL arithmetic)

Give the six values.

```sql {filename="p14-nulls.sql"}
CREATE TABLE emp (id INTEGER PRIMARY KEY, dept INTEGER, bonus INTEGER);
INSERT INTO emp VALUES (1, 10, 500), (2, 10, NULL), (3, 20, 300),
                       (4, NULL, 200), (5, 30, NULL);
CREATE TABLE dept (id INTEGER PRIMARY KEY);
INSERT INTO dept VALUES (10), (20), (30), (40);

SELECT (SELECT COUNT(*) FROM dept
        WHERE id NOT IN (SELECT dept FROM emp))           AS a,
       (SELECT COUNT(*) FROM dept d WHERE NOT EXISTS
          (SELECT 1 FROM emp e WHERE e.dept = d.id))      AS b,
       (SELECT COUNT(bonus) FROM emp)                     AS c,
       (SELECT ROUND(AVG(bonus), 2) FROM emp)             AS d,
       (SELECT SUM(bonus) / COUNT(*) FROM emp)            AS e,
       (SELECT COUNT(*) FROM (SELECT DISTINCT dept FROM emp) t) AS f;
```

<details class="nb-hint">
<summary>Hint</summary>

One employee has a `NULL` department; two have `NULL` bonuses.

</details>

<details class="nb-sol">
<summary>Solution</summary>

a $=0$ (`NOT IN` a list containing `NULL`); b $=1$ (department 40); c $=3$; d $=1000/3\approx333.33$; e $=1000/5=200$; f $=4$ (`DISTINCT` keeps one `NULL`: $10,20,30,$`NULL`).

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 a | b | c |   d    |  e  | f
---+---+---+--------+-----+---
 0 | 1 | 3 | 333.33 | 200 | 4
(1 row)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-12">

<strong>Problem 14.12</strong> (EXISTS and ORDER BY)

What does the query print?

```sql {filename="p14-exists.sql"}
CREATE TABLE client (cid INTEGER PRIMARY KEY, name VARCHAR(8));
CREATE TABLE bill (bid INTEGER PRIMARY KEY, cid INTEGER, amt INTEGER);
INSERT INTO client VALUES (11, 'Om'), (12, 'Ira'), (13, 'Raj'),
                          (14, 'Ved'), (15, 'Anu');
INSERT INTO bill VALUES (1, 13, 900), (2, 11, 50), (3, 13, 20),
                        (4, 15, 700);

SELECT c.name FROM client c
WHERE EXISTS (SELECT * FROM bill b WHERE b.cid = c.cid AND b.amt > 100)
ORDER BY c.name DESC;
```

<details class="nb-hint">
<summary>Hint</summary>

The subquery is correlated; only bills above $100$ count.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Raj (bill of 900) and Anu (700), in descending name order: Raj, Anu. Om’s only bill is 50; Ira and Ved have none.

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 name
------
 Raj
 Anu
(2 rows)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-13">

<strong>Problem 14.13</strong> (Valid grouping)

Which of S1–S7 are valid standard SQL?

```sql {filename="p14-groupby.sql"}
CREATE TABLE sale (region VARCHAR(5), rep VARCHAR(5), amount INTEGER);
INSERT INTO sale VALUES ('N', 'ab', 10), ('N', 'cd', 20), ('S', 'ef', 5);
-- S1
SELECT region, SUM(amount) FROM sale
GROUP BY region HAVING SUM(amount) > 10;
-- S2
SELECT region, rep FROM sale GROUP BY region;
-- S3
SELECT SUM(amount) FROM sale GROUP BY region;
-- S4
SELECT region FROM sale WHERE SUM(amount) > 10 GROUP BY region;
-- S5
SELECT region, COUNT(*) FROM sale GROUP BY region HAVING MAX(amount) > 6;
-- S6
SELECT MAX(SUM(amount)) FROM sale GROUP BY region;
-- S7
SELECT region, AVG(amount) FROM sale WHERE amount > 6 GROUP BY region;
```

<details class="nb-hint">
<summary>Hint</summary>

Every selected column must be grouped or aggregated; aggregates are not allowed in `WHERE` and do not nest.

</details>

<details class="nb-sol">
<summary>Solution</summary>

S1, S3, S5, S7 are valid. S2 selects an ungrouped column (SQLite accepts it anyway), S4 puts an aggregate in `WHERE`, S6 nests aggregates.

```text {filename="Result on SQLite 3.45.1"}
S1: ok, 1 row
S2: ok, 2 rows
S3: ok, 2 rows
S4: ERROR: misuse of aggregate: SUM()
S5: ok, 1 row
S6: ERROR: misuse of aggregate function SUM()
S7: ok, 1 row
```

```text {filename="Result on PostgreSQL 16.14"}
S1: ok, 1 row
S2: ERROR: column "sale.rep" must appear in the GROUP BY clause or be used in
    an aggregate function
S3: ok, 2 rows
S4: ERROR: aggregate functions are not allowed in WHERE
S5: ok, 1 row
S6: ERROR: aggregate function calls cannot be nested
S7: ok, 1 row
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-14">

<strong>Problem 14.14</strong> (Clauses and operators)

(a) Which clause restricts the groups returned to those satisfying a condition? (b) Which of these is not an operator of the `WHERE` clause: `BETWEEN`, `LIKE`, `IN`, `ORDER BY`, `IS NULL`? (c) Which command lists each distinct value of column `c` of table `t` once?

<details class="nb-hint">
<summary>Hint</summary>

Groups exist only after `GROUP BY`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) `HAVING`. (b) `ORDER BY`, a separate clause. (c) `SELECT DISTINCT c FROM t` (`GROUP BY c` also works; Oracle accepts `SELECT UNIQUE`).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-15">

<strong>Problem 14.15</strong> (Largest difference between two columns)

Which of A–D return the largest difference between men and women in any ward, and which ward(s) have it?

```sql {filename="p14-maxdiff.sql"}
CREATE TABLE ward (ward VARCHAR(3), men INTEGER, women INTEGER);
INSERT INTO ward VALUES ('W1', 410, 470), ('W2', 380, 440),
  ('W3', 505, 455), ('W4', 300, 350), ('W5', 290, 260);
-- A
SELECT MAX(men - women) AS a FROM ward;
-- B
SELECT MAX(ABS(men - women)) AS b FROM ward;
-- C
SELECT MAX(men) - MAX(women) AS c FROM ward;
-- D
SELECT ward FROM ward
WHERE ABS(men - women) = (SELECT MAX(ABS(men - women)) FROM ward)
ORDER BY ward;
```

<details class="nb-hint">
<summary>Hint</summary>

“Largest difference” means the absolute value, per row.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Only B ($60$). A ignores wards with more women; C subtracts maxima from different rows. D names the wards: W1 and W2 (both $60$).

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- A
 a
----
 50
(1 row)

-- B
 b
----
 60
(1 row)

-- C
 c
----
 35
(1 row)

-- D
 ward
------
 W1
 W2
(2 rows)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-16">

<strong>Problem 14.16</strong> (Third highest)

Salaries are $64000, 91000, 91000, 58000, 77000, 64000$. What does each query return, and how would you write the third-highest distinct salary with SQL Server’s `TOP`?

```sql {filename="p14-third.sql"}
CREATE TABLE pay (emp INTEGER, salary INTEGER);
INSERT INTO pay VALUES (1, 64000), (2, 91000), (3, 91000), (4, 58000),
                       (5, 77000), (6, 64000);
-- A
SELECT salary AS a FROM pay ORDER BY salary DESC LIMIT 1 OFFSET 2;
-- B
SELECT DISTINCT salary AS b FROM pay ORDER BY salary DESC LIMIT 1 OFFSET 2;
-- C
SELECT DISTINCT salary AS c FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS r FROM pay) t
WHERE r = 3;
-- D
SELECT MAX(salary) AS d FROM pay
WHERE salary < (SELECT MAX(salary) FROM pay
                WHERE salary < (SELECT MAX(salary) FROM pay));
```

<details class="nb-hint">
<summary>Hint</summary>

Rows or distinct values?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A ranks rows: $91000, 91000, 77000$, so $77000$. B, C and D rank distinct values: $64000$. With `TOP`: `SELECT TOP 1 salary FROM (SELECT DISTINCT TOP 3 salary FROM pay ORDER BY salary DESC) t ORDER BY salary ASC`.

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- A
 a
-------
 77000
(1 row)

-- B
 b
-------
 64000
(1 row)

-- C
 c
-------
 64000
(1 row)

-- D
 d
-------
 64000
(1 row)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-17">

<strong>Problem 14.17</strong> (Top sale per department)

Which rows are printed?

```sql {filename="p14-topsale.sql"}
CREATE TABLE staff (emp_id INTEGER PRIMARY KEY, name VARCHAR(8),
                    dept VARCHAR(8));
CREATE TABLE sales (emp_id INTEGER, amount INTEGER, sold_on DATE);
INSERT INTO staff VALUES (1, 'Ayaan', 'Toys'), (2, 'Bhavna', 'Toys'),
  (3, 'Charu', 'Books'), (4, 'Dev', 'Books'), (5, 'Ela', 'Garden');
INSERT INTO sales VALUES (1, 300, '2026-04-01'), (2, 450, '2026-04-02'),
  (1, 450, '2026-04-05'), (3, 120, '2026-04-03'), (4, 180, '2026-04-04'),
  (3, 180, '2026-04-06');

SELECT dept, name, amount FROM (
  SELECT s.dept, s.name, x.amount,
         RANK() OVER (PARTITION BY s.dept ORDER BY x.amount DESC) AS r
  FROM staff s JOIN sales x ON x.emp_id = s.emp_id) t
WHERE r = 1
ORDER BY dept, name;
```

<details class="nb-hint">
<summary>Hint</summary>

`RANK` keeps ties; Garden has no sales.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Books: Charu and Dev with $180$; Toys: Ayaan and Bhavna with $450$. Garden (Ela) has no sale and the inner join drops it.

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
  dept |  name  | amount
-------+--------+--------
 Books | Charu  |    180
 Books | Dev    |    180
 Toys  | Ayaan  |    450
 Toys  | Bhavna |    450
(4 rows)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-18">

<strong>Problem 14.18</strong> (Customers and products without a sale)

The tables are `customer(id, customer_name, city_id)`, `product(id, product_name)` and `sale(id, customer_id, product_id, qty)`. Write one query listing every customer who bought nothing and every product never sold, labelled by kind. (Data: customers Arnav, Bina, Chetna, Daksh; products Pen, Ink, Nib, Pad; sales (Arnav, Ink), (Chetna, Ink), (Arnav, Pad).)

<details class="nb-hint">
<summary>Hint</summary>

Two anti-joins and a `UNION ALL`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Two anti-joins glued by `UNION ALL`:

```sql {filename="p14-unsold.sql"}
CREATE TABLE customer (id INTEGER PRIMARY KEY, customer_name VARCHAR(10),
                       city_id INTEGER);
CREATE TABLE product (id INTEGER PRIMARY KEY, product_name VARCHAR(10));
CREATE TABLE sale (id INTEGER PRIMARY KEY, customer_id INTEGER,
                   product_id INTEGER, qty INTEGER);
INSERT INTO customer VALUES (1, 'Arnav', 1), (2, 'Bina', 2),
                            (3, 'Chetna', 1), (4, 'Daksh', 3);
INSERT INTO product VALUES (1, 'Pen'), (2, 'Ink'), (3, 'Nib'), (4, 'Pad');
INSERT INTO sale VALUES (1, 1, 2, 5), (2, 3, 2, 1), (3, 1, 4, 2);

SELECT 'customer' AS kind, c.customer_name AS name FROM customer c
WHERE NOT EXISTS (SELECT 1 FROM sale s WHERE s.customer_id = c.id)
UNION ALL
SELECT 'product', p.product_name FROM product p
WHERE NOT EXISTS (SELECT 1 FROM sale s WHERE s.product_id = p.id)
ORDER BY kind, name;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
   kind   |  name
----------+-------
 customer | Bina
 customer | Daksh
 product  | Nib
 product  | Pen
(4 rows)
```

`NOT EXISTS` is safe even if `sale` has `NULL` ids; `NOT IN` would not be, and `LEFT JOIN ... IS NULL` works too.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-19">

<strong>Problem 14.19</strong> 🌶 (Red boats)

On the sailors instance of [Chapter 2](../02-algebra/), which of A–D correctly list the names of sailors who reserved a red boat, each sailor once?

```sql {filename="p14-sailors.sql"}
-- A
SELECT DISTINCT s.sname FROM sailors s, reserves r, boats b
WHERE s.sid = r.sid AND r.bid = b.bid AND b.color = 'red' ORDER BY 1;
-- B
SELECT s.sname FROM sailors s WHERE s.sid IN
  (SELECT r.sid FROM reserves r JOIN boats b ON r.bid = b.bid
   WHERE b.color = 'red') ORDER BY 1;
-- C
SELECT s.sname FROM sailors s WHERE EXISTS
  (SELECT * FROM reserves r, boats b
   WHERE r.bid = b.bid AND b.color = 'red') ORDER BY 1;
-- D
SELECT s.sname FROM sailors s, reserves r
WHERE s.sid = r.sid
  AND r.bid IN (SELECT bid FROM boats WHERE color = 'red')
ORDER BY 1;
```

<details class="nb-hint">
<summary>Hint</summary>

Is C correlated? Does D remove duplicates?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A and B. C’s subquery does not mention `s`, so it is TRUE for every sailor. D is right in content but lists a sailor once per red reservation (Arjun, Divya twice).

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- A
 sname
-------
 Arjun
 Bina
 Divya
(3 rows)

-- B
 sname
-------
 Arjun
 Bina
 Divya
(3 rows)

-- C
 sname
--------
 Arjun
 Bina
 Bina
 Chetan
 Divya
 Esha
 Farhan
(7 rows)

-- D
 sname
-------
 Arjun
 Arjun
 Bina
 Divya
 Divya
(5 rows)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-20">

<strong>Problem 14.20</strong> (Ranks and running sums)

Fill in `rk`, `dr` and `run`.

```sql {filename="p14-window.sql"}
CREATE TABLE score (name VARCHAR(5), pts INTEGER);
INSERT INTO score VALUES ('p', 70), ('q', 90), ('r', 70), ('s', 50),
                         ('t', 90), ('u', 60);
SELECT name, pts,
       RANK() OVER (ORDER BY pts DESC) AS rk,
       DENSE_RANK() OVER (ORDER BY pts DESC) AS dr,
       SUM(pts) OVER (ORDER BY pts DESC) AS run
FROM score ORDER BY pts DESC, name;
```

<details class="nb-hint">
<summary>Hint</summary>

The default frame includes peers with equal `pts`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The real result:

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 name | pts | rk | dr | run
------+-----+----+----+-----
 q    |  90 |  1 |  1 | 180
 t    |  90 |  1 |  1 | 180
 p    |  70 |  3 |  2 | 320
 r    |  70 |  3 |  2 | 320
 u    |  60 |  5 |  3 | 380
 s    |  50 |  6 |  4 | 430
(6 rows)
```

The two $90$s share rank $1$, the next rank is $3$ (`RANK`) or $2$ (`DENSE_RANK`); the running sum jumps by both tied rows at once ($180$, then $320$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-21">

<strong>Problem 14.21</strong> (Set operations)

Give `u`, `ua`, `i`, `e` and `j`.

```sql {filename="p14-setops.sql"}
CREATE TABLE p (v INTEGER);
CREATE TABLE q (v INTEGER);
INSERT INTO p VALUES (1), (2), (2), (3), (NULL), (NULL);
INSERT INTO q VALUES (2), (3), (3), (4), (NULL);

SELECT (SELECT COUNT(*) FROM (SELECT v FROM p UNION SELECT v FROM q) t) AS u,
       (SELECT COUNT(*) FROM (SELECT v FROM p UNION ALL
                              SELECT v FROM q) t)                  AS ua,
       (SELECT COUNT(*) FROM (SELECT v FROM p INTERSECT
                              SELECT v FROM q) t)                  AS i,
       (SELECT COUNT(*) FROM (SELECT v FROM p EXCEPT
                              SELECT v FROM q) t)                  AS e,
       (SELECT COUNT(*) FROM p JOIN q ON p.v = q.v)                AS j;
```

<details class="nb-hint">
<summary>Hint</summary>

Set operations treat `NULL`s as equal; joins never match `NULL`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\{1,2,3,4,\text{NULL}\}$: $5$; $6+5=11$; $\{2,3,\text{NULL}\}$: $3$; $\{1\}$: $1$; the join pairs two $2$s with one and one $3$ with two: $4$.

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 u | ua | i | e | j
---+----+---+---+---
 5 | 11 | 3 | 1 | 4
(1 row)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-22">

<strong>Problem 14.22</strong> (A recursive CTE)

How many rows does the CTE produce, and what is the largest `a`?

```sql {filename="p14-recursive.sql"}
WITH RECURSIVE f(a, b) AS (
  SELECT 0, 1
  UNION ALL
  SELECT b, a + b FROM f WHERE b < 100
)
SELECT COUNT(*) AS n, MAX(a) AS largest_a FROM f;
```

<details class="nb-hint">
<summary>Hint</summary>

The test `b < 100` is on the row being extended, not on the new row.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$12$ rows; $a$ runs through $0,1,1,2,3,5,8,13,21,34,55,89$. The row $(55,89)$ passes the test and produces $(89,144)$, which does not.

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 n  | largest_a
----+-----------
 12 |        89
(1 row)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-23">

<strong>Problem 14.23</strong> (Which queries can seek the index?)

Table `ord` has an index on `(cust, day, status)`. For each query, will SQLite seek the index, on which columns, and is it covering?

```sql {filename="p14-index.sql"}
CREATE TABLE ord (id INTEGER PRIMARY KEY, cust INTEGER, day INTEGER,
                  status TEXT, total INTEGER);
INSERT INTO ord
  WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n
                          WHERE i < 5000)
  SELECT i, i % 997, i % 365, 'st' || (i % 3), i * 7 % 1000 FROM n;
CREATE INDEX ix ON ord (cust, day, status);
-- Q1
EXPLAIN QUERY PLAN SELECT * FROM ord WHERE cust = 5 AND day > 100;
-- Q2
EXPLAIN QUERY PLAN SELECT * FROM ord WHERE day = 7 AND status = 'st1';
-- Q3
EXPLAIN QUERY PLAN SELECT status FROM ord WHERE cust = 5 AND day = 7;
-- Q4
EXPLAIN QUERY PLAN SELECT * FROM ord WHERE cust = 5 AND status = 'st1';
```

<details class="nb-hint">
<summary>Hint</summary>

Left prefix; a range ends the usable prefix; a gap ends it too.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Q1: seek on `cust` and the range on `day`. Q2: no prefix, full scan. Q3: seek on both, and covering (only `status` is needed). Q4: seek on `cust` only; `status` is filtered afterwards because `day` is skipped.

```text {filename="Result on SQLite 3.45.1"}
-- Q1
 query plan
----------------------------------------------
 SEARCH ord USING INDEX ix (cust=? AND day>?)
(1 row)

-- Q2
 query plan
------------
 SCAN ord
(1 row)

-- Q3
 query plan
-------------------------------------------------------
 SEARCH ord USING COVERING INDEX ix (cust=? AND day=?)
(1 row)

-- Q4
 query plan
------------------------------------
 SEARCH ord USING INDEX ix (cust=?)
(1 row)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-24">

<strong>Problem 14.24</strong> (Range partitioning in Oracle)

`orders(order_id PRIMARY KEY, customer_id, order_date, total_amount)` is to be range-partitioned by year of `order_date`. Which statement is valid Oracle? (a) `CREATE TABLE orders (...) PARTITION BY RANGE (order_date) (PARTITION p24 VALUES LESS THAN (DATE '2025-01-01'), PARTITION p25 VALUES LESS THAN (DATE '2026-01-01'))`; (b) the same with `PARTITION p24 VALUES FROM ('2024-01-01') TO ('2025-01-01')`; (c) `CREATE TABLE orders (..., PARTITION BY RANGE (order_date))`; (d) `CREATE TABLE orders (...) PARTITION BY LIST (order_date) (PARTITION p24 VALUES LESS THAN (2025))`.

<details class="nb-hint">
<summary>Hint</summary>

Where does the clause go, and which keyword introduces range bounds in Oracle?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a). (b) is PostgreSQL’s syntax (`FOR VALUES FROM ... TO`, written on separate `PARTITION OF` tables, [Section 4.10](../04-sql-advanced/#sec-dbms-partition)); (c) puts the clause inside the column list; (d) mixes `LIST` partitioning with range bounds.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-25">

<strong>Problem 14.25</strong> (Filegroups)

In SQL Server, which query lists the filegroups of the current database with their type and read-only flag? (a) `SELECT * FROM information_schema.filegroups`; (b) `SELECT name, type_desc, is_read_only FROM sys.filegroups`; (c) `SHOW FILEGROUPS`; (d) `SELECT name FROM sys.databases`.

<details class="nb-hint">
<summary>Hint</summary>

SQL Server’s own catalog views live in the `sys` schema.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b). `information_schema` has no filegroups view, `SHOW` is MySQL syntax, and `sys.databases` lists databases ([Section 4.11](../04-sql-advanced/#sec-dbms-dialects)).

</details>

</div>

## 14.4 Functional dependencies and normalization {#s14-4}

<div class="nb nb-problem nb-block" id="problem-14-26">

<strong>Problem 14.26</strong> (Implied dependencies)

$R(A,B,C,D,E,F)$ with $F=\{AB\to C, C\to D, D\to B, E\to F\}$. Which hold: $A\to D$, $AB\to D$, $AC\to B$, $CE\to BF$, $D\to C$? What is $(AC)^+$?

<details class="nb-hint">
<summary>Hint</summary>

One closure per left side.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$AB\to D$, $AC\to B$ and $CE\to BF$ hold; $A^+=A$ and $D^+=BD$, so the other two do not. $(AC)^+=ABCD$.

```text {filename="Computed by p14-checks.py"}
A->D: False
AB->D: True
AC->B: True
CE->BF: True
D->C: False
closure of AC: ABCD
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-27">

<strong>Problem 14.27</strong> 🌶 (Keys and normal form)

$R(A,B,C,D,E,F)$ with $A\to B$, $BC\to D$, $D\to E$, $E\to C$, $F\to A$. Find all candidate keys, the prime attributes and the highest normal form.

<details class="nb-hint">
<summary>Hint</summary>

$F$ is on no right side. What does $F$ alone give?

</details>

<details class="nb-sol">
<summary>Solution</summary>

$F^+=FAB$; add one of $C$, $D$, $E$: keys $CF$, $DF$, $EF$; prime $CDEF$. $F\to A$ makes the non-prime $A$ depend on part of a key: only 1NF.

```text {filename="Computed by p14-checks.py"}
keys: CF, DF, EF (3)
prime: CDEF
highest normal form: 1NF
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-28">

<strong>Problem 14.28</strong> (Highest normal form)

Give the highest normal form of each: $R_1(ABCD)$: $A\to B$, $B\to C$, $C\to D$; $R_2(ABCD)$: $AB\to C$, $C\to D$, $D\to A$; $R_3(ABC)$: $AB\to C$, $C\to A$; $R_4(ABCD)$: $A\to BCD$, $BC\to A$.

<details class="nb-hint">
<summary>Hint</summary>

Find the keys first; then look for non-key left sides, and check whether the right side is prime.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$R_1$: key $A$, transitive dependencies on non-prime attributes: 2NF. $R_2$: keys $AB$, $BC$, $BD$; everything is prime: 3NF, not BCNF. $R_3$: keys $AB$, $BC$; $C\to A$ has a prime right side: 3NF. $R_4$: keys $A$ and $BC$, both left sides are keys: BCNF.

```text {filename="Computed by p14-checks.py"}
R1(ABCD): A->B, B->C, C->D   keys A          -> 2NF
R2(ABCD): AB->C, C->D, D->A  keys AB, BC, BD -> 3NF
R3(ABC): AB->C, C->A        keys AB, BC     -> 3NF
R4(ABCD): A->BCD, BC->A      keys A, BC      -> BCNF
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-29">

<strong>Problem 14.29</strong> (3NF and BCNF: true or false)

(a) Every BCNF relation is in 3NF. (b) Every 3NF relation is in BCNF. (c) A relation with only two attributes is in BCNF. (d) If every attribute is prime, the relation is in BCNF. (e) A lossless, dependency-preserving 3NF decomposition always exists. (f) A lossless, dependency-preserving BCNF decomposition always exists. (g) A 3NF relation that is not in BCNF has overlapping candidate keys.

<details class="nb-hint">
<summary>Hint</summary>

$R(S,C,T)$ with $SC\to T$, $T\to C$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

True: (a), (c), (e), (g). False: (b) and (d) (the $SCT$ relation is all-prime and in 3NF, not BCNF), and (f) (its only BCNF decomposition loses $SC\to T$). See [Section 6.5](../06-normalization/#sec-dbms-nf).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-30">

<strong>Problem 14.30</strong> (Minimal cover)

Find a minimal cover of $\{A\to BC,\ B\to C,\ AB\to D,\ D\to BE,\ A\to E\}$.

<details class="nb-hint">
<summary>Hint</summary>

Split right sides, drop extraneous left attributes ($B$ in $AB\to D$?), then redundant FDs.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\{B\to C,\ A\to D,\ D\to B,\ D\to E\}$: $AB\to D$ loses $B$ ($A\to B$), then $A\to B$ ($A\to D\to B$), $A\to C$ and $A\to E$ follow from the rest. Other minimal covers exist ([Section 6.4](../06-normalization/#sec-dbms-cover)).

```text {filename="Computed by p14-checks.py"}
minimal cover: B->C, A->D, D->B, D->E
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-31">

<strong>Problem 14.31</strong> 🌶🌶 (Lossless or not?)

$R(ABCDE)$ with $A\to B$, $B\to C$, $CD\to E$. Which decompositions are lossless? (a) $AB, BC, ACDE$; (b) $AB, CD, BDE$; (c) $ABC, CDE$; (d) $AB, ACD, CDE$.

<details class="nb-hint">
<summary>Hint</summary>

Run the chase; for (c), use the binary test.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) and (d). In (c) the common attribute $C$ determines nothing. In (b) no row of the tableau can be completed. In (d), $A\to B\to C$ fills row 2 ($ACD$) with $B$, and $CD\to E$ then completes it.

```text {filename="Computed by p14-checks.py"}
{AB, BC, ACDE}: lossless True
{AB, CD, BDE}: lossless False
{ABC, CDE}: lossless False
{AB, ACD, CDE}: lossless True
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-32">

<strong>Problem 14.32</strong> 🌶🌶 (Decompose it)

$R(ABCD)$ with $AB\to C$, $C\to B$, $B\to D$. Give the keys and normal form, a BCNF decomposition (is it dependency preserving?), and a 3NF synthesis.

<details class="nb-hint">
<summary>Hint</summary>

$B\to D$ is a partial dependency; $C\to B$ makes the keys overlap.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Keys $AB$, $AC$; 1NF. Splitting on $B\to D$ then $C\to B$ gives $BD$, $BC$, $AC$: lossless, but $AB\to C$ can no longer be checked in one table. 3NF synthesis keeps $ABC$ and $BD$, preserving everything.

```text {filename="Computed by p14-checks.py"}
R(ABCD) AB->C, C->B, B->D: keys AB, AC, 1NF
BCNF decomposition: BD, BC, AC; lossless True; lost: AB->C
3NF synthesis: ABC, BD
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-33">

<strong>Problem 14.33</strong> (Interview: normalization)

“What is normalization, and why do we need it?” Answer in four sentences with an example.

<details class="nb-hint">
<summary>Hint</summary>

Redundancy, anomalies, keys; and the price.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Normalization organizes tables so that every fact is stored once, by decomposing them along functional dependencies. A table `enroll(roll, course, name, grade)` stores a student’s name once per course: renaming her needs many updates (update anomaly), a student with no course cannot be stored (insertion anomaly), and deleting the last enrolment loses the student (deletion anomaly). Splitting off `student(roll, name)` removes all three and lets keys enforce the rules. The price is more joins on reads, so analytical systems sometimes denormalize deliberately ([Section 6.1](../06-normalization/#sec-dbms-why-norm)).

</details>

</div>

## 14.5 Transactions and concurrency {#s14-5}

<div class="nb nb-problem nb-block" id="problem-14-34">

<strong>Problem 14.34</strong> (What a transaction is not)

Which statements define a transaction <em>incorrectly</em>? (a) A logical unit of work that is executed completely or not at all. (b) A sequence of operations whose partial results are made permanent as each statement completes. (c) A unit of work that moves the database from one consistent state to another. (d) Any single `SELECT` statement, which cannot be part of a larger transaction. (e) A unit whose effects, once committed, survive crashes.

<details class="nb-hint">
<summary>Hint</summary>

Atomicity, consistency, durability; and `BEGIN ... COMMIT`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b) contradicts atomicity; (d) is wrong because reads take part in transactions (and matter for isolation). (a), (c), (e) are ACID.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-35">

<strong>Problem 14.35</strong> (ACID)

Which is not one of the ACID properties: atomicity, consistency, concurrency, isolation, durability? For each real one, name the DBMS component that provides it.

<details class="nb-hint">
<summary>Hint</summary>

[Section 7.1](../07-transactions/#sec-dbms-acid).

</details>

<details class="nb-sol">
<summary>Solution</summary>

Concurrency. Atomicity: recovery manager (undo); consistency: constraints plus correct transactions; isolation: concurrency control; durability: the write-ahead log.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-36">

<strong>Problem 14.36</strong> (Equivalent serial orders)

Is the following schedule conflict serializable?

$$
r_1(A)\,r_2(B)\,w_3(A)\,w_2(C)\,r_4(C)\,r_3(B)\,w_4(D)
$$

How many serial schedules is it conflict equivalent to?

<details class="nb-hint">
<summary>Hint</summary>

Draw the precedence graph; count topological orders.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Edges $T_1\to T_3$ ($A$) and $T_2\to T_4$ ($C$) only; $r_2(B)$, $r_3(B)$ do not conflict. Two independent chains of two: $\binom42=6$ orders.

```text {filename="Computed by p14-checks.py"}
edges: T1->T3, T2->T4
6 equivalent serial orders:
   T1T2T3T4, T1T2T4T3, T1T3T2T4, T2T1T3T4, T2T1T4T3, T2T4T1T3
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-37">

<strong>Problem 14.37</strong> 🌶 (View but not conflict)

Classify $S=w_1(A)\,r_2(A)\,w_2(B)\,w_1(B)\,w_3(B)$ and $T=r_1(A)\,w_2(A)\,w_1(A)\,w_3(A)\,w_2(B)\,w_3(B)$ (all commit).

<details class="nb-hint">
<summary>Hint</summary>

Blind writes overwritten by $T_3$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Both have a $T_1$–$T_2$ cycle, so neither is conflict serializable. Both are view serializable: in $S$, $T_2$ reads $A$ from $T_1$ and $T_3$ writes $B$ last, exactly as in $T_1T_2T_3$; in $T$, $T_1$ reads the initial $A$ and $T_3$ writes both items last, again as in $T_1T_2T_3$.

```text {filename="Computed by p14-checks.py"}
S: CS False, VS True
T: CS False, VS ['T1T2T3']
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-38">

<strong>Problem 14.38</strong> 🌶🌶 (Counting interleavings)

$T_1=r_1(A)\,w_1(A)\,r_1(B)$ and $T_2=r_2(B)\,w_2(B)\,r_2(A)$. How many interleavings are there, and how many are conflict equivalent to $T_1T_2$, to $T_2T_1$?

<details class="nb-hint">
<summary>Hint</summary>

For $T_1T_2$: $w_1(A)$ before $r_2(A)$ and $r_1(B)$ before $w_2(B)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\binom63=20$ interleavings. $T_1T_2$ needs $r_1(B)<w_2(B)$, which forces all of $T_1$ before $w_2(B)$; only $r_2(B)$ may move earlier: $4$ positions. Symmetrically $4$ for $T_2T_1$; the other $12$ have a cycle.

```text {filename="Computed by p14-checks.py"}
20 interleavings
conflict-equivalent to T1T2: 4; to T2T1: 4; not serializable: 12
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-39">

<strong>Problem 14.39</strong> (Recoverability)

Classify each schedule as not recoverable, recoverable, cascadeless or strict: (a) $w_1(X)\,r_2(X)\,w_2(Y)\,c_1\,c_2$; (b) $w_1(X)\,r_2(X)\,c_2\,c_1$; (c) $w_1(X)\,w_2(X)\,c_2\,c_1$; (d) $r_1(X)\,w_2(X)\,c_2\,w_1(X)\,c_1$; (e) $w_1(X)\,r_2(Y)\,c_1\,r_2(X)\,c_2$.

<details class="nb-hint">
<summary>Hint</summary>

Who reads from whom, and who commits first?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) recoverable (dirty read, but $T_1$ commits first); (b) not recoverable; (c) cascadeless (no dirty read, but a dirty overwrite); (d) and (e) strict. Note that (d) is not serializable: strictness says nothing about serializability.

```text {filename="Computed by p14-checks.py"}
w1(X) r2(X) w2(Y) c1 c2    recoverable
w1(X) r2(X) c2 c1          not recoverable
w1(X) w2(X) c2 c1          cascadeless
r1(X) w2(X) c2 w1(X) c1    strict
w1(X) r2(Y) c1 r2(X) c2    strict
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-40">

<strong>Problem 14.40</strong> 🌶 (Timestamp ordering)

$TS(T_i)=i$. Run the schedule

$$
r_2(X)\,w_3(X)\,w_2(X)\,r_1(Y)\,w_2(Y)\,w_1(Z)\,r_3(Z)
$$

under basic timestamp ordering and under Thomas’ write rule.

<details class="nb-hint">
<summary>Hint</summary>

$w_2(X)$ arrives after a younger write and no younger read of $X$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Basic TO aborts $T_2$ at $w_2(X)$ ($WTS(X)=3>2$), so $w_2(Y)$ never runs. Thomas ignores the obsolete $w_2(X)$ and $T_2$ continues; $w_2(Y)$ is fine ($RTS(Y)=1<2$).

```text {filename="Computed by p14-checks.py"}
r2(X): ok                    | r2(X): ok
w3(X): ok                    | w3(X): ok
w2(X): abort T2              | w2(X): ignored (Thomas)
r1(Y): ok                    | r1(Y): ok
w2(Y): skipped (T2 aborted)  | w2(Y): ok
w1(Z): ok                    | w1(Z): ok
r3(Z): ok                    | r3(Z): ok
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-41">

<strong>Problem 14.41</strong> (Deadlock prevention)

Timestamps equal subscripts. What happens under wait-die and under wound-wait when (a) $T_3$ requests a lock held by $T_7$; (b) $T_7$ requests a lock held by $T_3$?

<details class="nb-hint">
<summary>Hint</summary>

Wait-die: old waits, young dies. Wound-wait: old wounds, young waits.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Older (smaller) timestamps have priority:

```text {filename="Computed by p14-checks.py"}
T3 wants a lock held by T7: wait-die -> wait; wound-wait -> T7 wounded
T7 wants a lock held by T3: wait-die -> T7 dies; wound-wait -> wait
```

A transaction that dies or is wounded restarts with its original timestamp.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-42">

<strong>Problem 14.42</strong> 🌶 (Name the anomaly)

For each scenario name the anomaly and the weakest standard isolation level that prevents it: (a) $T_1$ reads a balance written by an uncommitted $T_2$ that later aborts; (b) $T_1$ counts orders of a day twice and gets $8$, then $9$; (c) two clerks read stock $5$, each sells one and writes $4$; (d) two doctors each check that the other is on call and both go off call. Which of these can PostgreSQL’s `REPEATABLE READ` exhibit?

<details class="nb-hint">
<summary>Hint</summary>

[Section 8.6](../08-concurrency/#sec-dbms-isolation); PostgreSQL’s `REPEATABLE READ` is snapshot isolation.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) dirty read: `READ COMMITTED`. (b) phantom: `SERIALIZABLE` in the standard. (c) lost update: prevented by `REPEATABLE READ` in PostgreSQL (the second writer is aborted) and by `SERIALIZABLE` in general. (d) write skew: only `SERIALIZABLE`. PostgreSQL’s `REPEATABLE READ` exhibits only (d), as demo 6 of [Section 8.6](../08-concurrency/#sec-dbms-isolation) shows.

</details>

</div>

## 14.6 Storage and indexing {#s14-6}

<div class="nb nb-problem nb-block" id="problem-14-43">

<strong>Problem 14.43</strong> 🌶 (B$^+$-tree order and capacity)

Blocks are $4096$ bytes, keys $12$, block pointers $8$, record pointers $10$. Find the internal order $p$, the leaf capacity, and the maximum and minimum number of keys in a B$^+$-tree with three levels.

<details class="nb-hint">
<summary>Hint</summary>

$8p+12(p-1)\le4096$ and $22n+8\le4096$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$p=205$, leaves hold $185$. Maximum $205\cdot205\cdot185$; minimum: root with $2$ children, $\lceil205/2\rceil=103$ per internal node, $\lceil185/2\rceil=93$ per leaf.

```text {filename="Computed by p14-checks.py"}
internal order p = 205, leaf capacity = 185
3 levels (root + 2): max 7,774,625 keys, min 19,158 keys
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-44">

<strong>Problem 14.44</strong> 🌶🌶 (B$^+$-tree insertions)

Insert $8,5,1,7,3,12,9,6$ into an empty B$^+$-tree of order $3$ (at most $2$ keys per node; a full leaf splits $2+1$ with the right leaf’s first key copied up; an internal node with $3$ keys splits $1+1$ with the middle key moved up). Draw the final tree.

<details class="nb-hint">
<summary>Hint</summary>

The root splits twice.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The tree built by `lib/bptree.py` with exactly these rules:

```text {filename="Computed by p14-checks.py"}
order 3, insert 8 5 1 7 3 12 9 6:
    [7]
    [5]  [8 12]
    [1 3]  [5 6]  [7]  [8 9]  [12]
```

Height $3$; the leaf $[7]$ holds the minimum of one key for order $3$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-45">

<strong>Problem 14.45</strong> (Index access cost)

$100000$ records of $200$ bytes, $4096$-byte blocks, unspanned; index entries of $16+8$ bytes. How many block reads for an equality search on the key with (a) a heap file (average), (b) binary search on a sorted file, (c) a primary sparse index searched by binary search, (d) a dense secondary index searched by binary search?

<details class="nb-hint">
<summary>Hint</summary>

$\mathit{bfr}=20$, $5000$ blocks, index fan-out $170$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $2500$; (b) $13$; (c) $30$ index blocks: $5+1=6$; (d) $589$ index blocks: $10+1=11$.

```text {filename="Computed by p14-checks.py"}
bfr 20, blocks 5000; linear avg 2500, binary 13
index fan-out 170; primary index blocks 30, cost 6
dense secondary index blocks 589, cost 11
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-46">

<strong>Problem 14.46</strong> 🌶🌶 (Extendible hashing)

Buckets hold $2$ keys, the directory starts at global depth $1$ and uses the low bits of the key. Insert $3, 11, 19, 6, 27$. What is the final global depth?

<details class="nb-hint">
<summary>Hint</summary>

Write the keys in binary: $3=00011$, $11=01011$, $19=10011$, $27=11011$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$4$. The four odd keys agree on their last three bits, so separating $3,19$ from $11,27$ needs bit $3$: three doublings, each followed by a split, leaving empty buckets behind. Skewed keys are the weakness of extendible hashing.

```text {filename="Computed by p14-checks.py"}
global depth 4, directory size 16, 5 buckets:
   local depth 1: [6]
   local depth 2: []
   local depth 4: [3, 19]
   local depth 3: []
   local depth 4: [11, 27]
```

</details>

</div>

## 14.7 Query processing {#s14-7}

<div class="nb nb-problem nb-block" id="problem-14-47">

<strong>Problem 14.47</strong> (Join costs)

$b_r=400$, $b_s=1000$, $M=22$ buffer blocks. Cost of block nested-loop join with $r$ outer and with $s$ outer, and of a hash join without recursive partitioning?

<details class="nb-hint">
<summary>Hint</summary>

$\lceil b_{\text{outer}}/(M-2)\rceil \,b_{\text{inner}}+b_{\text{outer}}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$20\cdot1000+400=20400$; $50\cdot400+1000=21000$; $3(400+1000)=4200$.

```text {filename="Computed by p14-checks.py"}
r outer: 20400 transfers; s outer: 21000 transfers
hash join: 4200 transfers
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-48">

<strong>Problem 14.48</strong> (External sort)

Sort $10000$ blocks with (a) $M=101$, (b) $M=11$ buffer blocks. Runs, merge passes, block transfers (final output not written)?

<details class="nb-hint">
<summary>Hint</summary>

$\lceil b/M\rceil$ runs, then $(M-1)$-way merges.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $100$ runs fit in one $100$-way merge; (b) $910$ runs need $\lceil \log_{10}910\rceil=3$ merge passes:

```text {filename="Computed by p14-checks.py"}
b = 10000, M = 101: 100 runs, 1 merge passes, 30000 transfers
b = 10000, M = 11: 910 runs, 3 merge passes, 70000 transfers
```

</details>

</div>

## 14.8 Beyond relational {#s14-8}

<div class="nb nb-problem nb-block" id="problem-14-49">

<strong>Problem 14.49</strong> (Pick the store)

Which is a key-value store: (a) Neo4j, (b) Redis, (c) Cassandra, (d) PostgreSQL? And which is the poorest reason to choose a non-relational database: (i) a simple key-based access pattern at very high write volume, (ii) data with varying, schemaless shape, (iii) many multi-table transactions with strict integrity constraints, (iv) horizontal scaling across data centres?

<details class="nb-hint">
<summary>Hint</summary>

[Section 12.2](../12-beyond/#sec-dbms-nosql).

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b) Redis (Neo4j is a graph database, Cassandra wide-column, PostgreSQL relational). (iii): multi-table ACID transactions and integrity constraints are what relational databases are for.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-50">

<strong>Problem 14.50</strong> (Quorums and rings)

(a) With $N=5$ replicas, which $(R,W)$ pairs guarantee that reads see the latest write: $(1,5)$, $(2,3)$, $(3,3)$, $(2,4)$? (b) A cluster grows from $9$ to $10$ servers. About what fraction of keys move with $h(k)\bmod N$ placement and with consistent hashing?

<details class="nb-hint">
<summary>Hint</summary>

$R+W>N$. Ideal movement is the new server’s share.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $(1,5)$, $(3,3)$, $(2,4)$; $(2,3)$ has $R+W=5=N$. (b) Measured on $30000$ keys:

```text {filename="Computed by p14-checks.py"}
9 -> 10 servers: mod N moves 89.6%, consistent hashing moves 10.1%
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-51">

<strong>Problem 14.51</strong> 🌶 (Coordinator failure)

In two-phase commit, the coordinator crashes after all participants voted YES but before any decision was logged. What may a participant do on its own? What if one participant had voted NO?

<details class="nb-hint">
<summary>Hint</summary>

A YES vote is a promise.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Nothing: having voted YES it can neither commit (others may have voted NO) nor abort (the coordinator may have decided commit), so it blocks, holding its locks, until the coordinator recovers or another participant knows the outcome. A participant that voted NO may abort unilaterally, and the coordinator can only decide abort ([Section 12.5](../12-beyond/#sec-dbms-2pc)).

</details>

</div>
