---
title: "1443. Minimum Time to Collect All Apples in a Tree"
weight: 2
---

[LeetCode 1443](https://leetcode.com/problems/minimum-time-to-collect-all-apples-in-a-tree/) · Medium · Tree DFS

**Approach.** Walk from vertex 0 and return to it, so every edge that leads to an apple is crossed twice and no other edge is crossed at all.
`solve(u, p)` returns the time spent inside the subtree of `u`. For each child `v`, if `v` has an apple or its subtree spent any time, add `child + 2` for the edge to `v`.

```cpp
class Solution {
public:
    int solve(int u, int p, vector<vector<int>>& adj, vector<bool>& hasApple) {
        int total = 0;
        for (int v : adj[u]) {
            if (v == p) continue;
            int child = solve(v, u, adj, hasApple);
            if (child > 0 || hasApple[v]) total += child + 2;
        }
        return total;
    }

    int minTime(int n, vector<vector<int>>& edges, vector<bool>& hasApple) {
        vector<vector<int>> adj(n);
        for (auto& e : edges) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
        }
        return solve(0, -1, adj, hasApple);
    }
};
```

Time $O(n)$. Space $O(n)$ for the adjacency list plus the recursion stack.
