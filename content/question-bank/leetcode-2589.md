---
title: "2589. Minimum Time to Complete All Tasks"
weight: 3
---

[LeetCode 2589](https://leetcode.com/problems/minimum-time-to-complete-all-tasks/) · Hard · Greedy, sorting

**Approach.** Sort tasks by end time. For each task, count the already-active seconds inside `[start, end]` and subtract them from `duration`.
If more is needed, switch on the latest inactive seconds before `end`, because late seconds are the most likely to be reused by tasks that end later.

```cpp
class Solution {
public:
    static bool cmp(vector<int>& a, vector<int>& b) {
        return a[1] < b[1];
    }

    int findMinimumTime(vector<vector<int>>& tasks) {
        sort(tasks.begin(), tasks.end(), cmp);
        vector<bool> on(2002, false);
        int ans = 0;
        for (auto& t : tasks) {
            int start = t[0], end = t[1], need = t[2];
            for (int i = start; i <= end; i++) {
                if (on[i]) need--;
            }
            for (int i = end; i >= start && need > 0; i--) {
                if (!on[i]) {
                    on[i] = true;
                    need--;
                    ans++;
                }
            }
        }
        return ans;
    }
};
```

Time $O(n \log n + n \cdot T)$ where $T = 2000$ is the time range. Space $O(T)$.
