---
title: "1 · ER model, relational model and keys"
linkTitle: "1 ER and keys"
weight: 1
math: true
---
## 1.1 Why a DBMS {#db-1-1}

Plain files give: data redundancy and inconsistency, hard ad-hoc queries, no integrity checks, no safe concurrent access, no crash recovery, weak security. A **DBMS** solves these.

- **Schema** = the structure (designed once). **Instance** = the data at a moment.
- **Three-schema architecture:** **external** (user views) → **conceptual/logical** (tables, constraints) → **internal/physical** (files, indexes).
- **Physical data independence:** change storage (add an index) without changing the logical schema. **Logical data independence:** change the logical schema without breaking views/apps (harder).

**SQL statement families:**

| Family | Statements |
|---|---|
| **DDL** (definition) | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME` |
| **DML** (manipulation) | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| **DCL** (control) | `GRANT`, `REVOKE` |
| **TCL** (transaction) | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

<div class="nb nb-remark">

<strong>Trap: DELETE vs TRUNCATE vs DROP</strong> — `DELETE` removes chosen rows (DML, can use `WHERE`, can be rolled back, fires triggers). `TRUNCATE` removes all rows fast (DDL, usually no rollback, structure stays). `DROP` removes the whole table, structure included.

</div>

## 1.2 The ER model {#db-1-2}

- **Entity** (a thing: Student), **entity set** (all students), **attribute** (name, roll no).
- Attribute kinds: **simple vs composite** (name = first + last), **single vs multi-valued** (phone numbers, double oval), **derived** (age from DOB, dashed oval), **key** (underlined).
- **Relationship** (Student *enrols in* Course) with **cardinality** 1:1, 1:N, M:N and **participation**: **total** (every entity must take part, double line) or **partial**.
- **Weak entity:** cannot be identified by its own attributes; depends on an **owner** entity (Dependent of an Employee). Its **partial key** (discriminator) + the owner's key identify it. Always total participation in its identifying relationship.
- **Specialisation/generalisation:** IS-A hierarchies (Employee → Manager, Engineer). **Aggregation:** treating a relationship as an entity so it can take part in another relationship.

## 1.3 ER to tables {#db-1-3}

| ER element | Tables |
|---|---|
| Strong entity | one table, its key is the primary key |
| Weak entity | one table: owner's key + partial key as primary key |
| 1:1 relationship | no new table: put one side's key in the other (prefer the total-participation side) |
| 1:N relationship | no new table: put the **"1" side's key into the "N" side** as a foreign key |
| M:N relationship | **a new table** with both keys (together the primary key) |
| Multi-valued attribute | a new table (entity key + value) |

<div class="nb nb-example">

<strong>Example</strong> (Minimum number of tables)

Two entity sets A and B and a relationship R between them:

- R is **M:N** → **3** tables (A, B, R).
- R is **1:N** → **2** tables (B carries A's key).
- R is **1:1** → **2** tables (or 1 if both sides have total participation and you merge them).

</div>

## 1.4 Relational model and integrity {#db-1-4}

A **relation** is a table: **tuples** = rows, **attributes** = columns, **degree** = number of columns, **cardinality** = number of rows, **domain** = allowed values of a column. Rows are unordered and (in theory) distinct.

**Integrity constraints:** domain, **NOT NULL**, **UNIQUE**, **entity integrity** (a primary key is never NULL), **referential integrity** (a foreign key matches an existing primary key or is NULL; on delete/update: `CASCADE`, `SET NULL`, `RESTRICT`).

## 1.5 Keys {#db-1-5}

| Key | Meaning |
|---|---|
| **Super key** | any set of attributes that uniquely identifies a row |
| **Candidate key** | a **minimal** super key (remove any attribute and it stops being unique) |
| **Primary key** | the candidate key chosen; never NULL |
| **Alternate key** | the other candidate keys |
| **Foreign key** | refers to another table's primary key |
| **Composite key** | a key with more than one attribute |

<div class="nb nb-theorem nb-block">

<strong>Counting super keys</strong> (relation with $n$ attributes)

- One candidate key with $k$ attributes: $2^{\,n-k}$ super keys (any superset).
- Two candidate keys $K_1, K_2$: $2^{\,n-|K_1|} + 2^{\,n-|K_2|} - 2^{\,n-|K_1 \cup K_2|}$ (inclusion–exclusion).

</div>

<div class="nb nb-example">

<strong>Example</strong> (Super keys)

- $R(A, B, C, D)$, candidate key $A$: $2^{3} = $ **8** super keys.
- $R(A, B, C, D)$, candidate keys $A$ and $B$: $8 + 8 - 2^{2} = $ **12**.
- $R(A, B, C, D, E)$, candidate keys $AB$ and $BC$: $2^3 + 2^3 - 2^{5-3} = 8 + 8 - 4 = $ **12** (the 4 removed are supersets of $ABC$, counted twice).

</div>

<div class="nb nb-moral">

M:N needs its own table; 1:N puts the "1" key in the "N" side. A candidate key is a minimal super key; count super keys as $2^{n-k}$ and use inclusion–exclusion for two keys.

</div>
