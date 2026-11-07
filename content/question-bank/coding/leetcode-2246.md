---
aliases: ["/question-bank/leetcode-2246/"]
title: "2246. Longest Path With Different Adjacent Characters"
weight: 27
---

[LeetCode 2246](https://leetcode.com/problems/longest-path-with-different-adjacent-characters/) · Hard · Tree DFS, best two children · MathWorks OA

**Problem.** A tree is rooted at node 0 and given by `parent[]`. Each node has a letter in `s`. Return the length of the longest path (counted in **nodes**) where no two neighbouring nodes on the path have the same letter. In example 1, the path `0 -> 1 -> 3` has length 3.

**The idea in easy words.** Every path in a tree has one **highest node**, the node closest to the root. From that node the path goes down along at most two different children. So for every node `u`, ask: "what is the best path whose highest node is `u`?" and take the maximum over all `u`.

**What each node reports.** Let `dfs(u)` return the length of the longest valid path that starts at `u` and only goes **downwards**, counted in nodes.

1. Look at every child `v`. First compute `len = dfs(v)`.
2. If `s[v] == s[u]`, we cannot step from `u` to `v`, so ignore this child.
3. Otherwise `len` is a usable branch. Keep the two largest usable branches, `top1 >= top2` (both start at 0).
4. The best path with `u` as its highest node joins the two best branches: `top1 + top2 + 1` nodes (the `+1` is `u` itself). Update the global `best`.
5. `u` reports `top1 + 1` to its parent, because a path continuing upwards can use only one branch.

Note the `dfs(v)` call is made **before** the letter check, so deeper nodes are still processed even when the edge to `v` is not usable.

**Dry run, example 1.** `parent = [-1,0,0,1,1,2]`, `s = "abacbe"`. Tree: 0 has children 1, 2; node 1 has children 3, 4; node 2 has child 5.

| node | letter | usable child branches | top1, top2 | path through node | returns |
|---|---|---|---|---|---|
| 3 | c | none | 0, 0 | 1 | 1 |
| 4 | b | none | 0, 0 | 1 | 1 |
| 1 | b | child 3 (c is not b): 1; child 4 (b equals b): ignored | 1, 0 | 2 | 2 |
| 5 | e | none | 0, 0 | 1 | 1 |
| 2 | a | child 5 (e is not a): 1 | 1, 0 | 2 | 2 |
| 0 | a | child 1 (b): 2; child 2 (a equals a): ignored | 2, 0 | 3 | 3 |

The answer is 3.

```cpp
class Solution {
public:
    vector<vector<int>> kids;
    int best;

    int dfs(int u, string& s) {
        int top1 = 0, top2 = 0;
        for (int v : kids[u]) {
            int len = dfs(v, s);
            if (s[v] == s[u]) continue;
            if (len > top1) {
                top2 = top1;
                top1 = len;
            } else if (len > top2) {
                top2 = len;
            }
        }
        best = max(best, top1 + top2 + 1);
        return top1 + 1;
    }

    int longestPath(vector<int>& parent, string s) {
        int n = parent.size();
        kids.assign(n, {});
        for (int i = 1; i < n; i++) kids[parent[i]].push_back(i);
        best = 1;
        dfs(0, s);
        return best;
    }
};
```

**Testing.** Both examples give 3. Compared with a brute force that tries every simple path from every start node, on 5000 random trees with up to 10 nodes.

**If the tree is a very long chain.** The recursion can go $10^5$ levels deep, which is fine on LeetCode. If you worry about stack overflow, use the iterative order from the next problem (process nodes in reverse BFS order).

Time $O(n)$, every node and edge is visited once. Space $O(n)$ for the child lists and the recursion stack.
