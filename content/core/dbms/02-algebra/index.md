---
title: "2 · Relational algebra and calculus"
linkTitle: "2 Relational algebra"
weight: 2
math: true
---
The running example: `Sailors(sid, sname, rating, age)`, `Boats(bid, bname, color)`, `Reserves(sid, bid, day)`.

## 2.1 The operators {#db-2-1}

| Operator | Symbol | Does | SQL equivalent |
|---|---|---|---|
| Selection | $\sigma_{c}(R)$ | keeps **rows** satisfying $c$ | `WHERE` |
| Projection | $\pi_{A}(R)$ | keeps **columns** $A$ (removes duplicates) | `SELECT DISTINCT A` |
| Union | $R \cup S$ | rows in either (same columns needed) | `UNION` |
| Difference | $R - S$ | rows in $R$ but not $S$ | `EXCEPT` |
| Cartesian product | $R \times S$ | every pair of rows | `FROM R, S` |
| Rename | $\rho$ | rename a relation or column | `AS` |
| Intersection | $R \cap S$ | rows in both $= R - (R - S)$ | `INTERSECT` |
| Join | $R \bowtie_{c} S$ | $\sigma_c(R \times S)$ | `JOIN ... ON` |
| Division | $R \div S$ | "for all" | `NOT EXISTS ... NOT EXISTS` |

The six **basic** operators are $\sigma, \pi, \cup, -, \times, \rho$; the rest can be built from them.

<div class="nb nb-example">

<strong>Example</strong> (Three queries)

- Sailors who reserved boat 103: $\pi_{sid}(\sigma_{bid = 103}(\text{Reserves}))$.
- Names of sailors who reserved a red boat: $\pi_{sname}(\sigma_{color = \text{'red'}}(\text{Boats}) \bowtie \text{Reserves} \bowtie \text{Sailors})$.
- Sailors with no reservation: $\pi_{sid}(\text{Sailors}) - \pi_{sid}(\text{Reserves})$. Negative questions ("never", "no") are set difference.

</div>

<div class="nb nb-remark">

<strong>Trap: "red AND green"</strong> — $\sigma_{color = \text{red} \wedge color = \text{green}}$ is always empty: one boat cannot have two colours. Sailors who reserved a red boat **and** a green boat = (red-boat sailors) $\cap$ (green-boat sailors), computed separately.

</div>

## 2.2 Joins and their sizes {#db-2-2}

- **Theta join** $R \bowtie_c S$, **equi-join** (only $=$), **natural join** $R \bowtie S$ (equality on all common columns, which appear once).
- **Outer joins** keep unmatched rows, padded with NULL: left ⟕, right ⟖, full ⟗.

| Join of $R$ ($m$ rows) and $S$ ($n$ rows) | Rows |
|---|---|
| Cartesian product | exactly $m \times n$ |
| Inner join | 0 to $m \times n$ |
| Natural join on a column that is a key of $S$ (FK from $R$) | at most $m$ |
| Left outer join | at least $m$ |
| Full outer join | at least $\max(m, n)$; $m + n$ when nothing matches |

## 2.3 Division: "for all" {#db-2-3}

$R(A, B) \div S(B)$ = the values of $A$ that appear in $R$ with **every** $B$ in $S$.

<div class="nb nb-example">

<strong>Example</strong> (Division)

Sailors who reserved **all** boats: $\pi_{sid, bid}(\text{Reserves}) \div \pi_{bid}(\text{Boats})$. If Reserves(sid, bid) = {(1,101), (1,102), (1,103), (2,101), (2,102)} and Boats = {101, 102, 103}, the answer is {1}: only sailor 1 has all three.

</div>

Always project $R$ down to the two columns first; extra columns (like `day`) make division give wrong answers.

## 2.4 Relational calculus, briefly {#db-2-4}

- **Tuple relational calculus (TRC):** variables range over rows: $\{\, t \mid t \in \text{Sailors} \wedge t.rating > 7 \,\}$.
- **Domain relational calculus (DRC):** variables range over column values.
- Both are **declarative** (say *what*), algebra is **procedural** (say *how*). Safe calculus, relational algebra and basic SQL have the same expressive power (**relational completeness**).

<div class="nb nb-moral">

σ picks rows, π picks columns, × pairs everything, ⋈ is a filtered ×, − answers "never", ÷ answers "for all".

</div>
