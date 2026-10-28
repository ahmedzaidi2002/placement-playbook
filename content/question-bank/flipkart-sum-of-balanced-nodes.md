---
title: "Sum of Balanced Nodes"
weight: 9
---

Flipkart OA, 24 Oct 2026 (IIT Delhi) · Medium · Tree DFS, subtree sums · Same problem as GeeksforGeeks [Sum of specially balanced nodes](https://www.geeksforgeeks.org/sum-of-specially-balanced-nodes-from-a-given-binary-tree/)

A node is balanced if the sum of its left subtree is even and the sum of its right subtree is odd, or the other way round. A node with one child or no child is not balanced. Return the sum of the values of all balanced nodes.
Example (level order `11 20 33 31 40 null 41`): the root (91 odd, 74 even) and node 20 (31 odd, 40 even) are balanced, so the answer is $11 + 20 = 31$.

**Approach.** A node's status depends only on the two subtree sums below it, so one postorder pass is enough. `solve(node)` returns the sum of the subtree rooted at `node`.
After computing the left sum `l` and right sum `r`, the node is balanced when both children exist and `l` and `r` have different parity, i.e. `(l ^ r) & 1`. Then add the node's own value to the answer. The subtree sum includes the child node itself, and `& 1` also gives the right parity for negative sums.

```cpp
class Solution {
public:
    long long solve(TreeNode* node, long long& ans) {
        if (!node) return 0;
        long long l = solve(node->left, ans);
        long long r = solve(node->right, ans);
        if (node->left && node->right && ((l ^ r) & 1)) ans += node->val;
        return l + r + node->val;
    }

    long long sumBalancedNodes(TreeNode* root) {
        long long ans = 0;
        solve(root, ans);
        return ans;
    }
};
```

Time $O(n)$. Space $O(h)$ for the recursion stack, where $h$ is the tree height. `TreeNode` is the usual LeetCode struct.

The report does not give constraints, so sums are kept in `long long`. A level-order input with `null` is built into a tree first, the same way LeetCode does it.
