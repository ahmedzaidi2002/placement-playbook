---
title: "Minimum Tree Depth After K Reattachments"
weight: 8
---

Recalled interview question · Hard · Binary search on the answer, tree greedy

A tree with `n` nodes rooted at 1. In one operation, cut the edge between a node `u` and its parent and attach `u` to the root. Use at most `k` operations and return the minimum possible depth (the height) of the tree.

**Approach.** Binary search the final depth `H`. For a fixed `H`, count the operations needed. Go bottom-up and keep `h[v]`, the height of `v`'s subtree after cuts below it.
When `h[v] == H - 1` and `v` is not already a child of the root, cut `v` and attach it to the root, which costs one operation and removes `v` from its parent's height. Cutting the deepest such node first is optimal, since it saves every ancestor above it.
The smallest `H` with `need(H) <= k` is the answer. `need` never increases as `H` grows, so the binary search is valid.

```cpp
class Solution {
public:
    int need(int H, int n, vector<int>& par, vector<int>& order) {
        vector<int> h(n + 1, 0);
        int ops = 0;
        for (int i = n - 1; i >= 1; i--) {
            int v = order[i];
            if (h[v] == H - 1 && par[v] != 1) ops++;
            else h[par[v]] = max(h[par[v]], h[v] + 1);
        }
        return ops;
    }

    int minDepth(int n, vector<vector<int>>& edges, int k) {
        if (n == 1) return 0;
        vector<vector<int>> adj(n + 1);
        for (auto& e : edges) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
        }
        vector<int> par(n + 1, 0), order;
        vector<bool> vis(n + 1, false);
        queue<int> q;
        q.push(1);
        vis[1] = true;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            order.push_back(u);
            for (int v : adj[u]) {
                if (vis[v]) continue;
                vis[v] = true;
                par[v] = u;
                q.push(v);
            }
        }
        int lo = 1, hi = n - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (need(mid, n, par, order) <= k) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
};
```

Time $O(n \log n)$. Space $O(n)$. The BFS is iterative, so a path-shaped tree does not overflow the stack.

Assumptions: the signature and input format are made up, nodes are 1-indexed, depth is counted in edges (the root has depth 0), and the edges are undirected pairs. The original constraints were not remembered. The author also saw public tests where a node had several parents, which is not a tree. The BFS from node 1 keeps the first parent it finds and ignores the extra edges, which is a guess at what those tests meant. This problem is not matched to a known platform problem, so there is no link.
