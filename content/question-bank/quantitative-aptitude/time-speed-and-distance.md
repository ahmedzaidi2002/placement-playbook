---
title: "Time, speed and distance"
weight: 4
---

14 questions asked by Axxela, NVIDIA, Qualcomm, Siemens Energy, Texas Instruments, Wells Fargo. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q3, a boat that doubles its speed every km

*Asked by: Axxela (NIT Bhopal 2024)*

A boat starts with a speed of 1 km/h. After every 1 km the speed of the boat becomes twice.
What will be the average speed of the boat at the end of a journey of 25 km? (The options
in the photos read 2.5/1.5125, 2.5/1.75, 2.5/1.625 and 2.5/1.5.)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: about 12.5 km/h; none of the options as photographed matches** (they are probably garbled fractions of the form 25/x).

**Why.** The k-th kilometre is covered at 2^(k−1) km/h, taking 1/2^(k−1) h. Total time = 1 + 1/2 + 1/4 + ... + 1/2²⁴ = 2 − 2⁻²⁴ ≈ 2 h. Average speed = 25/2 ≈ 12.5 km/h.

**Concept: average speed = total distance ÷ total time.** It is not the average of the speeds. Here the slow first kilometre takes half the whole journey's time. The times form a geometric series that sums to almost 2.

{{< /details >}}

### 2 · Q5, three runners on a circular track

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

Three machines move along a circular track of 360 m at 37, 45 and 57 metres per minute.
They start together from the same point. After how many minutes will they all be
together again?

- **(a)** 40
- **(b)** 60
- **(c)** 90
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 90 minutes**

**Why.** Two runners meet again when the faster has gained a whole lap (360 m). Pair 37 and 45: relative speed 8 m/min, every 45 min. Pair 45 and 57: relative speed 12, every 30 min. All three are together at a common multiple: LCM(45, 30) = 90 min. (Check the third pair: 37 and 57 differ by 20, meeting every 18 min, and 18 divides 90.)

**Concept: meetings on a circular track.** Two runners in the same direction are together again every (track length ÷ speed difference). For several runners, take the LCM of the pairwise meeting times. They need not be back at the start point, just together.

{{< /details >}}

### 3 · Q8, average speed

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

A person walks from $A$ to $B$. He covers the first quarter of the distance at a constant
speed and takes the same amount of time to cover the rest at a different constant speed.
If he started from $A$ at 6 km/h, what was his average speed from $A$ to $B$?

- **(a)** 12 kmph
- **(b)** 15 kmph
- **(c)** 9 kmph
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 12 km/h**

**Why.** The first quarter takes time t at 6 km/h, so D/4 = 6t and D = 24t. The rest takes the same time t, so total time 2t. Average speed = 24t/2t = 12 km/h.

**Concept: average speed = total distance ÷ total time.** Express both in one unknown (t) and it cancels. The second speed (18t/t = 18 km/h) is never needed.

{{< /details >}}

### 4 · Q5, train and platform

*Asked by: Qualcomm (Nov 2024 (HirePro))*

A train travelling at 36 km/h crosses a platform in 50 seconds; the platform's length equals
the length of the train. Find the length (of the train) [cut off in the source].

- **(a)** 300 metres
- **(b)** 250 metres
- **(c)** 225 metres
- **(d)** 200 metres

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 250 metres**

**Why.** 36 km/h = 36 × 5/18 = 10 m/s. In 50 s the train covers 500 m. To cross a platform it must cover platform + its own length = 2L. So L = 250 m.

**Concept: crossing distances.** Crossing a pole or a person: distance = train length. Crossing a platform or bridge: train length + platform length. Convert km/h to m/s by multiplying by 5/18.

{{< /details >}}

### 5 · Q7, boat downstream

*Asked by: Qualcomm (HirePro, Aug 2025)*

Avinash is riding a boat that travels at 62 km/h in still water. It goes 90 km upstream in
3 hours 40 minutes. How long will it take to cover the same distance down the stream? (The
end of the question is cut off; the options are in minutes.)

- **(a)** 58 minutes
- **(b)** 52 minutes
- **(c)** 50 minutes
- **(d)** 54 minutes

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 54 minutes**

**Why.** Upstream speed = 90 km ÷ (3 h 40 min = 11/3 h) = 270/11 ≈ 24.55 km/h. Upstream = boat − stream, so stream = 62 − 24.55 = 37.45 km/h. Downstream = 62 + 37.45 = 99.45 km/h. Time = 90/99.45 h ≈ 54.3 min.

**Concept: boats and streams.** Downstream speed = boat + stream; upstream = boat − stream. From one of them and the still-water speed, you get the stream, then the other.

{{< /details >}}

### 6 · Problem Solving

*Asked by: Qualcomm (60-question online assessment)*

Car P leaves point O at 09:00 at 72 km/h. Car Q leaves O at 09:20 at 96 km/h. Car P makes a 15-minute refuel stop starting at 10:05. When does Q first overtake P, and at what distance from O?

- **(a)** 10:07:30, 76.8 km
- **(b)** 10:10:00, 80.0 km
- **(c)** 10:09:00, 78.4 km
- **(d)** 10:08:45, 78.0 km

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 10:08:45, 78.0 km**

**Why.** P drives from 9:00 to 10:05 at 72 km/h: 72 × 65/60 = 78 km, then stops until 10:20. Q starts at 9:20 at 96 km/h and needs 78/96 h = 48.75 min = 48 min 45 s to reach 78 km: at 10:08:45. P is still parked there, so that is where and when Q passes.

**Concept: check the stop before using relative speed.** If one car stops, relative speed no longer applies; find where the stopped car is and when the other reaches it. Always check whether the meeting happens during the stop, before it or after it.

{{< /details >}}

### 7 · C3, round trip at twice the speed

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Alex drove from city P to city Q in $y$ hours. On the return trip his average speed was
twice as fast. What is the total driving time for the round trip?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 1.5y hours**

**Why.** Same distance at twice the speed takes half the time: y/2. Round trip = y + y/2 = 1.5y.

**Concept: time = distance ÷ speed.** For a fixed distance, time is inversely proportional to speed.

{{< /details >}}

### 8 · a fisherman

*Asked by: Texas Instruments (BITS Pilani)*

20 km up and 40 km down take 6 h; 25 km up and 35 km down take 7 h. Speed of the current?

- **(a)** 12.5
- **(b)** 13.5
- **(c)** 14.5
- **(d)** 15.5
- **(e)** Cannot be determined

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no option matches; the data give a current of 90/7 ≈ 12.9 km/h** (the candidate chose 12.5).

**Why.** Let a = 1/upstream speed and b = 1/downstream speed. 20a + 40b = 6 and 25a + 35b = 7. Scale the first by 5/4: 25a + 50b = 7.5; subtract: 15b = 0.5 → b = 1/30 (downstream 30 km/h). Then 20a = 6 − 4/3 → a = 7/30 (upstream 30/7 km/h). Current = (30 − 30/7)/2 = 90/7 ≈ 12.86.

**Concept: substitute reciprocals.** Time = distance/speed puts speeds in denominators. Setting a = 1/u and b = 1/d makes the equations linear. Then current = (downstream − upstream)/2 and boat = (downstream + upstream)/2.

{{< /details >}}

### 9 · Jill fishing

*Asked by: Texas Instruments (IIT ISM 2024)*

8 km upstream in 4 h and 3 km downstream in 40 min. Time for 10 km in still water?

- **(a)** 3 h 30 min
- **(b)** 4 h
- **(c)** 2 h
- **(d)** 2 h 30 min

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no option matches; the data give about 3 h 5 min.**

**Why.** Upstream: 8 km in 4 h = 2 km/h. Downstream: 3 km in 40 min = 4.5 km/h. Still water = (2 + 4.5)/2 = 3.25 km/h. 10 km takes 10/3.25 ≈ 3.08 h ≈ 3 h 5 min.

**Concept: still-water speed is the average of upstream and downstream speeds**, because the stream adds to one and subtracts from the other by the same amount.

{{< /details >}}

### 10 · overtaking trains

*Asked by: Texas Instruments (BITS Pilani)*

Trains of 65 m (34 km/h) and 70 m (25 km/h) run the same way. Time to pass?

- **(a)** 54
- **(b)** 56
- **(c)** 50
- **(d)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 54 s**

**Why.** Same direction: relative speed = 34 − 25 = 9 km/h = 2.5 m/s. To pass completely the faster train covers both lengths: 65 + 70 = 135 m. Time = 135/2.5 = 54 s.

**Concept: overtaking.** In the same direction subtract speeds; in opposite directions add them. The distance to fully pass is the sum of the two lengths.

{{< /details >}}

### 11 · speeds from times after crossing

*Asked by: Texas Instruments (IISc 2023)*

Two trains start towards each other; after meeting they take 12 s and 3 s to finish. Speed
ratio?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 1 : 2**

**Why.** After meeting, train A takes 12 s and train B 3 s to finish. Speed ratio = √(t_B/t_A) = √(3/12) = 1/2.

**Concept: the √(time) rule.** Before meeting both trains run for the same time T. A then covers B's pre-meeting distance (v_B T) in 12 s, and B covers A's (v_A T) in 3 s. So v_B T = 12 v_A and v_A T = 3 v_B; dividing gives (v_A/v_B)² = 3/12.

{{< /details >}}

### 12 · tracking two vehicles

*Asked by: Texas Instruments (BITS Pilani)*

B leaves at 10 am going south at 40 km/h; A leaves at 2 pm going north at 60 km/h. When are they
460 km apart?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 5 pm**

**Why.** Let t be hours after 10 am. B has gone 40t km south; A, starting at 2 pm, has gone 60(t − 4) km north. They are 40t + 60(t − 4) apart: 100t − 240 = 460 → t = 7, i.e. 5 pm.

**Concept: opposite directions add distances.** Measure time from one fixed moment and give each vehicle its own running time.

{{< /details >}}

### 13 · a moving walkway

*Asked by: Texas Instruments (BITS Pilani)*

Jill (10 m/s) and Adam (5 m/s) run towards each other along a 4500 m walkway moving at 40 m/s.
When do they meet?

- **(a)** 55
- **(b)** 53
- **(c)** 62
- **(d)** 65

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no option matches; the data give 300 s.**

**Why.** The walkway carries both runners at 40 m/s, which does not change the gap between them. Relative to the walkway they close at 10 + 5 = 15 m/s, so 4500/15 = 300 s (5 minutes).

**Concept: choose the right frame.** Motion shared by both objects (a moving walkway, a river current, a moving train) cancels when you look at their separation. Work in the frame of the walkway.

{{< /details >}}

### 14 · cycling and walking

*Asked by: Wells Fargo (SHL test, Oct 2022)*

I started on my bicycle at 7 a.m. to reach a certain place. After some distance the
bicycle broke down; I rested for 35 minutes and walked all the way back home, reaching at
1 p.m. If my cycling speed is 10 km/h and walking speed 1 km/h, what distance did I
cover on the bicycle?

- **(a)** 4.92 km
- **(b)** 13.44 km
- **(c)** 14.375 km
- **(d)** 15.476 km

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 4.92 km**

**Why.** 7 am to 1 pm is 6 h; minus 35 min rest gives 5 h 25 min = 65/12 h of moving. Cycling out d km and walking back d km: d/10 + d/1 = 65/12 → 11d/10 = 65/12 → d = 650/132 ≈ 4.92 km.

**Concept: total time = sum of leg times.** Write each leg's time as distance ÷ speed, subtract any rest from the total, and solve for the unknown distance.

{{< /details >}}
