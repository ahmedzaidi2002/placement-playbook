---
title: "Graphs (BFS, DFS, shortest path, MST)"
weight: 5
---

11 questions asked by Cisco, EPAM, Fujitsu, MAQ Software, MathWorks, Paytm, Texas Instruments, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q13, Dijkstra with road opening times

*Asked by: Cisco (Code with Cisco, Jun 2025)*

You manage deliveries across one-way roads, each with a travel time and an opening time:
you cannot enter a road before it opens, so if you reach a city early you wait. Roads
(from, to, travel, opens): (A, B, 5, 0), (A, C, 2, 0), (B, D, 3, 10), (C, D, 7, 0),
(C, E, 1, 8), (D, E, 2, 0). You leave city A at time 0. What is the earliest arrival time
at city E using Dijkstra's algorithm modified for opening times?

- **(a)** 9
- **(b)** 10
- **(c)** 11
- **(d)** 13

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 9**

**Why.** You may enter a road at time max(arrival, opening time), and arriving earlier never hurts, so Dijkstra on arrival times still works.
- A → C arrives at 2. C → E opens at 8, so leave at 8 and arrive at 9.
- Via D: A → C → D arrives at 9, then E at 11.
- Via B: A → B at 5, wait until 10 for B → D, D at 13.
The earliest arrival at E is 9.

**Concept: Dijkstra with waiting times.** Dijkstra is correct when edge costs are "first-in-first-out": leaving later never lets you arrive earlier. With opening times, the arrival time is max(t, open) + travel, which keeps that property, so the greedy choice of the earliest unvisited node still works.

{{< /details >}}

### 2 · Q4, value of x in an adjacency matrix

*Asked by: EPAM (EPAM freshers test)*

An undirected graph has the adjacency matrix with rows $0\,0\,0\,1$, $0\,0\,0\,0$,
$0\,0\,0\,1$, $1\,0\,x\,0$. What is the value of $x$?

- **(a)** 1
- **(b)** 0
- **(c)** Either 0 or 1
- **(d)** Data insufficient

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 1**

**Why.** An undirected graph's adjacency matrix is symmetric: entry (i, j) = entry (j, i). Entry (3, 4) is 1, so entry (4, 3), which is x, must be 1.

**Concept: adjacency matrix.** A[i][j] = 1 if there is an edge i–j. For undirected graphs every edge appears twice (A[i][j] and A[j][i]); directed graphs need not be symmetric.

{{< /details >}}

### 3 · DS Q4, Dijkstra

*Asked by: Fujitsu (IIT Kharagpur 2023)*

In graph theory, what is the time complexity of finding the shortest path between two
nodes in a weighted graph using Dijkstra's algorithm?

- **(a)** $O(V)$
- **(b)** $O(V^2)$
- **(c)** $O(E + V \log V)$
- **(d)** $O(V^2 \log V)$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) O(E + V log V)**

**Why.** That is Dijkstra with a Fibonacci heap. With a binary heap it is O((E + V) log V); with a plain array O(V²), which is best for dense graphs. The question expects the heap bound.

**Concept: Dijkstra's algorithm.** Repeatedly take the unvisited vertex with the smallest tentative distance (from a priority queue), fix it, and relax its outgoing edges. Works only with non-negative weights.

{{< /details >}}

### 4 · Q23, all-pairs shortest paths with negative edges

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

Which algorithm determines the shortest path between all pairs of vertices in a graph whose
edges may have positive or negative weights, with no negative cycles?

- **(a)** Dijkstra's algorithm
- **(b)** Bellman-Ford algorithm
- **(c)** Kruskal's algorithm
- **(d)** Floyd-Warshall algorithm

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Floyd–Warshall**

**Why.** It computes shortest paths between all pairs, handles negative edges, and needs no negative cycles. O(V³). Bellman–Ford handles negative edges but from a single source; Dijkstra needs non-negative weights; Kruskal builds spanning trees.

**Concept: Floyd–Warshall.** dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) for each intermediate vertex k in turn. After processing k, paths may use vertices 1..k in the middle. A negative dist[i][i] at the end reveals a negative cycle.

{{< /details >}}

### 5 · Q30, edges of a spanning tree

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

A graph has 10 vertices and 15 edges. How many edges does a minimum spanning tree have?

- **(a)** 10
- **(b)** 9
- **(c)** 15
- **(d)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 9**

**Why.** A spanning tree on V vertices always has V − 1 edges (if the graph is connected), whatever the number of edges in the graph.

**Concept: trees have V − 1 edges.** A tree is connected with no cycles. Fewer edges would disconnect it; one more edge would create a cycle.

{{< /details >}}

### 6 · Q7, BFS and DFS

*Asked by: MathWorks (IIT Bombay 2024)*

The data structures used by BFS and DFS are:

{{< details title="Answer and explanation" closed="true" >}}

**Answer: a queue (BFS) and a stack (DFS)**

**Why.** BFS processes vertices in the order they were discovered (FIFO), level by level. DFS goes as deep as possible, returning to the most recent vertex with unexplored neighbours (LIFO); recursion supplies the stack.

**Concept: traversal order follows the container.** Swap the queue in BFS for a stack and you get a DFS-like order; use a priority queue and you get Dijkstra/Prim.

{{< /details >}}

### 7 · Q9, maximum spanning tree

*Asked by: MathWorks (NIT Durgapur 2024)*

Which algorithm helps generate the maximum spanning tree of a graph?

- **(a)** Prim's algorithm, which selects the root vertex in the beginning and then traverses from vertex to vertex adjacently
- **(b)** Kruskal's algorithm, starting from the least-weight edge and selecting each new edge by the next least weight
- **(c)** Prim's algorithm, starting from the highest-weight edge and selecting each new edge by the next highest weight
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a)** (Prim's algorithm, growing from a root to adjacent vertices; picking the heaviest crossing edge each time gives a maximum spanning tree)

**Why.** Prim's algorithm grows one tree from a starting vertex through adjacent vertices. Taking the heaviest edge leaving the tree each time (instead of the lightest) produces a maximum spanning tree. (b) builds a minimum tree; (c) describes Kruskal's edge order but calls it Prim's. (The candidate chose (d).)

**Concept: maximum spanning tree.** Any MST algorithm finds a maximum spanning tree if you reverse the comparison (or negate all weights).

{{< /details >}}

### 8 · Critical MST edges

*Asked by: Paytm (HackerRank, Sep 2025)*

A critical MST edge is an edge whose deletion would increase the weight of the minimum
spanning tree; if deleting it disconnects the graph, the MST weight becomes infinite. The
graph has edges $0\!-\!1$ (2), $1\!-\!2$ (2), $2\!-\!3$ (1), $3\!-\!4$ (5), $0\!-\!4$ (5)
and $4\!-\!5$ (5). Which of the following are critical edges? (Pick one or more.)

- **(a)** the edge between 0 and 1
- **(b)** the edge between 0 and 4
- **(c)** the edge between 3 and 4
- **(d)** the edge between 4 and 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) and (d)**

**Why.** The MST weight is 1 + 2 + 2 + 5 + 5 = 15: the three light edges (0–1, 1–2, 2–3), one of the two weight-5 cycle edges (3–4 or 0–4), and 4–5.
- Remove 0–1: both weight-5 cycle edges are needed, weight 18 > 15, so critical.
- 4–5 is a bridge (the only link to vertex 5): removing it disconnects the graph, so critical.
- 3–4 and 0–4 can replace each other, so neither is critical.
(1–2 and 2–3 are critical too, but not offered.)

**Concept: critical vs pseudo-critical MST edges.** An edge is critical if every MST must contain it (removing it raises the MST weight). It is pseudo-critical if some MSTs use it and some don't (ties). Test: remove the edge and recompute the MST weight.

{{< /details >}}

### 9 · DFS-4, valid depth-first orders

*Asked by: Paytm (HackerRank, Sep 2025)*

Which of the paths is or are valid for a depth-first search from node 0? The graph has
edges $0\!-\!5$, $0\!-\!4$, $0\!-\!2$, $2\!-\!3$, $5\!-\!7$, $5\!-\!6$, $5\!-\!1$,
$1\!-\!8$ and $1\!-\!4$. (Pick one or more.)

- **(a)** 0 2 4 1 8 3 5 7 6
- **(b)** 0 5 6 7 1 8 4 2 3
- **(c)** 0 5 6 7 1 8 4 3 2
- **(d)** 0 5 1 8 2 3 4 6 7

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) only**

**Why.** In DFS the next vertex must be an unvisited neighbour of the deepest vertex on the current path that still has one.
- (a): after 0, 2 the search must go to 3 (2's only unvisited neighbour) before anything else.
- (b): 0 → 5 → 6, back to 5 → 7, back → 1 → 8, back to 1 → 4; back to 0 → 2 → 3. Valid.
- (c): visits 3 right after 4, but 3 is adjacent only to 2.
- (d): after 8 the search backtracks to 1, which still has 4 unvisited, so 4 must come next, not 2.

**Concept: checking a DFS order.** Keep the current path as a stack. Each next vertex must be adjacent to the top of the stack; if the top has no unvisited neighbours, pop and try again. Neighbour order is free, so many orders can be valid.

{{< /details >}}

### 10 · sort edges, avoid cycles

*Asked by: Texas Instruments (BITS Pilani)*

Repeatedly add the smallest edge that does not form a cycle, until $V - 1$ edges. Which
algorithm?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: Kruskal's algorithm**

**Why.** Sorting all edges and repeatedly adding the lightest one that does not form a cycle, until V − 1 edges, is exactly Kruskal's method.

**Concept: Kruskal vs Prim.** Kruskal: global sorted edge list, union-find to detect cycles, O(E log E). Prim: grow one tree from a vertex with a priority queue, O(E log V). Both are greedy and correct by the cut property.

{{< /details >}}

### 11 · Q16, data structure for BFS

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

What data structure would you use to traverse a given graph using the breadth-first search
(BFS) algorithm?

- **(a)** Stack
- **(b)** Linked List
- **(c)** Queue
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) queue**

**Why.** BFS visits vertices in the order they were discovered, which is first-in-first-out.

**Concept: BFS finds shortest paths in unweighted graphs.** Because it explores all vertices at distance d before any at d + 1, the first time it reaches a vertex is along a shortest path.

{{< /details >}}
