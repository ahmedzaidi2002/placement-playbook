---
aliases: ["/question-bank/mathworks-min-operations-power-of-two-groups/"]
title: "Minimum Operations to Empty the Array (Power-of-Two Sums)"
weight: 29
---

MathWorks OA · Hard · Binary representation, carrying · The source text is incomplete, so the formula is an assumption

**What the source says.** In one operation you pick any non-empty subset of the remaining array. For every picked element $x$ you compute a power of two, and the sum of those powers

$$2^{a_1} + 2^{a_2} + \dots + 2^{a_k} = 2^p, \quad p \ge 1$$

must itself be a power of 2. If so, the picked elements are removed. Find the minimum number of operations to empty the array, or $-1$ if impossible.

**What is missing.** The line that says *what to compute for each picked element* did not survive in the source, and so did the example. The solution below assumes the natural reading: **an element $x$ contributes $2^x$**, so $a_i = x_i$. The method depends only on the exponents $e_i$ each element contributes. If the real formula was some $f(x)$, first replace every element by $f(x)$ and then run the same code unchanged.

**The idea in easy words.** Think in binary. Let $T = \sum 2^{e_i}$ be the sum of everything.

1. We split the array into groups, and every group sum is a power of two (and at least $2$, because $p \ge 1$).
2. So $T$ is a sum of as many powers of two as there are groups. The fewest powers of two that add up to $T$ is the number of 1-bits of $T$. Therefore **the number of operations is at least `popcount(T)`**.
3. **That many is always enough.** Go through the bits of $T$ from the highest down. For each bit $2^b$, build one group by taking the biggest remaining elements until the sum is exactly $2^b$. Because every element is a power of two, taking the biggest ones first never overshoots and always lands exactly on the target.
4. **When is it impossible?** Every group sum is at least $2$, so it is even, so $T$ must be even. $T$ is even exactly when the number of elements with exponent $0$ (each equals 1) is **even**. If it is odd, print $-1$.

**Not computing the huge number.** The exponents can be large, so $T$ cannot be stored. But we only need its bits, and binary addition does the work for us: `cnt[k]` is how many elements have exponent `k`. Two copies of $2^k$ make one copy of $2^{k+1}$, so:

- bit `k` of $T$ is `cnt[k] % 2` (an odd leftover stays here, so one more group);
- carry `cnt[k] / 2` into `cnt[k + 1]`.

Go through the exponents in increasing order. The carries create only about $\log_2 n$ extra exponents.

**Worked examples.**

- `e = [1, 1, 2]`. The values are 2 + 2 + 4 = 8. `cnt[1] = 2` carries 1 to exponent 2, so `cnt[2] = 2`, carries 1 to exponent 3, which is odd and gives one group. Answer 1: a single group of everything.
- `e = [0, 0, 3, 1]`. The values are 1 + 1 + 8 + 2 = 12 = 8 + 4. Two copies of exponent 0 are even (no problem), carry to exponent 1, which becomes 2 copies, carry to exponent 2: one odd leftover (group 1). Exponent 3 has one copy (group 2). Answer 2: the groups are `{3}` and `{0, 0, 1}` (1 + 1 + 2 = 4).
- `e = [0, 5]`. One element with exponent 0 is odd. Answer $-1$.

```cpp
class Solution {
public:
    int minOperations(vector<long long>& e) {
        map<long long, long long> cnt;
        for (long long x : e) cnt[x]++;
        int ans = 0;
        for (auto it = cnt.begin(); it != cnt.end(); ++it) {
            long long k = it->first, c = it->second;
            if (c % 2 == 1) {
                if (k == 0) return -1;
                ans++;
            }
            if (c / 2 > 0) cnt[k + 1] += c / 2;
        }
        return ans;
    }
};
```

**Testing.** Compared with an exhaustive bitmask search (the fewest groups whose sum is a power of two at least 2) over 20000 random arrays of up to 9 elements with exponents 0 to 3. An array of exponents like $10^9$ works because we never build $T$.

Time $O(n \log n)$ for the map. Space $O(n)$.
