---
title: "1281. Subtract the Product and Sum of Digits of an Integer"
weight: 19
---

[LeetCode 1281](https://leetcode.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer/) · Easy · Digit extraction · Flipkart OA (related to Digit Sum of ASCII)

**Approach.** Peel digits off with `% 10` and `/ 10`, keeping a running product (start at 1) and a running sum (start at 0). Return `product - sum`.

```cpp
class Solution {
public:
    int subtractProductAndSum(int n) {
        int product = 1, sum = 0;
        while (n) {
            int d = n % 10;
            product *= d;
            sum += d;
            n /= 10;
        }
        return product - sum;
    }
};
```

Time $O(\log_{10} n)$. Space $O(1)$.
