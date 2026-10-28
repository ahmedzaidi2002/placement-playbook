---
title: "1945. Sum of Digits of String After Convert"
weight: 17
---

[LeetCode 1945](https://leetcode.com/problems/sum-of-digits-of-string-after-convert/) · Easy · Digit sum · Flipkart OA (related to Digit Sum of ASCII)

**Approach.** Turn each letter into its position `1..26` and write the numbers one after another. The first "transform" is the digit sum of that long digit string, which is just the sum of the digits of every letter's number (`v / 10 + v % 10`). Then repeat the digit-sum step $k-1$ more times on the resulting number.

```cpp
class Solution {
public:
    int getLucky(string s, int k) {
        int sum = 0;
        for (char ch : s) {
            int v = ch - 'a' + 1;
            sum += v / 10 + v % 10;
        }
        while (--k > 0) {
            int next = 0;
            while (sum) {
                next += sum % 10;
                sum /= 10;
            }
            sum = next;
        }
        return sum;
    }
};
```

Time $O(|s| + k)$, since after the first step the number is small. Space $O(1)$.
