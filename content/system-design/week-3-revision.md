---
title: Week 3 revision
weight: 23
---

One page for chapters 15 to 20 (more designs and LLD). Earlier weeks:
[week 1](../week-1-revision) and [week 2](../week-2-revision). The final one-pager for all
chapters is the [cheat sheet](../21-cheat-sheet-and-mock-questions).

## HLD designs

| Design | Lock in these points |
|---|---|
| **News feed** ([15](../15-design-news-feed)) | Reads dominate, so **precompute feeds** (fan-out on write) as per-user lists of post ids. Pure push breaks for celebrities, so **hybrid**: push for normal users, **pull and merge** for celebrities. Fan-out is async via a queue, skip inactive users. **Cursor** pagination. Eventual consistency |
| **Notification system** ([16](../16-design-notification-system)) | API returns **202**, then dedupe → preferences → rate limit → template → **queue** → workers → provider. Separate queues by **priority and channel** (OTP must not wait behind marketing). At-least-once + dedupe key. Retry with backoff, dead-letter, **never retry permanent failures** (bad token) |
| **File storage** ([17](../17-design-file-storage)) | **Chunks with hashes**: resume, delta sync, dedupe, parallel upload. **Metadata in a DB, bytes in object storage.** Upload **directly** with pre-signed URLs, then **commit** atomically. Sync with a **change log + cursor** and a notification. Conflict = **keep both**. Delete a chunk only when `refCount` is zero |

## LLD

- **Routine:** requirements → entities (nouns) → behaviours (verbs) → relationships → small class diagram → code the core → walk an example, then extensions and concurrency.
- **Relationships:** association, aggregation (parts live on their own), composition (part dies with the whole), inheritance. **Prefer composition.**
- **SOLID:** one reason to change, extend don't modify, substitutable children, small interfaces, depend on abstractions.
- **Patterns:** **Strategy** swaps an algorithm. **Observer** notifies many. **Factory** picks the class. **Singleton** one instance (global state, use with care). **Builder** assembles step by step. **State** replaces status `if`s with objects.

## The five LLD designs ([20](../20-lld-designs))

| Design | Core idea | Complexity |
|---|---|---|
| **LRU cache** | Doubly linked list + hash map of **iterators**, `splice` to the front | O(1) get and put |
| **Parking lot** | **Smallest fitting spot**, pricing as a **Strategy**, ticket stores entry time | `park` O(S) (improve with per-size free sets), `leave` O(1) |
| **Elevator** | Ordered `set` of stops, keep direction, **reverse only when nothing is ahead** | O(log n) per step |
| **Vending machine** | State-checked operations, a failed selection **never swallows money** | O(1) |
| **Seat booking** | Hold **all or none** under one lock, holds **expire**, only the same user confirms. Distributed version: atomic set-if-free | O(S + k) here |

## Decisions at a glance

| You see in the problem... | Think |
|---|---|
| Celebrity or hot key | Pull for the few, push for the many |
| Slow third-party calls, bursts | Queue, priority lanes, retries, dead-letter |
| Huge files | Chunks, object storage, direct upload |
| "Different pricing / payment / sorting" | Strategy |
| "Notify A, B and C when X" | Observer |
| "Behaves differently by status" | State |
| "Two users must not get the same thing" | One lock around check-and-update (or atomic compare-and-set across servers) |

## Self-test (answer out loud)

1. Why does fan-out on write break for a user with 10 million followers, and what is the fix?
2. Why separate notification queues by priority?
3. How does a file upload avoid sending bytes that already exist?
4. What does `splice` give the LRU cache that makes the iterator map safe?
5. Which pattern removes a long `if (paymentType == ...)` chain?
6. Why must the seat hold check and update happen under the **same** lock?
7. The elevator is at floor 2 going up with stops at 1 and 3. What is served first?
8. When does a vending machine need State **classes** instead of an enum?

{{< details title="Answers" >}}

1. One post means 10 million feed writes. Use a hybrid: do not fan out for celebrities, and merge their recent posts into each follower's feed at read time.
2. So a large low-priority blast cannot delay a time-critical message such as an OTP.
3. The client sends chunk hashes first. The server replies with only the missing chunks, and the client uploads just those.
4. `splice` relinks a node inside the list without invalidating iterators, so the stored iterators stay valid.
5. Strategy: each payment type becomes a class behind one interface.
6. Otherwise two threads could both see the seat free and both mark it held, giving one seat to two users.
7. Floor 3. It continues in the direction of travel, then turns around and serves floor 1.
8. When per-state behaviour grows (more states, each with different rules). With two or three simple states an enum is fine.

{{< /details >}}
