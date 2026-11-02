---
title: "Data interpretation (tables, charts)"
weight: 1
---

32 questions asked by EPAM, EXL, Flipkart, JSW, Oracle, Qualcomm, Sigmoid, Texas Instruments, Wells Fargo. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q10, total production in region R2, 2023

*Asked by: EPAM (EPAM freshers test)*

Production in tons. 2022: R1 wheat 500, rice 400, maize 300; R2 wheat 600, rice 800,
maize 500. 2023: R1 wheat 550, rice 450, maize 350; R2 wheat 650, rice 600, maize 400.
What is the total production in region R2 in 2023?

- **(a)** 1550
- **(b)** 1650
- **(c)** 1750
- **(d)** 1850

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1650**

**Why.** Region R2 in 2023: wheat 650 + rice 600 + maize 400 = 1650 tons.

**Concept: read the exact cell.** Data-interpretation questions often give two years and two regions so that a careless read picks the wrong row (R2 in 2022 totals 1900). Underline the year and region asked before adding.

{{< /details >}}

### 2 · Q17, highly literate cities

*Asked by: EPAM (EPAM freshers test)*

A chart gives the population (millions) and literacy rate (%) of ten cities: Mumbai 20.1,
89.5; Delhi 18.3, 88.2; Bengaluru 13.5, 91; Hyderabad 11.8, 90.3; Chennai 10.9, 89.4;
Kolkata 14.2, 89; Ahmedabad 8.7, 85.2; Pune 7.2, 92.1; Jaipur 6.8, 83.3; Lucknow 6.5, 85.
A city is highly literate if its literacy rate exceeds 90%. How many cities meet this,
which of them has the highest population, and what is the population difference between it
and the least populous highly literate city?

- **(a)** 3 cities, Bengaluru, 6.3 million
- **(b)** 4 cities, Pune, 6.7 million
- **(c)** 3 cities, Bengaluru, 7.2 million
- **(d)** 4 cities, Pune, 6.8 million

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 3 cities, Bengaluru, 6.3 million**

**Why.** Literacy above 90%: Bengaluru (91), Hyderabad (90.3) and Pune (92.1) — three cities. The most populous of them is Bengaluru (13.5 million), the least is Pune (7.2 million). Difference = 13.5 − 7.2 = 6.3 million.

**Concept: filter, then compare.** Multi-part DI questions are a pipeline: apply the condition first (literacy > 90%), then work only with the survivors. Note "exceeds 90%" is strict, so a city at exactly 90 would not count.

{{< /details >}}

### 3 · Q8, minimum price breach after a bearish engulfing candle

*Asked by: EPAM (EPAM freshers test)*

A candlestick chart shows a company's daily stock price; the previous close is ₹345 and the
current day's low is about ₹300. The Average True Range (ATR) is defined as the difference
between the previous close and the lowest price of the current day. A bearish engulfing
pattern signals a possible trend reversal, which is confirmed on the next day by a breach
of the minimum price $= \text{close} - 1.5 \times \text{ATR}$. What is the minimum price
breach on the downside, relative to the current close, that confirms the reversal (rounded
to the nearest option)?

- **(a)** ₹270
- **(b)** ₹280
- **(c)** ₹290
- **(d)** ₹300

{{< details title="Answer and explanation" closed="true" >}}

**Answer: most likely (b) ₹280** (the chart photo is blurred, so treat this as the best reading)

**Why.** ATR as defined = previous close − today's low = 345 − 300 = 45. The confirmation level = close − 1.5 × ATR = close − 67.5. Using the ₹345 close, that is 277.5, nearest option ₹280.

**Concept: apply the definition you are given.** Finance-flavoured DI questions define their own terms (here a simplified "ATR"); do not use the textbook meaning, just plug the numbers into the stated formula. A bearish engulfing candle is a down day whose body covers the previous up day's body, a hint that a rise may be reversing.

{{< /details >}}

### 4 · pass percentage of college T

*Asked by: EXL (HackerEarth test, 2025)*

Two pie charts show the share of each college (P to U) among the 2000 students who took an
entrance exam (P 11, Q 9, R 28, S 19, T 26, U 7 per cent) and among the 1000 who passed
(P 9, Q 9, R 35, S 18, T 22, U 7). What percentage of the students from college T passed?

- **(a)** 51.30%
- **(b)** 56.00%
- **(c)** 42.31%
- **(d)** 43.28%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 42.31%**

**Why.** College T's candidates = 26% of 2000 = 520. T's passes = 22% of 1000 = 220. Pass rate = 220/520 = 42.31%.

**Concept: percentages of different totals.** The two pie charts have different bases (2000 appeared, 1000 passed). Convert each percentage to an actual count using its own base before dividing. Comparing 22% with 26% directly would be meaningless.

{{< /details >}}

### 5 · selling price from a cost-percentage chart

*Asked by: EXL (HackerEarth test, 2025)*

A chart gives each product part's share of the cost: A 10%, B 20%, C 10%, D 25%,
E 20%, F 15%. 5500 products were sold, and the total spent on part C was 82.5 dollars.
What should be the selling price of a product (in cents) to earn a profit of 25%?

- **(a)** 15
- **(b)** 18.75
- **(c)** 20.55
- **(d)** 21.56

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 18.75 cents**

**Why.**
1. Total spent on part C = \$82.5 = 8250 cents across 5500 products, so 1.5 cents per product.
2. Part C is 10% of a product's cost, so the full cost = 1.5/0.10 = 15 cents.
3. For 25% profit, selling price = 15 × 1.25 = 18.75 cents.

**Concept: from a part to the whole.** If a part is p% of a total and the part is worth x, the total is x ÷ (p/100). Then "profit of r%" means selling price = cost × (1 + r/100). Keep units consistent: convert dollars to cents early.

{{< /details >}}

### 6 · bar chart, hockey against golf

*Asked by: EXL (HackerEarth test, 2025)*

A bar chart shows how many people in a society like each sport: cricket 40, hockey 50,
football 20, golf 15, tennis 5. Approximately what percentage more people like hockey than
golf?

- **(a)** 2.1212
- **(b)** 233
- **(c)** 2.5
- **(d)** 2.75

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) about 233%**

**Why.** Hockey 50, golf 15. "How much more, as a percentage of golf" = (50 − 15)/15 × 100 = 35/15 × 100 ≈ 233%.

**Concept: "percentage more than" uses the second quantity as the base.** A is x% more than B means x = (A − B)/B × 100. 50 is 3.33 times 15, i.e. 233% **more** (not 333%). The options 2.1–2.75 are ratios, not percentages, set as traps.

{{< /details >}}

### 7 · Mahesh's average interest

*Asked by: Flipkart (Neev 2025)*

Mahesh's expenditure (lakh rupees) from 2004 to 2008. Food: 56, 60, 65, 50, 45. Transport:
20, 25, 15, 20, 25. Housing and maintenance: 40, 50, 45, 35, 55. Interest on loans: 15,
12, 10, 18, 14. Taxes: 60, 55, 50, 65, 50. What is the approximate average amount of
interest per year?

- **(a)** 14 lakhs
- **(b)** 16 lakhs
- **(c)** 12 lakhs
- **(d)** 15 lakhs

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 14 lakhs**

**Why.** Interest over the five years: 15 + 12 + 10 + 18 + 14 = 69. Average = 69/5 = 13.8 ≈ 14 lakhs. (The photo has 12 selected, which is wrong.)

**Concept: average of a row.** Sum the values and divide by how many there are. "Approximate" means round at the end, not before, so you do not pile up rounding errors.

{{< /details >}}

### 8 · year closest to the twenty-year average

*Asked by: Flipkart (Neev 2025)*

A company's revenue (in Cr) for 2001-2020 was 93, 95, 100, 105, 108, 109, 110, 120, 125,
130, 132, 134, 140, 145, 150, 150, 155, 160, 160, 180. Which year's revenue equals
(approximately) the average of the twenty years?

- **(a)** 2009
- **(b)** 2012
- **(c)** 2010
- **(d)** 2011

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 2010**

**Why.** The twenty values add to 2601, so the average is 130.05. The year with revenue 130 is 2010 (the 10th value).

**Concept: estimate the mean quickly.** Adding 20 numbers is slow; pair them from the ends (93 + 180, 95 + 160, ...) or use a guessed mean and add the deviations. Then scan for the value closest to the average.

{{< /details >}}

### 9 · savings to expenditure in 2008

*Asked by: Flipkart (Neev 2025)*

Same table. If Mahesh earned Rs 6 crore in 2008, what is the ratio of his savings to his
expenditure that year?

- **(a)** 139:63
- **(b)** 134:65
- **(c)** 137:63
- **(d)** 131:65

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 137 : 63**

**Why.**
1. 2008 expenditure = food 45 + transport 25 + housing 55 + interest 14 + taxes 50 = 189 lakhs.
2. Income = Rs 6 crore = 600 lakhs, so savings = 600 − 189 = 411 lakhs.
3. 411 : 189; both divide by 3: 137 : 63.

**Concept: units and the savings identity.** Savings = income − expenditure. 1 crore = 100 lakhs, so 6 crore = 600 lakhs; mixing crore and lakh is the usual trap. Reduce a ratio by the greatest common divisor (here 3).

{{< /details >}}

### 10 · transport 2004 against food and taxes 2005

*Asked by: Flipkart (Neev 2025)*

Same table. The amount paid on transport in 2004 is approximately what percentage of the
amount paid in 2005 on food and taxes?

- **(a)** 13%
- **(b)** 17%
- **(c)** 15%
- **(d)** 19%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 17%**

**Why.** Transport 2004 = 20. Food 2005 + taxes 2005 = 60 + 55 = 115. 20/115 × 100 ≈ 17.4% ≈ 17%.

**Concept: "A is what percent of B" = A/B × 100.** The year and category of each quantity differ here on purpose, so pick each value from its own row and column.

{{< /details >}}

### 11 · two bus timetables, income ratio

*Asked by: JSW (Aptitude test)*

With the timetables of the previous question, and also the number of people boarding and
the fare per person at each station (bus P: 25, 30, 20, 10, 30 boarding at A-E, fares
$-, 50, 100, 150, 200, 300$ at A-F; bus Q: 30, 10, 20, 25, 15 boarding at F-B, fares
$-, 20, 40, 50, 90, 200$ at F-A): the total income of bus P is what percentage of the
total income of bus Q?

- **(a)** 243.67%
- **(b)** 237.50%
- **(c)** 241.37%
- **(d)** 250%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: the question is flawed; (d) 250% is the nearest option to the only sensible reading that comes close.**

**Why.** Income depends on where each passenger gets off, which the table does not say. Three readings:
- Each passenger pays the fare listed at their boarding station: 11000/3600 = 305.6%.
- Everyone rides to the end and pays (final fare − boarding fare): 23500/16400 = 143.3%.
- Each passenger pays the fare at the next station: about 251.7%, closest to (d).

**Concept: check that the data determines the answer.** Before computing, ask what information the quantity depends on. Here income = Σ passengers × fare paid, and the fare depends on the trip length. When a question leaves that out, pick the option that matches the most natural reading and note the ambiguity.

{{< /details >}}

### 12 · two bus timetables, speed and time

*Asked by: JSW (Aptitude test)*

Bus P runs A (departs 6:00 pm) $\to$ B (arr. 7:30 pm, dep. 7:35 pm, 15 km) $\to$ C
(9:50/10:00 pm, 25 km) $\to$ D (12:00/12:10 am, 60 km) $\to$ E (2:30/2:45 am, 100 km)
$\to$ F (arrives 4:00 am, 200 km). Bus Q runs F (7:00 pm) $\to$ E (8:40/8:45 pm, 10 km)
$\to$ D (10:30/10:35 pm, 25 km) $\to$ C (11:40/11:45 am, 65 km) $\to$ B (4:00/4:10 am,
200 km) $\to$ A (arrives 7:00 am, 300 km). The column with the distances is headed
"distance from origin".

1. Find the difference between the speeds of bus P and bus Q (in km/h). Options:
    11, 10, 12, 8.
2. If bus P increases its average speed by 25%, find the time it reaches its
    destination. Options: 1:45 am, 2:00 am, 2:45 am, 1:00 am.

{{< details title="Answer and explanation" closed="true" >}}

**Answers: 1. 10 km/h; 2. 2:00 am**

**Why.**
1. The keyed answer comes from treating the distance column as station-to-station gaps and adding them: bus P covers 400 km in 10 h (6 pm to 4 am) = 40 km/h; bus Q covers 600 km in 12 h (7 pm to 7 am) = 50 km/h. Difference = 10. (Reading the column literally as distance from the origin gives 20 and 25 km/h, a difference of 5, which is not an option.)
2. A 25% higher average speed means time = 10/1.25 = 8 hours, so the bus arrives at 6 pm + 8 h = 2:00 am.

**Concept: speed and time are inversely proportional.** Average speed = total distance ÷ total time (including halts). For a fixed distance, multiplying speed by k divides time by k. "25% faster" means k = 1.25, so time × 0.8. You don't even need the distance for part 2.

{{< /details >}}

### 13 · phone brands, data interpretation

*Asked by: Oracle (HackerRank MCQ test)*

Customers (in millions) using each brand of phone, and customers added in each month (Euphore
has two versions):
|  | Customers | Added in the month |  |  |  |
|---|---|---|---|---|---|
| Month | Hington | Euphore | Hington | Euphore V1 | Euphore V2 |
| Aug-12 | 46.18 | 47.28 | 0.36 | 1.24 | 0.6 |
| Sep-12 | 47.34 | 48.91 | 1.16 | 1.08 | 0.8 |
| Oct-12 | 49.32 | 49.27 | 1.98 | 0.84 | 0.48 |
What was the total number of people using either of the two brands in July 2012?
(Transcribed from video frames; some digits are blurred.)

- **(a)** 91.21 million
- **(b)** 6.87 million
- **(c)** 98.23 million
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 91.21 million** (the ticked option; the blurred digits read give 91.26)

**Why.** The August figure includes customers added in August, so July = August − August's additions.
- Hington: 46.18 − 0.36 = 45.82
- Euphore: 47.28 − (1.24 + 0.6) = 45.44
- Total ≈ 91.26 million, nearest option 91.21 (one blurred digit was probably misread).

**Concept: stock and flow.** A "customers" column is a stock (a total at a moment); "added in the month" is a flow (the change). Previous stock = current stock − flow. Remember Euphore's additions come in two parts (V1 and V2) that must both be subtracted.

{{< /details >}}

### 14 · branches pie chart

*Asked by: Qualcomm (Nov 2024 (HirePro))*

A pie chart gives the number of branches of a company by state (TN 16%, WB 22%, JH 20%,
MP 24%, UP 18%), and a second chart (partly visible) gives employees by state; all branches of
a state have the same employee strength. Three questions were asked: which state has the most
employees per branch (options MP, JH, TN, cannot be determined); a ratio question starting "If
MP has 1872 employees and UP has 9 branches ..."; and an office-area question for JH
(50{,}000 sq ft). The employee chart and the ends of the questions are [cut off in the source].

{{< details title="Answer and explanation" closed="true" >}}

**Answer: not answerable from the photo** (the employee chart and the ends of the questions are cut off).

**Method.** All branches of a state have the same strength, so employees per branch in a state = (state's employees) ÷ (state's branches). With both charts in percentages of the company totals, compare (employee % ÷ branch %) across states: the largest ratio wins. For the ratio question, find total branches from "UP has 9 branches = 18%" (total 50), then scale.

**Concept: ratios of shares.** If a pie chart gives shares of a total, you can compare per-unit values across slices without knowing the total, because the total cancels in the ratio.

{{< /details >}}

### 15 · subjects chart, share in 2011

*Asked by: Qualcomm (HirePro, Aug 2025)*

Same chart. If the total number of students in the university was 20000 in 2011, what
percentage of students chose at least one subject?

- **(a)** 88%
- **(b)** 91%
- **(c)** 97%
- **(d)** 94%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 91%**

**Why.** 2011 bars: 34 + 67 + 36 + 45 = 182 hundred = 18,200 students. 18,200/20,000 = 91%.

**Concept: chart units.** The bars are "in hundreds", so multiply by 100 before comparing with the 20,000 total. This assumes each student chose one subject, so the counts can be added.

{{< /details >}}

### 16 · subjects chart, boys in 2012

*Asked by: Qualcomm (HirePro, Aug 2025)*

A bar graph shows the number of students (in hundreds) who chose Science, Maths, English and
Hindi: 2010: 20, 34, 54, 33; 2011: 34, 67, 36, 45; 2012: 12, 46, 44, 30; 2013: 46, 36, 24,
47; 2014: 35, 36, 30, 20; 2016: 32, 27, 52, 40 (the 2016 Science and Maths bars are hard to
separate). How many boys chose at least one of the subjects in 2012, if 25% of the students
in 2012 were girls?

- **(a)** 9600
- **(b)** 9700
- **(c)** 9800
- **(d)** 9900

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 9900**

**Why.** 2012 total = 12 + 46 + 44 + 30 = 132 hundred = 13,200. If 25% are girls, 75% are boys: 0.75 × 13,200 = 9,900.

**Concept: complement percentages.** If 25% are girls, boys are 100 − 25 = 75%. Multiply the whole by the complement rather than computing girls and subtracting.

{{< /details >}}

### 17 · subjects chart, average English

*Asked by: Qualcomm (HirePro, Aug 2025)*

Same chart. What is the average number of students who chose English over the 6 years?

- **(a)** 6000
- **(b)** 4000
- **(c)** 2000
- **(d)** 8000

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 4000**

**Why.** English over the six years: 54 + 36 + 44 + 24 + 30 + 52 = 240 hundred. Average = 240/6 = 40 hundred = 4000.

**Concept: average of one series.** Pick the same bar (English) from each year, add, divide by the number of years, and convert units at the end.

{{< /details >}}

### 18 · Data Analysis

*Asked by: Qualcomm (60-question online assessment)*

In how many years did U1 receive more applications than every other university? (Table: applications 2018-2023 for U1-U5)

- **(a)** 2
- **(b)** 3
- **(c)** 4
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 5**

**Why.** Compare U1 with every other university year by year. 2018: U1 = 120 but U4 = 140, so no. 2019 (150), 2020 (140), 2021 (155), 2022 (160) and 2023 (170): U1 is the highest each time. That is 5 years.

**Concept: "more than every other".** For each year you need U1 > max(others). Find the year's maximum among the rest and compare once; one bigger value is enough to rule the year out.

{{< /details >}}

### 19 · Data Analysis

*Asked by: Qualcomm (60-question online assessment)*

For which university was the overall number of applications received (sum over all 6 years) the lowest?

- **(a)** U5
- **(b)** U4
- **(c)** U3
- **(d)** U2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) U5**

**Why.** Six-year totals: U1 = 895, U2 = 740, U3 = 743, U4 = 863, U5 = 615. The lowest is U5.

**Concept: compare totals, not single years.** "Overall" means the sum across all years. When totals are close (U2 740 vs U3 743), add carefully; when one is clearly lower in most years, you can often see the answer before adding.

{{< /details >}}

### 20 · Data Analysis

*Asked by: Qualcomm (60-question online assessment)*

Consider the combined number of applications received by U1 and U5 in 2023. Approximately what percentage of this total was contributed by U5?

- **(a)** 40%
- **(b)** 25%
- **(c)** 35%
- **(d)** 30%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 40%**

**Why.** 2023: U1 = 170, U5 = 115, combined 285. U5's share = 115/285 ≈ 40.35% ≈ 40%.

**Concept: share of a combined total.** Share = part ÷ (sum of parts) × 100. Quick check: 115 is a bit more than 0.4 × 285 = 114.

{{< /details >}}

### 21 · Data Analysis

*Asked by: Qualcomm (60-question online assessment)*

If U4 continues to grow by exactly 5,000 applications every year, in which year will it first reach or surpass 170,000 applications?

- **(a)** 2025
- **(b)** 2026
- **(c)** 2024
- **(d)** 2027

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 2026**

**Why.** U4 had 155 thousand in 2023. Adding 5 thousand a year: 160 (2024), 165 (2025), 170 (2026). It first reaches 170,000 in 2026.

**Concept: linear growth.** Constant yearly increase means value after n years = start + n × step. Solve 155 + 5n ≥ 170 → n ≥ 3, so 2023 + 3 = 2026.

{{< /details >}}

### 22 · decrease in car sales 2006 to 2008

*Asked by: Sigmoid (Campus hiring 2026)*

A bar chart shows car sales by year (2006: 40000, 2008: 25000, as far as the photo shows).
What is the percentage decrease from 2006 to 2008?

- **(a)** 28.5%
- **(b)** 37.5%
- **(c)** 42.5%
- **(d)** 44.5%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 37.5%**

**Why.** From 40,000 to 25,000 is a fall of 15,000. Percentage decrease = 15,000/40,000 × 100 = 37.5%.

**Concept: percentage change uses the old value as the base.** Change % = (new − old)/old × 100. Using the new value as the base (15,000/25,000 = 60%) is the classic mistake.

{{< /details >}}

### 23 · a die's bar graph

*Asked by: Texas Instruments (IIT BHU 2023)*

A bar graph gives 20 rolls of a red die: 1 seven times, 2 eight times, 3, 5 and 6 once each and
4 twice. Estimate the mean roll.

- **(a)** 2.25
- **(b)** 3.6
- **(c)** 5.8
- **(d)** 7.5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 2.25**

**Why.** Total = 1×7 + 2×8 + 3×1 + 4×2 + 5×1 + 6×1 = 7 + 16 + 3 + 8 + 5 + 6 = 45 over 20 rolls. Mean = 45/20 = 2.25.

**Concept: mean from a frequency table.** Mean = Σ(value × frequency) ÷ Σ frequency. Each bar's height tells how many times that face appeared.

{{< /details >}}

### 24 · will the mean go up?

*Asked by: Texas Instruments (IIT ISM 2024)*

With the same bar graph (the white die was rolled 19 times: 3, 3, 4, 3, 3, 3 of the faces 1-6)
and the white die fair, what is the probability that the mean score increases after one more
roll?

- **(a)** 1/6
- **(b)** 1/3
- **(c)** 2/3
- **(d)** 5/6

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 2/3** (taking "the mean" as the mean of all 39 rolls of both dice)

**Why.**
1. Red total = 45 (20 rolls). White total = 1×3 + 2×3 + 3×4 + 4×3 + 5×3 + 6×3 = 66 (19 rolls).
2. Combined mean = 111/39 ≈ 2.85.
3. A new roll raises the mean only if it is above the current mean, so it must be 3, 4, 5 or 6: 4 of 6 faces, probability 2/3.

**Concept: adding a value above the mean raises the mean.** The mean is the balance point; a new value larger than it pulls it up, smaller pulls it down, equal leaves it unchanged. So you only need to compare the next roll with the current mean, not recompute it.

{{< /details >}}

### 25 · dollar against euro

*Asked by: Texas Instruments (IISc, second set)*

With the dollar graph above and euros per pound 1.40, 1.35, 1.35, 1.30, 1.35, 1.30, 1.25, 1.20
over the same days, by how much did the dollar depreciate against the euro over the week?

- **(a)** 5%
- **(b)** 5.5%
- **(c)** 6.25%
- **(d)** 7.5%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 6.25%**

**Why.** Both rates are quoted per pound, so euros per dollar = (euros per pound) ÷ (dollars per pound).
- Start: 1.40/1.75 = 0.80 euro per dollar.
- End: 1.20/1.60 = 0.75 euro per dollar.
- Fall = 0.05/0.80 = 6.25%.

**Concept: cross rates.** If 1 pound = 1.75 dollars and 1 pound = 1.40 euros, then 1.75 dollars = 1.40 euros, so 1 dollar = 1.40/1.75 euros. A currency depreciates when it buys fewer units of the other currency; measure the change against the starting value.

{{< /details >}}

### 26 · gym members

*Asked by: Texas Instruments (BITS Pilani)*

A bar graph shows members of gyms A and B in 1990-94 (1994: A 70, B 150). If 1995 has 30%
more members in total than 1994, how many?

- **(a)** 282
- **(b)** 296
- **(c)** 292
- **(d)** 286

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 286**

**Why.** 1994 total = 70 + 150 = 220. 30% more = 220 × 1.3 = 286.

**Concept: increase by a percentage = multiply by (1 + p/100).** One multiplication is faster and safer than finding 30% and adding.

{{< /details >}}

### 27 · pounds bought and sold

*Asked by: Texas Instruments (IIT ISM 2024)*

A graph gives US dollars per pound for a week: Sun 1.75, Mon 1.75, Tue 1.70, Wed 1.75, Thu
1.70, Fri 1.70, Sat 1.65, Sun 1.60. Mrs Lindsay buys 200 pounds on Tuesday and sells them on
Wednesday. Her profit in dollars?

- **(a)** \$5
- **(b)** \$8
- **(c)** \$10
- **(d)** \$15

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) \$10**

**Why.** Tuesday: 1 pound costs \$1.70, so 200 pounds cost \$340. Wednesday: 1 pound sells for \$1.75, so 200 pounds bring \$350. Profit = \$10.

**Concept: profit from an exchange rate move.** Buying a currency and selling it after its price rises earns (sell rate − buy rate) × amount = 0.05 × 200.

{{< /details >}}

### 28 · a pie chart

*Asked by: Texas Instruments (IISc, second set)*

A pie chart splits 160000 as Hemant 15%, Dharam 10%, Chandru 15%, Abir 25%, Bhanu 35%.
By what percent does Chandru's share exceed Dharam's?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 50%**

**Why.** Chandru 15%, Dharam 10%. Excess as a percentage of Dharam's share = (15 − 10)/10 × 100 = 50%. The 160,000 total is not needed.

**Concept: percentage points vs percent.** Chandru's share is 5 percentage **points** higher, which is 50 **percent** more than Dharam's. When both values are shares of the same total, the total cancels.

{{< /details >}}

### 29 · sweet shop table

*Asked by: Texas Instruments (IIT ISM 2024)*

A table gives the marked price, discount and profit of sweets. Ras Malai's cost equals
Rasgulla's (Rasgulla: marked price $1.25\times$ cost, 8% discount, profit Rs. 48); Ras Malai
is marked at $1.5625\times$ cost and sold at a 20% discount. Profit on Ras Malai?

- **(a)** 60
- **(b)** 80
- **(c)** 100
- **(d)** 120

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 80**

**Why.**
1. Rasgulla: selling price = cost × 1.25 × 0.92 = 1.15 × cost, so profit = 0.15 × cost = 48, giving cost = 320.
2. Ras Malai has the same cost, 320. Selling price = 320 × 1.5625 × 0.8 = 400. Profit = 400 − 320 = 80.

**Concept: marked price, discount and profit as multipliers.** Marked price = cost × (1 + markup). Selling price = marked price × (1 − discount). Chain the multipliers: 1.25 × 0.92 = 1.15 means a 15% profit. Working in multipliers avoids computing prices you don't need.

{{< /details >}}

### 30 · bank rates (1)

*Asked by: Wells Fargo (SHL test, Oct 2022)*

Figure 1: interest rates (%) offered by banks on fixed deposits for four terms.
| Term | A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|---|
| I (1-2 yrs) | 4.75 | 5.5 | 4 | 6 | 5.25 | 5 | 5.25 | 6 | 3.5 | 5.25 |
| II (2-3 yrs) | 5 | 5.75 | 4.25 | 6.25 | 5.5 | 5.25 | 5.25 | 6 | 3.8 | 5.5 |
| III (3-5 yrs) | 5.6 | 5.8 | 4.5 | 6.5 | 5.75 | 5.5 | 5.5 | 6.25 | 4 | 5.75 |
| IV ($>$5 yrs) | 6 | 6 | 4.75 | 6.7 | 5.8 | 5.8 | 5.8 | 6.5 | 4.25 | 5.8 |
How many banks have interest rates that remain the same between any two terms from I
to IV?

- **(a)** 0
- **(b)** 1
- **(c)** 2
- **(d)** 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 2**

**Why.** Look along each bank's row for two equal rates. Bank G: 5.25 in both term I and term II. Bank H: 6 in both term I and term II. Every other bank's rate rises strictly from term to term.

**Concept: scan systematically.** For "how many rows satisfy X", check each row once with the same test and tick it. Here, in a rising row an equal pair can only sit next to each other, so compare neighbouring terms only.

{{< /details >}}

### 31 · bank rates (2), Zeta index

*Asked by: Wells Fargo (SHL test, Oct 2022)*

Figure 2: the *Zeta index* $Z_{XY}$ of bank $X$ with respect to bank $Y$ is the
number of terms in which $X$ offers a higher rate than $Y$ (e.g. $Z_{AE} = 1$: only in
term IV does A beat E). Ratings are based on $Z_{XY} - Z_{YX}$: 4 gives A1+ (rating of
$X$ w.r.t. $Y$) and A1$-$ (of $Y$ w.r.t. $X$); 3 gives A2+/A2$-$; 2 gives A3+/A3$-$;
1 gives A4+/A4$-$; 0 gives par/par. Using Figure 1 from the previous question, what is
the rating of Bank J with respect to Bank G?

- **(a)** A3+
- **(b)** A2-
- **(c)** A1+
- **(d)** A2+

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) A3+**

**Why.** Compare J and G term by term: I 5.25 = 5.25; II 5.5 > 5.25; III 5.75 > 5.5; IV 5.8 = 5.8. J beats G in 2 terms, G beats J in 0, so Z_JG − Z_GJ = 2, which is A3+ for J with respect to G.

**Concept: follow a made-up definition exactly.** New-index questions test careful reading. Ties count for neither bank. The rating's sign (+ or −) depends on whose point of view is asked: J's view of G is positive because J wins more terms.

{{< /details >}}

### 32 · branches and ATMs

*Asked by: Wells Fargo (SHL test, Oct 2022)*

Figure 1: branches and ATMs of ABC Bank by city category.
|  | 2011/12 | 2012/13 | 2013/14 |  |  |  |
|---|---|---|---|---|---|---|
| Category | Branches | ATMs | Branches | ATMs | Branches | ATMs |
| A | 1,341 | 4,390 | 1,852 | 6,789 | 2,415 | 8,012 |
| B | 984 | 2,789 | 1,331 | 3,789 | 1,749 | 4,076 |
| C | 654 | 1,672 | 972 | 2,581 | 1,129 | 3,850 |
| D | 564 | 1,123 | 678 | 2,056 | 731 | 2,010 |
| E | 321 | 590 | 451 | 876 | 602 | 1,062 |
Figure 2 gives the average city population per category (A 120{,}000; B 75{,}000;
C 35{,}000; D 15{,}000; E 7{,}500) and Figure 3 the share of cities in 2013/14 (A 10%,
B 15%, C 20%, D 25%, E 30%). Which statement shows an *incorrect* analysis of
the trends during 2011-14?

- **(a)** The largest number of new branches and ATMs combined were opened in Category A cities.
- **(b)** The smallest number of new ATMs introduced were in Category E cities.
- **(c)** The bank opened the fewest new branches in Category D cities.
- **(d)** More than 700 branches and ATMs apiece were opened in Category E cities.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d)** is the incorrect analysis.

**Why.** Additions from 2011/12 to 2013/14 (branches, ATMs):
- A (1074, 3622), B (765, 1287), C (475, 2178), D (167, 887), E (281, 472).
- (a) A has the largest combined additions: true. (b) E added the fewest ATMs (472): true. (c) D added the fewest branches (167): true.
- (d) says more than 700 branches **and** more than 700 ATMs each were added in E. Only 281 branches and 472 ATMs were added, so (d) is false.

**Concept: "apiece" means each one separately.** "More than 700 apiece" requires both numbers to exceed 700, not their sum (753). Compute changes as (final − initial) for each category before judging statements.

{{< /details >}}
