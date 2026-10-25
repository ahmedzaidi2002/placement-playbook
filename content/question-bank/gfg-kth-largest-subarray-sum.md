---
title: "K-th Largest Sum Contiguous Subarray"
weight: 4
---

[GeeksforGeeks](https://www.geeksforgeeks.org/problems/k-th-largest-sum-contiguous-subarray/1) · Medium · Heap

**Approach.** Generate every subarray sum by fixing the left end and extending the right end with a running sum. Keep a min-heap of size `k` holding the `k` largest sums seen so far.
A new sum enters only if it beats the heap top, so after all sums are processed the top is the k-th largest. This fits the limit $n \le 1000$.

```cpp
class Solution {
public:
    int kthLargest(vector<int>& arr, int k) {
        int n = arr.size();
        priority_queue<int, vector<int>, greater<int>> pq;
        for (int i = 0; i < n; i++) {
            int sum = 0;
            for (int j = i; j < n; j++) {
                sum += arr[j];
                if ((int)pq.size() < k) pq.push(sum);
                else if (sum > pq.top()) {
                    pq.pop();
                    pq.push(sum);
                }
            }
        }
        return pq.top();
    }
};
```

Time $O(n^2 \log k)$. Space $O(k)$.

The signature is the usual GeeksforGeeks one and was not confirmed against the site. Rename the method and parameters to match the editor if they differ.
