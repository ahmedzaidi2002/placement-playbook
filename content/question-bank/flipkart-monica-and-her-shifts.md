---
title: "Monica and Her Shifts"
weight: 13
---

Flipkart OA, 24 Oct 2026 (IIT Delhi) · Hard · Bitmask DP over sites · No public match found, solved from the reported statement

Monica stands at $(0,0)$ in an $n \times m$ grid and can work 8 hours per day. She must visit every site, a site needs $x$ hours of work, and moving to an adjacent cell (up, down, left, right) takes 2 hours. Return the minimum number of days needed to visit all sites.

**Assumptions** (the report is vague, so these are fixed here). The grid holds the work hours of each cell, $0$ means no site. The limit is 8 hours per day. A site's work and a single move are never split across two days, so if the next item does not fit in today's remaining hours, it starts a new day. Monica keeps her position overnight and does not return. If a site needs more than 8 hours, the answer is $-1$.

**Approach.** The days only depend on the *order* in which sites are visited, because between two sites the shortest walk is the Manhattan distance, each step costing 2 hours. So try all orders with a bitmask over the sites.
State: `solve(mask, last, used)` = extra days still needed, with `mask` the visited sites, `last` the current site and `used` the hours already spent today (0 to 8). Choose the next unvisited site `j`: spend the moves (`2` hours each), then its work `w[j]`, rolling to a new day whenever an item does not fit. Take the best over all `j`, and memoise. The start $(0,0)$ is a virtual node, and the first day is counted once at the end.

```cpp
class Solution {
public:
    int k;
    vector<int> r, c, w;
    vector<vector<vector<int>>> memo;

    int place(int used, int t, int& days) {
        if (used + t > 8) {
            days++;
            used = 0;
        }
        return used + t;
    }

    int solve(int mask, int last, int used) {
        if (mask == (1 << k) - 1) return 0;
        int& res = memo[mask][last][used];
        if (res != -1) return res;
        res = INT_MAX;
        for (int j = 0; j < k; j++) {
            if ((mask >> j) & 1) continue;
            int days = 0, u = used;
            int steps = abs(r[last] - r[j]) + abs(c[last] - c[j]);
            while (steps--) u = place(u, 2, days);
            u = place(u, w[j], days);
            res = min(res, days + solve(mask | (1 << j), j, u));
        }
        return res;
    }

    int minDays(vector<vector<int>>& grid) {
        int n = grid.size(), m = grid[0].size();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (grid[i][j] == 0) continue;
                if (grid[i][j] > 8) return -1;
                r.push_back(i);
                c.push_back(j);
                w.push_back(grid[i][j]);
            }
        }
        k = r.size();
        if (k == 0) return 0;
        r.push_back(0);
        c.push_back(0);
        memo.assign(1 << k, vector<vector<int>>(k + 1, vector<int>(9, -1)));
        return 1 + solve(0, k, 0);
    }
};
```

Time $O(2^k \cdot k^2 \cdot (n+m))$ for $k$ sites, space $O(2^k \cdot k \cdot 9)$. This only works when the number of sites $k$ is small (about 16 to 18), which is why the report hints at a bitmask.
If the original allows work to be split across days, drop the "fits in the day" rule: the answer becomes $\lceil (2 \cdot \text{shortest tour length} + \sum x) / 8 \rceil$, so only the shortest visiting order matters.
