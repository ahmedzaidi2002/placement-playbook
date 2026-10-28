---
title: "980. Unique Paths III"
weight: 15
---

[LeetCode 980](https://leetcode.com/problems/unique-paths-iii/) · Hard · Backtracking · Flipkart OA (related to Monica and Her Shifts)

**Approach.** Count the cells you may walk on (everything except `-1`) as `left`. DFS from the start, marking the current cell as blocked while it is on the path and restoring it on the way back. Reaching the end cell counts as one path only if `left == 1`, meaning every other cell was already used (the end cell is the last one).

```cpp
class Solution {
public:
    int solve(int r, int c, int left, vector<vector<int>>& grid) {
        if (grid[r][c] == 2) return left == 1 ? 1 : 0;
        int saved = grid[r][c];
        grid[r][c] = -1;
        int dr[4] = {1, -1, 0, 0};
        int dc[4] = {0, 0, 1, -1};
        int ways = 0;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d];
            int nc = c + dc[d];
            if (nr < 0 || nc < 0 || nr >= (int)grid.size() || nc >= (int)grid[0].size()) continue;
            if (grid[nr][nc] == -1) continue;
            ways += solve(nr, nc, left - 1, grid);
        }
        grid[r][c] = saved;
        return ways;
    }

    int uniquePathsIII(vector<vector<int>>& grid) {
        int sr = 0, sc = 0, left = 0;
        for (int i = 0; i < (int)grid.size(); i++) {
            for (int j = 0; j < (int)grid[0].size(); j++) {
                if (grid[i][j] != -1) left++;
                if (grid[i][j] == 1) {
                    sr = i;
                    sc = j;
                }
            }
        }
        return solve(sr, sc, left, grid);
    }
};
```

Time $O(3^{nm})$ in the worst case (at most 20 cells here, 3 choices per step after the first). Space $O(nm)$ for the recursion.
