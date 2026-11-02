---
title: "Averages"
weight: 16
---

4 questions asked by Axxela, EPAM, Flipkart. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q11, mean of consecutive numbers

*Asked by: Axxela (NIT Bhopal 2024)*

The mean of a group of eleven consecutive natural numbers is $m$. What is the percentage
change in the mean when the next six consecutive natural numbers are included?

- **(a)** $m\%$
- **(b)** $m/3\%$
- **(c)** $m/300\%$
- **(d)** $300/m\%$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 300/m %**

**Why.**
1. Eleven consecutive numbers have their mean in the middle (the 6th number), so they are m − 5, ..., m + 5.
2. Add the next six: the list becomes m − 5, ..., m + 11 (17 numbers). Its middle (9th) number is m + 3, so the new mean is m + 3.
3. Percentage change = 3/m × 100 = 300/m %.

**Concept: the mean of an evenly spaced list is its middle value.** For consecutive numbers (or any arithmetic progression), the average equals (first + last)/2, which is the middle term. So you can find the new mean without adding anything: just find the new middle.

{{< /details >}}

### 2 · Q7, museum visitors

*Asked by: Axxela (NIT Bhopal 2024)*

A museum has an average of 520 visitors on Sunday and 100 on other days. What is the
average number of visitors per day in a month of 30 days beginning with a Sunday?

- **(a)** 220
- **(b)** 170
- **(c)** 180
- **(d)** 300

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 170**

**Why.** A 30-day month that starts on Sunday has Sundays on days 1, 8, 15, 22 and 29: five Sundays and 25 other days. Total visitors = 5 × 520 + 25 × 100 = 2600 + 2500 = 5100. Average = 5100/30 = 170.

**Concept: weighted average.** When groups have different sizes, the overall average is (sum of group size × group average) ÷ total size. You cannot just average 520 and 100; the 25 ordinary days carry far more weight than the 5 Sundays.

{{< /details >}}

### 3 · Q20, average of the primes between 10 and 20

*Asked by: EPAM (EPAM freshers test)*

What is the average of all prime numbers between 10 and 20?

- **(a)** 13
- **(b)** 19
- **(c)** 15
- **(d)** 17

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 15**

**Why.** The primes between 10 and 20 are 11, 13, 17 and 19. Sum = 60, count = 4, average = 15.

**Concept: primes and averages.** A prime has exactly two divisors, 1 and itself. Check each odd number: 15 = 3 × 5 is not prime. Average = sum ÷ count. Notice the list is symmetric about 15 (11 and 19, 13 and 17), which gives the average instantly.

{{< /details >}}

### 4 · batting average after the tenth innings

*Asked by: Flipkart (Neev 2025)*

A batsman has an average of 40 after 9 innings. If he scores 100 in the 10th innings, what
is his new average?

- **(a)** 52
- **(b)** 46
- **(c)** 56
- **(d)** 48

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 46**

**Why.** Runs after 9 innings = 9 × 40 = 360. After the 10th: 360 + 100 = 460 runs in 10 innings, average 46.

**Concept: average × count = total.** To update an average, go back to the total, add the new value, and divide by the new count. Shortcut: the new score is 60 above the old average, and that excess is shared over 10 innings, raising the average by 6.

{{< /details >}}
