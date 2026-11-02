---
title: "Normalization and functional dependencies"
weight: 3
---

3 questions asked by DP World, MathWorks, Oracle. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · what normalisation is and why we need it

*Asked by: DP World (Interview rounds)*

What is normalisation, and why do we need it?

{{< details title="Answer and explanation" closed="true" >}}

**Answer.** Normalisation splits tables into smaller ones, guided by functional dependencies, so that every fact is stored once. It removes redundancy and the anomalies it causes:
- **Update anomaly:** a fact stored in many rows; changing only some leaves the data inconsistent.
- **Insertion anomaly:** a fact cannot be stored without an unrelated one.
- **Deletion anomaly:** deleting one fact loses another.

**The normal forms (each stricter).**
- 1NF: every value is atomic (no lists in a cell).
- 2NF: no non-key attribute depends on only part of a candidate key.
- 3NF: no non-key attribute depends on the key through another non-key attribute (no transitive dependency).
- BCNF: the left side of every non-trivial dependency is a super key.

**Concept: the trade-off.** A good decomposition is lossless (joining the parts gives back exactly the original) and ideally preserves dependencies. Normalised schemas need more joins, so read-heavy systems sometimes denormalise on purpose.

{{< /details >}}

### 2 · Q7, 3NF and BCNF

*Asked by: MathWorks (IIIT Delhi 2024)*

Which are TRUE about 3NF and BCNF?

- **(a)** R is in 3NF if every non-prime attribute is fully functionally dependent on every key (text [cut off in the source])
- **(b)** Every relation in 3NF is also in BCNF
- **(c)** Every relation in BCNF is also in 3NF
- **(d)** No relation can be in both BCNF and 3NF

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) every relation in BCNF is also in 3NF**

**Why.** BCNF is stricter than 3NF: every BCNF relation satisfies 3NF, but not the other way round (b is false, d is false). (a) describes 2NF ("fully functionally dependent"), not 3NF.

**Concept: 3NF vs BCNF.** For every dependency X → A: BCNF requires X to be a super key. 3NF also allows A to be a prime attribute (part of some candidate key). That small exception is why 3NF can always preserve dependencies and BCNF sometimes cannot.

{{< /details >}}

### 3 · ACID

*Asked by: Oracle (HackerRank MCQ test)*

Which of the following is not a property of a relational database (transaction)?

- **(a)** Atomicity
- **(b)** Consistency
- **(c)** Isolation
- **(d)** Dependency

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) dependency**

**Why.** The transaction properties are ACID: Atomicity, Consistency, Isolation, Durability. "Dependency" is not one of them.

**Concept: ACID.**
- Atomicity: all of a transaction happens or none of it (rollback on failure).
- Consistency: it takes the database from one valid state to another (constraints hold).
- Isolation: concurrent transactions don't see each other's partial work.
- Durability: once committed, changes survive crashes (write-ahead log).

{{< /details >}}
