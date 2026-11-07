---
aliases: ["/question-bank/mathworks-count-subsets-or-not-present/"]
title: "Count Subsets Whose OR Is Not in the Subset"
weight: 30
---

MathWorks OA · Hard · Complement counting + sum over submasks · The source had no constraints or example, so some choices below are assumptions

**Problem.** Take every non-empty subset of an array. Compute the bitwise OR of its elements. If that OR value is **one of the elements of the subset**, the subset is *not* counted. Otherwise it is *valid*. Return the number of valid subsets.

**Assumptions.** We count valid subsets, the answer is taken modulo $10^9 + 7$ (the count can be as large as $2^n$), and the values are below $2^{20}$ so a 20-bit table is fine. If the real limits are different, only the table size changes.

**Step 1: count the bad ones instead.** It is easier to count subsets whose OR **is** present and subtract from $2^n - 1$.

**Step 2: what does a bad subset look like?** The OR of a set is at least as large as every element. So if the OR equals some element, that element must be the **largest** one, call it $v$. The OR equals $v$ exactly when every other element is a **submask** of $v$ (all its 1-bits are also 1-bits of $v$). So:

> a subset is bad exactly when all its elements are submasks of its maximum $v$, and $v$ itself is in the subset.

**Step 3: count bad subsets with maximum value $v$.** Let $c_v$ be how many times $v$ appears, and let $m_v$ be the number of elements that are *proper* submasks of $v$ (submasks different from $v$, so smaller than $v$).

- Choose at least one copy of $v$: $2^{c_v} - 1$ ways.
- Choose anything from the $m_v$ smaller submasks: $2^{m_v}$ ways.

Bad subsets for $v$: $(2^{c_v} - 1) \cdot 2^{m_v}$. Different $v$ never overlap, because the maximum is unique. Sum over all distinct $v$.

**Step 4: how to get $m_v$ fast.** We need, for every value, how many array elements are submasks of it. This is the standard *sum over subsets* (SOS) table: start with `sub[mask] = how many elements equal mask`, then for every bit `b`, for every `mask` that has bit `b` set, do `sub[mask] += sub[mask without bit b]`. Afterwards `sub[v]` counts all elements that are submasks of `v`, including the $c_v$ copies of $v$, so $m_v = \text{sub}[v] - c_v$. This costs $O(2^B \cdot B)$ for $B$ bits.

**Answer** = $(2^n - 1) - \sum_v (2^{c_v} - 1) \cdot 2^{m_v}$ (all modulo $10^9 + 7$).

**Worked example.** `a = [1, 2, 3]`. Subsets: `{1}`, `{2}`, `{3}` have OR equal to themselves, bad. `{1,2}` has OR 3, which is not in it, valid. `{1,3}` and `{2,3}` and `{1,2,3}` have OR 3, which is present, bad. Valid = 1. By the formula: total = 7. For $v = 1$: $c = 1$, submasks of 1 below it: none, so $(2-1) \cdot 2^0 = 1$. For $v = 2$: also 1. For $v = 3$: $c = 1$, proper submasks of 3 in the array are 1 and 2, so $m = 2$ and $(2-1) \cdot 2^2 = 4$. Bad = 6, valid = $7 - 6 = 1$. ✓

The value 0 is handled too: $0$ is a submask of everything, a subset of zeros has OR 0 which is present, so it is bad. Example: `{0, 1}` has OR 1, present, bad; it is counted under $v = 1$.

```cpp
class Solution {
public:
    int countValidSubsets(vector<int>& a) {
        const long long MOD = 1000000007LL;
        int n = a.size();
        int B = 1;
        int mx = *max_element(a.begin(), a.end());
        while ((1 << B) <= mx) B++;
        int size = 1 << B;
        vector<long long> cnt(size, 0), sub(size, 0);
        for (int x : a) cnt[x]++;
        sub = cnt;
        for (int b = 0; b < B; b++) {
            for (int mask = 0; mask < size; mask++) {
                if (mask >> b & 1) sub[mask] += sub[mask ^ (1 << b)];
            }
        }
        vector<long long> pw(n + 1, 1);
        for (int i = 1; i <= n; i++) pw[i] = pw[i - 1] * 2 % MOD;
        long long bad = 0;
        for (int v = 0; v < size; v++) {
            if (cnt[v] == 0) continue;
            long long withV = (pw[cnt[v]] - 1 + MOD) % MOD;
            long long others = pw[sub[v] - cnt[v]];
            bad = (bad + withV * others) % MOD;
        }
        long long total = (pw[n] - 1 + MOD) % MOD;
        return (total - bad + MOD) % MOD;
    }
};
```

**Testing.** Compared with a brute force over all subsets for 20000 random arrays of up to 12 elements (values below 4, 16 and 40). A random array of $10^5$ values below $2^{20}$ runs instantly.

Time $O(2^B \cdot B + n)$. Space $O(2^B + n)$.
