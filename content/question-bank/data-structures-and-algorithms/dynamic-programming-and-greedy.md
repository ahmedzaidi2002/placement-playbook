---
title: "Dynamic programming and greedy"
weight: 9
---

1 question asked by Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · TSP with an unreachable city

*Asked by: Texas Instruments (IIT ISM 2024)*

In the DP for the travelling salesman, what happens if city $k$ is unreachable?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: the cost becomes infinite** (no valid tour exists)

**Why.** In the TSP dynamic program, unreachable edges have weight ∞. Any tour must visit city k, so every candidate tour includes an ∞ edge, and the minimum stays ∞.

**Concept: Held–Karp DP.** dp[S][j] = cheapest path that starts at the origin, visits exactly the set S and ends at j. Missing edges are modelled as ∞, so they are never chosen unless there is no alternative. Time O(n² 2ⁿ).

{{< /details >}}
