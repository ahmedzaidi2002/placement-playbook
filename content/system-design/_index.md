---
title: System Design
weight: 2
cascade:
  type: docs
---

A from-zero track for fresher (SDE-1) interviews. Those interviews are mostly **LLD**
(class and object design) plus one **light HLD** round (URL shortener, chat, rate limiter),
so that is where the time goes.

Every page follows the same shape: why it matters in an interview, the idea from scratch,
a diagram, trade-offs, what to say out loud, a few check-yourself questions, and a five-line recap.

{{< callout type="info" >}}
These are teaching notes, not candidate accounts, so the "Reported / Editor's note" split used
on the company pages does not apply here. Numbers are the standard **rules of thumb** used in
interviews, and they are labelled as such. Real company internals are not claimed.
{{< /callout >}}

## Week 1: Foundations

{{< cards >}}
  {{< card link="01-how-a-design-interview-works" title="01 · How a design interview works" subtitle="The 7-step framework you will reuse in every question." icon="map" >}}
  {{< card link="02-networking-in-one-page" title="02 · Networking in one page" subtitle="DNS, HTTP, REST vs RPC, TCP vs UDP, WebSocket, latency vs throughput." icon="globe-alt" >}}
  {{< card link="03-scaling-basics" title="03 · Scaling basics" subtitle="Vertical vs horizontal, stateless servers, load balancers, reverse proxy, monolith vs microservices." icon="arrows-expand" >}}
  {{< card link="04-databases" title="04 · Databases" subtitle="SQL vs NoSQL, ACID, the four NoSQL types, indexes, normalisation." icon="database" >}}
  {{< card link="05-replication-and-sharding" title="05 · Replication and sharding" subtitle="Leader/follower, replication lag, shard keys, hot spots, consistent hashing, federation." icon="duplicate" >}}
  {{< card link="06-caching" title="06 · Caching" subtitle="Cache-aside and friends, eviction, invalidation, CDN, stampede and other failure modes." icon="lightning-bolt" >}}
  {{< card link="07-back-of-envelope-estimation" title="07 · Back-of-envelope estimation" subtitle="QPS, storage, bandwidth, the numbers to memorise, and three worked examples." icon="calculator" >}}
  {{< card link="week-1-revision" title="Week 1 revision" subtitle="One page of recaps, decisions and a self-test for chapters 01 to 07." icon="refresh" >}}
{{< /cards >}}

## Week 2: Building blocks and the first designs

{{< cards >}}
  {{< card link="08-message-queues-and-async" title="08 · Message queues and async" subtitle="Queue vs pub-sub, Kafka-style log vs RabbitMQ-style broker, delivery guarantees, idempotency, dead-letter queues." icon="mail" >}}
  {{< card link="09-cap-and-consistency" title="09 · CAP and consistency" subtitle="CP vs AP, strong vs eventual, read-your-writes, quorum (R + W > N)." icon="scale" >}}
  {{< card link="10-api-design-auth-and-rate-limiting" title="10 · API design, auth and rate limiting" subtitle="REST conventions, pagination, sessions vs JWT, API gateway, security basics." icon="key" >}}
  {{< card link="11-reliability-and-observability" title="11 · Reliability and observability" subtitle="Nines, failover, timeouts, retries, circuit breakers, logs, metrics and traces." icon="shield-check" >}}
  {{< card link="12-design-url-shortener" title="12 · Design a URL shortener" subtitle="Full 7-step walkthrough: base62 codes, key blocks, 301 vs 302, cache." icon="link" >}}
  {{< card link="13-design-rate-limiter" title="13 · Design a rate limiter" subtitle="Fixed and sliding windows, token bucket in C++, Redis counters, fail open vs closed." icon="clock" >}}
  {{< card link="14-design-chat-app" title="14 · Design a chat app" subtitle="WebSocket gateways, session registry, ordering, offline sync, delivery status." icon="chat" >}}
  {{< card link="week-2-revision" title="Week 2 revision" subtitle="Recaps, decisions and a self-test for chapters 08 to 14." icon="refresh" >}}
{{< /cards >}}

## Week 3: More designs, LLD and interview readiness

{{< cards >}}
  {{< card link="15-design-news-feed" title="15 · Design a news feed" subtitle="Fan-out on write vs read, the celebrity problem, hybrid feeds, cursor pagination." icon="rss" >}}
  {{< card link="16-design-notification-system" title="16 · Design a notification system" subtitle="Priority queues, retries, dedupe, preferences, provider limits." icon="bell" >}}
  {{< card link="17-design-file-storage" title="17 · Design file storage" subtitle="Chunking, dedupe, metadata vs object storage, pre-signed uploads, sync and conflicts." icon="folder" >}}
  {{< card link="18-lld-basics" title="18 · LLD basics" subtitle="The 7-step LLD routine, OOP pillars, relationships, SOLID with C++ snippets." icon="cube" >}}
  {{< card link="19-design-patterns" title="19 · Design patterns that get asked" subtitle="Strategy, Observer, Factory, Singleton, Builder, State in C++17." icon="puzzle" >}}
  {{< card link="20-lld-designs" title="20 · LLD designs in C++" subtitle="LRU cache, parking lot, elevator, vending machine, seat booking. All compiled and run." icon="code" >}}
  {{< card link="week-3-revision" title="Week 3 revision" subtitle="Recaps, the five LLD designs at a glance, and a self-test for chapters 15 to 20." icon="refresh" >}}
  {{< card link="21-cheat-sheet-and-mock-questions" title="21 · Cheat sheet and mock questions" subtitle="One-page revision, 20 mock prompts with the key idea, final-days plan, self-scoring checklist." icon="clipboard-check" >}}
{{< /cards >}}

## Bonus designs

Three more full walkthroughs for the most common extra prompts. Do these after the three weeks, or
earlier if an interview is close.

{{< cards >}}
  {{< card link="22-design-web-crawler" title="22 · Design a web crawler" subtitle="BFS over the web, URL frontier with priority and politeness, dedupe with a Bloom filter, spider traps." icon="search" >}}
  {{< card link="23-design-key-value-store" title="23 · Design a key-value store" subtitle="Log + memtable, consistent hashing, N replicas and quorums, gossip, Merkle trees, conflicts." icon="database" >}}
  {{< card link="24-design-search-autocomplete" title="24 · Design search autocomplete" subtitle="Trie with top-K per node in C++, read path vs offline build path, sharding by prefix." icon="search-circle" >}}
{{< /cards >}}

That is the full track: 21 chapters over three weeks, three revision pages, and three bonus designs.
