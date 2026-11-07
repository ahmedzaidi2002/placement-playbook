---
aliases: ["/question-bank/mathworks-number-game/"]
title: "Number Game: Smallest String After Swaps"
weight: 31
---

MathWorks OA · Medium · Greedy with three queues

**Problem.** `S` contains only the digits `1`, `2`, `3`. You may repeat these moves: swap an adjacent `21` into `12`; swap an adjacent `32` into `23`. A `1` and a `3` can never be swapped. Return the smallest string you can reach. Example: `"321"` gives `"231"`, and `"2213"` gives `"1223"`.

**What can move where.** Look at the two moves again: in `21 -> 12` the 1 hops **left** over a 2, and in `32 -> 23` the 2 hops **left** over a 3. Nothing ever hops right on its own, and the reverse swaps are not allowed. So:

- a **1** can hop left over 2s, but is stopped by a 3 (and by another 1, which is the same digit, so it makes no difference);
- a **2** can hop left over 3s, but is stopped by a 1;
- a **3** can never hop left.

**The idea in easy words.** To get the smallest string, build the answer from left to right and at every step place the **smallest digit that is able to reach the front** of what is left. Placing a digit at the front costs nothing for the others, because the digits it jumped over keep their relative order.

For the digits still unplaced, look at the **first** copy of each digit:

1. **Digit 1** can reach the front if there is **no 3 before it**. (Only 2s are before it, and a 1 hops over 2s.)
2. Else **digit 2** can reach the front if there is **no 1 before it**. (Only 3s are before it, and a 2 hops over 3s.)
3. Else the front of the remaining string is a 3, so place **3**.

**Implementation.** Keep three lists with the positions of all 1s, 2s and 3s, and a pointer into each list. The first remaining copy of a digit is the one the pointer points at.

- Pick 1 if a 1 remains and its position is smaller than the position of the first remaining 3.
- Else pick 2 if a 2 remains and its position is smaller than the position of the first remaining 1.
- Else pick 3.

Move that pointer forward and add the digit to the answer.

**Dry run, `S = "321"`.** Positions: 3 at 0, 2 at 1, 1 at 2.

| step | first 1 | first 2 | first 3 | choice | why |
|---|---|---|---|---|---|
| 1 | 2 | 1 | 0 | 2 | the 1 has a 3 in front (0 < 2), but the 2 has no 1 in front (1 < 2) |
| 2 | 2 | none | 0 | 3 | the 1 still has the 3 in front, no 2 left, so 3 |
| 3 | 2 | none | none | 1 | only the 1 is left |

Result `231`. ✓

**Dry run, `S = "2213"`.** Positions: 2 at 0 and 1, 1 at 2, 3 at 3. Step 1: the first 1 (position 2) is before the first 3 (position 3), so place 1. Step 2: no 1 left; the first 2 has no 1 before it, so place 2, then 2 again, then 3. Result `1223`. ✓

```cpp
class Solution {
public:
    string numberGame(string s) {
        int n = s.size();
        vector<int> pos[4];
        for (int i = 0; i < n; i++) pos[s[i] - '0'].push_back(i);
        int p[4] = {0, 0, 0, 0};
        auto has = [&](int d) { return p[d] < (int)pos[d].size(); };
        auto front = [&](int d) { return has(d) ? pos[d][p[d]] : INT_MAX; };
        string ans;
        for (int step = 0; step < n; step++) {
            int pick;
            if (has(1) && front(1) < front(3)) pick = 1;
            else if (has(2) && front(2) < front(1)) pick = 2;
            else pick = 3;
            ans += char('0' + pick);
            p[pick]++;
        }
        return ans;
    }
};
```

**Testing.** Compared with an exhaustive search (BFS over every string reachable with the two allowed swaps, then the smallest) for 20000 random strings up to length 10.

Time $O(n)$. Space $O(n)$ for the position lists.
