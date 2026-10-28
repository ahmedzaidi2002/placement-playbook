---
title: "508. Most Frequent Subtree Sum"
weight: 12
---

[LeetCode 508](https://leetcode.com/problems/most-frequent-subtree-sum/) · Medium · Postorder + hash map · Flipkart OA (related to Sum of Balanced Nodes)

**Approach.** One postorder pass computes the subtree sum of every node. Count each sum in a hash map as it is produced. After the pass, return all sums whose count equals the maximum count (ties are all returned).

```cpp
class Solution {
public:
    int solve(TreeNode* node, unordered_map<int, int>& freq) {
        if (!node) return 0;
        int sum = solve(node->left, freq) + solve(node->right, freq) + node->val;
        freq[sum]++;
        return sum;
    }

    vector<int> findFrequentTreeSum(TreeNode* root) {
        unordered_map<int, int> freq;
        solve(root, freq);
        int best = 0;
        for (auto& p : freq) best = max(best, p.second);
        vector<int> ans;
        for (auto& p : freq) {
            if (p.second == best) ans.push_back(p.first);
        }
        return ans;
    }
};
```

Time $O(n)$. Space $O(n)$ for the map.
