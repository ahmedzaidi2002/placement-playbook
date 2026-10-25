---
title: "6 · Functional dependencies and normalization"
linkTitle: "6 Functional dependencies and normalization"
weight: 6
math: true
---
Every number in this chapter (closures, keys, covers, normal forms, decompositions) comes from one small Python module, `lib/fd.py`, about 190 lines. Its core functions are shown where they are used; the scripts that call it are complete.

## 6.1 Why normalize {#sec-dbms-why-norm}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> one wide table `enroll(roll, course, sname, grade)` that stores a student’s name once per course taken.</em>

</div>

| `roll` | `course` | `sname` | `grade` |
|:--|:--|:--|:--|
| CS21B001 | CS3100 | Asha | S |
| CS21B001 | CS3200 | Asha | A |
| CS21B002 | CS3100 | Ravi | B |

The key is (`roll`, `course`), but `sname` depends on `roll` alone. That one misplaced dependency causes all four classic problems:

- <strong>redundancy</strong>: Asha’s name is stored once per course;
- <strong>update anomaly</strong>: renaming Asha needs every one of her rows changed, and missing one leaves the table contradicting itself;
- <strong>insertion anomaly</strong>: a newly admitted student who has taken no course cannot be recorded without a fake course (the key cannot be `NULL`);
- <strong>deletion anomaly</strong>: deleting Ravi’s only enrolment also deletes the fact that Ravi exists.

Splitting the table into `student(roll, sname)` and `enroll(roll, course, grade)` removes all four.

<div class="nb nb-definition" id="definition-6-1-1">

<strong>Definition 6.1.1</strong>. <strong>Normalization</strong> is the process of decomposing relations, guided by functional (and multivalued) dependencies, so that every fact is stored exactly once: each non-trivial dependency becomes a key constraint of some table. The normal forms (1NF, 2NF, 3NF, BCNF, 4NF, 5NF) are increasingly strict conditions measuring how far a schema is from that ideal. A good decomposition must also be <em>lossless</em> (joining the pieces gives back exactly the original) and preferably <em>dependency preserving</em>.

</div>

<div class="nb nb-remark" id="remark-6-1-2">

<strong>Remark 6.1.2</strong> (The interview answer) — “Normalization organizes tables so that each fact lives in one place. It removes redundancy, which removes update, insertion and deletion anomalies and saves space, and it turns integrity rules into keys that the database enforces. The price is more joins on read, so read-heavy analytical systems sometimes denormalize on purpose.” Then give the `enroll` example. Denormalization is in [Chapter 12](../12-beyond/).

</div>

## 6.2 Functional dependencies and closure {#sec-dbms-fd}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $F=\{A\to BC,\ CD\to E,\ B\to D,\ E\to A\}$: what does $A$ determine?</em>

</div>

<div class="nb nb-definition" id="definition-6-2-1">

<strong>Definition 6.2.1</strong>. $X\to Y$ (“$X$ functionally determines $Y$”) holds on $R$ if any two tuples that agree on $X$ agree on $Y$, in every legal instance. It is <strong>trivial</strong> if $Y\subseteq X$, <strong>non-trivial</strong> if $Y\not \subseteq X$, and <strong>completely non-trivial</strong> if $X\cap Y=\emptyset$. $X\to A$ is a <strong>full</strong> dependency if no proper subset of $X$ determines $A$, and <strong>partial</strong> otherwise (so a partial dependency needs $|X|\ge2$). $A$ is <strong>transitively</strong> dependent on $X$ if $X\to Y$ and $Y\to A$ with $Y\not \to X$ and $A\notin Y$.

</div>

Like keys, an FD is a statement about the schema: an instance can violate an FD (two rows agree on $X$ but not on $Y$) but can never prove one.

<div class="nb nb-theorem nb-block" id="theorem-6-2-2">

<strong>Theorem 6.2.2</strong> (Armstrong’s axioms)

<strong>Reflexivity</strong>: if $Y\subseteq X$ then $X\to Y$. <strong>Augmentation</strong>: if $X\to Y$ then $XZ\to YZ$. <strong>Transitivity</strong>: if $X\to Y$ and $Y\to Z$ then $X\to Z$. They are <em>sound</em> (derive only FDs that hold) and <em>complete</em> (derive every FD that holds). Derived rules: <strong>union</strong> ($X\to Y$, $X\to Z\Rightarrow X\to YZ$), <strong>decomposition</strong> ($X\to YZ\Rightarrow X\to Y$), <strong>pseudo-transitivity</strong> ($X\to Y$, $WY\to Z\Rightarrow WX\to Z$), <strong>composition</strong> ($X\to Y$, $Z\to W\Rightarrow XZ\to YW$).

</div>

<div class="nb nb-remark" id="remark-6-2-3">

<strong>Remark 6.2.3</strong> (Right side splits, left side does not) — $X\to YZ$ gives $X\to Y$ and $X\to Z$; but $XY\to Z$ does not give $X\to Z$ (grade depends on roll <em>and</em> course, not on either alone).

</div>

<div class="nb nb-definition" id="definition-6-2-4">

<strong>Definition 6.2.4</strong>. The <strong>closure</strong> $X^+$ of a set of attributes is the set of all attributes determined by $X$ under $F$. Then $F\models X\to Y$ iff $Y\subseteq X^+$, and $X$ is a super key iff $X^+$ contains every attribute. $X$ is <strong>closed</strong> if $X^+=X$.

</div>

The algorithm is a fixpoint: start from $X$, add the right side of every FD whose left side is already inside, repeat until nothing changes. It runs in time polynomial in $|F|$ and $|R|$:

```python {filename="lib/fd.py, lines 25–35",linenos=table,linenostart=25}
def closure(x, fds):
    """X+ : keep applying FDs whose left side is already inside."""
    res = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= res and not rhs <= res:
                res |= rhs
                changed = True
    return frozenset(res)
```

```python {filename="c06-closure.py"}
# Attribute closures and implication tests for R(ABCDEG).
from fd import parse, closure, implies, s

F = parse("A->BC, CD->E, B->D, E->A")
print("F =", "A->BC, CD->E, B->D, E->A")
for x in ["A", "B", "C", "D", "E", "CD", "BC"]:
    print(f"  {x:>2}+ = {s(closure(frozenset(x), F))}")
for lhs, rhs in [("BC", "A"), ("D", "A"), ("AG", "EG"), ("CG", "B")]:
    ok = implies(F, frozenset(lhs), frozenset(rhs))
    print(f"  F implies {lhs}->{rhs}?  {ok}")
```

```text {filename="Output (Python 3.11)"}
F = A->BC, CD->E, B->D, E->A
   A+ = ABCDE
   B+ = BD
   C+ = C
   D+ = D
   E+ = ABCDE
  CD+ = ABCDE
  BC+ = ABCDE
  F implies BC->A?  True
  F implies D->A?  False
  F implies AG->EG?  True
  F implies CG->B?  False
```

$A^+$ contains everything, so $A$ is a key of $ABCDE$ (and $AG$ of $ABCDEG$, since nothing determines $G$). $BC\to A$ follows ($BC\to BCD\to E\to A$) although it is not in $F$; $D\to A$ does not, since $D^+=D$.

<div class="nb nb-moral">

To test any FD, compute one closure; never search for an Armstrong derivation by hand.

</div>

## 6.3 Finding and counting candidate keys {#sec-dbms-fd-keys}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $R(ABCDE)$ with $A\to B$, $BC\to E$, $ED\to A$ has three candidate keys.</em>

</div>

<div class="nb nb-definition" id="fact-6-3-1">

<strong>Fact 6.3.1</strong> (Pruning the search). An attribute that appears on no right side (after removing trivial parts) cannot be derived, so it is in <em>every</em> key. An attribute that appears only on right sides is in <em>no</em> key. Only the attributes on both sides need to be tried: start from the “core” of never-derived attributes and add subsets of the rest in increasing size, skipping supersets of keys already found.

</div>

```python {filename="lib/fd.py, lines 67–81",linenos=table,linenostart=67}
def candidate_keys(attrs, fds):
    attrs = frozenset(attrs)
    rhs_all = frozenset().union(*(r - l for l, r in fds))
    lhs_all = frozenset().union(*(l for l, r in fds))
    core = attrs - rhs_all                  # never derived: in EVERY key
    middle = sorted((attrs & rhs_all) & lhs_all)   # may or may not be in a key
    keys = []
    for k in range(len(middle) + 1):
        for extra in combinations(middle, k):
            cand = core | frozenset(extra)
            if closure(cand, fds) >= attrs and \
                    not any(key <= cand for key in keys):
                keys.append(cand)
    return keys
```

```python {filename="c06-keys.py"}
# Candidate keys and prime attributes, found by lib/fd.py.
from itertools import combinations
from fd import parse, candidate_keys, closure, s


def brute_keys(attrs, fds):           # minimal super keys, by brute force
    sup = [frozenset(c) for k in range(1, len(attrs) + 1)
           for c in combinations(attrs, k)
           if closure(frozenset(c), fds) >= set(attrs)]
    return {k for k in sup if not any(o < k for o in sup)}


cases = [
    ("ABCDEG", "A->BC, CD->E, B->D, E->A"),
    ("ABCD",   "AB->CD, C->A, D->B"),
    ("ABCDE",  "A->B, BC->E, ED->A"),
    ("ABCDEF", "AB->C, C->D, D->E, E->F, F->A"),
    ("ABCD",   "A->B, B->C, C->D, D->A"),
]
for attrs, text in cases:
    keys = candidate_keys(attrs, parse(text))
    assert set(keys) == brute_keys(attrs, parse(text))
    prime = s(frozenset().union(*keys))
    print(f"R({attrs}) {text}")
    print(f"   keys: {', '.join(s(k) for k in keys)}   ({len(keys)})"
          f"   prime: {prime}")
print("(every key list cross-checked against brute force over all subsets)")
```

```text {filename="Output (Python 3.11)"}
R(ABCDEG) A->BC, CD->E, B->D, E->A
   keys: AG, EG, BCG, CDG   (4)   prime: ABCDEG
R(ABCD) AB->CD, C->A, D->B
   keys: AB, AD, BC, CD   (4)   prime: ABCD
R(ABCDE) A->B, BC->E, ED->A
   keys: ACD, BCD, CDE   (3)   prime: ABCDE
R(ABCDEF) AB->C, C->D, D->E, E->F, F->A
   keys: AB, BC, BD, BE, BF   (5)   prime: ABCDEF
R(ABCD) A->B, B->C, C->D, D->A
   keys: A, B, C, D   (4)   prime: ABCD
(every key list cross-checked against brute force over all subsets)
```

<div class="nb nb-definition" id="definition-6-3-2">

<strong>Definition 6.3.2</strong>. An attribute is <strong>prime</strong> if it belongs to some candidate key, and <strong>non-prime</strong> otherwise.

</div>

<div class="nb nb-example nb-block" id="example-6-3-3">

<strong>Example 6.3.3</strong> (Reading the output)

In $R(ABCDE)$, $A\to B$, $BC\to E$, $ED\to A$: $C$ and $D$ appear on no right side, so every key contains $CD$; $CD^+=CD$, so add one more attribute: $ACD$, $BCD$, $CDE$ all work. Every attribute is prime. In the cycle $A\to B\to C\to D\to A$, each single attribute is a key: $4$ keys and, by [Section 1.4](../01-relational/#sec-dbms-keys), $2^4-1=15$ super keys.

</div>

<div class="nb nb-moral">

Keys = core of never-derived attributes plus a minimal set of the rest; check each candidate with one closure.

</div>

## 6.4 Equivalence and minimal covers {#sec-dbms-cover}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $\{A\to BC, B\to C, AB\to D, AC\to D, D\to E\}$ shrinks to four FDs.</em>

</div>

<div class="nb nb-definition" id="definition-6-4-1">

<strong>Definition 6.4.1</strong>. $F$ <strong>covers</strong> $G$ if every FD of $G$ follows from $F$; they are <strong>equivalent</strong> if each covers the other ($F^+=G^+$). A <strong>minimal</strong> (canonical, irreducible) cover is an equivalent set in which every right side is a single attribute, no left-side attribute is <strong>extraneous</strong> (removable without changing $F^+$), and no FD is redundant.

</div>

<div class="nb nb-remark" id="algorithm-6-4-2">

<strong>Algorithm 6.4.2</strong> (Minimal cover) — (1) Split right sides into single attributes. (2) For each FD $X\to A$ and each $B\in X$: if $A\in(X-B)^+$ under the current set, drop $B$. (3) For each FD: if it follows from the others, drop it. Do step 2 before step 3; the other order can leave a redundant FD.

</div>

```python {filename="c06-cover.py"}
# Minimal (canonical) covers, and why there can be more than one.
from fd import parse, minimal_cover, equivalent, show

F = parse("A->BC, B->C, AB->D, AC->D, D->E")
G = minimal_cover(F)
print("F    =", show(F))
print("min  =", show(G), "   equivalent:", equivalent(F, G))

# The same FDs listed in a different order give a different minimal cover.
H = parse("A->B, B->C, C->A, A->C, B->A, C->B")
for order in (H, list(reversed(H))):
    print("in   =", show(order))
    print("min  =", show(minimal_cover(order)),
          "   equivalent:", equivalent(H, minimal_cover(order)))
```

```text {filename="Output (Python 3.11)"}
F    = A->BC, B->C, AB->D, AC->D, D->E
min  = A->B, B->C, A->D, D->E    equivalent: True
in   = A->B, B->C, C->A, A->C, B->A, C->B
min  = A->C, B->A, C->B    equivalent: True
in   = C->B, B->A, A->C, C->A, B->C, A->B
min  = C->A, B->C, A->B    equivalent: True
```

In the first set, $AB\to D$ loses $B$ because $A\to B$ already gives it, $AC\to D$ loses $C$, both become $A\to D$, and $A\to C$ is redundant via $A\to B\to C$. The cycle shows that a minimal cover is not unique: the same six FDs processed in another order keep a different three. Equivalence, not equality, is what matters; the number of FDs can differ between minimal covers too.

## 6.5 Normal forms {#sec-dbms-nf}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $\texttt{teach}(S, C, T)$: student, course, teacher, with $SC\to T$ and $T\to C$, in 3NF but not BCNF.</em>

</div>

<div class="nb nb-definition" id="definition-6-5-1">

<strong>Definition 6.5.1</strong> (The normal forms). Let $R$ have FDs $F$. Then $R$ is in

- <strong>1NF</strong> if every attribute is atomic (no lists, no nested tables, no repeating groups); a relation of the relational model is in 1NF by definition;
- <strong>2NF</strong> if it is in 1NF and no non-prime attribute is partially dependent on a candidate key;
- <strong>3NF</strong> if for every non-trivial $X\to A$ in $F^+$, $X$ is a super key <em>or</em> $A$ is prime (equivalently: no non-prime attribute is transitively dependent on a key);
- <strong>BCNF</strong> if for every non-trivial $X\to A$ in $F^+$, $X$ is a super key.

For 3NF and BCNF it suffices to check the FDs of $F$ itself (with split right sides), not all of $F^+$; for 2NF, check the closure of every proper subset of every key, since a partial dependency may be implied rather than listed.

</div>

```python {filename="c06-nf.py"}
# The highest normal form of a relation, with the reason.
from fd import parse, normal_form, candidate_keys, s

cases = [
    ("enroll", "SCNG", "SC->G, S->N"),    # student, course, name, grade
    ("emp",    "EDM",  "E->D, D->M"),     # emp, dept, manager
    ("teach",  "SCT",  "SC->T, T->C"),    # student, course, teacher
    ("ABCD",   "ABCD", "AB->CD, C->A, D->B"),
    ("ABC",    "ABC",  "A->B, B->C, C->A"),
]
for name, attrs, text in cases:
    keys = ", ".join(s(k) for k in candidate_keys(attrs, parse(text)))
    r = f"R({attrs})"
    print(f"{name:7}{r:9}{text:20} keys {keys:16}"
          f"-> {normal_form(attrs, parse(text))}")
```

```text {filename="Output (Python 3.11)"}
enroll R(SCNG)  SC->G, S->N          keys CS              -> 1NF
emp    R(EDM)   E->D, D->M           keys E               -> 2NF
teach  R(SCT)   SC->T, T->C          keys CS, ST          -> 3NF
ABCD   R(ABCD)  AB->CD, C->A, D->B   keys AB, AD, BC, CD  -> 3NF
ABC    R(ABC)   A->B, B->C, C->A     keys A, B, C         -> BCNF
```

<div class="nb nb-example nb-block" id="example-6-5-2">

<strong>Example 6.5.2</strong> (Reading the output)

`enroll`: key $SC$, $S\to N$ is a partial dependency of non-prime $N$: 1NF only. `emp`: key $E$ is a single attribute, so no partial dependency is possible (2NF), but $D\to M$ with $D$ not a key and $M$ non-prime is transitive: 2NF only. `teach`: keys $SC$ and $ST$; $T\to C$ has a non-key left side, but $C$ is prime: 3NF, not BCNF. The $ABCD$ relation is the same shape with four overlapping keys.

</div>

<div class="nb nb-theorem nb-block" id="theorem-6-5-3">

<strong>Theorem 6.5.3</strong> (Facts about 3NF and BCNF)

For relations with functional dependencies only:

1. BCNF $\Rightarrow$ 3NF $\Rightarrow$ 2NF $\Rightarrow$ 1NF, and none of the converses holds.
2. Every relation with two attributes is in BCNF.
3. If every attribute is prime, the relation is in 3NF (and possibly not in BCNF).
4. If every candidate key is a single attribute, 2NF is automatic; a 3NF relation whose keys are all single attributes is in BCNF (indeed, by a theorem of Date and Fagin, in 5NF).
5. A relation in 3NF but not in BCNF has at least two candidate keys that are composite and overlap: the violating $X\to A$ has $A$ prime, so $A$ is in a key $AY$, and $XY$ is then another key sharing $Y$.
6. BCNF removes all redundancy caused by FDs; 3NF can leave some ($T\to C$ repeats the course for every student of a teacher).
7. A lossless BCNF decomposition always exists; a lossless and dependency-preserving one may not (`teach`). A lossless and dependency-preserving 3NF decomposition always exists ([Section 6.6](#sec-dbms-decomp)).

</div>

<div class="nb nb-moral">

3NF: every non-trivial FD has a super key on the left <em>or</em> a prime attribute on the right; BCNF drops the “or”.

</div>

## 6.6 Decomposition: lossless joins and dependency preservation {#sec-dbms-decomp}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> splitting `teach`: lossless, but the rule “a student takes a course from one teacher” can no longer be checked in one table.</em>

</div>

<div class="nb nb-definition" id="definition-6-6-1">

<strong>Definition 6.6.1</strong>. A decomposition of $R$ into $R_1,\dots,R_n$ (whose attributes cover $R$) is <strong>lossless</strong> (non-additive) if for every legal instance $r$, $\pi_{R_1}(r)\bowtie \dots \bowtie \pi_{R_n}(r)=r$. The join always contains $r$; a lossy decomposition adds <strong>spurious tuples</strong>: it loses information by gaining rows. It is <strong>dependency preserving</strong> if $(F_1\cup \dots \cup F_n)^+=F^+$, where $F_i$ is the set of FDs of $F^+$ that mention only attributes of $R_i$, so that every FD can be checked inside one table.

</div>

<div class="nb nb-theorem nb-block" id="theorem-6-6-2">

<strong>Theorem 6.6.2</strong> (Binary test)

With FDs only, $\{R_1,R_2\}$ is lossless iff $R_1\cap R_2\to R_1$ or $R_1\cap R_2\to R_2$: the common attributes are a super key of one side.

</div>

For more than two pieces, joining pairs and applying the binary test (“successive combining”) can prove losslessness but cannot prove lossiness. The general test is the <strong>chase</strong>: a tableau with one row per piece, holding the distinguished symbol `a` in that piece’s columns and a row-specific `b`$_i$ elsewhere. Repeatedly, if two rows agree on the left side of an FD, make them agree on its right side (an `a` wins). The decomposition is lossless iff some row becomes all `a`.

```python {filename="c06-decomp.py"}
# Lossless join (binary test and chase), dependency preservation,
# BCNF decomposition and 3NF synthesis.
from fd import (parse, show, s, lossless_binary, chase, preserves,
                bcnf_decompose, synthesize_3nf, normal_form, project)

F = parse("A->B, C->D, AC->E")
print("R(ABCDE), F:", show(F))
print("  {AB, CD, ACE}: chase")
print("  lossless:", chase("ABCDE", ["AB", "CD", "ACE"], F, verbose=True))
print("  {AB, CDE}: chase")
print("  lossless:", chase("ABCDE", ["AB", "CDE"], F, verbose=True))

G = parse("A->B, B->C")
print("R(ABC), F:", show(G))
for parts in (["AB", "BC"], ["AB", "AC"], ["AC", "BC"]):
    lost = preserves(parts, G)
    print(f"  {{{', '.join(parts)}}}: lossless {lossless_binary(*parts, G)},"
          f" lost FDs: {show(lost) if lost else 'none'}")

T = parse("SC->T, T->C")                  # student, course, teacher
print("R(SCT), F:", show(T), "->", normal_form("SCT", T))
d = bcnf_decompose("SCT", T)
print("  BCNF decomposition:", ", ".join(s(p) for p in d),
      "| lost:", show(preserves(d, T)) or "none")
print("  3NF synthesis:", ", ".join(s(p) for p in synthesize_3nf("SCT", T)))

K = parse("A->BC, CD->E, B->D, E->A")
print("R(ABCDEG), F:", show(K), "->", normal_form("ABCDEG", K))
d = bcnf_decompose("ABCDEG", K)
print("  BCNF decomposition:", ", ".join(s(p) for p in d))
for p in d:
    fds = show(project(p, K)) or "-"
    print(f"    {s(p):6} FDs {fds:24} {normal_form(p, project(p, K))}")
print("  lossless:", chase("ABCDEG", d, K),
      "| lost:", show(preserves(d, K)) or "none")
t = synthesize_3nf("ABCDEG", K)
print("  3NF synthesis:", ", ".join(s(p) for p in t))
print("  lossless:", chase("ABCDEG", t, K),
      "| lost:", show(preserves(t, K)) or "none")
```

```text {filename="Output (Python 3.11)"}
R(ABCDE), F: A->B, C->D, AC->E
  {AB, CD, ACE}: chase
  R1:  a  a b1 b1 b1
  R2: b2 b2  a  a b2
  R3:  a  a  a  a  a
  lossless: True
  {AB, CDE}: chase
  R1:  a  a b1 b1 b1
  R2: b2 b2  a  a  a
  lossless: False
R(ABC), F: A->B, B->C
  {AB, BC}: lossless True, lost FDs: none
  {AB, AC}: lossless True, lost FDs: B->C
  {AC, BC}: lossless False, lost FDs: A->B
R(SCT), F: CS->T, T->C -> 3NF
  BCNF decomposition: CT, ST | lost: CS->T
  3NF synthesis: CST
R(ABCDEG), F: A->BC, CD->E, B->D, E->A -> 3NF
  BCNF decomposition: BD, ABCE, AG
    BD     FDs B->D                     BCNF
    ABCE   FDs A->E, E->B, E->C, BC->A  BCNF
    AG     FDs -                        BCNF
  lossless: True | lost: CD->E
  3NF synthesis: ABC, CDE, BD, AE, AG
  lossless: True | lost: none
```

<div class="nb nb-example nb-block" id="example-6-6-3">

<strong>Example 6.6.3</strong> (Reading the chase)

For $\{AB, CD, ACE\}$: rows 1 and 3 agree on $A$, so $A\to B$ copies `a` into row 3’s $B$; rows 2 and 3 agree on $C$, so $C\to D$ fills row 3’s $D$; row 3 already had $ACE$, and is now all `a`: lossless. For $\{AB, CDE\}$ the rows share no column, nothing fires: lossy. For $R(ABC)$ with $A\to B\to C$, $\{AB, AC\}$ is lossless (common $A$ is a key of $AB$) but loses $B\to C$; $\{AC, BC\}$ is lossy (common $C$ determines nothing).

</div>

The dependency-preservation test does not compute $F^+$ (exponential); for each $X\to Y$ it grows $Z=X$ by $(Z\cap R_i)^+\cap R_i$ over the pieces until it stops, and checks $Y\subseteq Z$.

<div class="nb nb-remark" id="algorithm-6-6-4">

<strong>Algorithm 6.6.4</strong> (BCNF decomposition) — While some piece $R_i$ is not in BCNF, take a violating $X\to A$ that holds on $R_i$ and replace $R_i$ by $X^+\cap R_i$ and $(R_i - X^+)\cup X$. Each split is lossless by the binary test (the common part $X$ determines the first piece). Different choices of violation give different results.

</div>

<div class="nb nb-remark" id="algorithm-6-6-5">

<strong>Algorithm 6.6.5</strong> (3NF synthesis (Bernstein)) — Compute a minimal cover; make one table $XA_1\dots A_k$ for each left side $X$ (merging FDs with the same left side); if no table contains a candidate key, add one table that is a key; delete any table contained in another. The result is in 3NF, lossless and dependency preserving.

</div>

In the output, `teach` splits into $CT$ and $ST$, losing $SC\to T$; 3NF synthesis keeps $SCT$ whole, because the FD $SC\to T$ needs all three attributes in one table. For $R(ABCDEG)$, BCNF gives three tables and loses $CD\to E$; synthesis gives five tables ($AG$ is the added key table) and loses nothing.

<div class="nb nb-moral">

Lossless is mandatory, dependency preservation is desirable: aim for BCNF, and fall back to 3NF when BCNF would lose a dependency.

</div>

## 6.7 Multivalued dependencies, 4NF and 5NF {#sec-dbms-4nf}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a course with independent sets of teachers and textbooks.</em>

</div>

<div class="nb nb-definition" id="definition-6-7-1">

<strong>Definition 6.7.1</strong>. A <strong>multivalued dependency</strong> $X\twoheadrightarrow Y$ holds if, for each $X$-value, the set of $Y$-values is independent of the remaining attributes: whenever $(x,y_1,z_1)$ and $(x,y_2,z_2)$ are in $r$, so are $(x,y_1,z_2)$ and $(x,y_2,z_1)$. Every FD is an MVD. $R$ is in <strong>4NF</strong> if for every non-trivial MVD $X\twoheadrightarrow Y$, $X$ is a super key. A <strong>join dependency</strong> says $R$ equals the join of some projections; $R$ is in <strong>5NF</strong> (project-join normal form) if every join dependency is implied by the candidate keys. 4NF $\Rightarrow$ BCNF and 5NF $\Rightarrow$ 4NF.

</div>

```sql {filename="c06-mvd.sql"}
-- course ->> teacher, course ->> book: teachers and books independent
CREATE TABLE ctb (course VARCHAR(6), teacher VARCHAR(8), book VARCHAR(8),
                  PRIMARY KEY (course, teacher, book));
INSERT INTO ctb VALUES
  ('DBMS', 'Rao', 'Korth'), ('DBMS', 'Rao', 'Navathe'),
  ('DBMS', 'Rao', 'Date'), ('DBMS', 'Iyer', 'Korth'),
  ('DBMS', 'Iyer', 'Navathe'), ('DBMS', 'Iyer', 'Date');

-- 4NF decomposition: one table per independent fact
CREATE TABLE ct AS SELECT DISTINCT course, teacher FROM ctb;
CREATE TABLE cb AS SELECT DISTINCT course, book FROM ctb;

-- Q1 2 + 3 rows store what took 6, and the join gives the 6 back exactly
SELECT (SELECT COUNT(*) FROM ct) AS ct_rows,
       (SELECT COUNT(*) FROM cb) AS cb_rows,
       (SELECT COUNT(*) FROM ct NATURAL JOIN cb) AS joined,
       (SELECT COUNT(*) FROM (SELECT course, teacher, book
                              FROM ct NATURAL JOIN cb
                              EXCEPT SELECT * FROM ctb) t) AS spurious;
```

```text {filename="Result on SQLite 3.45.1 and PostgreSQL 16.14 (identical)"}
 ct_rows | cb_rows | joined | spurious
---------+---------+--------+----------
       2 |       3 |      6 |        0
(1 row)
```

The table `ctb` is in BCNF (its only key is all three columns, and there are no non-trivial FDs), yet it stores every teacher once per book: adding a book means adding a row per teacher. The MVD `course` $\twoheadrightarrow$ `teacher` has a non-key left side, so it is not in 4NF; the split into `ct` and `cb` is lossless (a decomposition $\{R_1,R_2\}$ is lossless iff $R_1\cap R_2\twoheadrightarrow R_1$), which the query confirms: the join rebuilds exactly the six rows, with no spurious ones. 5NF problems (a relation that is the join of three projections but not of any two) are rare in practice; know the definition.

<div class="nb nb-moral">

BCNF removes redundancy caused by FDs, 4NF the redundancy caused by independent multivalued facts in one table.

</div>
