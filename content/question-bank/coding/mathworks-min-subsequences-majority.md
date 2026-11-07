---
aliases: ["/question-bank/mathworks-min-subsequences-majority/"]
title: "Minimum Subsequences With a Majority Element"
weight: 33
---

MathWorks OA · Hard · Counting argument, greedy on frequencies · The source had no constraints or example

**Problem.** Split an integer array into the **fewest subsequences** so that every subsequence has a *majority element*: a value that occurs strictly more than half the times in that subsequence. Every element goes into exactly one subsequence. Return the fewest subsequences.

**Order does not matter.** Whether a value is a majority depends only on how many times each value appears, not on the order. So a "subsequence" here is just a **group** of elements, and we are splitting the multiset into groups.

**A group needs a boss.** A group is valid when one value (the *boss*) has strictly more copies than **all the other elements of the group put together**. If the boss has $m$ copies, the group can hold at most $m - 1$ other elements, which we call *fillers*.

**The idea in easy words.**

1. Decide which $k$ values will be bosses, one group per boss. Put **all** copies of a boss value into its group (this only helps: it gives the group more capacity, and uses up elements).
2. Every element of a non-boss value is a filler. It can go into any group, since its value differs from that group's boss.
3. Group $j$ with $m_j$ boss copies absorbs up to $m_j - 1$ fillers. Over all groups that is $M - k$ fillers, where $M$ is the total number of boss copies.
4. Everything fits when the number of fillers $N - M$ is at most $M - k$, that is $2M - k \ge N$, or written per boss: $\sum_{\text{bosses}} (2 f_v - 1) \ge N$, where $f_v$ is the frequency of boss value $v$ and $N$ is the array length.

To satisfy this with as few bosses as possible, choose the **most frequent values** as bosses: sort frequencies from largest to smallest and add $2f - 1$ one value at a time. The answer is the first $k$ where the running total reaches $N$.

**Why more groups than bosses never helps.** Splitting a boss's copies into two groups creates a second group whose capacity is $m - 1$ smaller, so it can only absorb fewer fillers, and it costs one more group.

**Why it always ends.** If we make every distinct value a boss, there are no fillers and the sum is $2N - D \ge N$ ($D$ is the number of distinct values). So the answer is at most $D$.

**Worked examples.**

- `[1,1,1,2,3]`: $N = 5$, frequencies $3, 1, 1$. With $k = 1$: $2 \cdot 3 - 1 = 5 \ge 5$, so one group. Indeed 1 appears 3 times out of 5, which is more than half.
- `[1,1,2,2,3]`: $N = 5$, frequencies $2, 2, 1$. $k = 1$: $3 < 5$. $k = 2$: $3 + 3 = 6 \ge 5$, so 2 groups: `{1,1,3}` and `{2,2}`.
- `[1,2,3]`: every frequency is 1, so each step adds 1. We need $k = 3$: three groups of one element.

```cpp
class Solution {
public:
    int minSubsequences(vector<int>& a) {
        int n = a.size();
        unordered_map<int, int> cnt;
        for (int x : a) cnt[x]++;
        vector<int> f;
        for (auto& kv : cnt) f.push_back(kv.second);
        sort(f.rbegin(), f.rend());
        long long total = 0;
        for (int k = 0; k < (int)f.size(); k++) {
            total += 2LL * f[k] - 1;
            if (total >= n) return k + 1;
        }
        return f.size();
    }
};
```

**Testing.** Compared with a brute force that tries every way to split the array into groups (all set partitions), for 6000 random arrays up to 9 elements.

Time $O(n \log n)$ for sorting the frequencies. Space $O(n)$.
