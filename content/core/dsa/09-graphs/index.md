---
title: "9 · Graphs and graph algorithms"
linkTitle: "9 Graphs"
weight: 9
math: true
---
## 9.1 Vocabulary and counting facts {#dsa-9-1}

A graph $G = (V, E)$: vertices and edges, **directed** or **undirected**, **weighted** or not. **Degree** (in/out for directed), **path**, **cycle**, **connected**, **DAG** (directed acyclic graph), **tree** (connected, acyclic), **bipartite** (2-colourable; no odd cycle).

- Sum of degrees $= 2|E|$ (handshake lemma), so the number of odd-degree vertices is even.
- A simple undirected graph has at most $\binom{n}{2} = n(n-1)/2$ edges; a simple directed graph $n(n-1)$.
- A tree on $n$ vertices has exactly $n - 1$ edges; a forest with $k$ trees has $n - k$.
- $K_n$ has $n^{n-2}$ spanning trees (Cayley's formula): 16 for $n = 4$.

## 9.2 Representations {#dsa-9-2}

| | Adjacency matrix | Adjacency list |
|---|---|---|
| Space | $O(V^2)$ | $O(V + E)$ |
| Is $(u, v)$ an edge? | **$O(1)$** | $O(\deg u)$ |
| Visit all neighbours of $u$ | $O(V)$ | **$O(\deg u)$** |
| Best for | dense graphs | **sparse graphs** (most real ones) |

An **edge list** (just the pairs) suits Kruskal.

## 9.3 BFS and DFS {#dsa-9-3}

| | BFS | DFS |
|---|---|---|
| Data structure | **queue** | **stack** (or recursion) |
| Explores | level by level | as deep as possible, then backtracks |
| Finds | **shortest paths in unweighted graphs** | cycles, topological order, components, bridges |
| Time | $O(V + E)$ (list) / $O(V^2)$ (matrix) | same |

Both mark visited vertices so each is processed once. Bipartiteness: BFS-colour levels alternately; a conflict means an odd cycle.

**DFS edge types** (directed): tree, **back** (to an ancestor → **cycle**), forward, cross.

## 9.4 Topological sort {#dsa-9-4}

A linear order of a **DAG**'s vertices with every edge going forward (task scheduling, course prerequisites, build order). Exists **iff** the graph has no cycle.

- **Kahn's algorithm:** repeatedly output a vertex with in-degree 0 and remove its edges. If vertices remain, there is a cycle.
- **DFS:** output vertices in **reverse order of finishing**.

Example: edges A→C, B→C, C→D: valid orders **A B C D** or **B A C D**.

## 9.5 Shortest paths {#dsa-9-5}

| Algorithm | Problem | Negative edges? | Time |
|---|---|---|---|
| **BFS** | unweighted | — | $O(V + E)$ |
| **Dijkstra** | single source, non-negative weights | **no** | $O((V + E)\log V)$ with a heap |
| **Bellman–Ford** | single source | **yes**; detects negative cycles | $O(VE)$ |
| **Floyd–Warshall** | all pairs | yes (no negative cycles) | $O(V^3)$ |
| DAG relaxation | single source on a DAG | yes | $O(V + E)$ |

**Dijkstra:** distances start at ∞ (source 0); repeatedly take the unvisited vertex with the smallest distance (min-heap) and **relax** its edges: $d[v] = \min(d[v],\ d[u] + w(u, v))$.

<div class="nb nb-example">

<strong>Example</strong> (Dijkstra)

Undirected edges: A–B 4, A–C 1, C–B 2, B–D 1, C–D 5. Source A.

- Take **A (0)**: C = 1, B = 4.
- Take **C (1)**: B = min(4, 1 + 2) = **3**, D = 1 + 5 = 6.
- Take **B (3)**: D = min(6, 3 + 1) = **4**.
- Take **D (4)**.

Result: A 0, C 1, B 3, D 4 (path to D: A → C → B → D).

</div>

**Why Dijkstra fails with negative edges:** it finalises a vertex when it is taken, assuming no later path can be shorter; a negative edge found later can break that.

**Bellman–Ford:** relax **all** edges $V - 1$ times; if a $V$-th round still improves something, there is a **negative cycle**. **Floyd–Warshall:** $d[i][j] = \min(d[i][j],\ d[i][k] + d[k][j])$ for every intermediate $k$.

## 9.6 Minimum spanning trees {#dsa-9-6}

A **minimum spanning tree (MST)** connects all vertices of a weighted undirected graph with $V - 1$ edges and minimum total weight.

- **Kruskal:** sort edges by weight; add each edge unless it creates a cycle (check with **union–find**). $O(E \log E)$. Good for sparse graphs.
- **Prim:** grow one tree from a start vertex, always adding the cheapest edge leaving it (min-heap). $O(E \log V)$. Good for dense graphs.

<div class="nb nb-example">

<strong>Example</strong> (Kruskal on the same graph)

Edges sorted: A–C 1, B–D 1, C–B 2, A–B 4, C–D 5. Take **A–C**, take **B–D**, take **C–B** (joins the two pieces); A–B and C–D would make cycles. MST weight $1 + 1 + 2 = $ **4**. Prim from A picks the same edges (A–C, C–B, B–D).

</div>

If all edge weights are distinct, the MST is unique. **Cut property:** the lightest edge crossing any cut is in some MST.

## 9.7 Connectivity and more {#dsa-9-7}

- **Union–find (disjoint set union):** `find` and `union` with path compression + union by rank → nearly $O(1)$ amortized ($\alpha(n)$). Used in Kruskal and dynamic connectivity.
- **Strongly connected components** (directed): Kosaraju (two DFS passes) or Tarjan, $O(V + E)$.
- **Bridges and articulation points:** DFS with discovery times and low-links, $O(V + E)$.
- **Max flow** (Ford–Fulkerson / Edmonds–Karp), **bipartite matching**, and **NP-hard** problems with no known polynomial algorithm: travelling salesman, Hamiltonian cycle, graph colouring with $k \ge 3$ colours, vertex cover.

<div class="nb nb-moral">

BFS = queue, shortest unweighted paths; DFS = stack, cycles and topological order. Dijkstra needs non-negative weights; Bellman–Ford handles negatives and finds negative cycles; Floyd–Warshall does all pairs in O(V³). MST: Kruskal sorts edges with union–find, Prim grows a tree with a heap.

</div>
