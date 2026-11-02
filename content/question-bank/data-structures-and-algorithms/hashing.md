---
title: "Hashing"
weight: 7
---

5 questions asked by Fujitsu, ION Group, Sigmoid, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · DS Q1, open addressing

*Asked by: Fujitsu (IIT Kharagpur 2023)*

Which data structure is commonly used to implement a hash table with open addressing,
where collisions are resolved by searching for the next available slot in the array?

- **(a)** Linked List
- **(b)** Binary Search Tree
- **(c)** Linear Probing
- **(d)** Quadratic Probing

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) linear probing**

**Why.** "Searching for the next available slot" is linear probing: try h, h + 1, h + 2, ... (mod size). Quadratic probing tries h + 1², h + 2², ...; a linked list is used by separate chaining, the opposite of open addressing. (Strictly the underlying structure is an array; probing is the collision strategy.)

**Concept: open addressing.** All keys live in the array itself. On a collision you probe other slots in a fixed sequence. Linear probing is cache-friendly but forms clusters; quadratic probing and double hashing spread keys out more.

{{< /details >}}

### 2 · Q19, collisions with chaining

*Asked by: ION Group (SDE OA, Jul 2025)*

In a hash table using chaining, what happens if two keys hash to the same slot?

- **(a)** The second key overwrites the first
- **(b)** Both keys are stored in a linked list at that slot
- **(c)** The second key is discarded
- **(d)** The table size is increased automatically

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) both keys are stored in a list at that slot**

**Why.** With separate chaining, each slot holds a list (or another container) of all entries that hash there. Resizing is a separate policy based on the load factor, not a response to one collision.

**Concept: separate chaining.** Search = hash to a bucket, then scan its list. Average cost O(1 + α), where α = n / buckets is the load factor.

{{< /details >}}

### 3 · no value in the first 5 slots

*Asked by: Sigmoid (Campus hiring 2026)*

Five values are inserted into a hash table of size 20 with chaining. If hashing is uniform,
what is the probability that no value is stored in the first 5 slots?

- **(a)** $(15 \cdot 16 \cdot 17 \cdot 18 \cdot 19)/20^5$
- **(b)** $15^5/20^5$
- **(c)** $15^5/(20 \cdot 19 \cdot 18 \cdot 17 \cdot 16)$
- **(d)** $(16 \cdot 17 \cdot 18 \cdot 19 \cdot 20)/20^5$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 15⁵/20⁵**

**Why.** Each value lands in a uniformly random slot independently. Avoiding the first 5 slots has probability 15/20 for each value. With chaining, slots can be reused, so the five factors are all 15/20: (15/20)⁵.

**Concept: independent uniform hashing.** Each key's slot is like a die roll with "number of slots" faces. With chaining, keys do not exclude each other's slots, so probabilities multiply without decreasing (unlike drawing without replacement, which is option (c)).

{{< /details >}}

### 4 · Q14, separate chaining worst case

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

For hashing using separate chaining, what is the worst-case search time?

- **(a)** $O(1)$
- **(b)** $O(\log n)$
- **(c)** $O(n)$
- **(d)** $O(n^2)$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) O(n)**

**Why.** In the worst case every key hashes to the same bucket, forming one chain of n entries, and a search may scan all of it. (Java 8's HashMap turns long chains into trees to get O(log n), but the textbook answer is O(n).)

**Concept: average vs worst case.** Hash tables are O(1) on average with a good hash function and bounded load factor, but O(n) in the worst case. Adversarial inputs can trigger it, which is why some libraries use randomised hashing.

{{< /details >}}

### 5 · Q23, hash table lookup

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

Which of the following does NOT impact how efficiently a lookup operation can be performed
in a hash table?

- **(a)** Number of buckets in the hash table
- **(b)** Quality of the hash function
- **(c)** Number of elements stored in the hash table
- **(d)** Size of elements stored in the hash table

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) the size of the elements stored**

**Why.** Lookup cost depends on the load factor (elements ÷ buckets) and on how evenly the hash function spreads keys. How big each stored value is does not change the number of probes (only, slightly, the cost of hashing and comparing keys).

**Concept: load factor.** α = n / buckets. Tables resize (usually doubling) when α passes a threshold (e.g. 0.75) to keep chains short.

{{< /details >}}
