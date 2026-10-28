---
title: "Digit Sum of ASCII"
weight: 16
---

Flipkart OA, 24 Oct 2026 (IIT Delhi) · Easy · Digit extraction · No public match found, solved from the reported statement

For each character of a string take its ASCII value, add the digits of that value, and return the total over the whole string.
Example: `hello` gives 104, 101, 108, 108, 111, digit sums 5, 2, 9, 9, 3, total 28.

**Approach.** Simulate it directly. For each character, convert to its integer code, then peel off digits with `% 10` and `/ 10` and add them to the total.

```cpp
class Solution {
public:
    int asciiDigitSum(string s) {
        int total = 0;
        for (char ch : s) {
            int v = (unsigned char)ch;
            while (v) {
                total += v % 10;
                v /= 10;
            }
        }
        return total;
    }
};
```

Time $O(|s|)$ since every ASCII code has at most 3 digits. Space $O(1)$.
