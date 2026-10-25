---
title: "11 · NoSQL, CAP and distributed databases"
linkTitle: "11 NoSQL and CAP"
weight: 11
math: true
---
## 11.1 OLTP vs OLAP {#db-11-1}

| | OLTP | OLAP |
|---|---|---|
| Workload | many short reads/writes (orders, payments) | few long analytical queries |
| Design | normalized | denormalized: **star schema** (a fact table + dimension tables) or snowflake |
| Storage | row-oriented | often **column-oriented** (reads few columns of many rows) |
| Example | MySQL, PostgreSQL | data warehouses (Redshift, BigQuery, Snowflake) |

**ETL:** extract from OLTP systems, transform, load into the warehouse.

## 11.2 NoSQL families {#db-11-2}

| Family | Data model | Good for | Examples |
|---|---|---|---|
| **Key-value** | key → opaque value | caching, sessions | Redis, DynamoDB |
| **Document** | key → JSON-like document | flexible schemas, catalogues | MongoDB, Couchbase |
| **Wide-column** | rows with dynamic column families | huge write-heavy data, time series | Cassandra, HBase |
| **Graph** | nodes and edges | relationships: social graphs, recommendations | Neo4j |

**SQL vs NoSQL:** SQL gives a fixed schema, joins, strong ACID transactions and powerful queries; NoSQL gives flexible schemas, easy horizontal scaling and high write throughput, usually with weaker consistency and limited joins. Choose by the data's shape and the consistency you need.

## 11.3 Replication and sharding {#db-11-3}

- **Replication:** copies of the same data on several machines → availability and read scaling. **Leader–follower** (writes go to the leader; followers may lag → stale reads) or multi-leader / leaderless (quorums: with $N$ replicas, $W + R > N$ guarantees a read sees the latest write).
- **Sharding (partitioning):** split data across machines by a **shard key** → write scaling. **Range** sharding (good for range queries, risk of hot spots) or **hash** sharding (even spread, no range queries).
- **Consistent hashing:** keys and servers on a ring; adding or removing a server moves only about $1/n$ of the keys (plain `hash mod n` moves almost all of them).

## 11.4 CAP and consistency {#db-11-4}

<div class="nb nb-theorem nb-block">

<strong>CAP theorem</strong>

When a **network partition** happens, a distributed system must choose between **Consistency** (every read sees the latest write) and **Availability** (every request gets a non-error response). You cannot have both during a partition.

</div>

- **CP** systems refuse some requests during a partition (HBase, MongoDB with majority writes, ZooKeeper).
- **AP** systems keep answering, possibly with stale data (Cassandra, DynamoDB): **eventual consistency**.
- **PACELC:** if Partition, choose A or C; **Else** (normal operation), choose **L**atency or **C**onsistency.
- **BASE** (basically available, soft state, eventually consistent) is the NoSQL counterpart to ACID.

## 11.5 Distributed transactions: two-phase commit {#db-11-5}

A **coordinator** asks every participant to **prepare** (phase 1: each votes yes after making its changes durable, or no). If all vote yes, it sends **commit**, else **abort** (phase 2). Weakness: if the coordinator crashes after participants voted yes, they are **blocked** holding locks until it recovers. (Three-phase commit and consensus protocols like Paxos/Raft address this.)

## 11.6 Practical points {#db-11-6}

- **N+1 query problem:** an ORM fetches a list (1 query) and then each item's related rows (N queries). Fix with a join or eager loading.
- **Connection pooling:** reuse a fixed set of database connections instead of opening one per request.
- **Caching** (Redis) in front of the database for hot reads; invalidate on writes.

<div class="nb nb-moral">

OLTP is normalized and row-oriented; OLAP is star-schema and columnar. Replication scales reads and adds availability; sharding scales writes. Under a partition, pick consistency or availability.

</div>
