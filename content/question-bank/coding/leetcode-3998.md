---
aliases: ["/question-bank/leetcode-3998/"]
title: "3998. Transform Binary String Using Subsequence Sort"
weight: 26
---

[LeetCode 3998](https://leetcode.com/problems/transform-binary-string-using-subsequence-sort/) · Medium · Prefix counts, greedy fill of `?` · MathWorks OA

**Problem.** You get a binary string `s` and a list `strs` of strings made of `0`, `1` and `?` (each `?` can become `0` or `1`). In one operation you choose **any subsequence** of `s`, sort it (all 0s first, then all 1s), and write it back into the same positions. You may repeat this any number of times. For each `strs[i]`, say whether you can replace its `?` and then turn `s` into it. Here $n \le 2000$ and there are up to 2000 strings.

**Think about what one operation does.** Sorting a subsequence moves 1s to the right and 0s to the left. It never creates new 1s. So two things can never be broken:

1. The **total number of 1s** stays the same.
2. For every prefix, the **number of 1s in that prefix can only go down or stay**, never go up. A 1 can only leave a prefix by moving right, and no 1 can enter it from the right.

So the target `t` is reachable only if `ones(t) == ones(s)` and for every `i`, `ones in t[0..i] <= ones in s[0..i]`.

**These two conditions are also enough.** Look at the 1s from left to right. The $k$-th 1 of `s` is at position $p_k$ and the $k$-th 1 of `t` at $q_k$. The prefix condition says exactly $p_k \le q_k$. Now move the 1s **from the last one to the first**: slide the last 1 right until it reaches its place, then the one before it, and so on. When we move the $k$-th 1, the later ones have already moved to the right of $q_k$, so the cells in between are all 0s. Each single step swaps `10` into `01`, which is a legal operation (choose just those two positions and sort them).

**Now the `?`.** For one query string `t`:

1. Count the fixed `1`s as `f` and the `?`s as `q`. We need exactly `r = K - f` of the `?` to become 1, where `K` is the number of 1s in `s`. If `r < 0` or `r > q`, the answer is false.
2. Which `?` should become 1? We want the prefix counts of 1s as **small** as possible, so put the 1s at the **last** `r` question marks and 0s at the first `q - r`. Every other choice with the same total only has more 1s early, so if this choice fails, every choice fails.
3. Walk through `t`, counting its 1s in a running variable. If it ever exceeds the number of 1s in `s[0..i]` (precomputed `onesS`), answer false.

**Examples.** `s = "1100"`, `K = 2`.

- `"11?1"`: fixed ones `f = 3 > K`, so false.
- `"1?1?"`: `f = 2`, `r = 0`, so both `?` become 0, giving `1010`. Running ones: 1, 1, 2, 2. Against `s`: 1, 2, 2, 2. All fit, so true.
- `"0011"`: ones 0, 0, 1, 2 against 1, 2, 2, 2. True.

```cpp
class Solution {
public:
    vector<bool> canTransform(string s, vector<string>& strs) {
        int n = s.size();
        vector<int> onesS(n + 1, 0);
        for (int i = 0; i < n; i++) onesS[i + 1] = onesS[i] + (s[i] == '1');
        int K = onesS[n];
        vector<bool> ans;
        for (auto& t : strs) {
            int fixedOnes = 0, q = 0;
            for (char c : t) {
                if (c == '1') fixedOnes++;
                if (c == '?') q++;
            }
            int r = K - fixedOnes;
            if (r < 0 || r > q) {
                ans.push_back(false);
                continue;
            }
            int zerosToPlace = q - r;
            int ones = 0;
            bool ok = true;
            for (int i = 0; i < n && ok; i++) {
                char c = t[i];
                if (c == '?') {
                    if (zerosToPlace > 0) zerosToPlace--;
                    else c = '1';
                    if (c == '?') c = '0';
                }
                if (c == '1') ones++;
                if (ones > onesS[i + 1]) ok = false;
            }
            ans.push_back(ok);
        }
        return ans;
    }
};
```

**Testing.** The three examples from the statement give `[true, true, false]`, `[true, false, true]`, `[true]`. Also compared against an exhaustive search (BFS over every string reachable by sorting any subsequence) for all `s` up to length 7 with random queries.

Time $O(n \cdot m)$ for $m$ query strings, about $4 \cdot 10^6$ steps. Space $O(n)$.
