---
title: "Clocks and calendars"
weight: 8
---

9 questions asked by Axxela, EXL, Flipkart, ION Group, MAQ Software, Texas Instruments, Wells Fargo. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q6, two clocks gaining time

*Asked by: Axxela (NIT Bhopal 2024)*

Two clocks are set correctly at 09:00 AM on Monday. They gain 3 and 5 minutes per hour
respectively. What will the second clock show when the clock that gains 3 minutes an hour
shows 06:27 PM on the same day?

- **(a)** 06:55 PM
- **(b)** 06:25 PM
- **(c)** 06:45 PM
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 06:45 PM**

**Why.**
1. The first clock gains 3 minutes per hour, so it shows 63 clock-minutes for every 60 real minutes.
2. It shows 06:27 PM, which is 9 h 27 min = 567 minutes after 9 AM on its own face. Real time passed = 567 × 60/63 = 540 minutes = 9 hours.
3. In 9 real hours the second clock gains 9 × 5 = 45 minutes, so it shows 9 AM + 9 h 45 min = 06:45 PM.

**Concept: a fast clock runs at a fixed ratio to real time.** A clock that gains g minutes an hour shows (60 + g) minutes for each 60 real ones. Convert the clock reading back to real time with that ratio, then apply the other clock's ratio. Always work in real time as the common reference.

{{< /details >}}

### 2 · Sundays in June 2004

*Asked by: EXL (HackerEarth test, 2025)*

Determine the dates on which it will be a Sunday in June 2004, if 1 January 2004 was a
Thursday.

- **(a)** 5, 12, 19, 26
- **(b)** 6, 13, 20, 27
- **(c)** 7, 14, 21, 28
- **(d)** 8, 15, 22, 29

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 6, 13, 20, 27**

**Why.**
1. 2004 is divisible by 4 (and not a century year), so February has 29 days.
2. Days from 1 January to 1 June = Jan 31 + Feb 29 + Mar 31 + Apr 30 + May 31 = 152.
3. 152 = 21 × 7 + 5, so 1 June is 5 weekdays after Thursday: Tuesday.
4. Tuesday 1 June means Sunday 6 June, then 13, 20, 27.

**Concept: odd days.** Weekdays repeat every 7 days, so only the remainder after dividing by 7 matters (the "odd days"). Add the days between two dates, take the remainder mod 7, and move that many weekdays forward. Leap year rule: divisible by 4, except century years, which must be divisible by 400.

{{< /details >}}

### 3 · March and November dates

*Asked by: EXL (HackerEarth test, 2025)*

Is any date in March of a year the same day of the week as the corresponding date in
November of that year?

- **(a)** Same day
- **(b)** Not same day
- **(c)** Next day
- **(d)** Previous day

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) same day**

**Why.** From 1 March to 1 November: March 31 + April 30 + May 31 + June 30 + July 31 + August 31 + September 30 + October 31 = 245 days. 245 = 35 × 7, an exact number of weeks, so every March date falls on the same weekday as the same date in November.

**Concept: months that share a calendar.** Two dates fall on the same weekday when the days between them are a multiple of 7. Since February is not between March and November, leap years do not matter here. Other pairs worth remembering: in a non-leap year, January and October share a calendar; April and July do too.

{{< /details >}}

### 4 · right angle between 4 and 5

*Asked by: Flipkart (Neev 2025)*

Between 4 and 5 o'clock, when are the hands of a clock at a right angle? (The first
option is covered by the selection highlight; the others read "35(12/55) minutes before
5" and "40(5/55) minutes before 5".)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 5 5/11 minutes past 4** (the option hidden under the selection highlight). The other right angle is at 38 2/11 minutes past 4, i.e. 21 9/11 minutes before 5; neither visible option matches that.

**Why.**
1. At m minutes past 4, the minute hand is at 6m degrees (from 12) and the hour hand at 120 + 0.5m degrees.
2. The gap is |5.5m − 120|. Set it to 90: 5.5m = 30 gives m = 60/11 = 5 5/11, and 5.5m = 210 gives m = 420/11 = 38 2/11.

**Concept: clock-hand angle formula.** The minute hand moves 6° per minute; the hour hand moves 30° per hour, which is 0.5° per minute. So the angle between them at H:M is |30H − 5.5M|. The minute hand gains 5.5° on the hour hand every minute, so every angle except 0° and 180° happens twice each hour.

{{< /details >}}

### 5 · Q4, clock angle at 3:15

*Asked by: ION Group (SDE OA, Jul 2025)*

A clock shows 3:15. What is the angle between the hour and the minute hand?

- **(a)** $0^\circ$
- **(b)** $30^\circ$
- **(c)** $7.5^\circ$
- **(d)** $15^\circ$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 7.5°**

**Why.** At 3:15 the minute hand points at 3, which is 90°. The hour hand has moved a quarter of the way from 3 to 4: 90° + 15 × 0.5° = 97.5°. The angle is 7.5°.

**Concept: the hour hand never sits still.** A common trap is to say 0° because both hands "point at 3". The hour hand moves 0.5° every minute, so after 15 minutes it is 7.5° past the 3. Formula: |30 × 3 − 5.5 × 15| = |90 − 82.5| = 7.5°.

{{< /details >}}

### 6 · Q14, clock hands in a straight line

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

At what time between 11 and 12 o'clock will the hands of a clock form a straight line?

- **(a)** 27 minutes past 11
- **(b)** 28 minutes past 11
- **(c)** 25 minutes past 11
- **(d)** 30 minutes past 11

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) about 27 minutes past 11** (exactly 27 3/11)

**Why.** At t minutes past 11 the hour hand is at 330 + 0.5t degrees and the minute hand at 6t. In a straight line (opposite) means they are 180° apart: 330 + 0.5t − 6t = 180, so 5.5t = 150 and t = 300/11 = 27 3/11 minutes.

**Concept: "straight line" usually means opposite (180°).** Use angle = |30H − 5.5M| and set it equal to 180. (Strictly, overlapping hands, 0°, also form a line; between 11 and 12 that only happens at 12:00, so the answer is the 180° case.)

{{< /details >}}

### 7 · a gaining clock

*Asked by: Texas Instruments (BITS Pilani)*

A clock is 10 min slow at 10 am Monday and 10 min 50 s fast at 10 pm the next Monday. When was
it correct?

- **(a)** 12:25 pm Thursday
- **(b)** 12:25 am Thursday
- **(c)** 10:00 pm Thursday
- **(d)** 10:25 pm Wednesday

{{< details title="Answer and explanation" closed="true" >}}

**Answer: by the data, about 00:24 on Friday; of the options, (b) 12:25 am Thursday is the only one at 12:25 am, so it is the intended key, but the computed day is Friday.**

**Why.**
1. From 10 am Monday to 10 pm the next Monday is 7 days 12 hours = 180 hours.
2. The clock goes from 10 min slow to 10 min 50 s fast: a total gain of 600 + 650 = 1250 s in 180 h.
3. It is correct when it has gained the first 600 s: 600/1250 × 180 = 86.4 hours after 10 am Monday.
4. 86.4 h = 3 days 14 h 24 min, so Monday 10:00 am → Thursday 10:00 am → Friday 00:24 am.

**Concept: a steadily gaining clock.** The error changes at a constant rate, so it goes from −10 min to +10 min 50 s in a straight line. "Correct" means error = 0, and the time to get there is (initial error ÷ total change) × total time. Turn the time into days and hours carefully; this is where the key appears to have slipped a day.

{{< /details >}}

### 8 · founder's day on 29 February

*Asked by: Texas Instruments (BITS Pilani)*

A company celebrates founder's day only on 29 February. Four years after the celebration of
2016, the 8th founder's day was held; Julian is 4 years younger than the company. Julian's age?

- **(a)** 28
- **(b)** 36
- **(c)** 34
- **(d)** 30

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 28**

**Why.**
1. The 8th founder's day was 4 years after 2016, so in 2020.
2. The company was founded on a 29 February, and a founder's day is an anniversary of that date. The 1st founder's day comes 4 years after founding (the next 29 February), the 2nd after 8 years, so the 8th comes after 8 × 4 = 32 years. The company was founded in 1988 and is 32 in 2020.
3. Julian is 4 years younger: 28.

**Concept: anniversaries of a leap day.** 29 February exists only in leap years, every 4 years. The n-th anniversary of a date is n periods after it, not n − 1: the founding day itself is not counted as a founder's day. Getting this off by one gives 24, which is why the options include nearby numbers.

{{< /details >}}

### 9 · clock hands

*Asked by: Wells Fargo (SHL test, Oct 2022)*

How many times in a day do the minute and hour hands of a clock cross each other?

- **(a)** 21
- **(b)** 24
- **(c)** 23
- **(d)** 22

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 22**

**Why.** The minute hand gains 330° per hour on the hour hand (360° − 30°), so it laps it every 360/330 = 12/11 hours. In 24 hours that is 24 ÷ 12/11 = 22 meetings. In 12 hours they meet 11 times, not 12, because the meeting between 11 and 12 o'clock happens exactly at 12.

**Concept: relative speed of clock hands.** Treat the hands like two runners on a circular track. The faster one gains 5.5° per minute, so it gains a full lap (360°) every 65 5/11 minutes. Meetings = total time ÷ lap time. The same idea gives: hands are at right angles 44 times a day, and opposite 22 times a day.

{{< /details >}}
