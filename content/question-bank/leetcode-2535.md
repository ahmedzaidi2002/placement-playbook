---
title: "2535. Difference Between Element Sum and Digit Sum of an Array"
weight: 18
---

[LeetCode 2535](https://leetcode.com/problems/difference-between-element-sum-and-digit-sum-of-an-array/) · Easy · Digit extraction · Flipkart OA (related to Digit Sum of ASCII)

**Approach.** In one pass keep two totals: the sum of the elements, and the sum of all their digits taken with `% 10` and `/ 10`. Return the absolute difference.

```cpp
class Solution {
public:
    int differenceOfSum(vector<int>& nums) {
        int elementSum = 0, digitSum = 0;
        for (int x : nums) {
            elementSum += x;
            while (x) {
                digitSum += x % 10;
                x /= 10;
            }
        }
        return abs(elementSum - digitSum);
    }
};
```

Time $O(n \log_{10} V)$ for the largest value $V$. Space $O(1)$.
