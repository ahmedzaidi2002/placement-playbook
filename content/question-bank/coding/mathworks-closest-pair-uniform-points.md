---
aliases: ["/question-bank/mathworks-closest-pair-uniform-points/"]
title: "Closest Pair of Points (Uniformly Distributed)"
weight: 23
---

MathWorks OA · Hard · Grid bucketing, expected linear time

**Problem.** $n \le 10^5$ points lie on a plane and are *uniformly distributed*. Find the smallest distance between any two of them.

**The textbook answers.** The standard solutions are divide and conquer or "sort by x and sweep with a set sorted by y", both $O(n \log n)$ for **any** input. The hint in the question says the uniform spread allows something simpler and faster: a grid.

**The idea in easy words.**

1. Draw a grid over the bounding box and choose the cell side `s` so that there are about $n$ cells, i.e. about **one point per cell**. For a box of width `W` and height `H`, that is `s = sqrt(W*H / n)`.
2. If the points are spread evenly, the closest pair is almost always in the same cell or in neighbouring cells, so we do not need to compare far-away points.
3. For each point look at its own cell (ring 0), then the 8 cells around it (ring 1), then the next ring, and so on.
4. After we have a candidate `best`, we can stop. A point in ring `k` can be as close as `(k - 1) * s`. So when `(k - 1) * s >= best` no point in ring `k` or beyond can beat `best`.

**Why it is correct even if the points are not uniform.** The stop rule is a proof, not a guess: we only stop when every unseen point is provably farther than `best`. Uniformity is used only for *speed*. With about one point per cell, each point sees a handful of other points, so the whole run is expected $O(n)$. With badly clustered input the code stays correct but becomes slower.

**Two small details.**

- If all points are on one line the box has area 0 and `sqrt(W*H/n)` would be 0. So we use `s = max(sqrt(W*H/n), max(W, H) / n)`, which keeps the number of cells at most about $3n$. If all points coincide, `s = 0` and the answer is 0.
- The first point may have to look at many empty rings until it meets a neighbour. That happens only until `best` is finite, and it costs at most the number of cells, so it is paid once.

```cpp
class Solution {
public:
    double closestPair(vector<pair<double, double>>& pts) {
        int n = pts.size();
        double minx = pts[0].first, maxx = minx, miny = pts[0].second, maxy = miny;
        for (auto& p : pts) {
            minx = min(minx, p.first);
            maxx = max(maxx, p.first);
            miny = min(miny, p.second);
            maxy = max(maxy, p.second);
        }
        double W = maxx - minx, H = maxy - miny;
        double s = max(sqrt(W * H / n), max(W, H) / n);
        if (s <= 0) return 0;
        int cols = (int)(W / s) + 1, rows = (int)(H / s) + 1;
        vector<vector<int>> grid(cols * rows);
        vector<int> cx(n), cy(n);
        for (int i = 0; i < n; i++) {
            cx[i] = min(cols - 1, (int)((pts[i].first - minx) / s));
            cy[i] = min(rows - 1, (int)((pts[i].second - miny) / s));
            grid[cx[i] * rows + cy[i]].push_back(i);
        }
        double best = 1e300;
        int maxK = max(cols, rows);
        for (int i = 0; i < n; i++) {
            for (int k = 0; k <= maxK; k++) {
                if (k > 0 && (k - 1) * s >= best) break;
                for (int x = cx[i] - k; x <= cx[i] + k; x++) {
                    if (x < 0 || x >= cols) continue;
                    for (int y = cy[i] - k; y <= cy[i] + k; y++) {
                        if (y < 0 || y >= rows) continue;
                        if (max(abs(x - cx[i]), abs(y - cy[i])) != k) continue;
                        for (int j : grid[x * rows + y]) {
                            if (j == i) continue;
                            double dx = pts[i].first - pts[j].first;
                            double dy = pts[i].second - pts[j].second;
                            best = min(best, sqrt(dx * dx + dy * dy));
                        }
                    }
                }
            }
        }
        return best;
    }
};
```

**Testing.** Compared with an all-pairs brute force on 3000 small inputs, including points on a vertical line, a horizontal line, and a tiny 3 by 3 lattice full of duplicates. On 100000 random uniform points it matches the sort-and-sweep answer and runs in about 20 ms.

**If the interviewer asks for the general solution.** Sort by x. Keep points whose x is within `best` of the current one, in a set ordered by y. For each new point, look only at points whose y is within `best` of it. A box of that size holds a constant number of points, so this is $O(n \log n)$ for any distribution.

Time expected $O(n)$ for uniform points. Space $O(n)$ for the grid.
