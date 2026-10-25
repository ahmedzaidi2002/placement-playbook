---
title: "8 · Hashing"
linkTitle: "8 Hashing"
weight: 8
math: true
---
## 8.1 The idea {#dsa-8-1}

A **hash table** stores key–value pairs in an array of $m$ buckets; a **hash function** $h(k)$ picks the bucket. A good hash function is fast, deterministic and spreads keys uniformly. Common choices: **division** $h(k) = k \bmod m$ (choose $m$ prime, not a power of 2), multiplication, and polynomial rolling hashes for strings.

Two keys landing in the same bucket is a **collision**; it is unavoidable (pigeonhole), so the table must resolve it.

**Load factor** $\alpha = n/m$ (items per bucket).

## 8.2 Collision resolution {#dsa-8-2}

| Method | Idea | Notes |
|---|---|---|
| **Separate chaining** | each bucket holds a list of its keys | simple; $\alpha$ can exceed 1; expected search $O(1 + \alpha)$ |
| **Linear probing** | try $h, h+1, h+2, \dots$ | cache-friendly; suffers **primary clustering** |
| **Quadratic probing** | try $h + 1^2, h + 2^2, \dots$ | avoids primary clustering; secondary clustering |
| **Double hashing** | try $h_1 + i \cdot h_2(k)$ | best spread; $h_2(k) \ne 0$ |

Open addressing (the last three) needs $\alpha < 1$, and deletions must leave a **tombstone** marker so later searches do not stop early.

<div class="nb nb-example">

<strong>Example</strong> (Inserting with collisions)

Table size $m = 7$, $h(k) = k \bmod 7$. Insert **15, 11, 27, 8, 12**: hashes 1, 4, 6, **1**, 5 (8 collides with 15).

- **Chaining:** bucket 1 holds 15 → 8; buckets 4, 6, 5 hold 11, 27, 12.
- **Linear probing:** 8 finds slot 1 taken → goes to **2**. Table: `[_, 15, 8, _, 11, 12, 27]`.
- **Double hashing** with $h_2(k) = 5 - (k \bmod 5)$: for 8, $h_2 = 5 - 3 = 2$ → try 1 (taken), then $1 + 2 = $ **3**.

</div>

## 8.3 Why hashing is O(1), and when it is not {#dsa-8-3}

With a good hash function and $\alpha$ kept below a constant, the **expected** cost of insert, search and delete is **$O(1)$**: a chain has about $\alpha$ items on average. To keep $\alpha$ bounded the table **rehashes**: when $\alpha$ passes a threshold (Java `HashMap`: 0.75), allocate a table about twice as large and reinsert everything. One rehash is $O(n)$, but doubling makes it **$O(1)$ amortized**.

It is **not** $O(1)$ when:

- many keys collide (bad hash function, or an attacker choosing keys) → $O(n)$ per operation in the worst case; Java 8 turns long chains into balanced trees ($O(\log n)$).
- you need **ordered** operations (min, max, range, sorted iteration): use a balanced BST (`std::map`, `TreeMap`) instead.

## 8.4 Hashing in the standard libraries {#dsa-8-4}

| Need | C++ | Java | Python |
|---|---|---|---|
| Hash map | `unordered_map` | `HashMap` | `dict` |
| Hash set | `unordered_set` | `HashSet` | `set` |
| Ordered map | `map` (red–black) | `TreeMap` | (sorted containers) |

A custom key needs both a hash function and equality that agree (`equals`/`hashCode` in Java).

## 8.5 Related structures {#dsa-8-5}

- **Bloom filter:** a bit array + $k$ hash functions; answers "definitely not present" or "probably present" (**false positives possible, no false negatives**); tiny memory. Used to skip disk lookups.
- **Consistent hashing:** distributes keys over servers so adding a server moves only ~$1/n$ of the keys.
- **Perfect / cuckoo hashing:** worst-case $O(1)$ lookups.

## 8.6 Design: an LRU cache {#dsa-8-6}

**Least recently used** cache with capacity $C$, `get` and `put` both $O(1)$: a **hash map** from key to node + a **doubly linked list** in recency order. `get`: find via the map, move the node to the front. `put`: insert or update at the front; if over capacity, remove the node at the **back** (least recently used) and its map entry.

<div class="nb nb-moral">

Hashing is O(1) on average because a good hash keeps buckets short and rehashing keeps α bounded; it degrades to O(n) under heavy collisions and gives no ordering. LRU cache = hash map + doubly linked list.

</div>
