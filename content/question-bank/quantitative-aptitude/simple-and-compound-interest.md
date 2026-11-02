---
title: "Simple and compound interest"
weight: 14
---

6 questions asked by EPAM, EXL, Sigmoid, Texas Instruments, Wells Fargo. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q18, two loans and an average rate

*Asked by: EPAM (EPAM freshers test)*

Mr. Vijay Walia took two loans for one year: Rs. 12000 at 8.5% simple interest and an
unknown amount $X$ at 11.2%. If the average interest rate for both loans combined was
10%, what was $X$?

- **(a)** 12000
- **(b)** 15000
- **(c)** 16000
- **(d)** 15500

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 15000**

**Why.** Alligation: the 8.5% loan is 1.5 below the average and the 11.2% loan is 1.2 above it. Balance: 12000 × 1.5 = X × 1.2 → X = 15000.

**Concept: the weighted average balances deviations.** In a weighted average, (amount below × its distance) = (amount above × its distance), like a see-saw balancing at the mean.

{{< /details >}}

### 2 · depreciating car and compounding deposit

*Asked by: EXL (HackerEarth test, 2025)*

A sum is divided between Alice and Bob in the ratio 1:2. Alice buys a car with her part,
which depreciates 14.7% per annum; Bob deposits his part in a bank paying 20% per annum
compounded annually. By what percentage will the total sum increase after two years
(approximately)?

- **(a)** 3.36%
- **(b)** 1.66%
- **(c)** 3%
- **(d)** 7%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: none of the options with the numbers as photographed** (the question is flawed; the depreciation rate is printed as "147%", probably garbled).

**Why.** Split 3 units as 1 : 2. Alice's car after 2 years: 1 × (1 − 0.147)² = 0.7276. Bob's deposit: 2 × 1.2² = 2.88. Total 3.6076, up about 20.3%.

**Concept: compound growth and compound depreciation.** Value after n years = P(1 + r)ⁿ for growth and P(1 − r)ⁿ for depreciation. With several parts, compound each part separately, add them, and compare with the starting total.

{{< /details >}}

### 3 · interest reinvested in two funds

*Asked by: EXL (HackerEarth test, 2025)*

Mary Brown invested \$4000 in Fund A at 6% for 6 years. The interest earned is invested in
Funds B and C for 5 years in the ratio 1:2. The rate in Fund B is 8%, and the difference
between the simple interest from Funds C and B is \$288. What is the rate of interest for
Fund C?

- **(a)** 9
- **(b)** 10
- **(c)** 12
- **(d)** 15

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 10%**

**Why.**
1. Fund A interest: 4000 × 6% × 6 = 1440.
2. Split 1 : 2: 480 into B, 960 into C.
3. B earns 480 × 8% × 5 = 192, so C earns 192 + 288 = 480.
4. r_C = 480/(960 × 5) = 10%.

**Concept: simple interest SI = P × R × T / 100.** Interest is earned on the principal only. Rearranged: R = SI × 100/(P × T).

{{< /details >}}

### 4 · simple versus compound interest

*Asked by: Sigmoid (Campus hiring 2026)*

A sum is invested at 8% simple interest and the same sum at 10% compound interest
(annually). The difference between the interests after 2 years is Rs. 128. The sum is:

- **(a)** Rs. 12000
- **(b)** Rs. 12800
- **(c)** Rs. 16000
- **(d)** Rs. 18000

{{< details title="Answer and explanation" closed="true" >}}

**Answer: none of the options as printed** (with these numbers the sum is Rs 2560).

**Why.** In 2 years: SI at 8% = 0.16P. CI at 10% = (1.1² − 1)P = 0.21P. Difference 0.05P = 128 → P = 2560. If both rates were 10%, the difference would be 0.01P = 128 and P = 12,800, option (b); the question was probably garbled.

**Concept: CI vs SI.** Compound interest earns interest on interest. Over 2 years at the same rate r, CI − SI = P(r/100)², the interest on the first year's interest.

{{< /details >}}

### 5 · doubling money

*Asked by: Texas Instruments (IISc 2023)*

10 million at 40% a year compounded half-yearly. When does it double?

- **(a)** Exactly 2 years
- **(b)** More than 2 years
- **(c)** Slightly less than 2 years
- **(d)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) slightly less than 2 years** (the tick)

**Why.** 40% a year compounded half-yearly = 20% per half-year. After 3 half-years: 1.2³ = 1.728; after 4: 1.2⁴ = 2.0736. So the money passes double during the 4th half-year; if growth were continuous within it, the moment is 1.2ᵗ = 2 → t ≈ 3.8 half-years ≈ 1.9 years. (If interest is only credited at the end of each half-year, the balance first exceeds double exactly at 2 years.)

**Concept: compounding frequency.** With annual rate R compounded k times a year, each period uses rate R/k and there are k periods per year: A = P(1 + R/k)^(kn). More frequent compounding grows money slightly faster, so doubling comes a little sooner than at simple 40% (which would take 2.5 years).

{{< /details >}}

### 6 · simple interest

*Asked by: Wells Fargo (SHL test, Oct 2022)*

Kriti invested an amount; at the end of 3 years it was worth Rs 4{,}960, and at the end of
another 5 years it was worth Rs 5{,}600. What is the rate of interest, if interest is
earned only on the principal?

- **(a)** 12.50%
- **(b)** 8.33%
- **(c)** 8%
- **(d)** 4%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 8%** (reading "at the end of 5 years" as 5 years from the start)

**Why.** From year 3 to year 5 the amount grows by 5600 − 4960 = 640 in 2 years, so SI = 320 a year. Principal = 4960 − 3 × 320 = 4000. Rate = 320/4000 = 8%. (Read literally as 5 more years, the rate is 2.8%, not offered.)

**Concept: simple interest grows linearly.** Amount = P + P·R·T/100, a straight line in T. The rise between two dates gives the interest per year; going back to T = 0 gives the principal.

{{< /details >}}
