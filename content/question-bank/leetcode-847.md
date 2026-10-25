---
title: "847. Shortest Path Visiting All Nodes"
weight: 1
---

[LeetCode 847](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) · Hard · BFS, bitmask

**Approach.** A state is (current node, set of visited nodes as a bitmask). Start BFS from every node at once with only its own bit set, so any start node is allowed.
The first time a state with all bits set is popped, the BFS level is the answer. Mark a state visited when it is pushed, so nodes and edges can be revisited with a different mask.

```cpp
class Solution {
public:
    int shortestPathLength(vector<vector<int>>& graph) {
        int n = graph.size();
        int full = (1 << n) - 1;
        vector<vector<bool>> vis(n, vector<bool>(1 << n, false));
        queue<pair<int, int>> q;
        for (int i = 0; i < n; i++) {
            q.push({i, 1 << i});
            vis[i][1 << i] = true;
        }
        int steps = 0;
        while (!q.empty()) {
            int sz = q.size();
            while (sz--) {
                int u = q.front().first;
                int mask = q.front().second;
                q.pop();
                if (mask == full) return steps;
                for (int v : graph[u]) {
                    int nmask = mask | (1 << v);
                    if (vis[v][nmask]) continue;
                    vis[v][nmask] = true;
                    q.push({v, nmask});
                }
            }
            steps++;
        }
        return 0;
    }
};
```

Time $O(n \cdot 2^n \cdot \text{deg})$, i.e. $O(n^2 \cdot 2^n)$ in the worst case. Space $O(n \cdot 2^n)$.
