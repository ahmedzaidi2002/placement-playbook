---
title: Week 2 revision
weight: 16
---

One page for chapters 08 to 14. Read it the night before a mock. If a line feels fuzzy, open
that chapter. The week-1 version is [here](../week-1-revision).

## Message queues and async ([08](../08-message-queues-and-async))

- Queues **decouple, buffer and let you scale workers**. The producer drops a message and moves on.
- **Queue** = one consumer per message. **Pub-sub** = every subscriber gets a copy.
- A traditional broker **deletes after ack**. A log-based one **keeps and lets you replay**, scaling by **partitions**.
- Use **at-least-once delivery + idempotent consumers**. Retry with backoff, send repeat failures to a **dead-letter queue**.
- Watch **queue length and lag**. The price is eventual consistency and more to operate.

## CAP and consistency ([09](../09-cap-and-consistency))

- Partitions will happen, so **during a partition: consistency or availability, not both**.
- **CP** refuses to answer when unsure. **AP** answers, possibly stale. Choose by the **cost of being wrong**.
- Models: **strong, eventual, weak**, plus **read-your-writes** and **monotonic reads**.
- **Quorum:** if **R + W > N**, reads overlap the latest write.
- Decide **per feature**: payments lean CP, feeds and counters lean AP.

## API design, auth and rate limiting ([10](../10-api-design-auth-and-rate-limiting))

- REST: **plural nouns**, the method carries the verb, correct **status codes**, **versioned** paths.
- **Paginate every list.** Cursor pagination for big or changing data.
- **401** = not logged in. **403** = logged in but not allowed.
- **Session** = state on the server, easy to revoke. **JWT** = signed token, stateless, hard to revoke, keep it short-lived.
- **API gateway** centralises auth, rate limiting, routing. Rate-limit with **429**.
- Security: **HTTPS, salted slow password hashes, parameterised queries, least privilege**.

## Reliability and observability ([11](../11-reliability-and-observability))

- Each extra nine ≈ **10× less downtime** and much more cost. **Parallel copies raise availability, chains lower it.**
- Find **single points of failure** by walking the request path. Fix each with a copy plus failover.
- **Timeouts everywhere.** Retry only **idempotent** calls, with **backoff and jitter**. **Circuit breaker**: closed → open → half-open.
- Degrade gracefully, shed load, isolate with bulkheads.
- Observe with **logs, metrics, traces**. Watch error rate, **p99 latency**, saturation. Alert on symptoms users feel.

## The three designs

| Design ([chapter](../12-design-url-shortener)) | Lock in these points |
|---|---|
| **URL shortener** (12) | Read-heavy, tiny writes → cache, no sharding at this size. 7-char **base62** (62⁷ ≈ 3.5 trillion). Unique codes from a counter handed out in **blocks**. **302** for analytics and expiry. Analytics via queue |
| **Rate limiter** (13) | Decide key, placement (gateway), algorithm (**token bucket**). Fixed window has the **edge burst**. Lazy refill with `steady_clock` + **mutex**. Across servers: shared Redis, **atomic** increment or script, expiring keys. **429** + `Retry-After`. Fail open or closed |
| **Chat app** (14) | **WebSocket** gateways are stateful, a **session registry** finds a user's gateway. **Store first, then deliver.** At-least-once, dedupe by id. Shard messages by conversation, order by a **server-assigned id**. Offline users **sync from their last message id** |

## Decisions at a glance

| Situation | Reach for |
|---|---|
| Slow or optional side work (email, analytics) | Queue + workers |
| Several services must react to one event | Pub-sub |
| A message may be processed twice | Idempotency key |
| Money, seats, stock must be exact | CP, transactions |
| Likes, feeds, counters | AP, eventual consistency |
| Abuse or overload | Rate limiter (429) |
| A dependency keeps failing | Timeout, backoff, circuit breaker |
| Need real-time push to a client | WebSocket |
| Need unique ids across servers | Block allocation from a coordinator |

## Self-test (answer out loud)

1. Why does a queue make a flash-sale spike survivable?
2. A payment message is delivered twice. How do you stop a double charge?
3. State CAP in one sentence. Which side for a seat-booking app, and why?
4. N = 3, W = 2, R = 2: do reads see the latest write? What if W = 1, R = 1?
5. Why store the chat message **before** delivering it?
6. Why do tokens refill **lazily** in a token bucket, and what protects the state?
7. Two gateways both read the count 99 and let a request through. What is this bug and the fix?
8. Why 302 and not 301 for a shortener that wants click counts?

{{< details title="Answers" >}}

1. The queue buffers the burst, so the service takes work at its own pace instead of crashing, and you can add consumers to drain it.
2. Attach an idempotency key (or message id). The consumer records processed ids and ignores repeats.
3. During a partition you must choose consistency or availability. Seat booking is CP: refusing is better than double-selling a seat.
4. W = 2, R = 2: R + W = 4 > 3, so yes. W = 1, R = 1: R + W = 2 ≤ 3, so reads can be stale.
5. If you delivered first and crashed before storing, the message would be lost. Stored messages can always be re-delivered or synced.
6. It needs no timer: compute tokens earned since the last call, capped at capacity. A mutex makes the read-update-write on the token count atomic.
7. A read-then-write race condition. Use an atomic increment, or run the check and update as one atomic script in the store.
8. A 301 is cached by the browser, so later clicks never reach the server and cannot be counted. A 302 is asked for every time.

{{< /details >}}
