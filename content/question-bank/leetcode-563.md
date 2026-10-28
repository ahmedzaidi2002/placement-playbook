---
title: "563. Binary Tree Tilt"
weight: 10
---

[LeetCode 563](https://leetcode.com/problems/binary-tree-tilt/) · Easy · Postorder subtree sums · Flipkart OA (related to Sum of Balanced Nodes)

**Approach.** The tilt of a node is $|\text{left sum} - \text{right sum}|$, so it needs the two subtree sums, the same postorder pass as Sum of Balanced Nodes. `solve` returns the subtree sum and adds the tilt of the current node to a running total.

```cpp
class Solution {
public:
    int solve(TreeNode* node, int& tilt) {
        if (!node) return 0;
        int l = solve(node->left, tilt);
        int r = solve(node->right, tilt);
        tilt += abs(l - r);
        return l + r + node->val;
    }

    int findTilt(TreeNode* root) {
        int tilt = 0;
        solve(root, tilt);
        return tilt;
    }
};
```

Time $O(n)$. Space $O(h)$ for the recursion stack.
