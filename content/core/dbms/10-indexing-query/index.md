---
title: "10 · Indexing and query processing"
linkTitle: "10 Indexing and queries"
weight: 10
math: true
---
## 10.1 Why the block is what counts {#db-10-1}

Data lives on disk in **blocks** (pages). Reading a block costs far more than any CPU work on it, so query cost is measured in **block transfers**. **Blocking factor** $bfr = \lfloor \text{block size} / \text{record size} \rfloor$ = records per block.

File organisations: **heap** (unordered: insert fast, search = full scan), **sorted** (binary search, inserts expensive), **hashed** (equality lookup in ~1 block, useless for ranges).

## 10.2 Index types {#db-10-2}

| Index | On | Entries |
|---|---|---|
| **Primary** | the ordering key of a sorted file | **sparse**: one per block |
| **Clustering** | the ordering field when it is not a key | one per distinct value |
| **Secondary** | any other field | **dense**: one per record |

- **Dense index:** an entry for every record. **Sparse index:** an entry for some records (one per block); needs the file sorted on that key.
- **Clustered index:** the table's rows are physically stored in index order (only **one** per table; in InnoDB it is the primary key). **Non-clustered:** a separate structure pointing to rows (many allowed).
- **Composite index** on (a, b) helps queries on `a` or on `a AND b`, **not** on `b` alone (leftmost-prefix rule).
- **Covering index:** contains every column the query needs, so the table is never read.
- Indexes speed up reads but **slow down inserts/updates/deletes** and use space. Do not index tiny tables or columns with very few distinct values.

<div class="nb nb-example">

<strong>Example</strong> (Single-level index cost)

30,000 records of 100 B, blocks of 1024 B → $bfr = 10$ → **3,000** data blocks. Binary search on the sorted file: $\lceil \log_2 3000 \rceil = $ **12** block reads. A primary (sparse) index with 15-byte entries: $\lfloor 1024/15 \rfloor = 68$ entries per block, 3,000 entries → $\lceil 3000/68 \rceil = 45$ index blocks; binary search $\lceil \log_2 45 \rceil = 6$, plus 1 data block = **7** reads.

</div>

## 10.3 B-trees and B+ trees {#db-10-3}

A **B+ tree** is a balanced multi-way search tree: all **data pointers are in the leaves**, internal nodes only guide the search, and the leaves are **linked** for fast range scans. Every node (except the root) is at least half full; all leaves are at the same depth. Search, insert and delete are $O(\log_p n)$ block reads, where the fan-out $p$ is in the hundreds, so trees are only 3–4 levels deep.

| | B-tree | B+ tree |
|---|---|---|
| Data pointers | in every node | only in leaves |
| Range queries | awkward | easy (linked leaves) |
| Fan-out | lower (nodes also hold data pointers) | higher |
| Used by | rarely in practice | almost every DBMS index |

**Insertion:** insert into the leaf; if it overflows, **split** it in two and push (copy) the middle key up to the parent; splits can propagate to the root, which is the only way the tree grows taller.

<div class="nb nb-example">

<strong>Example</strong> (B+ tree order and height)

Block 4096 B, key 12 B, pointer 8 B.

- **Internal node** with $p$ child pointers and $p - 1$ keys: $8p + 12(p - 1) \le 4096$ → $p = $ **205**.
- **Leaf** with $k$ (key, record pointer) pairs plus one next-leaf pointer: $20k + 8 \le 4096$ → $k = $ **204**.
- 1,000,000 keys: $\lceil 10^6/204 \rceil = 4902$ leaves → $\lceil 4902/205 \rceil = 24$ internal nodes → 1 root. **3 levels**, so a lookup reads 3 index blocks + 1 data block = **4** reads.

</div>

## 10.4 Hash indexes {#db-10-4}

A hash function maps a key to a **bucket** (block). Equality search ~1 block; no range queries. **Static hashing** suffers overflow chains as the data grows. **Extendible hashing** uses a directory of $2^d$ pointers (**global depth** $d$) that doubles when a bucket with local depth $= d$ overflows; only that bucket splits. **Linear hashing** splits buckets one at a time in a fixed order, with no directory.

## 10.5 Query processing {#db-10-5}

SQL → **parse** → **relational-algebra tree** → **optimise** (choose a plan) → **execute**. See the chosen plan with `EXPLAIN`.

**Heuristic rules:** push selections and projections down (filter early), and do the most selective joins first. **Cost-based optimisation** estimates each plan's cost from table statistics (row counts, distinct values, histograms) and picks the cheapest join order and algorithms.

**Join algorithms** ($b_r$, $b_s$ = blocks of the two tables):

| Algorithm | Approximate block transfers | When |
|---|---|---|
| Nested loop (block), 1 buffer each | $b_r + b_r \cdot b_s$ | small tables; put the **smaller** table outside |
| Block nested loop with $M$ buffers | $b_r + \lceil b_r/(M-2) \rceil \cdot b_s$ | more memory → fewer passes |
| Index nested loop | $b_r + n_r \times$ (index lookup cost) | index on the inner join column |
| Sort-merge join | $b_r + b_s$ (+ sorting cost) | inputs already sorted on the join key |
| Hash join | $\approx 3(b_r + b_s)$ | equi-joins on large unsorted tables |

<div class="nb nb-example">

<strong>Example</strong> (Join cost)

$b_r = 1000$, $b_s = 500$. Block nested loop with $r$ outside: $1000 + 1000 \times 500 = 501{,}000$; with $s$ outside: $500 + 500 \times 1000 = 500{,}500$ (smaller outside is better). With $M = 12$ buffers and $s$ outside: $500 + \lceil 500/10 \rceil \times 1000 = $ **50,500**. Hash join: $3 \times 1500 = $ **4,500**.

</div>

**External merge sort** (data bigger than memory): sort runs that fit in memory, then merge $M - 1$ runs at a time; about $2b(1 + \lceil \log_{M-1}(b/M) \rceil)$ transfers.

<div class="nb nb-moral">

Cost = block transfers. B+ trees keep data in linked leaves and are 3–4 levels deep; compute order from block size, key size and pointer size. Use the smaller table as the outer loop; hash join for big equi-joins.

</div>
