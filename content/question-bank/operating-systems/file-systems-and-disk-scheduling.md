---
title: "File systems and disk scheduling"
weight: 7
---

1 question asked by Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Disk scheduling

*Asked by: Qualcomm (IISc 2024, Q34)*

A disk driver receives requests for cylinders in the order 67, 45, 22, 180, 112, 95, 77, 69, 66, 55, 10. C-SCAN is used, where each seek … (the rest of the sentence is cut off in the photo). The head is currently at cylinder 30. What is the total seek time?

- **(a)** 558 ms
- **(b)** 1096 ms
- **(c)** 996 ms
- **(d)** 408 ms

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (the time per cylinder and the disk size are cut off in the photo)

**Why.** The service order is clear. Moving up from 30, C-SCAN serves 45, 55, 66, 67, 69, 77, 95, 112, 180, then jumps back to the low end and serves 10 and 22.
- Counting only cylinders crossed while serving: 30 → 180 = 150, wrap 180 → 10 = 170, 10 → 22 = 12, total 332; at 3 ms per cylinder that is 996 ms (option (c)).
- If the head runs to the last cylinder (199) and the return to 0 counts: 169 + 199 + 22 = 390 cylinders.

**Concept: C-SCAN disk scheduling.** The head sweeps in one direction serving requests, then returns to the other end without serving on the way back, and sweeps again. It gives more uniform waiting times than SCAN, which serves in both directions.

{{< /details >}}
