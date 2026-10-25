---
title: "4 · Linked lists"
linkTitle: "4 Linked lists"
weight: 4
math: true
---
## 4.1 Singly, doubly and circular lists {#sec-dsa-lists}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a playlist where songs are inserted and removed in the middle while you hold a pointer to the current song.</em>

</div>

<div class="nb nb-definition" id="definition-4-1-1">

<strong>Definition 4.1.1</strong>. A <strong>singly linked list</strong> is a chain of nodes, each holding a value and a pointer to the next node; the list is reached through a <strong>head</strong> pointer and ends at a null pointer. A <strong>doubly linked list</strong> also stores a pointer to the previous node. In a <strong>circular</strong> list the last node points back to the first.

</div>

<figure class="nb-fig"><img src="fig-1.svg" alt="Figure 1" loading="lazy"></figure>

| Operation | Singly linked | Doubly linked |
|:--|:--|:--|
| Access the $k$-th element | $\Theta(k)$ | $\Theta(\min(k, n-k))$ with a tail pointer |
| Search for a value | $\Theta(n)$ | $\Theta(n)$ |
| Insert / delete at the head | $\Theta(1)$ | $\Theta(1)$ |
| Insert at the tail | $\Theta(1)$ with a tail pointer | $\Theta(1)$ |
| Delete the tail | $\Theta(n)$ (need its predecessor) | $\Theta(1)$ |
| Insert after a given node | $\Theta(1)$ | $\Theta(1)$ |
| Delete a given node | $\Theta(n)$ (find predecessor)$^{*}$ | $\Theta(1)$ |
| Extra memory per element | 1 pointer | 2 pointers |

<div class="nb-caption" id="table-4-1">

<strong>Table 4.1.</strong> Costs of linked-list operations. ${}^{*}$Unless the node is not the last one: then copy the next node’s value into it and delete the next node instead, $\Theta(1)$.

</div>

<div class="nb nb-remark" id="remark-4-1-2">

<strong>Remark 4.1.2</strong> (Sentinels) — A <strong>sentinel</strong> (dummy) node before the first element removes the special cases for an empty list and for inserting or deleting at the head. A circular doubly linked list with one sentinel is how `std::list` is typically implemented.

</div>

## 4.2 Arrays versus linked lists {#sec-dsa-list-vs-array}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “If insertion in a list is $\Theta(1)$, why is `std::vector` almost always faster?”</em>

</div>

<div class="nb nb-definition" id="fact-4-2-1">

<strong>Fact 4.2.1</strong>.

- Arrays: $\Theta(1)$ indexing, contiguous memory (cache friendly, no per-element overhead), but $\Theta(n)$ insertion in the middle and occasional resizing.
- Lists: $\Theta(1)$ insertion and deletion <em>once you hold the node</em>, no resizing, stable addresses of elements; but $\Theta(n)$ access by position, one heap allocation per node, $8$ to $16$ bytes of pointers per element, and a likely cache miss per node.

</div>

<div class="nb nb-remark" id="remark-4-2-2">

<strong>Remark 4.2.2</strong> — “Insert in the middle” in a list is $\Theta(1)$ only after you have found the position, and finding it is $\Theta(n)$ pointer chasing. Shifting an array tail with `memmove` is a sequential copy at memory bandwidth. Lists win when you already hold the node (an LRU cache’s hash map points straight at it, [Section 9.10](../09-hashing/#sec-dsa-lru)), when elements must not move, or when splicing whole lists in $\Theta(1)$.

</div>

## 4.3 Classic list techniques {#sec-dsa-listtricks}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> reverse a singly linked list in place with three pointers.</em>

</div>

<div class="nb nb-remark" id="algorithm-4-3-1">

<strong>Algorithm 4.3.1</strong> (In-place reversal) — Keep `prev = null`, `cur = head`. Repeat: `next = cur->next; cur->next = prev; prev = cur; cur = next;`. At the end `prev` is the new head. $\Theta(n)$ time, $\Theta(1)$ space. The recursive version uses $\Theta(n)$ stack.

</div>

<div class="nb nb-remark" id="algorithm-4-3-2">

<strong>Algorithm 4.3.2</strong> (Slow and fast pointers) — Advance `slow` by one and `fast` by two nodes per step. When `fast` reaches the end, `slow` is at the middle. The same idea finds the $k$-th node from the end (start `fast` $k$ nodes ahead) and detects cycles.

</div>

### 4.3.i Floyd’s cycle detection {#sec-dsa-floyd}

<div class="nb nb-theorem nb-block" id="theorem-4-3-3">

<strong>Theorem 4.3.3</strong> (Tortoise and hare)

Let the list have a tail of $\mu$ nodes before a cycle of length $\lambda$. Start both pointers at the head; `slow` moves $1$ and `fast` moves $2$ per step.

1. If there is a cycle they meet, after at most $\mu + \lambda$ steps.
2. Then put one pointer back at the head and move both by $1$: they meet exactly at the start of the cycle, after $\mu$ steps.

</div>

<div class="nb nb-proof">

<em>Proof.</em> (1) Once both are in the cycle, the gap between them shrinks by $1$ per step, so they meet within $\lambda$ more steps. (2) Suppose they meet after $k$ steps. Then the hare has walked $2k$, the tortoise $k$, and the difference $k$ is a multiple of $\lambda$. The meeting point is $k - \mu$ steps into the cycle. A pointer starting there and walking $\mu$ more steps is at $k$ steps into the cycle, which is the cycle start because $k \equiv 0 \pmod \lambda$; a pointer walking $\mu$ steps from the head also arrives at the cycle start.

</div>

```cpp {filename="floyd.cpp"}
// Floyd's tortoise and hare on a list with a tail of length mu and a cycle of length lambda.
#include <cstdio>

int main() {
    const int mu = 4, lambda = 6, n = mu + lambda;
    int next[n];
    for (int i = 0; i < n; ++i) next[i] = i + 1;
    next[n - 1] = mu;                                   // last node points back into the list
    int slow = next[0], fast = next[next[0]], steps = 1;
    while (slow != fast) { slow = next[slow]; fast = next[next[fast]]; ++steps; }
    std::printf("tail mu = %d, cycle lambda = %d\n", mu, lambda);
    std::printf("phase 1: they meet at node %d after %d steps\n", slow, steps);
    int p = 0, q = slow, s2 = 0;                        // phase 2: one from head, one from meeting point
    while (p != q) { p = next[p]; q = next[q]; ++s2; }
    std::printf("phase 2: they meet at node %d (the cycle start) after %d steps\n", p, s2);
    int len = 1;
    for (int r = next[p]; r != p; r = next[r]) ++len;
    std::printf("phase 3: cycle length %d\n", len);
}
```

```text {filename="Output of floyd.cpp"}
tail mu = 4, cycle lambda = 6
phase 1: they meet at node 6 after 6 steps
phase 2: they meet at node 4 (the cycle start) after 4 steps
phase 3: cycle length 6
```

With $\mu = 4$ and $\lambda = 6$ they first meet after $k = 6$ steps (the smallest multiple of $6$ that is at least $4$), at node $\mu + (k - \mu) = 6$; phase 2 then takes $\mu = 4$ steps. $\Theta(n)$ time and $\Theta(1)$ space; a hash set of visited nodes also works but needs $\Theta(n)$ memory.

<div class="nb nb-remark" id="remark-4-3-4">

<strong>Remark 4.3.4</strong> (More list tricks interviewers ask) —

- <em>Intersection of two lists</em>: walk both; when one pointer ends, restart it at the other list’s head. They meet at the intersection after at most $m + n$ steps, or both reach null together.
- <em>Merge two sorted lists</em> in $\Theta(m + n)$ by relinking, no new nodes; <em>merge sort</em> on a list needs no extra array, which is why it is the sort of choice for lists (`std::list::sort`).
- <em>XOR linked list</em>: each node stores $\text{prev} \oplus \text{next}$, a doubly linked list with one pointer field; traversal needs the previous address. A curiosity, not usable with garbage collectors.
- <em>Palindrome check</em>: find the middle, reverse the second half, compare.

</div>

## 4.4 Skip lists {#sec-dsa-skiplist}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> Redis sorted sets: a linked list with express lanes.</em>

</div>

<div class="nb nb-definition" id="definition-4-4-1">

<strong>Definition 4.4.1</strong>. A <strong>skip list</strong> is a sorted linked list in which each node is also promoted to level $1$ with probability $1/2$, to level $2$ with probability $1/4$, and so on; each level is a sorted list of the nodes promoted to it. Search starts on the top level, moves right while the next key is smaller, and drops one level otherwise.

</div>

<div class="nb nb-definition" id="fact-4-4-2">

<strong>Fact 4.4.2</strong>. With $n$ keys the expected number of levels is $\Theta(\log n)$, the expected search, insert and delete time is $O(\log n)$, and the expected space is $2n$ pointers. The bounds are <em>expected</em> over the coin flips, for every input, like randomized quicksort. Skip lists are simpler than balanced trees to make concurrent, which is why they appear in databases and in Java’s `ConcurrentSkipListMap`.

</div>

<div class="nb nb-moral">

A linked list trades indexing for cheap splicing; most list problems are solved with two pointers that move at different speeds or start at different places.

</div>

## 4.5 A few harder problems to think about {#s4-5}

<div class="nb nb-problem nb-block" id="problem-4a">

<strong>Problem 4A</strong> (Delete without the head)

You are given only a pointer to a node of a singly linked list (not the last node). Delete it in $O(1)$. Why can the last node not be deleted this way?

<details class="nb-hint">
<summary>Hint</summary>

You cannot reach the predecessor, but you can reach the successor.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Copy the successor’s value into the node and unlink the successor: `n->val = n->next->val; n->next = n->next->next;`. The last node has no successor to copy from, and its predecessor’s `next` cannot be set to null without access to it.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-4b">

<strong>Problem 4B</strong> (Cycle arithmetic)

A list has a tail of $\mu = 7$ nodes and a cycle of $\lambda = 3$ nodes. After how many steps do the tortoise and the hare first meet?

<details class="nb-hint">
<summary>Hint</summary>

They meet after the smallest $k \ge \mu$ with $k \equiv 0 \pmod \lambda$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$k = 9$. At step $k$ the tortoise is $k$ nodes from the head and the hare $2k$; they coincide when both are in the cycle ($k \ge \mu$) and $\lambda$ divides $2k - k = k$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-4c">

<strong>Problem 4C</strong> (Which structure?)

A text editor needs: insert a character at the cursor, delete at the cursor, move the cursor left or right by one. Which structure makes all three $O(1)$? What if it also needs “jump to position $p$” fast?

<details class="nb-hint">
<summary>Hint</summary>

Doubly linked list, or two stacks.

</details>

<details class="nb-sol">
<summary>Solution</summary>

A doubly linked list with a cursor pointer, or a <strong>gap buffer</strong> (two stacks: text left of the cursor and text right of it), gives $O(1)$ for all three. Jumping to position $p$ is $\Theta(|p - \text{cursor}|)$ in both; a balanced tree keyed by position (a <em>rope</em>) makes every operation $O(\log n)$.

</details>

</div>
