---
title: "SQL queries and joins"
weight: 1
---

16 questions asked by EXL, ION Group, Info Edge, MAQ Software, MathWorks, Oracle, Paytm, Protium Finance. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · listing filegroups in SQL Server

*Asked by: EXL (HackerEarth test, 2025)*

To search for created and available filegroups in the current database, with their type
and read-only status, which query can you use?

1. `SELECT name, type, is_read_only FROM sys.filegroups WHERE type = 'FG'`
2. `SELECT name, type, is_read_only FROM sys.data_spaces WHERE type = 'FG'`
3. `SELECT name, type, is_read_only FROM sys.groups WHERE type = 'FG'`
4. `SELECT name, type, is_read_only FROM sys.sysfile WHERE type = 'FG'`

- **(a)** 1
- **(b)** 2
- **(c)** 3
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) query 1** (`sys.filegroups`)

**Why.** The catalog view `sys.filegroups` has one row per filegroup with `name`, `type` ('FG' for a row filegroup) and `is_read_only`. `sys.data_spaces` has no `is_read_only` column; `sys.groups` and `sys.sysfile` are not the right views.

**Concept: SQL Server catalog views.** The `sys.*` views describe the database's own metadata (tables, columns, files, filegroups). A filegroup is a named set of data files that tables and indexes can be placed on.

{{< /details >}}

### 2 · maximum difference between boys and girls

*Asked by: EXL (HackerEarth test, 2025)*

Ron works with a table `CLASS(CLASS_SECTION VARCHAR, NO_OF_BOYS NUMBER,
NO_OF_GIRLS NUMBER, TOTAL_STUDENTS NUMBER)`, one row per class section. He needs the
maximum difference between the number of boys and the number of girls in any section.
Which query is correct? Options 1 and 2 read
`SELECT MAX(NO_OF_BOYS) - MIN(NO_OF_GIRLS) AS DIFF FROM CLASS` and
`SELECT MAX(NO_OF_BOYS - NO_OF_GIRLS) AS DIFF FROM CLASS`; options 3 and 4 are
below the photo [cut off in the source].

{{< details title="Answer and explanation" closed="true" >}}

**Answer: option 2, `SELECT MAX(NO_OF_BOYS - NO_OF_GIRLS) AS DIFF FROM CLASS`** (or `MAX(ABS(...))` if girls may outnumber boys)

**Why.** The difference must be computed per row (per section) and then maximised. Option 1 subtracts the minimum girls of one section from the maximum boys of possibly another section, which is not a difference within any section.

**Concept: row expression inside an aggregate.** `MAX(a − b)` computes a − b for each row and then takes the maximum. `MAX(a) − MIN(b)` aggregates each column separately, mixing rows.

{{< /details >}}

### 3 · RIGHT JOIN output

*Asked by: EXL (HackerEarth test, 2025)*

`Student(Course, Name, Credits)` has rows (Bio-101, Jack, 2), (Phy-104, Bob, 4),
(Che-102, Mike, 3); `Teacher(Course, Id)` has (Bio-101, 1000), (Phy-104, 1004),
(Mas-103, 1003). What does this MySQL query return?
`SELECT * FROM Student RIGHT JOIN Teacher ON Student.Course = Teacher.Course;`

1. Columns Course, Name, Credits, Course, Id: (Bio-101, Jack, 2, Bio-101, 1000),
    (Phy-104, Bob, 4, Phy-104, 1004), (NULL, NULL, NULL, Mas-103, 1003).
2. Course, Name, Credits, Id with a (NULL, NULL, NULL, 1003) row.
3. As 1, but the last row is (NULL, NULL, NULL, Che-102, 1002).
4. As 2, but the last row is all NULL.

- **(a)** 1
- **(b)** 2
- **(c)** 3
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) option 1**

**Why.** A right join keeps every Teacher row. Bio-101 and Phy-104 match students; Mas-103 has no student, so its Student columns are NULL. `SELECT *` returns both `Course` columns. Che-102 (a student with no teacher) is dropped.

**Concept: joins.** Inner join: only matching pairs. Left join: all rows of the left table, NULLs where the right has no match. Right join: the mirror. Full outer join: all rows of both.

{{< /details >}}

### 4 · third-highest salary with TOP

*Asked by: EXL (HackerEarth test, 2025)*

`EmployeePosition(EmpID, EmpName, DateOfJoining, Salary)` has the salaries 500000,
75000, 90000, 85000 and 300000. Which query finds the third-highest salary?

1. `SELECT TOP 3 salary FROM (SELECT TOP 1 salary FROM EmployeePosition ORDER BY salary DESC) AS emp ORDER BY salary ASC;`
2. `SELECT TOP 1 salary FROM (SELECT TOP 3 salary FROM EmployeePosition ORDER BY salary DESC) AS emp ORDER BY salary ASC;`
3. `SELECT TOP 1 salary FROM (SELECT TOP 3 salary FROM EmployeePosition ORDER BY salary ASC) AS emp ORDER BY salary DESC;`
4. `SELECT TOP 3 salary FROM (SELECT TOP 1 salary FROM EmployeePosition ORDER BY salary ASC) AS emp ORDER BY salary DESC;`

- **(a)** 1
- **(b)** 2
- **(c)** 3
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) query 2**

**Why.** The inner query keeps the three largest salaries (500000, 300000, 90000). Ordering them ascending and taking the top one gives the smallest of those: 90000, the third-highest. Query 3 returns the third-lowest (85000); queries 1 and 4 keep only one row inside.

**Concept: N-th highest value.** Take the top N in descending order, then the smallest of them. Other ways: `ORDER BY salary DESC LIMIT 1 OFFSET 2` (MySQL), or `DENSE_RANK()` to handle ties.

{{< /details >}}

### 5 · Q17, valid GROUP BY / HAVING syntax

*Asked by: ION Group (SDE OA, Jul 2025)*

Select every expression with correct syntax. (Pick one or more.)

- **(a)** `SELECT customer_id, MAX(is_active) FROM transactions GROUP BY customer_id HAVING MAX(is_active)`
- **(b)** `SELECT customer_id, is_active FROM transactions GROUP BY customer_id HAVING MAX(is_active)`
- **(c)** `SELECT customer_id, DISTINCT is_active FROM transactions GROUP BY customer_id HAVING MAX(is_active)`
- **(d)** `SELECT customer_id, MAX(is_active) AS is_active FROM transactions GROUP BY customer_id HAVING is_active`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) and (d)** (in MySQL, which HackerRank uses)

**Why.**
- (a) Fine: HAVING can test an aggregate; MySQL treats non-zero as true.
- (b) Selects `is_active` without aggregating or grouping by it; rejected under ONLY_FULL_GROUP_BY (MySQL's default) and standard SQL.
- (c) Syntax error: DISTINCT can only come right after SELECT.
- (d) Valid in MySQL, which lets HAVING refer to a select-list alias.

**Concept: GROUP BY rule.** Every selected column must either be in GROUP BY or inside an aggregate function, because each group produces one row and the database must know which single value to show.

{{< /details >}}

### 6 · Q39, distinct values

*Asked by: Info Edge (Data Science II)*

Which SQL command displays all the unique values of column `data1` in table
`MY_TABLE`?

- **(a)** select data1 from MY_TABLE;
- **(b)** select unique data1 from MY_TABLE;
- **(c)** select distinct data1 from MY_TABLE;
- **(d)** select data1 from MY_TABLE where data1 is distinct;

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) `select distinct data1 from MY_TABLE;`**

**Why.** DISTINCT removes duplicate rows from the result. (Oracle also accepts UNIQUE as a synonym, but DISTINCT is standard.)

**Concept: DISTINCT applies to the whole selected row.** `SELECT DISTINCT a, b` removes rows where both a and b repeat together.

{{< /details >}}

### 7 · Q36 (other set), EXISTS with ORDER BY

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

CUSTOMER(CUSTID, NAME): 4000 Mike, 5000 Tara, 6000 Alice, 7000 Bob, 8000 Mary, 9000 John.
ORDER has orders by customers 7000, 5000, 8000 and 4000. What does
`SELECT NAME FROM CUSTOMER WHERE EXISTS (SELECT * FROM ORDER WHERE CUSTOMER.CUSTID = ORDER.CUSTID) ORDER BY NAME;`
return?

- **(a)** Bob Mary Mike Tara
- **(b)** Error
- **(c)** Bob Tara Mary Mike
- **(d)** Mike Tara Bob Mary

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Bob Mary Mike Tara**

**Why.** EXISTS is true for customers with at least one order: 7000 Bob, 5000 Tara, 8000 Mary, 4000 Mike. Sorted by name: Bob, Mary, Mike, Tara. (Strictly, ORDER is a reserved word and the table would need quoting; the test intends the logical result.)

**Concept: correlated EXISTS.** The subquery runs for each outer row (it refers to CUSTOMER.CUSTID). EXISTS only checks whether any row comes back, not what it contains, so `SELECT *` or `SELECT 1` inside makes no difference.

{{< /details >}}

### 8 · Q33, sailors who reserved a red boat

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

Sailors(sid, sname, rating, age), Boats(bid, bname, color), Reserves(sid, bid, day).
Which query finds the names of sailors who have reserved a red boat?
(2) `... WHERE S.sid = R.sid AND R.bid = B.bid AND B.color = 'red'`;
(3) `... WHERE S.sid = R.sid AND B.color = 'red'`;
(4) `... WHERE R.bid = B.bid AND B.color = 'red'`; all
`SELECT S.sname FROM Sailors S, Reserves R, Boats B`.

- **(a)** None of these
- **(b)** (2)
- **(c)** (3)
- **(d)** (4)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) query (2)**

**Why.** Both join conditions are needed: S.sid = R.sid links sailors to their reservations, and R.bid = B.bid links reservations to boats. Without R.bid = B.bid, any sailor with any reservation qualifies when some red boat exists; without S.sid = R.sid, every sailor qualifies.

**Concept: joins in the WHERE clause.** Listing tables with commas makes a Cartesian product; the WHERE conditions keep only the matching combinations. With k tables you usually need k − 1 join conditions.

{{< /details >}}

### 9 · Q34, counting distinct addresses

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

STUDENT has addresses Chicago, New York, Boston, Seattle, Chicago, New York. What does
`SELECT COUNT(*) FROM (SELECT DISTINCT ADDRESS FROM STUDENT);` return?

- **(a)** 4
- **(b)** 2
- **(c)** 6
- **(d)** Error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 4**

**Why.** The distinct addresses are Chicago, New York, Boston, Seattle: 4. (Caveat for interviews: MySQL and SQL Server require an alias on a derived table, `(...) AS t`, and would reject this as written; SQLite, PostgreSQL 16+ and Oracle accept it.)

**Concept: counting distinct values.** `SELECT COUNT(DISTINCT address) FROM student;` does the same in one step.

{{< /details >}}

### 10 · Q35, not a WHERE-clause operator

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

In SQL, which of the following is not an operator for the WHERE clause?

- **(a)** IS NULL
- **(b)** IN BETWEEN
- **(c)** >=
- **(d)** !=

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) IN BETWEEN**

**Why.** IN and BETWEEN are two separate operators: `x IN (1, 2, 3)` and `x BETWEEN 1 AND 3`. There is no combined "IN BETWEEN".

**Concept: WHERE operators.** Comparison (=, !=, <>, <, >=), BETWEEN ... AND, IN (...), LIKE with % and _, IS NULL / IS NOT NULL, combined with AND, OR, NOT.

{{< /details >}}

### 11 · Q36, rows of a cross join

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

Students has 100 rows and Course has 5. How many rows does
`SELECT * FROM Students, Course;` return?

- **(a)** 500
- **(b)** 100
- **(c)** 0
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 500**

**Why.** Listing two tables without a join condition gives the Cartesian product: every student paired with every course, 100 × 5 = 500 rows.

**Concept: cross join.** Rows multiply. A forgotten join condition is a common bug that produces huge results.

{{< /details >}}

### 12 · Q9, = ALL on an empty set

*Asked by: MathWorks (IIT Bombay 2024)*

Table $R(A, B, C)$ (top rows [cut off in the source]; visible rows (8,5,6), (4,5,6), (3,4,5), (7,2,9)).
How many rows does

```sql
SELECT *
FROM R
WHERE C = ALL (SELECT B FROM R WHERE A > 10)
```

return?

- **(a)** 0
- **(b)** 1
- **(c)** 4
- **(d)** 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 4** (all the rows, assuming no row has A > 10)

**Why.** If the subquery returns no rows, `C = ALL (empty set)` is true for every row, so every row is returned. With the four visible rows, that is 4. (The candidate's 0 is the usual trap.)

**Concept: ALL and ANY on empty sets.** `x = ALL (S)` means "x equals every element of S", which is vacuously true when S is empty. `x = ANY (S)` means "x equals some element", which is false when S is empty.

{{< /details >}}

### 13 · filtering groups

*Asked by: Oracle (HackerRank MCQ test)*

Which clause restricts the groups of rows returned to those groups for which the specified
condition is true?

- **(a)** WHERE clause
- **(b)** HAVING clause
- **(c)** DISTINCT
- **(d)** EXISTS

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) HAVING**

**Why.** HAVING filters groups after GROUP BY (e.g. `HAVING COUNT(*) > 5`). WHERE filters individual rows before grouping and cannot use aggregates.

**Concept: logical order of a query.** FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.

{{< /details >}}

### 14 · range-partitioned table

*Asked by: Oracle (HackerRank MCQ test)*

A table `orders` has columns `order_id` (primary key), `customer_id`,
`order_date` and `total_amount`. Which SQL statement correctly creates a table
partitioned by range on `order_date`? (Each option is abbreviated to its partition
clause.)

- **(a)** partition by range columns (order_date) (partition p1 values less than ('2023-01-01') tablespace ts1, partition p2 values less than ('2024-01-01') tablespace ts2);
- **(b)** partition by range (order_date) (partition p1 ..., partition p2 ...) primary key (order_id);
- **(c)** partition by range (order_date) (partition p1 values less than ('2023-01-01') tablespace ts1, partition p2 values less than ('2024-01-01') tablespace ts2);
- **(d)** partition by range (order_date) (partition p1 ..., partition p2 ...) partition by range (order_id);

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c)**

**Why.** Oracle's syntax is `PARTITION BY RANGE (col) (PARTITION p VALUES LESS THAN (...) TABLESPACE t, ...)`. `RANGE COLUMNS` is MySQL syntax; a primary-key clause cannot follow the partition list; a table has one partitioning clause (two levels use SUBPARTITION BY).

**Concept: table partitioning.** A big table is split into pieces by a key (range of dates, list of regions, hash). Queries that filter on the key read only the relevant partitions ("partition pruning"), and old partitions can be dropped quickly.

{{< /details >}}

### 15 · List Customer and Product Without Sale

*Asked by: Paytm (HackerRank, Sep 2025)*

Tables: `customer(id, customer_name, city_id, customer_address, contact_person,
email, phone)`; `product(id, sku, product_name, product_description,
current_price, quantity_in_stock)`; `invoice(id, invoice_number, customer_id,
user_account_id, total_price, time_issued, time_due, time_paid, time_canceled,
time_refunded)`, where `customer_id` references `customer.id`; and
`invoice_item(id, invoice_id, product_id, quantity, price, line_total_price)`,
referencing `invoice` and `product`.

Using the `UNION` operator, return in one list all customers who do not have an
invoice and all products that were not sold. For each such customer return the string
`customer`, the customer id and the `customer_name`; for each such product the
string `product`, the product id and the `product_name`. The columns must be in
this order, but row order does not matter. The expected result starts with the line
`customer 2 Cosmetics Store`.

{{< details title="Answer and explanation" closed="true" >}}

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

{{< /details >}}

### 16 · top sale in the Electronics department

*Asked by: Protium Finance (OA 2025)*

Tables `employees(emp_id, name, department)` and `sales(emp_id, amount,
date)`. The question text is outside the photo; the candidate's answer, shown below,
reports the Electronics employee or employees with the largest sale amount:

```sql
SELECT emp_id, name, amount
FROM (
  SELECT s.emp_id, e.name, s.amount,
         RANK() OVER (ORDER BY s.amount DESC) AS rnk
  FROM sales s
  JOIN employees e ON e.emp_id = s.emp_id
  WHERE e.department = 'Electronics') t
WHERE rnk = 1;
```

What does this query return, and how would it change if the question asked for the
employee with the largest *total* sales?

{{< details title="Answer and explanation" closed="true" >}}

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

{{< /details >}}
