---
title: Week 1 revision
weight: 8
---

One page to re-read the night before a mock or an interview. It is only the recaps and the
decisions from chapters 01 to 07. If a line feels fuzzy, open that chapter.

## The routine ([01](../01-how-a-design-interview-works))

Requirements → estimates → API → data model → high-level design → deep dive → bottlenecks.
Ask first. Say what you leave out. Draw the smallest working system, then add parts one at a
time, each with a reason. Finish by attacking your own design.

## Networking ([02](../02-networking-in-one-page))

- Name → IP via **DNS** (cached) → **HTTPS** request → response with a **status code**.
- **GET, PUT, DELETE** are safe to repeat; **POST** is not, so retries need an idempotency key.
- **REST** for public APIs, **RPC** between internal services.
- **TCP** when data must arrive intact, **UDP** when speed beats completeness.
- **Polling** → **long polling** → **WebSocket** as you need more live, two-way updates.
- **Latency** is one request's time. **Throughput** is requests per second. They have different fixes.

## Scaling ([03](../03-scaling-basics))

- Vertical = bigger machine (simple, capped, one failure point). Horizontal = more machines.
- Keep the **app tier stateless**. Push state into the database or cache.
- A **load balancer** spreads traffic, checks health, hides the servers. Make it redundant.
- **L4** is fast and simple. **L7** can route on the request content.
- Start with a **monolith**. Split only for a named reason. The database is the next bottleneck.

## Databases ([04](../04-databases))

- **SQL**: tables, joins, **ACID**. Safe default. **NoSQL** has four kinds: key-value, document, wide-column, graph.
- ACID = all-or-nothing, rules hold, no interference, saved once committed.
- An **index** turns a scan into a lookup. It costs write speed and space. Index what you search and join on.
- **Normalise** first. **Denormalise** specific hot reads.
- Most real systems use more than one kind of database.

## Replication and sharding ([05](../05-replication-and-sharding))

- **Replication**: leader takes writes, followers serve reads. Scales reads and gives failover, not writes.
- Async replication can **lag**, so a read can return old data briefly.
- **Sharding** splits data across machines. The **shard key** decides everything: spread evenly, avoid hot spots.
- Order of escalation: **indexes → cache → replicas → shards**.
- **Consistent hashing**: nodes and keys on a ring, so adding a node moves only a few keys.

## Caching ([06](../06-caching))

- A cache keeps hot data in fast memory. Measure it with **hit ratio**.
- Default: **cache-aside with a TTL**. Know write-through, write-back (can lose data), refresh-ahead.
- Eviction: **LRU** is the default answer.
- Invalidate by deleting the key on write. A TTL is the safety net.
- Failure modes: **stampede, penetration, avalanche, hot key**. A **CDN** is a cache for static files near users.

## Estimation ([07](../07-back-of-envelope-estimation))

- One day ≈ 100,000 seconds, so **1 million per day ≈ 12 per second**.
- Each step in KB → MB → GB → TB → PB is about **×1,000**.
- DAU → requests per day → ÷ 86,400 → QPS → **×2 to 3 for peak**. Size × count × time for storage.
- Latency order: memory ≪ SSD ≪ disk ≪ network across continents.
- State assumptions, round hard, and **end with a design decision**.

## Decisions at a glance

| Situation | Reach for |
|---|---|
| Traffic grows, app tier is the limit | More stateless servers behind a load balancer |
| Reads dominate | Cache, then read replicas, CDN for static files |
| Related data, transactions | SQL |
| Huge scale, access by key | NoSQL (pick the type by access pattern) |
| A query is slow | Check the index first |
| One database cannot hold the writes or the data | Shard, after the cheaper options |
| Need live updates from the server | WebSocket |
| Numbers are tiny | Keep it simple, do not shard |

## Self-test (answer out loud, no peeking)

1. Walk through the 7 steps for "design a pastebin" in under two minutes.
2. Why must app servers be stateless before you add more of them?
3. Explain cache-aside, and what you do when the data changes.
4. Why is hash-mod-N a bad sharding scheme when nodes come and go?
5. 20 million daily users, 10 requests each: what are the average and peak QPS, and what do you conclude?
6. "The database is slow." List your escalation steps in order.
7. SQL or NoSQL for a bookings app, and why?
8. Latency or throughput: your server handles each request in 50 ms but falls over under load?

{{< details title="Answers" >}}

1. Requirements (paste, link, expiry; reads dominate) → estimate (about 12 writes/s) → API (`POST /paste`, `GET /paste/{id}`) → data (`Paste` record, body in blob storage) → simple design (client, server, database) then add a cache → deep dive on id generation → bottlenecks (hot pastes, cleanup, single database).
2. If a server keeps user data in its own memory, the next request must return to that server. Stateless servers keep nothing, so any server can serve any request.
3. Read the cache, on a miss read the database and store the result with a TTL. On a write, update the database and delete the cache key so the next read refills it.
4. Changing N remaps most keys, so most data moves (or a cache loses most entries). Consistent hashing moves only the keys near the changed node.
5. 200M requests per day ÷ 100,000 ≈ 2,000 per second (about 2,300 with 86,400). Peak ≈ 5,000. One database would struggle at that read rate if it is read-heavy, so add a cache and several app servers.
6. Check the index and the query, add a cache, add read replicas, and only then shard.
7. SQL: related data and transactions, so no double booking.
8. Throughput. Each request is fast, but the server cannot take enough at once, so add servers behind a load balancer.

{{< /details >}}
