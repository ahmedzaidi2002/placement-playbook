---
aliases: ["/question-bank/mathworks-min-deletions-beautiful-string/"]
title: "Minimum Deletions to Make a String Beautiful"
weight: 22
---

MathWorks OA · Medium · Greedy, non-overlapping pairs · The source had no constraints or examples, so $n \le 10^5$ is assumed

**Problem.** Delete as few characters as possible from a lowercase string so that what is left is *beautiful*: its length is even and, cutting it into pairs `(s[0], s[1]), (s[2], s[3]), ...`, the two letters of every pair are equal. For example `bbaa` is beautiful, `abba` is not.

**Turn it around.** What remains looks like `c1 c1 c2 c2 c3 c3 ...`. If the answer keeps $p$ pairs, it deletes exactly $n - 2p$ characters. So we do not minimise deletions, we **maximise the number of pairs** $p$.

A pair is two positions $i < j$ with `s[i] == s[j]`. Pairs must come one after the other: all of pair 1 is before all of pair 2, and so on. Whatever lies between $i$ and $j$ is deleted. So each pair is an *interval* $[i, j]$ with equal end letters, and the intervals must not overlap.

> Pick the largest number of non-overlapping intervals whose two ends hold the same letter.

**This is classic interval scheduling.** To fit the most intervals, always finish the interval that **ends earliest**, because that leaves the most room for the next ones.

**Step by step.**

1. Keep a set of the letters seen since the last finished pair (26 letters, so an integer bitmask).
2. Read the next letter. If it is already in the set, we have found the earliest possible end of a pair. Count `pairs++` and **clear the set**.
3. Otherwise add the letter to the set.
4. Answer = `n - 2 * pairs`.

**Why not "keep one letter waiting"?** The first idea that comes to mind is: hold the first letter, and delete everything until the same letter turns up. That is wrong. On `abbaa` it holds `a`, deletes both `b` and then pairs `aa`, keeping 2 letters and deleting 3. The best is `bbaa`, deleting only the first `a`. Clearing the *set* (not a single waiting letter) is what fixes this.

**Dry run on `abbaa`.**

| letter | set before | action | set after | pairs |
|---|---|---|---|---|
| a | {} | add | {a} | 0 |
| b | {a} | add | {a, b} | 0 |
| b | {a, b} | found, close a pair | {} | 1 |
| a | {} | add | {a} | 1 |
| a | {a} | found, close a pair | {} | 2 |

Answer = 5 - 2·2 = 1.

```cpp
class Solution {
public:
    int minDeletions(string s) {
        int n = s.size();
        int seen = 0, pairs = 0;
        for (char ch : s) {
            int bit = 1 << (ch - 'a');
            if (seen & bit) {
                pairs++;
                seen = 0;
            } else {
                seen |= bit;
            }
        }
        return n - 2 * pairs;
    }
};
```

Checked against a brute force that tries every subsequence for all strings up to length 13.

Time $O(n)$. Space $O(1)$, the set is one 26-bit integer.
