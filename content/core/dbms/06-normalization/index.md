---
title: "6 · Functional dependencies and normalization"
linkTitle: "6 Normalization"
weight: 6
math: true
---
## 6.1 Why normalize {#db-6-1}

A badly designed table like `Student(roll, name, course, instructor, instructor_phone)` repeats the instructor's phone in every row, which causes **anomalies**:

- **Update anomaly:** the phone changes → many rows to update; miss one and the data is inconsistent.
- **Insertion anomaly:** cannot record a new instructor until some student takes their course.
- **Deletion anomaly:** deleting the last student of a course loses the instructor's phone.

Normalization splits tables to remove these, without losing information.

## 6.2 Functional dependencies and closure {#db-6-2}

<div class="nb nb-definition">

<strong>Definition</strong> — $X \to Y$ (**$X$ functionally determines $Y$**): any two rows that agree on $X$ also agree on $Y$. Example: `roll → name`.

</div>

**Armstrong's axioms:** reflexivity ($Y \subseteq X \Rightarrow X \to Y$), augmentation ($X \to Y \Rightarrow XZ \to YZ$), transitivity ($X \to Y, Y \to Z \Rightarrow X \to Z$). Derived: union, decomposition, pseudo-transitivity.

**Attribute closure** $X^+$: all attributes determined by $X$. Start with $X$; whenever an FD's left side is inside the set, add its right side; repeat until nothing changes. **$X$ is a super key iff $X^+$ contains all attributes.**

<div class="nb nb-example">

<strong>Example</strong> (Closure)

$R(A, B, C, D, E)$, FDs: $A \to B$, $B \to C$, $CD \to E$. $A^+ = \{A, B, C\}$ (not a key). $(AD)^+ = \{A, D, B, C, E\}$ = all → $AD$ is a super key; neither $A^+$ nor $D^+$ is everything, so $AD$ is a **candidate key**.

</div>

## 6.3 Finding candidate keys {#db-6-3}

Shortcut: attributes that appear on **no right-hand side** must be in every key. Start from them, compute the closure, and add attributes one at a time until the closure is everything.

<div class="nb nb-example">

<strong>Example</strong> (Several keys)

$R(A, B, C, D, E)$ with $A \to B$, $BC \to E$, $ED \to A$. $C$ and $D$ are on no right side, so every key contains $CD$; $(CD)^+ = CD$, so add one more: $(ACD)^+$, $(BCD)^+$, $(CDE)^+$ are all everything. Candidate keys: **ACD, BCD, CDE**. Every attribute appears in some key, so every attribute is **prime**.

</div>

**Prime attribute:** part of some candidate key. **Non-prime:** part of none.

**Minimal (canonical) cover:** an equivalent set of FDs with single attributes on the right, no extraneous left-side attributes, and no redundant FDs. Used to design 3NF tables.

## 6.4 The normal forms {#db-6-4}

| Normal form | Condition | Removes |
|---|---|---|
| **1NF** | every value is atomic (no lists or repeating groups) | multi-valued cells |
| **2NF** | 1NF + no **partial dependency**: no non-prime attribute depends on **part** of a candidate key | partial dependencies |
| **3NF** | 2NF + no **transitive dependency**: for every $X \to A$, either $X$ is a super key **or** $A$ is prime | transitive dependencies |
| **BCNF** | for every non-trivial $X \to A$, $X$ is a **super key** | all FD-based redundancy |
| **4NF** | BCNF + no non-trivial multivalued dependency unless its left side is a super key | independent multi-valued facts |
| **5NF** | no non-trivial join dependency | join-decomposition redundancy |

<div class="nb nb-example">

<strong>Example</strong> (Which normal form?)

- `Enroll(S, C, N)`, key $SC$, FD $S \to N$ (name depends on student only): a **partial** dependency → only **1NF**.
- `Emp(E, D, M)`, key $E$, FDs $E \to D$, $D \to M$ (manager depends on department): no partial dependency (single-attribute key) but $D \to M$ is **transitive** → **2NF**, not 3NF.
- $R(A, B, C, D, E)$ from 6.3: every attribute is prime, so it is in **3NF**, but $A \to B$ has $A$ not a super key → **not BCNF**.

</div>

<div class="nb nb-remark">

<strong>Shortcuts</strong> — A relation with only **two attributes** is always in BCNF. If every candidate key is a **single attribute**, the relation is automatically in 2NF. If **all attributes are prime**, it is at least in 3NF.

</div>

## 6.5 Decomposition: lossless and dependency-preserving {#db-6-5}

Splitting $R$ into $R_1, R_2$ must be:

- **Lossless join** (essential): joining them back gives exactly $R$, no spurious rows. **Test:** $R_1 \cap R_2$ must be a super key of $R_1$ or of $R_2$.
- **Dependency preserving** (desirable): every FD can still be checked inside one table.

<div class="nb nb-example">

<strong>Example</strong> (Lossless test)

$R(A, B, C)$ with $B \to C$. Decompose into $(A, B)$ and $(B, C)$: common attribute $B$, and $B \to C$ makes $B$ a key of $(B, C)$ → **lossless**. Decomposing into $(A, C)$ and $(B, C)$: common $C$ is a key of neither → **lossy** (the join can create rows that never existed).

</div>

**3NF vs BCNF:** a **3NF** decomposition that is both lossless and dependency-preserving **always exists**. **BCNF** is always achievable losslessly, but **may lose dependency preservation**. That is the reason 3NF is often the practical target.

## 6.6 Denormalization {#db-6-6}

Deliberately adding redundancy (pre-joined or summary columns) to make reads faster, at the cost of harder updates. Common in reporting/OLAP systems and read-heavy services.

<div class="nb nb-moral">

Compute closures to find keys. 2NF kills partial dependencies, 3NF kills transitive ones (unless the right side is prime), BCNF demands every determinant be a super key. A decomposition is lossless if the common attributes form a key of one side.

</div>
