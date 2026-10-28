---
title: "864. Shortest Path to Get All Keys"
weight: 14
---

[LeetCode 864](https://leetcode.com/problems/shortest-path-to-get-all-keys/) · Hard · BFS on (cell, keys mask) · Flipkart OA (related to Monica and Her Shifts)

**Approach.** The position alone is not enough, since which locks you can open depends on the keys you hold. So a state is (row, column, bitmask of collected keys), and every move costs 1, which makes it a plain BFS.
Count the keys first to get the target mask. From a state, step to a neighbour that is inside the grid and not `#`. A lock `A`..`F` needs the matching key bit. A key `a`..`f` sets its bit. The first time a state with all key bits is popped, its BFS level is the answer, and if the queue empties the answer is $-1$.

```cpp
class Solution {
public:
    int shortestPathAllKeys(vector<string>& grid) {
        int n = grid.size(), m = grid[0].size();
        int sr = 0, sc = 0, keys = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (grid[i][j] == '@') {
                    sr = i;
                    sc = j;
                } else if (grid[i][j] >= 'a' && grid[i][j] <= 'f') {
                    keys++;
                }
            }
        }
        int full = (1 << keys) - 1;
        vector<vector<vector<bool>>> vis(n, vector<vector<bool>>(m, vector<bool>(1 << keys, false)));
        queue<array<int, 3>> q;
        q.push({sr, sc, 0});
        vis[sr][sc][0] = true;
        int dr[4] = {1, -1, 0, 0};
        int dc[4] = {0, 0, 1, -1};
        int steps = 0;
        while (!q.empty()) {
            int sz = q.size();
            while (sz--) {
                array<int, 3> cur = q.front();
                q.pop();
                if (cur[2] == full) return steps;
                for (int d = 0; d < 4; d++) {
                    int nr = cur[0] + dr[d];
                    int nc = cur[1] + dc[d];
                    if (nr < 0 || nc < 0 || nr >= n || nc >= m) continue;
                    char ch = grid[nr][nc];
                    if (ch == '#') continue;
                    int nmask = cur[2];
                    if (ch >= 'A' && ch <= 'F' && !((nmask >> (ch - 'A')) & 1)) continue;
                    if (ch >= 'a' && ch <= 'f') nmask |= 1 << (ch - 'a');
                    if (vis[nr][nc][nmask]) continue;
                    vis[nr][nc][nmask] = true;
                    q.push({nr, nc, nmask});
                }
            }
            steps++;
        }
        return -1;
    }
};
```

Time $O(n \cdot m \cdot 2^k)$ for $k \le 6$ keys. Space $O(n \cdot m \cdot 2^k)$.
