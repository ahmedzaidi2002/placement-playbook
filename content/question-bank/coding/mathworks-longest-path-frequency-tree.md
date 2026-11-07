---
aliases: ["/question-bank/mathworks-longest-path-frequency-tree/"]
title: "Longest Path in a Tree With a Frequency Constraint"
weight: 28
---

MathWorks OA · Medium · Tree diameter after cutting forbidden edges · The statement was reconstructed from memory, not the original wording

**Problem.** A tree has $N \le 2 \cdot 10^5$ nodes and each node has a frequency value in $\{1, 2, 3\}$. Find the maximum number of **edges** in a simple path in which every pair of consecutive nodes $u, v$ has $|\text{freq}[u] - \text{freq}[v]| \le 1$. The path may start and end anywhere.

Input: `N`, the `N` frequencies, then `N - 1` lines `u v` (0-indexed). Example: `5 / 1 2 3 1 2 / 0 1 / 1 2 / 1 3 / 3 4` gives 3 (path `0 -> 1 -> 3 -> 4` with values 1, 2, 1, 2).

**The key observation.** The rule only talks about **two neighbouring nodes**. So every edge is either allowed or forbidden by itself:

- an edge between values 1 and 2, 2 and 3, or two equal values is **allowed**;
- an edge between a 1 and a 3 is **forbidden** (difference 2).

A path is valid exactly when it uses only allowed edges. So: delete the forbidden edges. The tree falls apart into smaller trees (a forest), and the answer is the **longest path (diameter)** of any piece.

**Finding the longest path (the same trick as LeetCode 543).** For each node, `down[u]` is the longest downward path in edges using only allowed edges. When we process a child `u` of a parent `p` and the edge between them is allowed:

1. `cand = down[u] + 1` is the best branch that goes through this child.
2. A path that bends at `p` joins this branch with the best branch `p` already had: `ans = max(ans, down[p] + cand)`.
3. Then `down[p] = max(down[p], cand)`.

**Avoiding deep recursion.** $N$ can be 200000 and the tree can be one long chain, so a recursive DFS may overflow the stack. Instead:

1. Run a BFS from node 0 and store the visiting order and each node's parent.
2. Walk that order **backwards**. When we reach `u`, all of its children (which come later in BFS order) have already been processed, so `down[u]` is final. Push its value into its parent as above.

**Dry run of the example.** Edges: 0-1 (values 1, 2) allowed, 1-2 (2, 3) allowed, 1-3 (2, 1) allowed, 3-4 (1, 2) allowed. Nothing is forbidden. BFS order: 0, 1, 2, 3, 4. Going backwards:

| node | parent | edge allowed? | cand | ans | down[parent] |
|---|---|---|---|---|---|
| 4 | 3 | yes | 1 | max(0, 0 + 1) = 1 | 1 |
| 3 | 1 | yes | down[3] + 1 = 2 | max(1, 0 + 2) = 2 | 2 |
| 2 | 1 | yes | 1 | max(2, 2 + 1) = 3 | 2 |
| 1 | 0 | yes | down[1] + 1 = 3 | max(3, 0 + 3) = 3 | 3 |
| 0 | none | | | 3 | |

The answer is 3.

```cpp
class Solution {
public:
    int longestValidPath(int n, vector<int>& freq, vector<vector<int>>& edges) {
        vector<vector<int>> g(n);
        for (auto& e : edges) {
            g[e[0]].push_back(e[1]);
            g[e[1]].push_back(e[0]);
        }
        vector<int> order, parent(n, -1), down(n, 0);
        order.push_back(0);
        for (int i = 0; i < (int)order.size(); i++) {
            int u = order[i];
            for (int v : g[u]) {
                if (v == parent[u]) continue;
                parent[v] = u;
                order.push_back(v);
            }
        }
        int ans = 0;
        for (int i = n - 1; i >= 0; i--) {
            int u = order[i];
            int p = parent[u];
            if (p == -1) continue;
            if (abs(freq[u] - freq[p]) > 1) continue;
            int cand = down[u] + 1;
            ans = max(ans, down[p] + cand);
            down[p] = max(down[p], cand);
        }
        return ans;
    }
};
```

**Testing.** The example gives 3. Compared with a brute force that tries every start node and walks all valid simple paths, on 5000 random trees with up to 10 nodes. A chain of 200000 nodes returns 199999 immediately, without any stack problem.

Time $O(N)$. Space $O(N)$.
