---
title: "592D. Super M"
weight: 5
---

[Codeforces 592D](https://codeforces.com/problemset/problem/592/D) · rating 2200 · tags: dfs and similar, dp, graphs, trees

The tree has `n` cities and `m` of them are attacked. Pick a start city, visit every attacked city by walking along roads, and minimise the walk length. If several start cities give the minimum, print the smallest index. Output the start city, then the length.

**Approach.**
1. Only edges whose side away from the root contains an attacked city matter. Root at an attacked city and count attacked cities per subtree, so every edge with a positive count is needed. Call the number of such edges `E`.
2. Visiting all attacked cities and returning to the start costs `2E`, since each needed edge is crossed twice.
3. The walk does not have to return, so it ends at the attacked city farthest from the start, saving that distance. The best saving is the diameter of the attacked cities, so the answer is `2E - diameter`.
4. Find the diameter with two BFS runs. From any attacked city take the farthest attacked city `a`, breaking ties by smaller index. BFS from `a` and take the farthest attacked city `b`, again smaller index on ties.
5. The walk can start at either end of a diameter, so the start city is `min(a, b)`.
6. When `m = 1` there are no needed edges, the start is that city and the length is 0.

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<vector<int>> adj;
vector<int> att;

vector<int> bfs(int src, vector<int>& par, vector<int>& order) {
    vector<int> dist(n + 1, -1);
    par.assign(n + 1, 0);
    order.clear();
    queue<int> q;
    q.push(src);
    dist[src] = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : adj[u]) {
            if (dist[v] != -1) continue;
            dist[v] = dist[u] + 1;
            par[v] = u;
            q.push(v);
        }
    }
    return dist;
}

int farthestAttacked(vector<int>& dist) {
    int best = att[0];
    for (int x : att) {
        if (dist[x] > dist[best] || (dist[x] == dist[best] && x < best)) best = x;
    }
    return best;
}

int main() {
    scanf("%d %d", &n, &m);
    adj.assign(n + 1, {});
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    att.resize(m);
    vector<int> cnt(n + 1, 0);
    for (int i = 0; i < m; i++) {
        scanf("%d", &att[i]);
        cnt[att[i]] = 1;
    }
    vector<int> par, order;
    vector<int> d0 = bfs(att[0], par, order);
    int edges = 0;
    for (int i = n - 1; i > 0; i--) {
        int v = order[i];
        if (cnt[v] > 0) {
            edges++;
            cnt[par[v]] += cnt[v];
        }
    }
    int a = farthestAttacked(d0);
    vector<int> da = bfs(a, par, order);
    int b = farthestAttacked(da);
    printf("%d\n%d\n", min(a, b), 2 * edges - da[b]);
    return 0;
}
```

Time $O(n)$. Space $O(n)$. Everything is iterative, so a path-shaped tree does not overflow the recursion stack.

The statement is summarised from memory, because Codeforces blocks automated fetches. The problem ID, title and tags are verified against the Codeforces API. Check the output order against the statement before submitting.
