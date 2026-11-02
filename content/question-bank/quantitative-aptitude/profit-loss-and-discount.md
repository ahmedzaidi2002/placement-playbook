---
title: "Profit, loss and discount"
weight: 10
---

9 questions asked by EPAM, EXL, NVIDIA, Qualcomm, Siemens Energy, Texas Instruments, Wells Fargo. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q21, tea blend and selling price

*Asked by: EPAM (EPAM freshers test)*

Tea worth Rs. 180 per kg is mixed with tea worth Rs. 300 per kg to achieve a 9.09%
profit when selling the blend at Rs. $P$ per kg. Which of these values cannot be $P$?

- **(a)** 200
- **(b)** 250
- **(c)** 300
- **(d)** 350

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 350**

**Why.** Any blend of tea at 180 and 300 per kg costs strictly between 180 and 300 per kg. A 9.09% profit is 1/11, so P = cost × 12/11, which lies between 180 × 12/11 ≈ 196.4 and 300 × 12/11 ≈ 327.3. 200, 250 and 300 are inside that range; 350 is not.

**Concept: a mixture's cost lies between its ingredients' costs.** The average of two prices (weighted by quantity) can never go outside them. Useful fraction: 9.09% = 1/11, so "profit 1/11" means multiply cost by 12/11.

{{< /details >}}

### 2 · chain of profits

*Asked by: EXL (HackerEarth test, 2025)*

A shopkeeper sold an article to a customer at a 10% profit. The customer sold it in an
exchange market to A at a 45% profit, and A sold it to B at a 30% profit for \$1220. What
can be said about the shopkeeper's cost price?

- **(a)** CP is 509
- **(b)** CP is more than 509
- **(c)** CP is less than 509
- **(d)** CP is 415

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) more than 509**

**Why.** Work backwards through the three sales: CP = 1220 ÷ (1.10 × 1.45 × 1.30) = 1220 ÷ 2.0735 ≈ 588.4, which is more than 509.

**Concept: chained profits multiply.** Each sale multiplies the price by (1 + profit%). To recover the original cost from the final price, divide by the product of all the multipliers.

{{< /details >}}

### 3 · Q7, selling apples

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

A shopkeeper bought apples at Rs 10 each. He sold 70% of them at Rs $2X$ each and the
rest at Rs $X$ each, making an overall profit of 36%. What is $X$?

- **(a)** 8
- **(b)** 9
- **(c)** 10
- **(d)** 10.5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 8**

**Why.** Per apple, average revenue = 0.7 × 2X + 0.3 × X = 1.7X. A 36% profit on Rs 10 means revenue Rs 13.6 per apple. 1.7X = 13.6, so X = 8.

**Concept: work per unit.** When fractions of a stock sell at different prices, the average selling price is the weighted average. Compare it with the cost per unit times (1 + profit%).

{{< /details >}}

### 4 · Q6, selling at 2/5 of cost

*Asked by: Qualcomm (Nov 2024 (HirePro))*

The cost price of a book is Rs 350; it is sold at $2/5$ times the cost price. What is the
profit or loss percentage?

- **(a)** 60% loss
- **(b)** 50% profit
- **(c)** 52% profit
- **(d)** 62% loss

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 60% loss**

**Why.** Selling at 2/5 of cost means SP = 0.4 × CP. Loss = CP − 0.4CP = 0.6CP, i.e. 60% of cost. (The Rs 350 is not needed.)

**Concept: profit/loss % is always on cost price.** Loss % = (CP − SP)/CP × 100. If SP = f × CP, the loss is (1 − f) × 100%.

{{< /details >}}

### 5 · Q9, same selling price

*Asked by: Qualcomm (Nov 2024)*

The selling prices of two articles are the same. In one transaction the trader made a
[cut off in the source] ... the entire transaction?

- **(a)** 3.72% Loss
- **(b)** 4.32% Loss
- **(c)** 4.10% Loss
- **(d)** 3.46% Profit

{{< details title="Answer and explanation" closed="true" >}}

**Answer: not determinable** (the percentages are cut off in the photo).

**The rule the question tests.** Two articles sold at the same price, one at x% gain and the other at x% loss, always give an overall **loss** of x²/100 %. For example, at 10% each way: loss = 1%. If the gain and loss percentages differ, compute each cost as SP/(1 + g) and SP/(1 − l), add the costs, and compare with 2 × SP.

**Concept: why equal gain and loss is a net loss.** The gain is taken on a smaller cost and the loss on a larger cost (because SP is the same), so the rupee loss is bigger than the rupee gain.

{{< /details >}}

### 6 · C2, selling price for 20 per cent profit

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A retailer bought 100 artifacts for \$7000 and paid an extra \$500 in transportation.
What should the selling price of each artifact be to make a 20% profit?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: \$90 per artifact**

**Why.** Total cost = 7000 + 500 transport = 7500. 20% profit means total revenue 7500 × 1.2 = 9000. Per artifact 9000/100 = 90.

**Concept: cost includes overheads.** Transport, tax and handling are part of the cost price. Apply the profit percentage to the full cost, then divide by the number of items.

{{< /details >}}

### 7 · mixing rice

*Asked by: Texas Instruments (IISc, second set)*

Bob mixes rice R1 and R2 in the ratio $4 : 7$ and sells at Rs. 17/kg at a 15% loss. R2
costs Rs. 22/kg. What does R1 cost?

- **(a)** Rs. 15
- **(b)** Rs. 16.5
- **(c)** Rs. 17
- **(d)** Rs. 17.5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Rs 16.5**

**Why.** Selling at 17 at a 15% loss means 17 = 0.85 × cost, so the mixture costs 20 per kg. 11 kg (4 + 7) cost 220: 4x + 7 × 22 = 220 → 4x = 66 → x = 16.5.

**Concept: find the mixture's cost price first.** A loss of 15% means SP = 0.85 × CP, so CP = SP/0.85. Then use "total cost = sum of ingredient costs" for the ratio given.

{{< /details >}}

### 8 · selling cloth

*Asked by: Wells Fargo (SHL test, Oct 2022)*

A man bought 400 metres of cloth for Rs 40{,}000 and sold it at Rs 200 per one and a half
metres. What was his percentage profit or loss?

- **(a)** 36% loss
- **(b)** 25% profit
- **(c)** 33% profit
- **(d)** 27% loss

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 33 1/3% profit**

**Why.** Cost = 40,000/400 = Rs 100 per metre. Selling price = 200 per 1.5 m = 133.33 per metre. Profit = 33.33/100 = 33 1/3%.

**Concept: bring both prices to the same unit.** Profit % only makes sense when cost and selling price refer to the same quantity, here one metre.

{{< /details >}}

### 9 · buy one get one free

*Asked by: Wells Fargo (SHL test, Oct 2022)*

A shopkeeper offers "Buy 1, Get 1 Free" on a T-shirt marked at Rs 2{,}400. If after a
sale the shopkeeper earns a profit of 33.33%, what is the actual (cost) price of one
T-shirt?

- **(a)** Rs. 900
- **(b)** Rs. 800
- **(c)** Rs. 1,200
- **(d)** Rs. 1,000
- **(e)** Rs. 1,500

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Rs 900**

**Why.** "Buy 1, get 1 free" sells two shirts for Rs 2400. A 33.33% profit (= 1/3) means 2400 = (4/3) × cost of two shirts, so two shirts cost 1800 and one costs 900.

**Concept: effective discount.** Buy 1 get 1 free is a 50% discount per item. Then SP = CP × (1 + profit%), so CP = SP ÷ (4/3). 33.33% = 1/3 is worth memorising.

{{< /details >}}
