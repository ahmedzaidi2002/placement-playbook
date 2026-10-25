---
title: "9 · Hashing, and why it is O(1)"
linkTitle: "9 Hashing, and why it is O(1)"
weight: 9
math: true
---
“Why is a hash-table lookup $O(1)$?” is asked in almost every SDE interview, and the expected answer is not “because of the hash function”. It is a precise statement with four assumptions, and an interviewer will probe each one. This chapter builds up to that statement ([Section 9.6](#sec-dsa-whyo1)) and then shows what breaks when an assumption fails.

## 9.1 From direct addressing to hashing {#sec-dsa-hashidea}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> storing roll numbers $0..999$: an array of $1000$ cells answers “is $x$ present?” in one step.</em>

</div>

<div class="nb nb-definition" id="definition-9-1-1">

<strong>Definition 9.1.1</strong>. <strong>Direct addressing</strong> stores key $k$ in cell $k$ of an array: $\Theta(1)$ for everything, but it needs one cell per <em>possible</em> key, impossible for 64-bit integers or strings. A <strong>hash table</strong> uses an array of $m$ <strong>buckets</strong> (slots) and a <strong>hash function</strong> $h \colon U \to \{0, \ldots, m-1\}$ that maps the huge universe $U$ of keys to bucket indices. Key $k$ lives in bucket $h(k)$. Two keys with $h(k_1) = h(k_2)$ <strong>collide</strong>. With $n$ stored keys, the <strong>load factor</strong> is $\alpha = n/m$.

</div>

<div class="nb nb-definition" id="fact-9-1-2">

<strong>Fact 9.1.2</strong> (Collisions are unavoidable). Since $|U| > m$, some bucket receives many keys of $U$ (pigeonhole), so an adversary who knows $h$ can make every key collide. Even random keys collide early: by the <strong>birthday paradox</strong>, $n$ keys thrown uniformly into $m$ buckets produce a collision with probability about $1 - e^{-n^2/(2m)}$, which is $50\%$ already at $n \approx 1.18\sqrt m$ ($23$ people, $365$ birthdays). So a hash table must <em>resolve</em> collisions, not avoid them.

</div>

## 9.2 Hash functions {#sec-dsa-hashfn}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `h(k) = k mod 11` for integer keys.</em>

</div>

A good hash function is deterministic, fast ($O(1)$ for fixed-size keys, $O(L)$ for a key of length $L$), and spreads the keys that actually occur uniformly over the buckets.

<div class="nb nb-definition" id="definition-9-2-1">

<strong>Definition 9.2.1</strong> (Classic families).

- <strong>Division method</strong>: $h(k) = k \bmod m$. Choose $m$ prime and not close to a power of $2$: with $m = 2^p$ only the low $p$ bits of the key matter, and keys that share them (all multiples of $8$, say) collide.
- <strong>Multiplication method</strong>: $h(k) = \lfloor m \cdot \operatorname{frac}(kA) \rfloor$ with a constant $0 < A < 1$, Knuth suggests $A \approx (\sqrt5 - 1)/2 \approx 0.618$. Here $m$ can be a power of $2$, and the computation is a multiply and a shift.
- <strong>Universal hashing</strong>: pick $h$ at random, when the table is created, from a family $\mathcal H$ such that for any two distinct keys $\Pr_{h \in \mathcal H}[h(x) = h(y)] \le 1/m$. Example for integer keys: $h_{a,b}(k) = ((ak + b) \bmod p) \bmod m$ with a prime $p > |U|$ and random $1 \le a < p$, $0 \le b < p$.
- <strong>Strings</strong>: polynomial hashing $h(s) = \big(\sum_i s_i\, x^{L-1-i}\big) \bmod m$ computed by Horner’s rule; Java’s `String.hashCode` is this with $x = 31$ and arithmetic modulo $2^{32}$. Every character must influence the result: hashing only the first few characters makes all URLs of one website collide.
- <strong>Composite keys</strong> (pairs, tuples, objects): combine the field hashes in an order-dependent way, e.g. $h = 31h + h(\text{field})$. Equal objects must have equal hashes; in Java, overriding `equals` without `hashCode` breaks `HashMap`.

</div>

<div class="nb nb-remark" id="remark-9-2-2">

<strong>Remark 9.2.2</strong> (Cryptographic hashes are a different tool) — SHA-256 and similar functions are designed so that collisions are infeasible to <em>find</em>, not merely rare. They are much slower and are used for integrity and passwords, not for table indexing. Hash tables use fast non-cryptographic hashes, with a random seed when inputs may be hostile ([Section 9.6.i](#sec-dsa-hashflood)).

</div>

## 9.3 Separate chaining {#sec-dsa-chaining}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> each bucket is a linked list of the keys that hash to it.</em>

</div>

<div class="nb nb-definition" id="definition-9-3-1">

<strong>Definition 9.3.1</strong>. In <strong>separate chaining</strong> each bucket holds a list (or a small dynamic array) of its keys. Insert: add to the bucket’s list ($O(1)$, plus a scan if duplicates must be rejected). Search and delete: scan the list of bucket $h(k)$.

</div>

The program of the next section inserts `22 1 13 11 24 33 18 42 31` into $m = 11$ buckets with $h(k) = k \bmod 11$; the last part of its output shows the chains (new keys at the head). Three keys share bucket $0$: with $n = 9$ and $m = 11$, $\alpha \approx 0.82$ and a chain of three is entirely typical.

<div class="nb nb-theorem nb-block" id="theorem-9-3-2">

<strong>Theorem 9.3.2</strong> (Cost of chaining under simple uniform hashing)

Assume <strong>simple uniform hashing</strong>: each key is equally likely to hash to any of the $m$ buckets, independently of the others. Then

- the expected length of every chain is $\alpha = n/m$;
- an unsuccessful search examines $\alpha$ keys on average, $\Theta(1 + \alpha)$ time including computing the hash;
- a successful search examines $1 + \alpha/2 - \alpha/(2n)$ keys on average, also $\Theta(1 + \alpha)$.

The same bounds hold for <em>every</em> fixed set of keys if $h$ is drawn from a universal family.

</div>

<div class="nb nb-proof">

<em>Sketch.</em> A miss scans one whole chain, of expected length $n/m$. For a hit on the $i$-th inserted key (new keys at the head), we scan it plus the keys inserted after it into the same bucket, of which there are $(n - i)/m$ in expectation; averaging over $i$ gives $1 + (n-1)/(2m)$.

</div>

## 9.4 Open addressing {#sec-dsa-openaddr}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a car park with no assigned spaces: if your spot is taken, try the next one.</em>

</div>

<div class="nb nb-definition" id="definition-9-4-1">

<strong>Definition 9.4.1</strong>. In <strong>open addressing</strong> all keys live in the array itself, so $\alpha \le 1$. A key $k$ has a <strong>probe sequence</strong> $h(k, 0), h(k, 1), \ldots$; insertion takes the first empty slot, and a search follows the same sequence until it finds $k$ or an empty slot.

- <strong>Linear probing</strong>: $h(k, i) = (h'(k) + i) \bmod m$.
- <strong>Quadratic probing</strong>: $h(k, i) = (h'(k) + c_1 i + c_2 i^2) \bmod m$; below $c_1 = 0$, $c_2 = 1$.
- <strong>Double hashing</strong>: $h(k, i) = (h_1(k) + i\,h_2(k)) \bmod m$, where $h_2(k)$ is never $0$ and is coprime to $m$ (e.g. $m$ prime).

</div>

The same nine keys, $m = 11$, $h'(k) = h_1(k) = k \bmod 11$ and $h_2(k) = 7 - (k \bmod 7)$:

```cpp {filename="hashprobe.cpp, lines 5–31"}
const int M = 11;
const int keys[] = {22, 1, 13, 11, 24, 33, 18, 42, 31};

int h1(int k) { return k % M; }
int h2(int k) { return 7 - k % 7; }                      // never 0

// probe(k, i) = the i-th slot tried for key k
int linear(int k, int i) { return (h1(k) + i) % M; }
int quadratic(int k, int i) { return (h1(k) + i * i) % M; }
int doubleh(int k, int i) { return (h1(k) + i * h2(k)) % M; }

void run(const char* name, int (*probe)(int, int)) {
    std::vector<int> t(M, -1);
    int total = 0;
    std::printf("%s\n", name);
    for (int k : keys) {
        int i = 0;
        while (i < M && t[probe(k, i)] != -1) ++i;
        if (i == M) { std::printf("  %2d: no free slot found\n", k); continue; }
        t[probe(k, i)] = k;
        total += i + 1;
        std::printf("  %2d: home %2d, %d probe%s -> slot %2d\n", k, h1(k), i + 1, i ? "s" : "", probe(k, i));
    }
    std::printf("  table:");
    for (int s = 0; s < M; ++s) t[s] < 0 ? std::printf("  -") : std::printf(" %2d", t[s]);
    std::printf("\n  total probes = %d\n", total);
}
```

```text {filename="Output of hashprobe.cpp"}
linear probing   h(k,i) = (k + i) mod 11
  22: home  0, 1 probe -> slot  0
   1: home  1, 1 probe -> slot  1
  13: home  2, 1 probe -> slot  2
  11: home  0, 4 probes -> slot  3
  24: home  2, 3 probes -> slot  4
  33: home  0, 6 probes -> slot  5
  18: home  7, 1 probe -> slot  7
  42: home  9, 1 probe -> slot  9
  31: home  9, 2 probes -> slot 10
  table: 22  1 13 11 24 33  - 18  - 42 31
  total probes = 20
quadratic probing h(k,i) = (k + i^2) mod 11
  22: home  0, 1 probe -> slot  0
   1: home  1, 1 probe -> slot  1
  13: home  2, 1 probe -> slot  2
  11: home  0, 3 probes -> slot  4
  24: home  2, 2 probes -> slot  3
  33: home  0, 4 probes -> slot  9
  18: home  7, 1 probe -> slot  7
  42: home  9, 2 probes -> slot 10
  31: no free slot found
  table: 22  1 13 24 11  -  - 18  - 33 42
  total probes = 15
double hashing   h(k,i) = (k + i(7 - k mod 7)) mod 11
  22: home  0, 1 probe -> slot  0
   1: home  1, 1 probe -> slot  1
  13: home  2, 1 probe -> slot  2
  11: home  0, 2 probes -> slot  3
  24: home  2, 2 probes -> slot  6
  33: home  0, 3 probes -> slot  4
  18: home  7, 1 probe -> slot  7
  42: home  9, 1 probe -> slot  9
  31: home  9, 4 probes -> slot 10
  table: 22  1 13 11 33  - 24 18  - 42 31
  total probes = 16
chaining (insert at head)
  [ 0] -> 33 -> 11 -> 22
  [ 1] -> 1
  [ 2] -> 24 -> 13
  [ 7] -> 18
  [ 9] -> 31 -> 42
```

<div class="nb nb-example nb-block" id="example-9-4-2">

<strong>Example 9.4.2</strong> (Reading the three tables)

- <em>Linear probing</em>: $11$ and $33$ hash to $0$ like $22$, and $24$ to $2$ like $13$; they pile into one run `0..5`. Inserting $33$ needs $6$ probes because it has to walk past keys that belong to <em>other</em> home slots. This is <strong>primary clustering</strong>: a run grows by absorbing neighbouring runs, and the probability of landing in it grows with its length.
- <em>Quadratic probing</em> jumps by $1, 4, 9, 16, \ldots$, so neighbouring runs do not merge. Keys with the same home still follow the same sequence (<strong>secondary clustering</strong>). And with $8$ of $11$ slots full, the probes for $31$ ($9, 10, 2, 7, 3, 1, 1, 3, 7, 2, 10$) never reach the free slots $5$, $6$ and $8$: quadratic probing visits only about half of the slots of a prime table, which is why it is only guaranteed to succeed while $\alpha \le 1/2$.
- <em>Double hashing</em> gives keys with the same home different step sizes, so it behaves almost like an ideal random probe sequence. It inserted all nine keys in $16$ probes.

</div>

<div class="nb nb-theorem nb-block" id="theorem-9-4-3">

<strong>Theorem 9.4.3</strong> (Expected probes in open addressing)

Under <strong>uniform hashing</strong> (every probe sequence is a uniformly random permutation of the slots), with load factor $\alpha < 1$:

$$
\text{unsuccessful search / insert} \le \frac{1}{1 - \alpha}, \qquad
	\text{successful search} \le \frac{1}{\alpha}\ln \frac{1}{1-\alpha}.
$$

For linear probing (Knuth’s analysis) the expected numbers are about $\frac12\big(1 + \frac{1}{(1-\alpha)^2}\big)$ unsuccessful and $\frac12\big(1 + \frac{1}{1-\alpha}\big)$ successful.

</div>

<div class="nb nb-proof">

<em>Idea for $1/(1-\alpha)$.</em> Each probe of a miss hits an occupied slot with probability at most $\alpha$, so the number of probes is dominated by a geometric variable: $1 + \alpha + \alpha^2 + \cdots = 1/(1 - \alpha)$.

</div>

The program `hashsim.cpp` checks these formulas on a table of $1{,}000{,}003$ slots filled with random keys (measured value first, formula in parentheses):

```text {filename="Output of hashsim.cpp"}
alpha| chaining hit/miss     | linear probing hit/miss| double hash hit/miss  
     | measured  (formula)   | measured  (formula)   | measured  (formula)   
 0.50|1.25/ 0.50 (1.25/ 0.50)|1.50/ 2.52 (1.50/ 2.50)|1.39/ 2.00 (1.39/ 2.00)
 0.75|1.38/ 0.75 (1.38/ 0.75)|2.50/ 8.51 (2.50/ 8.50)|1.85/ 4.01 (1.85/ 4.00)
 0.90|1.45/ 0.90 (1.45/ 0.90)|5.54/49.75 (5.50/50.50)|2.56/ 9.97 (2.56/10.00)
```

<div class="nb nb-remark" id="remark-9-4-4">

<strong>Remark 9.4.4</strong> (What the numbers say) — Chaining degrades gracefully: even at $\alpha = 0.9$ a hit looks at $1.45$ keys. Linear probing is fine at $\alpha = 0.5$ but a miss costs about $50$ probes at $\alpha = 0.9$; that is why linear-probing tables resize at $\alpha$ around $0.5$ to $0.75$. Linear probing still wins in practice at moderate load because its probes are consecutive memory (one cache line), which is why many modern tables (Google’s Swiss tables, Rust’s `HashMap`) use open addressing.

</div>

<div class="nb nb-remark" id="remark-9-4-5">

<strong>Remark 9.4.5</strong> (Deleting in open addressing) — Emptying a slot breaks the probe sequences of keys inserted after it: a later search would stop at the hole. Deletion marks the slot with a <strong>tombstone</strong> that searches skip and inserts may reuse; tombstones count towards the load and are cleared by rehashing. Linear probing can instead shift later keys back (backward-shift deletion). Chaining simply unlinks the node.

</div>

|  | Separate chaining | Open addressing |
|:--|:--|:--|
| Load factor | any $\alpha$, typically $\le 1$ | must stay $< 1$, typically $\le 0.5$–$0.75$ |
| Degradation as $\alpha \to 1$ | linear in $\alpha$ | like $1/(1-\alpha)$ or worse |
| Memory | a pointer per key, one allocation per node | no pointers, but empty slots |
| Cache behaviour | pointer chasing | excellent with linear probing |
| Deletion | easy | tombstones |
| Clustering | none | primary (linear), secondary (quadratic) |
| Used by | C++ `unordered_map`, Java `HashMap` | Python `dict`, Rust, Go (since 1.24), Swiss tables |

<div class="nb-caption" id="table-9-1">

<strong>Table 9.1.</strong> Chaining versus open addressing.

</div>

## 9.5 Rehashing {#sec-dsa-rehash}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a table that doubles when $\alpha$ passes $1$, like a dynamic array.</em>

</div>

<div class="nb nb-definition" id="definition-9-5-1">

<strong>Definition 9.5.1</strong>. When the load factor exceeds a threshold (`max_load_factor`), the table allocates about twice as many buckets and <strong>rehashes</strong>: re-inserts every key, since $h(k) \bmod m$ changes with $m$. That costs $\Theta(n)$.

</div>

```cpp {filename="buckets.cpp"}
// How std::unordered_map grows: bucket count after each rehash, and the load factor limit.
#include <cstdio>
#include <unordered_map>

int main() {
    std::unordered_map<int, int> m;
    std::printf("max_load_factor = %.1f\n", m.max_load_factor());
    std::size_t last = m.bucket_count();
    std::printf("size %5u: %5u buckets\n", 0u, (unsigned)last);
    for (int i = 1; i <= 5000; ++i) {
        m[i] = i;
        if (m.bucket_count() != last) {
            last = m.bucket_count();
            std::printf("size %5u: %5u buckets (load factor now %.2f)\n", (unsigned)m.size(), (unsigned)last, m.load_factor());
        }
    }
    // Bloom filter: false-positive rate (1 - e^{-kn/m})^k for m/n = 10 bits per key.
    std::printf("Bloom filter, 10 bits per key:\n");
    for (int k = 1; k <= 10; ++k) {
        double p = 1;
        double x = 1 - __builtin_exp(-k / 10.0);
        for (int t = 0; t < k; ++t) p *= x;
        std::printf("  k = %2d hashes: false positives %.4f\n", k, p);
    }
}
```

```text {filename="Output of buckets.cpp"}
max_load_factor = 1.0
size     0:     1 buckets
size     1:     2 buckets (load factor now 0.50)
size     2:     5 buckets (load factor now 0.40)
size     5:    11 buckets (load factor now 0.45)
size    11:    23 buckets (load factor now 0.48)
size    23:    47 buckets (load factor now 0.49)
size    47:    97 buckets (load factor now 0.48)
size    97:   199 buckets (load factor now 0.49)
size   199:   409 buckets (load factor now 0.49)
size   409:   823 buckets (load factor now 0.50)
size   823:  1741 buckets (load factor now 0.47)
size  1741:  3739 buckets (load factor now 0.47)
size  3739:  7517 buckets (load factor now 0.50)
Bloom filter, 10 bits per key:
  k =  1 hashes: false positives 0.0952
  k =  2 hashes: false positives 0.0329
  k =  3 hashes: false positives 0.0174
  k =  4 hashes: false positives 0.0118
  k =  5 hashes: false positives 0.0094
  k =  6 hashes: false positives 0.0084
  k =  7 hashes: false positives 0.0082
  k =  8 hashes: false positives 0.0085
  k =  9 hashes: false positives 0.0091
  k = 10 hashes: false positives 0.0102
```

This libstdc++ `unordered_map` keeps $\alpha \le 1$ and grows to the next prime above roughly twice the bucket count ($1, 2, 5, 11, 23, 47, 97, \ldots$). Right after a rehash the load factor is about $0.5$. The analysis is exactly the dynamic array’s ([Section 1.4](../01-complexity/#sec-dsa-amortized)): between two rehashes the table receives as many inserts as it had keys, so the $\Theta(n)$ rehash is paid for by $\Theta(n)$ cheap inserts, and insertion is $O(1)$ amortized.

## 9.6 Why hashing is $O(1)$, precisely {#sec-dsa-whyo1}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “Insert, search and delete in a hash table are $O(1)$ expected amortized time.”</em>

</div>

<div class="nb nb-theorem nb-block" id="theorem-9-6-1">

<strong>Theorem 9.6.1</strong> (The $O(1)$ claim)

A hash table supports insert, search and delete in $O(1)$ <em>expected</em> time (insert: <em>expected amortized</em>) provided that

1. <em>computing $h(k)$ and comparing two keys take $O(1)$</em> (true for fixed-size keys; a string of length $L$ costs $O(L)$, so “$O(1)$” really means $O(L)$);
2. <em>the hash spreads keys uniformly</em>: either the keys behave randomly with respect to $h$ (simple uniform hashing) or, better, $h$ is drawn at random from a universal family, which gives the guarantee for <em>every</em> input, with the expectation over the choice of $h$;
3. <em>the load factor is bounded by a constant</em>, $\alpha = n/m = O(1)$;
4. <em>the table resizes geometrically</em> when $\alpha$ passes the bound, so the $\Theta(n)$ rehashes amortize to $O(1)$ per insertion.

Then each operation scans an expected $O(1 + \alpha) = O(1)$ keys.

</div>

<div class="nb nb-moral">

The one-line interview answer: “The hash function sends the key straight to a bucket, and because keys spread evenly and the table grows to keep the load factor constant, the expected number of keys in that bucket is a constant. It is expected and amortized, not worst case: if everything collides, it is $O(n)$.”

</div>

### 9.6.i When it is not $O(1)$ {#sec-dsa-hashflood}

<div class="nb nb-remark" id="remark-9-6-2">

<strong>Remark 9.6.2</strong> (Worst case $\Theta(n)$) — If all $n$ keys land in one bucket, every operation scans $\Theta(n)$ keys and $n$ insertions cost $\Theta(n^2)$. It happens with a bad hash function (identity hash on keys that are all multiples of $m$), with structured keys and a power-of-two table, or on purpose.

</div>

<div class="nb nb-remark" id="remark-9-6-3">

<strong>Remark 9.6.3</strong> (Hash flooding) — If an attacker knows the hash function, they can send keys that all collide, for example in the parameters of a web request, and make a server spend $\Theta(n^2)$ time parsing one request. Such attacks on many languages’ web stacks were published in 2011. The defences are:

- a <em>random per-process seed</em> in a keyed hash (Python and Rust use SipHash; Python randomizes string hashes since version 3.3), which is universal hashing in practice;
- <em>treeified buckets</em>: since Java 8, a `HashMap` bucket with more than $8$ entries (in a table of at least $64$ buckets) becomes a red–black tree, so the worst case is $O(\log n)$ instead of $O(n)$ when the keys are comparable;
- in competitive programming, the classic anti-hash tests against `unordered_map` are defeated by a custom hash with a random seed (for example a splitmix64-style mixer of `x + seed`).

</div>

<div class="nb nb-remark" id="remark-9-6-4">

<strong>Remark 9.6.4</strong> (What hashing cannot do) — A hash table keeps no order. It cannot answer “smallest key”, “all keys between $a$ and $b$”, “successor of $x$” or “iterate in sorted order” faster than $\Theta(n)$; a balanced BST does all of them in $O(\log n)$ (+ output). Iteration order of `unordered_map` is arbitrary and changes after a rehash. Every insert can also invalidate iterators (on rehash).

</div>

## 9.7 Guaranteed $O(1)$ lookups {#sec-dsa-perfecthash}

<div class="nb nb-definition" id="fact-9-7-1">

<strong>Fact 9.7.1</strong>.

- <strong>Perfect hashing</strong> (FKS, for a <em>static</em> set): a first-level table of $n$ buckets; bucket $j$ with $n_j$ keys gets its own second-level table of $n_j^2$ slots and a universal hash chosen until it has no collisions (expected $2$ tries). Total expected space $O(n)$, worst-case lookup two probes.
- <strong>Cuckoo hashing</strong>: two tables and two hash functions; every key lives in one of its two possible slots, so a lookup reads at most $2$ slots, $O(1)$ worst case. An insert that finds both slots full kicks the occupant to its other slot, and so on; it takes $O(1)$ expected amortized time if $\alpha < 1/2$, and a long cycle triggers a rehash.
- <strong>Robin Hood hashing</strong>: linear probing where a key that has travelled further from its home slot takes the slot from a key that has travelled less; it equalises probe lengths and makes unsuccessful searches stop early.

</div>

## 9.8 Hash tables in the standard libraries {#sec-dsa-unordered}

|  | `std::unordered_map` (hash) | `std::map` (red–black tree) |
|:--|:--|:--|
| Search, insert, erase | $O(1)$ average, $O(n)$ worst | $O(\log n)$ worst |
| Order | none | sorted by key |
| Range queries, `lower_bound` | no | yes, $O(\log n)$ |
| Requirements on the key | `std::hash` and `==` | `<` (strict weak order) |
| Memory | buckets + one node per element | three pointers + colour per node |
| Iterator invalidation | on rehash (all iterators) | only the erased element |

<div class="nb-caption" id="table-9-2">

<strong>Table 9.2.</strong> Hash map versus tree map. Java’s `HashMap`/`TreeMap` and Python’s `dict`/(no built-in sorted map) follow the same split.

</div>

<div class="nb nb-remark" id="remark-9-8-1">

<strong>Remark 9.8.1</strong> (Java `HashMap` details that interviews ask) — Default capacity $16$, load factor $0.75$, capacity always a power of $2$, so the index is `hash & (n-1)` after the hash’s high bits are XORed into the low bits (`h ^ (h >>> 16)`) to compensate for the power-of-two table. Treeification as above. `HashMap` allows one `null` key; `Hashtable` is synchronized and allows none; `ConcurrentHashMap` locks per bin. Python’s `dict` uses open addressing with a perturbed probe sequence and keeps insertion order (guaranteed since Python 3.7).

</div>

## 9.9 Related structures {#sec-dsa-bloom}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a browser checking “is this URL in the list of malicious sites?” without storing the list.</em>

</div>

<div class="nb nb-definition" id="definition-9-9-1">

<strong>Definition 9.9.1</strong>. A <strong>Bloom filter</strong> is a bit array of $m$ bits and $k$ hash functions. To add $x$, set the bits $h_1(x), \ldots, h_k(x)$. To query $x$, answer “maybe present” if all $k$ bits are set and “definitely absent” otherwise. There are no false negatives; the false-positive probability after $n$ insertions is about $\big(1 - e^{-kn/m}\big)^k$, minimised at $k = (m/n)\ln 2$. Plain Bloom filters cannot delete (counting Bloom filters can).

</div>

The last part of `buckets.cpp`’s output above evaluates the formula for $10$ bits per key: the best $k$ is $7$ ($\approx 10 \ln 2$) with $0.82\%$ false positives, about one byte per key whatever the size of the keys. Bloom filters sit in front of slow lookups: databases (LSM trees) check them before reading a disk block.

<div class="nb nb-definition" id="definition-9-9-2">

<strong>Definition 9.9.2</strong>. <strong>Consistent hashing</strong> places both servers and keys on a circle of hash values and assigns each key to the next server clockwise. Adding or removing one of $s$ servers moves only about $1/s$ of the keys, where $k \bmod s$ would move almost all of them. Virtual nodes (several points per server) balance the load. It is used by distributed caches and key-value stores.

</div>

## 9.10 Design: an LRU cache {#sec-dsa-lru}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “Design a cache of capacity $c$ with `get` and `put` in $O(1)$ that evicts the least recently used key.”</em>

</div>

<div class="nb nb-remark" id="algorithm-9-10-1">

<strong>Algorithm 9.10.1</strong> (Hash map + doubly linked list) — Keep the entries in a doubly linked list ordered from most to least recently used, and a hash map from key to the list node. `get(k)`: look up the node ($O(1)$ expected), move it to the front ($O(1)$, since it is doubly linked), return the value. `put(k, v)`: update and move to the front if present; otherwise, if full, remove the tail node and its map entry, then insert the new node at the front. Neither structure alone suffices: the list cannot find a key fast, and the map has no recency order. (Java’s `LinkedHashMap` with access order is exactly this.)

</div>

<div class="nb nb-remark" id="remark-9-10-2">

<strong>Remark 9.10.2</strong> (LFU) — A least-frequently-used cache needs one more level: a map from frequency to a list of keys and the current minimum frequency, still $O(1)$ per operation. Tie rules (least recent among the least frequent, or smallest key) change the details, so ask.

</div>

## 9.11 A few harder problems to think about {#s9-11}

<div class="nb nb-problem nb-block" id="problem-9a">

<strong>Problem 9A</strong> 🌶🌶 (Linear probing trace)

Insert `12 44 13 88 23 94 11 39 20 16 5` into a table of size $11$ with $h(k) = (2k + 5) \bmod 11$ and linear probing. Give the final table.

<details class="nb-hint">
<summary>Hint</summary>

Home slots: $12 \mapsto 7$, $44 \mapsto 5$, $13 \mapsto 9$, $88 \mapsto 5$, $23 \mapsto 7$, $94 \mapsto 6$, $11 \mapsto 5$, $39 \mapsto 6$, $20 \mapsto 1$, $16 \mapsto 4$, $5 \mapsto 4$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

In insertion order: $12 \to 7$, $44 \to 5$, $13 \to 9$, $88 \to 6$ (2 probes), $23 \to 8$ (2), $94 \to 10$ (5: slots $6..10$), $11 \to 0$ (7: slots $5..10, 0$), $39 \to 1$ (7), $20 \to 2$ (2), $16 \to 4$ (1), and $5$ needs all $11$ probes ($4, 5, \ldots, 10, 0, 1, 2, 3$) to reach the last free slot $3$. Final table, slots $0..10$: `[11 39 20 5 16 44 88 12 23 13 94]`, $40$ probes in total (checked by `hashcheck.cpp`). The single cluster covering the whole table is primary clustering at its worst.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-9b">

<strong>Problem 9B</strong> (Expected probes)

A table with linear probing holds $750$ keys in $1000$ slots. Estimate the average number of probes for a successful and an unsuccessful search. How do they change with double hashing?

<details class="nb-hint">
<summary>Hint</summary>

$\alpha = 0.75$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Linear probing: $\frac12(1 + 4) = 2.5$ for a hit and $\frac12(1 + 16) = 8.5$ for a miss. With double hashing (close to uniform hashing): $\frac{1}{0.75}\ln 4 \approx 1.85$ and $\frac{1}{0.25} = 4$. These are the numbers measured in the table of `hashsim.cpp`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-9c">

<strong>Problem 9C</strong> (Chains)

$n = 2000$ keys are hashed into $m = 1000$ buckets with chaining. What is the expected number of keys examined by an unsuccessful search? By a successful search? What happens to both if the table doubles to $2000$ buckets?

<details class="nb-hint">
<summary>Hint</summary>

$\alpha$ and $1 + \alpha/2$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\alpha = 2$: a miss examines $2$ keys, a hit about $1 + 2/2 = 2$. After doubling, $\alpha = 1$: $1$ and $1.5$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-9d">

<strong>Problem 9D</strong> (Double hashing probe sequence)

$m = 13$, $h_1(k) = k \bmod 13$, $h_2(k) = 1 + (k \bmod 11)$. Give the first four slots of the probe sequence of $k = 27$. Why must $h_2(k)$ be nonzero and coprime to $m$?

<details class="nb-hint">
<summary>Hint</summary>

$h_1 = 1$, $h_2 = 6$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$1, 7, 13 \bmod 13 = 0, 6$. If $h_2(k) = 0$ the sequence never moves; if $\gcd(h_2(k), m) = d > 1$ it visits only $m/d$ slots and can fail although the table has room. A prime $m$ makes every nonzero step coprime to it.

</details>

</div>
