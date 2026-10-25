---
title: "2565. Subsequence With the Minimum Score"
weight: 7
---

[LeetCode 2565](https://leetcode.com/problems/subsequence-with-the-minimum-score/) · Hard · Two pointers, prefix and suffix matching

Recalled as "remove characters from the second string so it becomes a subsequence of the first, score = max removed index - min removed index + 1". The recalled statement says "return score" and not minimum; this is LeetCode 2565 with `s` as the first string and `t` as the second, and the minimum is what LeetCode asks for.

**Approach.** Removing the whole range `[l, r]` of `t` is always at least as good as removing scattered indices with the same ends. So keep a prefix `t[0..p)` and a suffix `t[q..m)` and remove the middle, which costs `q - p`.
Precompute `suf[j]`, the latest start in `s` from which `t[j..]` is a subsequence. Walk `s` from the left matching a prefix of `t`. For each prefix length `p` ending at position `i`, the smallest valid `q >= p` with `suf[q] > i` only moves forward, so a second pointer finds it.

```cpp
class Solution {
public:
    int minimumScore(string s, string t) {
        int n = s.size(), m = t.size();
        vector<int> suf(m + 1, -1);
        suf[m] = n;
        int j = m - 1;
        for (int k = n - 1; k >= 0 && j >= 0; k--) {
            if (s[k] == t[j]) suf[j--] = k;
        }
        int ans = j + 1;
        int p = 0, q = 0;
        for (int i = 0; i < n && p < m; i++) {
            if (s[i] != t[p]) continue;
            p++;
            while (q < p || suf[q] <= i) q++;
            ans = min(ans, q - p);
        }
        return ans;
    }
};
```

Time $O(n + m)$. Space $O(m)$.
