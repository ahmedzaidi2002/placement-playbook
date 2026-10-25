---
title: "2 · Relational algebra and calculus"
linkTitle: "2 Relational algebra and calculus"
weight: 2
math: true
---
Relational algebra is the assembly language of query processing: every SQL query is parsed into an algebra tree, rewritten by algebraic identities, and executed operator by operator ([Chapter 11](../11-query/)). Relational calculus is the logic underneath SQL’s declarative `WHERE`. Both are on GATE-style papers; the algebra comes back in every optimizer question.

## 2.1 The operators {#sec-dbms-ra-ops}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the sailors database: who reserved a red boat?</em>

</div>

### 2.1.i The running instance {#s2-1-i}

All queries in this chapter run on the instance below (the classic sailors schema with new data). The same rows are loaded into SQLite and PostgreSQL by `schema-sailors.sql`, and into a small Python evaluator, `lib/ra.py`, that implements every operator of this chapter on sets of tuples.

| <strong>sailors</strong><br>`sid` | `sname` | `rating` | `age` |
|--:|:--|--:|--:|
| 1 | Arjun | 7 | 45 |
| 2 | Bina | 9 | 28 |
| 3 | Chetan | 3 | 35 |
| 4 | Divya | 9 | 31 |
| 5 | Esha | 5 | 26 |
| 6 | Farhan | 8 | 40 |
| 7 | Bina | 4 | 22 |

| <strong>boats</strong><br>`bid` | `bname` | `color` |
|--:|:--|:--|
| 101 | Sagar | red |
| 102 | Lehar | green |
| 103 | Tarang | red |
| 104 | Neel | blue |

| <strong>reserves</strong><br>`sid` | `bid` | `day` |
|--:|--:|:--|
| 1 | 101 | 06-01 |
| 1 | 102 | 06-02 |
| 1 | 103 | 06-05 |
| 1 | 104 | 06-07 |
| 2 | 101 | 06-03 |
| 2 | 104 | 06-08 |
| 4 | 101 | 06-04 |
| 4 | 102 | 06-09 |
| 4 | 103 | 06-04 |
| 6 | 102 | 06-06 |
| 7 | 102 | 06-10 |

Note the two sailors called Bina (sids 2 and 7): they are there to break a wrong query later.

### 2.1.ii Six basic operators {#s2-1-ii}

<div class="nb nb-definition" id="definition-2-1-1">

<strong>Definition 2.1.1</strong>. The <strong>basic operators</strong> of relational algebra take relations and return a relation:

- <strong>selection</strong> $\sigma_c(R)$: the tuples of $R$ satisfying condition $c$;
- <strong>projection</strong> $\pi_{A_1,\dots,A_k}(R)$: only the listed attributes, in that order, <em>duplicates removed</em>;
- <strong>union</strong> $R\cup S$ and <strong>difference</strong> $R-S$, for <strong>union-compatible</strong> relations (same number of attributes, same domains position by position);
- <strong>Cartesian product</strong> $R\times S$: every tuple of $R$ glued to every tuple of $S$;
- <strong>rename</strong> $\rho_{T(B_1,\dots,B_n)}(R)$: the same tuples under new relation or attribute names.

Everything else is derived: $R\cap S = R-(R-S)$; $R\bowtie_\theta S = \sigma_\theta(R\times S)$; natural join, division and outer joins below. The <strong>assignment</strong> $T\leftarrow E$ just names an intermediate result.

</div>

<div class="nb nb-definition" id="fact-2-1-2">

<strong>Fact 2.1.2</strong> (Cardinalities). $0\le|\sigma_c(R)|\le|R|$, and the schema is unchanged. $1\le|\pi_A(R)|\le|R|$ for nonempty $R$, with equality on the right whenever $A$ contains a key of $R$ (then no two tuples collapse). $|R\times S| = |R|\cdot|S|$ and the degree adds up. $\max(|R|,|S|)\le|R\cup S|\le|R|+|S|$; $0\le|R\cap S|\le \min(|R|,|S|)$; $0\le|R-S|\le|R|$.

</div>

Selection is <em>unary and tuple-at-a-time</em>: the condition looks at one tuple, so “students with the maximum marks” cannot be a single selection. It needs a comparison with every other tuple, i.e. a join (or aggregation).

<div class="nb nb-example nb-block" id="example-2-1-3">

<strong>Example 2.1.3</strong> (Q1 and Q2)

Sailors who reserved boat 103, and the names of sailors who reserved a red boat:

$$
\pi_{\mathit{sid}}\big(\sigma_{\mathit{bid}=103}(\mathit{reserves})\big), \qquad
	\pi_{\mathit{sname}}\big(\sigma_{\mathit{color}=\text{'red'}}(\mathit{boats})\bowtie
	\mathit{reserves}\bowtie \mathit{sailors}\big).
$$

```text {filename="Result (lib/ra.py)"}
 sid
-----
 1
 4
(2 rows)
```

```text {filename="Result (lib/ra.py)"}
 sname
-------
 Arjun
 Bina
 Divya
(3 rows)
```

Selecting the red boats <em>before</em> joining keeps the intermediate results small; the result is the same as selecting after the join. That is the first optimizer rule ([Section 2.5](#sec-dbms-ra-equiv)).

</div>

The evaluator’s core is short; projection is where set semantics lives:

```python {filename="lib/ra.py, lines 46–76",linenos=table,linenostart=46}
def select(r, pred):                      # sigma; pred sees a dict attr->value
    return Rel(r.attrs, [t for t in r.rows if pred(dict(zip(r.attrs, t)))])


def project(r, attrs):                    # pi: duplicates vanish (it is a set)
    ix = [r.col(a) for a in attrs]
    return Rel(attrs, [tuple(t[i] for i in ix) for t in r.rows])


def rename(r, mapping):                   # rho
    return Rel([mapping.get(a, a) for a in r.attrs], r.rows)


def cross(r, s):                          # x : attribute names must be distinct
    assert not set(r.attrs) & set(s.attrs), "rename first"
    return Rel(r.attrs + s.attrs, [a + b for a, b in _product(r.rows, s.rows)])


def theta_join(r, s, pred):
    return select(cross(r, s), pred)


def natural_join(r, s):
    common = [a for a in r.attrs if a in s.attrs]
    extra = [a for a in s.attrs if a not in common]
    rows = []
    for a in r.rows:
        for b in s.rows:
            if all(a[r.col(c)] == b[s.col(c)] for c in common):
                rows.append(a + tuple(b[s.col(e)] for e in extra))
    return Rel(r.attrs + tuple(extra), rows)
```

<div class="nb nb-moral">

Six operators, all closed over relations; projection and union remove duplicates because a relation is a set.

</div>

## 2.2 Joins, outer joins and their sizes {#sec-dbms-ra-joins}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `sailors` $\mathbin{\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}\mkern-4mu\bowtie}$ `reserves`: who reserved what, including sailors with no reservation.</em>

</div>

<div class="nb nb-definition" id="definition-2-2-1">

<strong>Definition 2.2.1</strong>. A <strong>theta join</strong> $R\bowtie_\theta S$ is $\sigma_\theta(R\times S)$; an <strong>equijoin</strong> is a theta join whose condition is a conjunction of equalities. The <strong>natural join</strong> $R\bowtie S$ equates all attributes with the same name and keeps one copy of each; with no common attribute it is the Cartesian product.

</div>

<div class="nb nb-definition" id="fact-2-2-2">

<strong>Fact 2.2.2</strong> (How big is a join?). $0\le|R\bowtie S|\le|R|\cdot|S|$. The extremes: no matching values gives $0$; no common attributes (or all tuples sharing one join value) gives $|R|\cdot|S|$. The case that matters in practice: if the join attributes are a <em>key</em> of $S$ and a <em>non-null foreign key</em> of $R$ referencing it, every $R$ tuple matches exactly one $S$ tuple and $|R\bowtie S|=|R|$. That is why joining `reserves` to `sailors` on `sid` returns exactly $|\mathit{reserves}| = 11$ rows.

</div>

<div class="nb nb-definition" id="definition-2-2-3">

<strong>Definition 2.2.3</strong>. A tuple of $R$ that matches no tuple of $S$ is <strong>dangling</strong>. The <strong>left outer join</strong> $R\mathbin{\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}\mkern-4mu\bowtie} S$ is $R\bowtie S$ plus every dangling $R$ tuple padded with `NULL`s; the <strong>right outer join</strong> $R\mathbin{\bowtie\mkern-4mu\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}} S$ adds the dangling $S$ tuples; the <strong>full outer join</strong> $R\mathbin{\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}\mkern-4mu\bowtie\mkern-4mu\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}} S$ adds both. In basic operators:

$$
R\mathbin{\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}\mkern-4mu\bowtie} S = (R\bowtie S)\ \cup \ \big(R - \pi_{\mathit{attrs}(R)}(R\bowtie S)\big)
	\times \{(\text{NULL},\dots,\text{NULL})\}.
$$

</div>

<div class="nb nb-example nb-block" id="example-2-2-4">

<strong>Example 2.2.4</strong> (Q8: every sailor with their boats)

$\pi_{\mathit{sid},\mathit{sname}}(\mathit{sailors}) \mathbin{\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}\mkern-4mu\bowtie} \pi_{\mathit{sid},\mathit{bid}}(\mathit{reserves})$ has the $11$ matched tuples plus $2$ dangling sailors (Chetan, Esha):

```text {filename="Result (lib/ra.py)"}
 sid | sname  | bid
-----+--------+------
 1   | Arjun  | 101
 1   | Arjun  | 102
 1   | Arjun  | 103
 1   | Arjun  | 104
 2   | Bina   | 101
 2   | Bina   | 104
 3   | Chetan | NULL
 4   | Divya  | 101
 4   | Divya  | 102
 4   | Divya  | 103
 5   | Esha   | NULL
 6   | Farhan | 102
 7   | Bina   | 102
(13 rows)
```

</div>

<div class="nb nb-remark" id="remark-2-2-5">

<strong>Remark 2.2.5</strong> (Row counts of outer joins) — $|R\mathbin{\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}\mkern-4mu\bowtie} S| = |R\bowtie S| + (\text{number of dangling } R \text{ tuples})$, and similarly for the others; in particular $|R\mathbin{\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}\mkern-4mu\bowtie} S|\ge|R|$ (as sets, assuming no duplicates). There is no “default” outer join: SQL requires `LEFT`, `RIGHT` or `FULL` before `OUTER JOIN`. Outer joins are neither associative in general nor commutative ($R\mathbin{\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}\mkern-4mu\bowtie} S = S\mathbin{\bowtie\mkern-4mu\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}} R$ up to column order).

</div>

<div class="nb nb-example nb-block" id="example-2-2-6">

<strong>Example 2.2.6</strong> (Q4: at least two different boats)

A self-join needs a rename so that the two copies have different attribute names:

$$
\pi_{\mathit{sid}}\Big(\mathit{reserves}\bowtie_{\mathit{sid}=\mathit{sid2}\ \wedge \
	\mathit{bid}\ne \mathit{bid2}}\rho_{(\mathit{sid2},\mathit{bid2},\mathit{day2})}(\mathit{reserves})\Big)
$$

```text {filename="Result (lib/ra.py)"}
 sid
-----
 1
 2
 4
(3 rows)
```

Without $\mathit{bid}\ne \mathit{bid2}$ every tuple joins with itself and the query returns every sailor with at least <em>one</em> reservation.

</div>

<div class="nb nb-moral">

Key–foreign-key joins preserve the size of the referencing side; outer joins add the dangling tuples back with `NULL`s.

</div>

## 2.3 Division: the “for all” operator {#sec-dbms-ra-div}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> sailors who reserved <em>all</em> boats.</em>

</div>

<div class="nb nb-definition" id="definition-2-3-1">

<strong>Definition 2.3.1</strong>. For $R(A,B)$ and $S(B)$, the <strong>division</strong> $R\div S$ is the largest relation $Q(A)$ with $Q\times S\subseteq R$: the $A$-values that appear in $R$ with <em>every</em> $B$-value of $S$. In basic operators:

$$
R\div S \;=\; \pi_A(R)\;-\;\pi_A\big((\pi_A(R)\times S) - R\big).
$$

Read it right to left: all candidate pairs, minus the pairs that exist, leaves the <em>missing</em> pairs; any $A$ with a missing pair is disqualified. Equivalently, $R\div S=\bigcap_{b\in S}\pi_A(\sigma_{B=b}(R))$.

</div>

<div class="nb nb-example nb-block" id="example-2-3-2">

<strong>Example 2.3.2</strong> (Q5 and Q6)

$\pi_{\mathit{sid},\mathit{bid}}(\mathit{reserves})\div \pi_{\mathit{bid}}(\mathit{boats})$ and the same divided by the red boats only:

```text {filename="Result (lib/ra.py)"}
 sid
-----
 1
(1 row)
```

```text {filename="Result (lib/ra.py)"}
 sid
-----
 1
 4
(2 rows)
```

Project `reserves` to $(\mathit{sid},\mathit{bid})$ first: dividing the three-column relation would require the same `day` for every boat.

</div>

The script checks that the definition and the $\pi,\times,-$ formula agree for all $16$ subsets of boats as divisor, and prints the size bound:

```text {filename="Output of c02-ra.py, last lines (Python 3.11)"}
division by definition == division by pi, x, -: all 16 divisors
|R| / |B| = 11 / 4: at most 2 sailors qualify
```

<div class="nb nb-definition" id="fact-2-3-3">

<strong>Fact 2.3.3</strong>. $|R\div S|\le \lfloor|R|/|S|\rfloor$ for nonempty $S$: each qualifying $A$-value needs $|S|$ tuples of $R$. Here $\lfloor 11/4\rfloor=2$ although only one sailor qualifies.

</div>

<div class="nb nb-remark" id="remark-2-3-4">

<strong>Remark 2.3.4</strong> (Dividing by an empty set) — If $S=\emptyset$, every candidate qualifies vacuously: $R\div \emptyset=\pi_A(R)$. SQL translations disagree with each other here. The double-`NOT EXISTS` form returns <em>every sailor</em> (even those with no reservation), and the counting form returns <em>nobody</em>, because no group has a count of $0$:

```sql {filename="c02-division-empty.sql"}
-- Divide by an EMPTY set of required boats.
CREATE TABLE required (bid INTEGER);

-- double NOT EXISTS: every sailor qualifies (vacuous truth)
SELECT COUNT(*) AS qualifying FROM sailors s
WHERE NOT EXISTS (SELECT * FROM required q
                  WHERE NOT EXISTS (SELECT * FROM reserves r
                                    WHERE r.sid = s.sid
                                      AND r.bid = q.bid));

-- counting: no group has COUNT(...) = 0, so nobody qualifies
SELECT COUNT(*) AS qualifying FROM (
  SELECT r.sid FROM reserves r JOIN required q ON r.bid = q.bid
  GROUP BY r.sid
  HAVING COUNT(DISTINCT r.bid) = (SELECT COUNT(*) FROM required)) t;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- double NOT EXISTS: every sailor qualifies (vacuous truth)
 qualifying
------------
          7
(1 row)

-- counting: no group has COUNT(...) = 0, so nobody qualifies
 qualifying
------------
          0
(1 row)
```

In an interview, say which semantics you want before you write the query.

</div>

<div class="nb nb-moral">

“All” in the question means division, or double negation in SQL: no required item that this candidate lacks.

</div>

## 2.4 Set operations, aggregation and the classic traps {#sec-dbms-ra-sets}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “sailors who reserved a red <em>and</em> a green boat”.</em>

</div>

<div class="nb nb-example nb-block" id="example-2-4-1">

<strong>Example 2.4.1</strong> (Q3: red and green)

A single selection $\sigma_{\mathit{color}=\text{'red'}\wedge \mathit{color}=\text{'green'}}$ is empty: one boat cannot have two colours. The “and” is across <em>different tuples</em>, so intersect the two sets of sailors. Intersect the <em>keys</em>:

$$
\pi_{\mathit{sname}}\Big(\big(\pi_{\mathit{sid}}(\sigma_{\text{red}}(\mathit{boats})\bowtie
	\mathit{reserves}) \cap \pi_{\mathit{sid}}(\sigma_{\text{green}}(\mathit{boats})\bowtie
	\mathit{reserves})\big)\bowtie \mathit{sailors}\Big)
$$

```text {filename="Result (lib/ra.py)"}
 sname
-------
 Arjun
 Divya
(2 rows)
```

Intersecting <em>names</em> instead returns Bina too: Bina 2 reserved a red boat and Bina 7 a green one, and as names they are the same value.

```text {filename="Result (lib/ra.py)"}
 sname
-------
 Arjun
 Bina
 Divya
(3 rows)
```

“Red <em>or</em> green” has no such trap: $\cup$ of names, or one selection with $\vee$, both work.

</div>

<div class="nb nb-example nb-block" id="example-2-4-2">

<strong>Example 2.4.2</strong> (Q7: sailors with no reservation)

$\pi_{\mathit{sid}}(\mathit{sailors})-\pi_{\mathit{sid}}(\mathit{reserves})$:

```text {filename="Result (lib/ra.py)"}
 sid
-----
 3
 5
(2 rows)
```

Negative questions (“no”, “never”, “not any”) are set difference, or an anti-join.

</div>

<div class="nb nb-definition" id="definition-2-4-3">

<strong>Definition 2.4.3</strong>. Extended relational algebra adds <strong>generalized projection</strong> $\pi_{F_1,\dots,F_k}(R)$ with arithmetic expressions, and <strong>aggregation</strong> $_{G_1,\dots,G_m}\gamma_{f_1(A_1),\dots}(R)$: group by the $G$’s, one output tuple per group with the aggregate values (`count`, `sum`, `avg`, `min`, `max`). With no grouping attributes the whole relation is one group.

</div>

<div class="nb nb-example nb-block" id="example-2-4-4">

<strong>Example 2.4.4</strong> (Q9: reservations per boat)

${}_{\mathit{bid}}\gamma_{\text{count}(*)\to n}(\mathit{reserves})$:

```text {filename="Result (lib/ra.py)"}
 bid | n
-----+---
 101 | 3
 102 | 4
 103 | 2
 104 | 2
(4 rows)
```

</div>

<div class="nb nb-moral">

“And” across different rows is an intersection (or a join), never one selection; intersect keys, not names.

</div>

## 2.5 Equivalences that an optimizer may use {#sec-dbms-ra-equiv}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> pushing $\sigma_{\mathit{color}=\text{'red'}}$ below the join.</em>

</div>

The optimizer ([Chapter 11](../11-query/)) rewrites the algebra tree using identities that hold on <em>every</em> instance. A claimed identity can be falsified by one counterexample, so the script tries $2000$ random instances of each and prints the smallest counterexample it finds:

```python {filename="c02-equiv.py"}
# Test algebraic equivalences on 2000 random small instances; print a
# counterexample for the ones that do not hold.
import random
from ra import (Rel, select, project, natural_join, union, intersect, minus,
                divide)

random.seed(7)
D = [0, 1, 2]


def rnd(attrs):
    rows = [(x, y) for x in D for y in D]
    return Rel(attrs, random.sample(rows, random.randint(0, 5)))


def same_up_to_order(x, y):       # joins may order their columns differently
    return project(x, sorted(x.attrs)) == project(y, sorted(y.attrs))


c = lambda t: t["a"] == 1             # a predicate on attribute a only
d = lambda t: t["b"] != 0

rules = [
    ("sigma_c AND d(R) = sigma_c(sigma_d(R))",
     lambda R, S, T, U: select(R, lambda t: c(t) and d(t)) ==
     select(select(R, d), c)),
    ("sigma_c(R u S) = sigma_c(R) u sigma_c(S)",
     lambda R, S, T, U: select(union(R, S), c) ==
     union(select(R, c), select(S, c))),
    ("sigma_c(R - S) = sigma_c(R) - S",
     lambda R, S, T, U: select(minus(R, S), c) == minus(select(R, c), S)),
    ("pi_a(R u S) = pi_a(R) u pi_a(S)",
     lambda R, S, T, U: project(union(R, S), ["a"]) ==
     union(project(R, ["a"]), project(S, ["a"]))),
    ("pi_a(R n S) = pi_a(R) n pi_a(S)",
     lambda R, S, T, U: project(intersect(R, S), ["a"]) ==
     intersect(project(R, ["a"]), project(S, ["a"]))),
    ("pi_a(R - S) = pi_a(R) - pi_a(S)",
     lambda R, S, T, U: project(minus(R, S), ["a"]) ==
     minus(project(R, ["a"]), project(S, ["a"]))),
    ("sigma_a=1(R |x| T) = sigma_a=1(R) |x| T",
     lambda R, S, T, U: select(natural_join(R, T), c) ==
     natural_join(select(R, c), T)),
    ("R |x| T = T |x| R",
     lambda R, S, T, U: same_up_to_order(natural_join(R, T),
                                         natural_join(T, R))),
    ("(R |x| T) |x| U = R |x| (T |x| U)",
     lambda R, S, T, U: natural_join(natural_join(R, T), U) ==
     natural_join(R, natural_join(T, U))),
    ("(R u S) / V = R/V u S/V",
     lambda R, S, T, U: divide(union(R, S), V) ==
     union(divide(R, V), divide(S, V))),
]

V = Rel(["b"], [(0,), (1,)])
for name, rule in rules:
    bad = None
    for _ in range(2000):
        R, S = rnd(["a", "b"]), rnd(["a", "b"])
        T, U = rnd(["b", "c"]), rnd(["c", "d"])
        if not rule(R, S, T, U):
            if bad is None or len(R) + len(S) < len(bad[0]) + len(bad[1]):
                bad = (R, S)
    if bad is None:
        print(f"holds   {name}")
    else:
        R, S = bad
        print(f"FAILS   {name}")
        print(f"        e.g. R = {sorted(R.rows)}, S = {sorted(S.rows)}")
```

```text {filename="Output (Python 3.11)"}
holds   sigma_c AND d(R) = sigma_c(sigma_d(R))
holds   sigma_c(R u S) = sigma_c(R) u sigma_c(S)
holds   sigma_c(R - S) = sigma_c(R) - S
holds   pi_a(R u S) = pi_a(R) u pi_a(S)
FAILS   pi_a(R n S) = pi_a(R) n pi_a(S)
        e.g. R = [(0, 0)], S = [(0, 1)]
FAILS   pi_a(R - S) = pi_a(R) - pi_a(S)
        e.g. R = [(0, 2)], S = [(0, 0)]
holds   sigma_a=1(R |x| T) = sigma_a=1(R) |x| T
holds   R |x| T = T |x| R
holds   (R |x| T) |x| U = R |x| (T |x| U)
FAILS   (R u S) / V = R/V u S/V
        e.g. R = [(0, 0)], S = [(0, 1)]
```

<div class="nb nb-theorem nb-block" id="theorem-2-5-1">

<strong>Theorem 2.5.1</strong> (The rules that hold)

On every instance:

1. Selections cascade and commute: $\sigma_{c\wedge d}(R)=\sigma_c(\sigma_d(R)) =\sigma_d(\sigma_c(R))$.
2. Selection distributes over $\cup$, $\cap$, $-$ (for $-$ it is enough to select from the left operand), and over a join when $c$ uses only one side’s attributes: $\sigma_c(R\bowtie S)=\sigma_c(R)\bowtie S$.
3. Projections cascade: $\pi_A(\pi_B(R))=\pi_A(R)$ when $A\subseteq B$; and $\pi_A(\sigma_c(R))=\sigma_c(\pi_A(R))$ when $c$ only uses attributes in $A$.
4. Natural and theta joins are commutative (up to column order) and associative.
5. Projection distributes over union: $\pi_A(R\cup S)=\pi_A(R)\cup \pi_A(S)$.

</div>

<div class="nb nb-remark" id="remark-2-5-2">

<strong>Remark 2.5.2</strong> (The ones that fail) — Projection does <em>not</em> distribute over $\cap$ or $-$: $R=\{(0,0)\}$ and $S=\{(0,1)\}$ have no common tuple, yet both project to $\{0\}$. Division does not distribute over union either. These are the “which of the following are equivalent” options that are meant to be rejected.

</div>

<div class="nb nb-moral">

Push selections and projections as far down as they go; never push a projection through $\cap$ or $-$.

</div>

## 2.6 Relational calculus {#sec-dbms-calculus}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $\{\,t.\mathit{sname} \mid t\in \mathit{sailors}\wedge \exists r\in \mathit{reserves}\, (r.\mathit{sid}=t.\mathit{sid}\wedge r.\mathit{bid}=103)\,\}$.</em>

</div>

### 2.6.i Tuple relational calculus {#s2-6-i}

<div class="nb nb-definition" id="definition-2-6-1">

<strong>Definition 2.6.1</strong>. A <strong>tuple relational calculus</strong> (TRC) query has the form $\{t\mid P(t)\}$: all tuples $t$ for which formula $P$ is true. Formulas are built from atoms $t\in R$, $t.A\ \theta \ s.B$, $t.A\ \theta \ c$, with $\wedge,\vee,\neg,\Rightarrow$ and the quantifiers $\exists s\in R$ and $\forall s\in R$. Algebra says <em>how</em> (a sequence of operations); calculus says <em>what</em> (a property of the answer). SQL’s `WHERE` with `EXISTS` is TRC with keywords.

</div>

<div class="nb nb-example nb-block" id="example-2-6-2">

<strong>Example 2.6.2</strong> (Red-boat sailors and all-boat sailors in TRC)

$$
\begin{align*}
		\{t.\mathit{sname}\mid{}& t\in \mathit{sailors}\wedge \exists r\in \mathit{reserves}\
		\exists b\in \mathit{boats}\\
		&(r.\mathit{sid}=t.\mathit{sid}\wedge r.\mathit{bid}=b.\mathit{bid}\wedge
		b.\mathit{color}=\text{'red'})\}\\[4pt]
		\{t\mid{}& t\in \mathit{sailors}\wedge \forall b\in \mathit{boats}\ \exists r\in \mathit{reserves}\\
		&(r.\mathit{sid}=t.\mathit{sid}\wedge r.\mathit{bid}=b.\mathit{bid})\}
	\end{align*}
$$

The second is division; SQL has no $\forall$, so it becomes $\neg \exists b\,\neg \exists r$: the double `NOT EXISTS` of [Section 2.3](#sec-dbms-ra-div).

</div>

### 2.6.ii Domain relational calculus {#s2-6-ii}

<div class="nb nb-definition" id="definition-2-6-3">

<strong>Definition 2.6.3</strong>. In <strong>domain relational calculus</strong> (DRC) variables range over attribute values: $\{\langle x_1,\dots,x_k\rangle \mid P(x_1,\dots,x_k)\}$ with atoms $\langle x_1,\dots,x_n\rangle \in R$. Red-boat sailors: $\{\langle n\rangle \mid \exists s,r,a\,(\langle s,n,r,a\rangle \in \mathit{sailors}\wedge \exists b,d\,(\langle s,b,d\rangle \in \mathit{reserves}\wedge \exists m\,(\langle b,m, \text{'red'}\rangle \in \mathit{boats})))\}$. QBE is DRC with a grid.

</div>

### 2.6.iii Safety and expressive power {#s2-6-iii}

<div class="nb nb-definition" id="definition-2-6-4">

<strong>Definition 2.6.4</strong>. A calculus query is <strong>unsafe</strong> if its answer can contain values that appear nowhere in the database or in the query, so that it may be infinite: $\{t\mid \neg(t\in \mathit{sailors})\}$ is “every tuple in the universe that is not a sailor”. A query is <strong>safe</strong> if every value in its result comes from the <strong>active domain</strong> (the values in the relations and constants of the query).

</div>

<div class="nb nb-theorem nb-block" id="theorem-2-6-5">

<strong>Theorem 2.6.5</strong> (Codd’s theorem)

Relational algebra, safe tuple relational calculus and safe domain relational calculus express exactly the same queries. A language that can express all of them is <strong>relationally complete</strong>; SQL is.

</div>

<div class="nb nb-remark" id="remark-2-6-6">

<strong>Remark 2.6.6</strong> (More than relationally complete, and less) — “Every algebra query has a calculus equivalent but not conversely” is only true if unsafe calculus is allowed; for safe queries the three are equivalent. SQL goes beyond the algebra with bags (duplicates), aggregation, arithmetic, `ORDER BY` and recursion. Plain algebra and calculus cannot express <em>transitive closure</em> (“all managers above Asha, at any depth”) for unbounded depth; SQL needs `WITH RECURSIVE` for it ([Chapter 4](../04-sql-advanced/)).

</div>

### 2.6.iv The same queries in SQL {#s2-6-iv}

```sql {filename="c02-ra-sql.sql"}
-- Q3 red AND green: intersect the sids, then look up names
SELECT s.sname FROM sailors s
WHERE s.sid IN (SELECT r.sid FROM reserves r JOIN boats b ON r.bid = b.bid
                WHERE b.color = 'red'
                INTERSECT
                SELECT r.sid FROM reserves r JOIN boats b ON r.bid = b.bid
                WHERE b.color = 'green')
ORDER BY s.sname;

-- Q3' the wrong version: intersect the NAMES
SELECT s.sname FROM sailors s JOIN reserves r ON s.sid = r.sid
                              JOIN boats b ON r.bid = b.bid
WHERE b.color = 'red'
INTERSECT
SELECT s.sname FROM sailors s JOIN reserves r ON s.sid = r.sid
                              JOIN boats b ON r.bid = b.bid
WHERE b.color = 'green'
ORDER BY 1;

-- Q5 division, double negation: no boat that this sailor has not reserved
SELECT s.sid, s.sname FROM sailors s
WHERE NOT EXISTS (SELECT * FROM boats b
                  WHERE NOT EXISTS (SELECT * FROM reserves r
                                    WHERE r.sid = s.sid
                                      AND r.bid = b.bid));

-- Q5 division by counting distinct boats
SELECT r.sid FROM reserves r
GROUP BY r.sid
HAVING COUNT(DISTINCT r.bid) = (SELECT COUNT(*) FROM boats);
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
-- Q3 red AND green: intersect the sids, then look up names
 sname
-------
 Arjun
 Divya
(2 rows)

-- Q3' the wrong version: intersect the NAMES
 sname
-------
 Arjun
 Bina
 Divya
(3 rows)

-- Q5 division, double negation: no boat that this sailor has not reserved
 sid | sname
-----+-------
   1 | Arjun
(1 row)

-- Q5 division by counting distinct boats
 sid
-----
   1
(1 row)
```

Both engines agree with the evaluator, including the wrong answer of the name-intersection. The counting form of division is the one most people write in an interview; it relies on `reserves.bid` being a foreign key into `boats` (otherwise reservations of unknown boats would inflate the count) and on `COUNT(DISTINCT ...)` (a sailor who reserved one boat twice would otherwise count twice).

<div class="nb nb-moral">

Safe calculus and algebra are equally powerful; SQL’s `NOT EXISTS` is how “for all” is spelled.

</div>
