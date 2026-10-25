---
title: "5 · SQL queries interviewers ask"
linkTitle: "5 SQL interview queries"
weight: 5
math: true
---
The handful of query shapes that cover most SQL interview questions. Table: `Employee(id, name, salary, dept_id, manager_id)`.

## 5.1 N-th highest salary {#db-5-1}

```sql
-- 2nd highest distinct salary
SELECT MAX(salary) FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```

General N-th highest (distinct), with a window function:

```sql
SELECT DISTINCT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS r FROM Employee
) t WHERE r = 3;
```

Or `SELECT DISTINCT salary FROM Employee ORDER BY salary DESC LIMIT 1 OFFSET N-1;`.

## 5.2 Highest-paid employee in each department {#db-5-2}

```sql
SELECT * FROM (
  SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r
  FROM Employee e
) t WHERE r = 1;
```

(Top 3 per department: `r <= 3`.)

## 5.3 Duplicates {#db-5-3}

Find duplicate emails: `SELECT email, COUNT(*) FROM Users GROUP BY email HAVING COUNT(*) > 1;`

Delete duplicates, keeping the smallest id:

```sql
DELETE FROM Users
WHERE id NOT IN (SELECT MIN(id) FROM Users GROUP BY email);
```

(MySQL refuses a subquery on the table being deleted from; wrap it: `… NOT IN (SELECT id FROM (SELECT MIN(id) AS id FROM Users GROUP BY email) t)`.)

## 5.4 Rows with no match (anti-join) {#db-5-4}

Departments with no employees:

```sql
SELECT d.* FROM Department d
LEFT JOIN Employee e ON e.dept_id = d.id
WHERE e.id IS NULL;
```

Or `WHERE NOT EXISTS (SELECT 1 FROM Employee e WHERE e.dept_id = d.id)`. (Avoid `NOT IN` if the column can be NULL.)

## 5.5 Employees earning more than their manager {#db-5-5}

```sql
SELECT e.name FROM Employee e
JOIN Employee m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

## 5.6 Running total and change from previous row {#db-5-6}

```sql
SELECT day, amount,
  SUM(amount) OVER (ORDER BY day) AS running_total,
  amount - LAG(amount) OVER (ORDER BY day) AS change
FROM Sales;
```

## 5.7 Count per group, including empty groups {#db-5-7}

```sql
SELECT d.dname, COUNT(e.id) AS n      -- COUNT(e.id), not COUNT(*)
FROM Department d LEFT JOIN Employee e ON e.dept_id = d.id
GROUP BY d.dname;
```

`COUNT(*)` would count the NULL-padded row as 1 for an empty department; `COUNT(e.id)` gives 0.

## 5.8 Consecutive values (gaps and islands) {#db-5-8}

Numbers appearing at least three times in a row:

```sql
SELECT DISTINCT a.num FROM Logs a
JOIN Logs b ON b.id = a.id + 1 AND b.num = a.num
JOIN Logs c ON c.id = a.id + 2 AND c.num = a.num;
```

General trick for runs: `id - ROW_NUMBER() OVER (PARTITION BY value ORDER BY id)` is constant within a run of consecutive ids.

## 5.9 Pivot with CASE {#db-5-9}

```sql
SELECT dept_id,
  SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) AS men,
  SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) AS women
FROM Employee GROUP BY dept_id;
```

<div class="nb nb-moral">

Nearly every interview query is one of: a ranking window (N-th highest, top per group), GROUP BY + HAVING (duplicates, counts), a self-join (manager, consecutive rows), or an anti-join (LEFT JOIN … IS NULL / NOT EXISTS).

</div>
