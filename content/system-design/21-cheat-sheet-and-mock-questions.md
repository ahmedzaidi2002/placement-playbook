---
title: 21 · Cheat sheet and mock questions
weight: 24
---

This is the last core page (the bonus designs after it are extra practice). It does not teach anything new. Use it three ways: **skim the cheat sheet**
the night before, **pick a mock prompt** and answer it out loud against a timer, and **score yourself**
with the checklist at the end.

## The routine (never skip)

| HLD (45 min) | LLD (45 to 60 min) |
|---|---|
| 1. Requirements and scope (5) | 1. Requirements and scope (5) |
| 2. Estimates (3) | 2. Entities from nouns (5) |
| 3. API (4) | 3. Behaviours from verbs (5) |
| 4. Data model (5) | 4. Relationships, small class diagram (5) |
| 5. High-level design, simple first (10) | 5. Code the core flow (20) |
| 6. Deep dive on 1 or 2 parts (12) | 6. Walk through an example (5) |
| 7. Bottlenecks and trade-offs (5) | 7. Extensions and concurrency (5) |

## HLD cheat sheet

### Numbers
- 1 day ≈ 100,000 seconds → **1 million per day ≈ 12 per second**
- KB → MB → GB → TB → PB: each step ≈ ×1,000
- Peak ≈ **2 to 3 ×** average
- Availability: 99.9% ≈ 8.8 hours down per year, 99.99% ≈ 53 minutes
- Memory ≪ SSD ≪ disk ≪ cross-continent network
- 62⁷ ≈ 3.5 trillion (7-character base62 codes)

### Building blocks: what to reach for

| Problem | Tool | Chapter |
|---|---|---|
| Too much traffic on the app tier | Stateless servers + load balancer | 03 |
| Reads dominate | Cache (cache-aside + TTL), read replicas, CDN | 05, 06 |
| Data or writes exceed one machine | Shard (consistent hashing) | 05 |
| Related data, transactions | SQL | 04 |
| Huge scale, access by key | NoSQL (pick the type) | 04 |
| Slow query | Index | 04 |
| Slow or bursty side work | Queue + workers (at-least-once + idempotency) | 08 |
| Server must push to client | WebSocket | 02, 14 |
| Abuse / overload | Rate limiter (token bucket), 429 | 10, 13 |
| Need correct vs always-available | CP vs AP, quorum R + W > N | 09 |
| Something might fail | Replication, failover, timeouts, retries with backoff + jitter, circuit breaker | 11 |
| Need to know it is broken | Logs, metrics (error rate, p99), traces, alerts | 11 |
| Big files | Object storage + chunks + pre-signed URLs | 17 |
| Celebrity / hot key | Pull for celebrities (hybrid), replicate hot keys | 15, 06 |

### One-line answers to frequent questions

| Question | Answer |
|---|---|
| Scale the database? | Index → cache → read replicas → shard (last) |
| Why stateless servers? | Any server can handle any request, so you can add or remove freely |
| SQL or NoSQL? | Start with SQL. NoSQL where scale or access pattern demands, often both |
| CAP? | Partitions happen, so during one choose consistency or availability. Decide per feature |
| Cache invalidation? | Delete the key on write, TTL as safety net |
| Exactly once? | Hard. Use at-least-once + idempotent consumers |
| Hash-mod-N problem? | Adding a node remaps most keys. Use consistent hashing |
| 301 or 302? | 302 if you need analytics or expiry control |
| Session or JWT? | Session = easy revoke. JWT = stateless, hard to revoke, keep it short-lived |
| Retry safely? | Only idempotent calls, or an idempotency key. Backoff plus jitter |
| Message order? | Per partition or per conversation, using a server-assigned increasing id |
| What if X dies? | Walk the path: redundancy, failover, degrade gracefully |

## LLD cheat sheet

- **Nouns → classes, verbs → methods.** Put each method where its data lives.
- **Composition over inheritance.** Interfaces for things that vary.
- **SOLID:** one reason to change, extend don't modify, substitutable children, small interfaces, depend on abstractions.
- **Patterns to name:** Strategy (swap algorithm), Observer (notify many), Factory (pick the class), Singleton (one instance, with care), Builder (many options), State (behaviour per status).
- **Always mention:** edge cases (full, unknown id, duplicate), complexity, thread safety and where the lock goes, how a new type would be added.
- **Familiar C++ moves:** `unique_ptr` for owned polymorphic objects, `virtual ~Base() = default`, `lock_guard<mutex>`, `list::splice` for LRU, `set` for ordered lookups.

## 20 mock prompts

Set a **45-minute timer**, speak aloud, and draw on paper. After each, look at the **key idea to land**
only after you have finished. Prompts 2, 3 and 4 have full write-ups to compare against:
[web crawler](../22-design-web-crawler), [key-value store](../23-design-key-value-store) and
[search autocomplete](../24-design-search-autocomplete). Prompts 1 and 10 are covered in
chapters [12](../12-design-url-shortener) and [06](../06-caching) plus [05](../05-replication-and-sharding).

### HLD

| # | Prompt | Key idea to land |
|---|---|---|
| 1 | Design a **pastebin** | Text body in object storage, id generation, expiry cleanup, cache for popular pastes. Reads dominate |
| 2 | Design a **web crawler** | A queue of URLs to visit (the frontier), politeness (do not hammer one host), a "seen" set or Bloom filter to avoid repeats, workers partitioned by host, respect `robots.txt` |
| 3 | Design a **key-value store** | Partition with consistent hashing, replicate to N nodes, tunable quorum (R + W > N), explain the CAP trade-off |
| 4 | Design **search autocomplete** | A trie with top suggestions per node, hot prefixes cached, rankings rebuilt offline from query logs |
| 5 | Design a **leaderboard** | A sorted structure in an in-memory store, top-K reads, shard by user or score range, periodic snapshots |
| 6 | Design a **unique ID generator** | Time-ordered ids built from timestamp + machine id + sequence, handle clock issues, no single counter bottleneck |
| 7 | Design a **ride-sharing** matcher | Frequent location updates, a geographic index (grid cells), match the nearest free driver, push updates over WebSocket |
| 8 | Design **video streaming** | Upload → queue → transcode into several qualities → object storage → CDN, adaptive bitrate, metadata DB |
| 9 | Design **ticket booking** | Hold seats with a TTL, atomic reserve in the database, queue or waiting room for spikes, idempotent payment |
| 10 | Design a **distributed cache** | Consistent hashing, eviction, replication for availability, hot key handling, stampede protection |

### LLD (use the C++ style from chapter 20)

| # | Prompt | Key idea to land |
|---|---|---|
| 11 | **Library management** | Library, Book, Member, Loan. Rule: a book is lent to one member at a time, enforced inside `lend` |
| 12 | **Tic-tac-toe** | Board, Player, game status. Check win by tracking row, column and diagonal counts, so a move is O(1) |
| 13 | **ATM** | State (card inserted, PIN verified, ...), transaction as an atomic debit, an interface for the bank backend |
| 14 | **Splitwise** | Users, expenses, balances between pairs. Split strategies (equal, exact, percent) as a Strategy. Simplify debts as an extension |
| 15 | **Logger library** | Levels, multiple sinks (console, file) as an interface, a formatter Strategy, a Singleton or injected logger, thread safety |
| 16 | **Hash map** | Array of buckets, hash function, collision handling (chaining), resize when load factor is high |
| 17 | **Deck of cards** | Card (suit, rank), Deck with shuffle and deal, a game as a class that uses a deck |
| 18 | **Snake and ladder** | Board with jumps in a map, Dice as an interface, Player, turn loop, win condition |
| 19 | **Call center** | Employee levels (fresher, manager, director), escalate a call up the chain, a dispatcher |
| 20 | **Rate limiter class** | Strategy for algorithm (token bucket, sliding window), per-client state in a map, a mutex per bucket |

## Final-days plan

**3 days before**
- Re-read the cheat sheet and the [week 1 revision](../week-1-revision).
- Do two timed HLD mocks (try prompts 1 and 3) and one LLD mock (11).

**2 days before**
- Redo one design from chapters 12 to 17 **without looking**: requirements, estimate, API, data model, diagram.
- Write chapter 20's LRU cache and parking lot from memory.

**The day before**
- One light mock. Read the one-line answers table. Sleep.

**In the room**
- Ask clarifying questions first. Think aloud. Start simple. Name trade-offs. Finish by attacking your own design.

## Self-scoring checklist

After each mock, give yourself **0** (missed), **1** (partly) or **2** (clearly done) on each line.

| # | Did you... | Score |
|---|---|---|
| 1 | Ask clarifying questions and state what you leave out? | |
| 2 | Do a quick estimate and use it to justify a decision? | |
| 3 | Define the API (HLD) or the entities and behaviours (LLD)? | |
| 4 | Start with the simplest working design? | |
| 5 | Give a reason for every box or class you added? | |
| 6 | Go deep on one or two parts instead of staying shallow? | |
| 7 | Mention failure handling (HLD) or edge cases (LLD)? | |
| 8 | Name trade-offs and say why you chose one side? | |
| 9 | Talk through your thinking and keep the interviewer involved? | |
| 10 | Finish by naming bottlenecks, extensions or concurrency? | |

**16 to 20:** interview-ready for this kind of question. **11 to 15:** good, repeat the weak lines.
**Below 11:** re-read the relevant chapters, then redo the same prompt.

## What freshers are *not* expected to know

- Internals of specific products (how a particular database or queue works inside).
- Exact numbers for hardware or cloud pricing.
- Deep distributed-systems theory such as consensus protocols.
- Production experience with scale.

What they **do** expect: a clear routine, sound basic trade-offs, clean code, and honest reasoning. Saying
*"I'm not certain, but I'd reason it like this"* is far better than bluffing.

{{< callout type="info" >}}
**Further reading:** the [System Design Primer](https://github.com/donnemartin/system-design-primer) has worked solutions
for several of these prompts (pastebin, web crawler, key-value store, social feed and more). Attempt each prompt **first**, then compare.
{{< /callout >}}
