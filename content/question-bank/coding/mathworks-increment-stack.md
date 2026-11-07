---
aliases: ["/question-bank/mathworks-increment-stack/"]
title: "IncrementStack"
weight: 21
---

MathWorks OA · Medium · Design, lazy increments

**Problem.** Build a stack with `push(x)`, `pop()` (returns `-1` when empty) and `increment(i, v)`, which adds `v` to the **bottom `i` elements** (all of them if the stack has fewer than `i`). Every operation must be $O(1)$.

Example: push 10, 20, 30, then `increment(2, 5)` makes the stack `[15, 25, 30]`, and three pops give 30, 25, 15.

This is the known LeetCode 1381 "Design a Stack With Increment Operation". The only twist is that the stack is allowed to be unbounded.

**Why the obvious way is too slow.** `increment` could loop over `i` elements and add `v` to each one. With 2·10^5 calls that is far too much, so we must *not* touch the elements at increment time.

**The idea in easy words: write the bonus down, pay it later.** Keep a second array `add`, the same size as the stack. `add[k]` means: "every element from the bottom up to position `k` still has to receive this bonus."

- `increment(i, v)`: let `k = min(i, size)`. Write the bonus on slot `k - 1`: `add[k - 1] += v`. One write, $O(1)$. If `k` is 0 (empty stack), do nothing.
- `push(x)`: put `x` on the stack and a fresh `0` on `add`. A new element must not get old bonuses, and it does not, because old bonuses are written on lower slots.
- `pop()`: the top element's real value is `st[top] + add[top]`. Before removing it, hand its bonus to the element underneath: `add[top - 1] += add[top]`. The bonus said "this slot **and everything below it**", so the elements below must still receive it.

**Dry run.**

| operation | st | add | result |
|---|---|---|---|
| push 10, 20, 30 | [10, 20, 30] | [0, 0, 0] | |
| increment(2, 5) | [10, 20, 30] | [0, 5, 0] | |
| pop | top is 30, 30 + 0 = 30, pass 0 down | st [10, 20], add [0, 5] | 30 |
| pop | top is 20, 20 + 5 = 25, pass 5 down | st [10], add [5] | 25 |
| pop | top is 10, 10 + 5 = 15 | empty | 15 |
| pop | empty | | -1 |

```cpp
class IncrementStack {
public:
    vector<int> st;
    vector<long long> add;

    IncrementStack() {}

    void push(int x) {
        st.push_back(x);
        add.push_back(0);
    }

    int pop() {
        if (st.empty()) return -1;
        int n = st.size();
        long long val = st[n - 1] + add[n - 1];
        if (n >= 2) add[n - 2] += add[n - 1];
        st.pop_back();
        add.pop_back();
        return val;
    }

    void increment(int i, int v) {
        int k = min(i, (int)st.size());
        if (k > 0) add[k - 1] += v;
    }
};
```

**Careful with size.** After 2·10^5 increments of up to 10^5 the sum can reach about 2·10^10, which does not fit in `int`. So `add` is `long long`. The required return type is `int`, so if the checker really has such values, return `long long` instead.

Time $O(1)$ for every operation. Space $O(n)$ for the elements on the stack.
