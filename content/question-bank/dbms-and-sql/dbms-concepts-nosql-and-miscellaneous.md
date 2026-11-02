---
title: "DBMS concepts, NoSQL and miscellaneous"
weight: 2
---

3 questions asked by Oracle. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · when not to use NoSQL

*Asked by: Oracle (HackerRank MCQ test)*

Which of the following design criteria is not valid/suitable for (choosing) non-relational
databases?

- **(a)** Your application requires super-low latency
- **(b)** Your data are unstructured without any relation between them
- **(c)** You only need to serialize and deserialize data (JSON, XML, YAML)
- **(d)** You need to store a very small amount of data

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) you need to store a very small amount of data**

**Why.** The usual reasons to choose NoSQL are very low latency, unstructured or loosely related data, simple storage of serialised objects (JSON, XML), and **massive** data volumes that need horizontal scaling. A tiny dataset is not a reason; any database handles it.

**Concept: SQL vs NoSQL.** Relational databases give schemas, joins and ACID transactions. NoSQL stores (key-value, document, wide-column, graph) relax some of that to gain flexible schemas and easy scaling across many machines.

{{< /details >}}

### 2 · key-value store

*Asked by: Oracle (HackerRank MCQ test)*

Which of the following is a key-value store NoSQL database system?

- **(a)** HBase
- **(b)** MongoDB
- **(c)** Redis
- **(d)** Accumulo

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Redis**

**Why.** Redis stores values under keys (in memory, with optional persistence). HBase and Accumulo are wide-column stores; MongoDB is a document store.

**Concept: NoSQL families.** Key-value (Redis, DynamoDB): get/put by key. Document (MongoDB): JSON-like documents with queries on fields. Wide-column (Cassandra, HBase): rows with dynamic column families. Graph (Neo4j): nodes and edges.

{{< /details >}}

### 3 · Oracle long-term release

*Asked by: Oracle (HackerRank MCQ test)*

What is the latest long-term release of Oracle Database?

- **(a)** 23ai
- **(b)** 22ai
- **(c)** 24ai
- **(d)** 19ai

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 23ai** (at the time of the test, 2024–25)

**Why.** Oracle Database 23ai (first announced as 23c) is the long-term-support release after 19c. There was no 22ai or 24ai, and 19 is named "19c", not "19ai". Check current names before an interview; this changes over time.

**Concept: long-term releases.** Vendors mark some versions for long support (years of patches); companies standardise on those. Oracle's recent LTS line: 12.2 → 19c → 23ai.

{{< /details >}}
