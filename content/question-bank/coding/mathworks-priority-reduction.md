---
aliases: ["/question-bank/mathworks-priority-reduction/"]
title: "Priority Reduction: Maximum Distinct Size"
weight: 32
---

MathWorks OA · Medium · Observation, parity

**Problem.** `arr` holds only the values 1, 2, 3 (low, medium, high priority). In one operation pick any three elements, find their minimum, maximum and middle (median) value, **remove the minimum and the maximum, and keep the middle one**. Each operation shrinks the array by 2. Find the largest possible size of the array such that **all remaining elements are distinct**.

Example: `[1,1,2,2,3]`, pick `(1,1,2)`: min 1, max 2, middle 1. Remove the min and max, keep 1, and the array becomes `[1,2,3]`, so the answer is 3.

**Observation 1: no new value can appear.** The kept element is always one of the three picked, so the values present at the end are a subset of the values present at the start. If the array has $d$ different values at the start ($d \in \{1, 2, 3\}$), then distinct elements at the end means **size at most $d$**.

**Observation 2: parity.** Every operation removes exactly 2 elements, so the final size has the **same parity as $n$**.

**The answer.** The best size is the largest number that is at most $d$ and has the same parity as $n$:

- if $n - d$ is even, the answer is $d$;
- otherwise the answer is $d - 1$.

When $d = 1$ and $n$ is even, this gives 0. The values can never become distinct (every element is the same value, and the array stays the same value with an odd size), so there is no valid array. The statement does not say what to return in that case. We return 0.

**Why $d$ is really reachable when $n - d$ is even.** The number of extra elements $n - d$ is even. If it is zero we are done. Otherwise one of two things is true:

- Some value $a$ appears at least 3 times. Pick three copies of $a$: min = max = $a$, we remove two and keep one. Two extras are gone, no value disappeared.
- Otherwise every value appears at most twice. The extras come one per doubled value, and an even number of them means at least two values $a, b$ appear twice. Pick $(a, a, b)$: we remove one $a$ and one $b$, and keep $a$. Both values still appear, and two extras are gone.

Repeat until no extras are left. The case $n - d$ odd and the final size $d - 1$ were checked by brute force rather than by hand: a search over **every** combination of counts of 1s, 2s and 3s for $n \le 11$ agrees with the formula on all 363 cases.

**Worked examples.**

- `[1,1,2,2,3]`: $n = 5$, $d = 3$, $n - d = 2$ is even, so the answer is 3.
- `[2,2,2,2]`: $n = 4$, $d = 1$, $n - d = 3$ is odd, so the answer is $d - 1 = 0$ (no valid way).
- `[1,2,2]`: $n = 3$, $d = 2$, $n - d = 1$ is odd, so the answer is 1. Indeed picking all three keeps one 2.

```cpp
class Solution {
public:
    int maxDistinctSize(vector<int>& arr) {
        int n = arr.size();
        bool has[4] = {false, false, false, false};
        for (int x : arr) has[x] = true;
        int d = has[1] + has[2] + has[3];
        if ((n - d) % 2 == 0) return d;
        return d - 1;
    }
};
```

**Testing.** Compared with an exhaustive search over every sequence of operations for 3000 random arrays up to 10 elements.

Time $O(n)$. Space $O(1)$.
