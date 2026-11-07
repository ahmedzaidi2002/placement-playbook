---
aliases: ["/question-bank/mathworks-perfect-square-product-subarrays/"]
title: "Subarrays With a Perfect-Square Product"
weight: 24
---

MathWorks OA · Medium · Prime parity mask + prefix XOR + counting equal pairs

**Problem.** Given $n \le 10^5$ numbers with $a[i] \le 200$ (taken as positive), count the subarrays whose **product** is a perfect square.

**Key fact: a number is a perfect square exactly when every prime in it appears an even number of times.** So we do not need the product itself (it is huge). For each number we only need to know, for every prime, whether its exponent is **odd or even**.

**Step by step.**

1. There are only 46 primes up to 200, so one `unsigned long long` can hold one bit per prime. Bit $i$ is 1 if prime $i$ appears an **odd** number of times in the number. Example with primes 2, 3 as bits 0, 1: $6 = 2 \cdot 3$ gives `11`, $4 = 2^2$ gives `00`, $2$ gives `01`.
2. Multiplying numbers adds their exponents, so the parity masks combine with **XOR**. A subarray is a perfect square exactly when the XOR of its masks is 0.
3. Use prefix XORs: `pref[k]` is the XOR of the first `k` masks. The XOR of subarray `(l, r]` is `pref[r] ^ pref[l]`. It is 0 exactly when `pref[r] == pref[l]`.
4. So the answer is the number of pairs of equal prefix values. Keep a hash map of how many times each value has appeared. For every new prefix, add the count seen so far to the answer, then increase that count. Start with `freq[0] = 1` for the empty prefix.

**Worked example.** `a = [2, 3, 6, 4, 9]`.

| index | number | mask | prefix after it |
|---|---|---|---|
| start | | | 00 |
| 1 | 2 | 01 | 01 |
| 2 | 3 | 10 | 11 |
| 3 | 6 | 11 | 00 |
| 4 | 4 | 00 | 00 |
| 5 | 9 | 00 | 00 |

The prefix `00` appears 4 times, giving $\binom{4}{2} = 6$ pairs. `01` and `11` appear once each, no pairs. Answer 6, and indeed the good subarrays are `[2,3,6]` (36), `[4]`, `[9]`, `[4,9]` (36), `[2,3,6,4]` (144) and the whole array (1296).

```cpp
class Solution {
public:
    long long countSquareProductSubarrays(vector<int>& a) {
        vector<int> primes;
        for (int p = 2; p <= 200; p++) {
            bool isP = true;
            for (int d = 2; d * d <= p; d++) if (p % d == 0) isP = false;
            if (isP) primes.push_back(p);
        }
        int m = primes.size();
        vector<unsigned long long> maskOf(201, 0);
        for (int x = 1; x <= 200; x++) {
            int y = x;
            for (int i = 0; i < m; i++) {
                int cnt = 0;
                while (y % primes[i] == 0) {
                    y /= primes[i];
                    cnt++;
                }
                if (cnt % 2) maskOf[x] |= 1ULL << i;
            }
        }
        unordered_map<unsigned long long, long long> freq;
        unsigned long long pref = 0;
        freq[0] = 1;
        long long ans = 0;
        for (int x : a) {
            pref ^= maskOf[x];
            ans += freq[pref];
            freq[pref]++;
        }
        return ans;
    }
};
```

**Notes.**

- The answer can be about $n(n+1)/2 = 5 \cdot 10^9$, so it is `long long`.
- A value $0$ would make the product 0, a perfect square, and break this method. The statement says $a[i] \le 200$ and we assume positive numbers.
- Checked against a brute force that multiplies out prime exponents, for small values and for values up to 200.

Time $O(46 \cdot 200 + n)$, the factorisation table is built once. Space $O(n)$ for the hash map.
