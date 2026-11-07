---
title: Coding problems
weight: 100
---


Coding questions with a 2-3 line approach and a direct solution. The code has no comments, in C++17 `class Solution` style. Each solution was compiled and checked against a brute force on small random inputs.

The 14 **MathWorks OA** problems (rows 20 to 33) have a longer explanation: the problem restated, the idea in easy words, step by step, a dry run, then the code. Where the report was incomplete (rows 22, 28, 29, 30, 33) the page says what was assumed.

| # | Problem | Platform | Level | Pattern | Source |
|---|---|---|---|---|---|
| 1 | [Shortest Path Visiting All Nodes](leetcode-847) | LeetCode 847 | Hard | BFS on (node, mask) | Spotnana Q1 (related), Flipkart Monica and Her Shifts (related) |
| 2 | [Minimum Time to Collect All Apples in a Tree](leetcode-1443) | LeetCode 1443 | Medium | Tree DFS | Spotnana Q1 (related) |
| 3 | [Minimum Time to Complete All Tasks](leetcode-2589) | LeetCode 2589 | Hard | Greedy by end time | Spotnana Q5 |
| 4 | [K-th Largest Sum Contiguous Subarray](gfg-kth-largest-subarray-sum) | GeeksforGeeks | Medium | Min-heap of size k | Spotnana Q6 |
| 5 | [Super M](codeforces-592d) | Codeforces 592D | 2200 | Tree diameter | Added |
| 6 | [Maximum Profit with OR at Most K](recalled-or-subset-profit) | Recalled | Medium | Candidate masks | Recalled interview question |
| 7 | [Subsequence With the Minimum Score](leetcode-2565) | LeetCode 2565 | Hard | Prefix + suffix, two pointers | Recalled interview question |
| 8 | [Minimum Tree Depth After K Reattachments](recalled-reattach-tree-depth) | Recalled | Hard | Binary search + tree greedy | Recalled interview question |
| 9 | [Sum of Balanced Nodes](flipkart-sum-of-balanced-nodes) | Flipkart OA | Medium | Postorder subtree sums | Flipkart OA, 24 Oct 2026 (IIT Delhi) |
| 10 | [Binary Tree Tilt](leetcode-563) | LeetCode 563 | Easy | Postorder subtree sums | Flipkart OA (related to Sum of Balanced Nodes) |
| 11 | [Count Nodes Equal to Average of Subtree](leetcode-2265) | LeetCode 2265 | Medium | Postorder (sum, count) | Flipkart OA (related to Sum of Balanced Nodes) |
| 12 | [Most Frequent Subtree Sum](leetcode-508) | LeetCode 508 | Medium | Postorder + hash map | Flipkart OA (related to Sum of Balanced Nodes) |
| 13 | [Monica and Her Shifts](flipkart-monica-and-her-shifts) | Flipkart OA | Hard | Bitmask DP over sites | Flipkart OA, 24 Oct 2026 (IIT Delhi) |
| 14 | [Shortest Path to Get All Keys](leetcode-864) | LeetCode 864 | Hard | BFS on (cell, keys mask) | Flipkart OA (related to Monica and Her Shifts) |
| 15 | [Unique Paths III](leetcode-980) | LeetCode 980 | Hard | Backtracking | Flipkart OA (related to Monica and Her Shifts) |
| 16 | [Digit Sum of ASCII](flipkart-digit-sum-of-ascii) | Flipkart OA | Easy | Digit extraction | Flipkart OA, 24 Oct 2026 (IIT Delhi) |
| 17 | [Sum of Digits of String After Convert](leetcode-1945) | LeetCode 1945 | Easy | Digit sum | Flipkart OA (related to Digit Sum of ASCII) |
| 18 | [Difference Between Element Sum and Digit Sum of an Array](leetcode-2535) | LeetCode 2535 | Easy | Digit extraction | Flipkart OA (related to Digit Sum of ASCII) |
| 19 | [Subtract the Product and Sum of Digits of an Integer](leetcode-1281) | LeetCode 1281 | Easy | Digit extraction | Flipkart OA (related to Digit Sum of ASCII) |
| 20 | [IP Address Request Filter](mathworks-ip-request-filter) | MathWorks OA | Medium | Wildcard match + sliding window per IP | MathWorks OA |
| 21 | [IncrementStack](mathworks-increment-stack) | MathWorks OA | Medium | Lazy increments | MathWorks OA |
| 22 | [Minimum Deletions to Make a String Beautiful](mathworks-min-deletions-beautiful-string) | MathWorks OA | Medium | Greedy, non-overlapping pairs | MathWorks OA (no constraints given) |
| 23 | [Closest Pair of Points (Uniformly Distributed)](mathworks-closest-pair-uniform-points) | MathWorks OA | Hard | Grid bucketing | MathWorks OA |
| 24 | [Subarrays With a Perfect-Square Product](mathworks-perfect-square-product-subarrays) | MathWorks OA | Medium | Prime parity mask + prefix XOR | MathWorks OA |
| 25 | [Maximum Elements Picked With at Most One Skip](mathworks-max-picked-with-one-skip) | MathWorks OA | Medium | Prefix sums, skip the largest | MathWorks OA |
| 26 | [Transform Binary String Using Subsequence Sort](leetcode-3998) | LeetCode 3998 | Medium | Prefix counts of ones | MathWorks OA |
| 27 | [Longest Path With Different Adjacent Characters](leetcode-2246) | LeetCode 2246 | Hard | Tree DFS, best two children | MathWorks OA |
| 28 | [Longest Path in a Tree With a Frequency Constraint](mathworks-longest-path-frequency-tree) | MathWorks OA | Medium | Tree diameter after cutting edges | MathWorks OA (statement reconstructed) |
| 29 | [Minimum Operations to Empty the Array (Power-of-Two Sums)](mathworks-min-operations-power-of-two-groups) | MathWorks OA | Hard | Binary carrying, popcount | MathWorks OA (formula missing, assumed) |
| 30 | [Count Subsets Whose OR Is Not in the Subset](mathworks-count-subsets-or-not-present) | MathWorks OA | Hard | Complement + SOS DP | MathWorks OA (no constraints given) |
| 31 | [Number Game: Smallest String After Swaps](mathworks-number-game) | MathWorks OA | Medium | Greedy with three queues | MathWorks OA |
| 32 | [Priority Reduction: Maximum Distinct Size](mathworks-priority-reduction) | MathWorks OA | Medium | Observation, parity | MathWorks OA |
| 33 | [Minimum Subsequences With a Majority Element](mathworks-min-subsequences-majority) | MathWorks OA | Hard | Frequencies, greedy bosses | MathWorks OA (no constraints given) |
