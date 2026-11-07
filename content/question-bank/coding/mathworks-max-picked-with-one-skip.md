---
aliases: ["/question-bank/mathworks-max-picked-with-one-skip/"]
title: "Maximum Elements Picked With at Most One Skip"
weight: 25
---

MathWorks OA · Medium · Prefix sums, skip the biggest element

**Problem.** You have `arr` (positive integers) and a budget `k`. Go left to right from index 0. You may pick an element if it is at most your remaining budget, and picking subtracts its value from the budget. You may **skip at most one element** for free. If you meet an element you cannot afford and you have no skip left, everything stops. Find the maximum number of elements you can pick.

Example 1: `arr = [2,3,8,1,2], k = 8` gives 4 (pick 2, 3, skip 8, pick 1, 2). Example 2: `arr = [4,2,7,3,1], k = 10` gives 4.

**Assumption.** The statement says you *may* skip one element, so the skip can be used on an element even when you could afford it. Example: `arr = [5,1,1,1], k = 5`. Picking the 5 first ends with 1 pick, but skipping the 5 lets you pick all three 1s. If the real checker used "skip only when forced", it would give 1 here. On both given examples the two readings agree.

**Reformulate.** Decide **which one element is skipped** (or none). Once that is fixed, the rest is easy: you pick every other element in order until the budget runs out, and then you stop. Because all numbers are positive, "pick in order until you cannot" means *the longest prefix whose total fits in `k`*.

**The key observation.** Suppose the last element you handle is at index `j`, so you look at the prefix `arr[0..j]`.

- If you skip nothing, you pick all `j + 1` elements, valid when `prefix_sum <= k`.
- If you skip one element inside the prefix, you pick `j` elements, and the money you spend is `prefix_sum - skipped`. To spend as little as possible, skip the **largest** element of the prefix. So `prefix_sum - max_so_far <= k` is the best test.

**Step by step.**

1. Walk `j` from 0 to `n - 1`, keeping `sum` (total of `arr[0..j]`) and `mx` (biggest value so far).
2. If `sum - mx > k`, even the best skip is too expensive, and it will stay too expensive for longer prefixes, so **break**. (Adding an element never lowers `sum - mx`.)
3. Otherwise `ans = max(ans, j)`.
4. If also `sum <= k`, then `ans = max(ans, j + 1)`.

**Dry run, example 1** (`k = 8`).

| j | arr[j] | sum | mx | sum - mx | ans |
|---|---|---|---|---|---|
| 0 | 2 | 2 | 2 | 0 | 1 (sum 2 fits, so j + 1 = 1) |
| 1 | 3 | 5 | 3 | 2 | 2 (sum 5 fits) |
| 2 | 8 | 13 | 8 | 5 | 2 (skip the 8; sum does not fit) |
| 3 | 1 | 14 | 8 | 6 | 3 |
| 4 | 2 | 16 | 8 | 8 | 4 |

The answer is 4: skip the 8, spend 2 + 3 + 1 + 2 = 8.

```cpp
class Solution {
public:
    int maxPicked(vector<int>& arr, long long k) {
        int n = arr.size();
        long long sum = 0;
        int mx = 0, ans = 0;
        for (int j = 0; j < n; j++) {
            sum += arr[j];
            mx = max(mx, arr[j]);
            if (sum - mx > k) break;
            ans = max(ans, j);
            if (sum <= k) ans = max(ans, j + 1);
        }
        return ans;
    }
};
```

**Testing.** Compared with a brute force that tries every possible skipped index (and no skip) and simulates the process, on 30000 random small cases.

Time $O(n)$. Space $O(1)$.
