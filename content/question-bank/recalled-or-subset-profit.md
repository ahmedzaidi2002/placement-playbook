---
title: "Maximum Profit with OR at Most K"
weight: 6
---

Recalled interview question · Medium · Bitmask

Two arrays `indicator` and `profit` of size `n` and an integer `K`. Select some indices so that the bitwise OR of their `indicator` values is $\le K$, and maximise the total profit. $1 \le n \le 10^5$, $1 \le K \le 2^{30}$.

**Approach.** If the chosen OR is `X` with $X \le K$, every chosen element is a submask of `X`, and any set of submasks of `X` has OR $\le X$. So the answer is the best total over elements that are submasks of some `X <= K`.
Only 31 such masks matter: `K` itself, and for each set bit `b` of `K`, the mask with bit `b` cleared and all lower bits set. Every other `X <= K` is a submask of one of these. For each candidate sum the profits of elements with `(a & ~mask) == 0` and keep the maximum.

```cpp
class Solution {
public:
    long long maxProfit(vector<int>& indicator, vector<int>& profit, int K) {
        int n = indicator.size();
        vector<int> cand;
        cand.push_back(K);
        for (int b = 30; b >= 0; b--) {
            if ((K >> b) & 1) cand.push_back((K ^ (1 << b)) | ((1 << b) - 1));
        }
        long long ans = 0;
        for (int mask : cand) {
            long long sum = 0;
            for (int i = 0; i < n; i++) {
                if ((indicator[i] & ~mask) == 0 && profit[i] > 0) sum += profit[i];
            }
            ans = max(ans, sum);
        }
        return ans;
    }
};
```

Time $O(31 \cdot n)$. Space $O(1)$ apart from the candidate list.

The signature is made up, since the original was recalled without one. Profits that are zero or negative are never taken, so the empty selection gives 0. If the original forces at least one element, handle the all-negative case separately. This problem is not matched to a known platform problem, so there is no link.
