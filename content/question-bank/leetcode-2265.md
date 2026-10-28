---
title: "2265. Count Nodes Equal to Average of Subtree"
weight: 11
---

[LeetCode 2265](https://leetcode.com/problems/count-nodes-equal-to-average-of-subtree/) · Medium · Postorder (sum, count) · Flipkart OA (related to Sum of Balanced Nodes)

**Approach.** A node counts when its value equals the integer average (rounded down) of its subtree. So each call returns two things, the subtree sum and the subtree node count. The node counts when `sum / count == node->val`.

```cpp
class Solution {
public:
    pair<int, int> solve(TreeNode* node, int& ans) {
        if (!node) return {0, 0};
        pair<int, int> l = solve(node->left, ans);
        pair<int, int> r = solve(node->right, ans);
        int sum = l.first + r.first + node->val;
        int cnt = l.second + r.second + 1;
        if (sum / cnt == node->val) ans++;
        return {sum, cnt};
    }

    int averageOfSubtree(TreeNode* root) {
        int ans = 0;
        solve(root, ans);
        return ans;
    }
};
```

Time $O(n)$. Space $O(h)$.
