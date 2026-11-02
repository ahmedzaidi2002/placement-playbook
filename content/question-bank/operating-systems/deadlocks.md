---
title: "Deadlocks"
weight: 4
---

8 questions asked by Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q37, livelock

*Asked by: Qualcomm (IISc)*

What is it called when two or more processes keep changing their states in response to
changes in the other processes without doing any meaningful work?

- **(a)** Atomic operation
- **(b)** Deadlock
- **(c)** Critical section
- **(d)** Livelock

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) livelock**

**Why.** In a livelock the processes are not blocked; they keep reacting to each other (like two people stepping aside the same way in a corridor) but make no progress.

**Concept: deadlock vs livelock vs starvation.** Deadlock: processes wait forever for each other, doing nothing. Livelock: processes keep changing state but achieve nothing. Starvation: one process never gets a resource while others proceed.

{{< /details >}}

### 2 · Operating Systems

*Asked by: Qualcomm (60-question online assessment)*

What is the order of the steps in a **deadlock detection algorithm**?

- (I) Initialise the temporary vector to the available vector.
- (II) Find the currently unmarked process.
- (III) If a row is not found, terminate the algorithm.
- (IV) If a row is found, add that row to the allocation matrix.
- (V) Mark the process that has a row of all zeroes.

- **(a)** (IV), (V), (III), (I) and (II)
- **(b)** (V), (I), (II), (IV) and (III)
- **(c)** (II), (I), (III), (IV) and (V)
- **(d)** (I), (II), (IV), (III) and (V)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) (I), (II), (IV), (III), (V)**

**Why.** Detection starts by initialising the work (temporary) vector to the available resources. Then repeatedly find an unmarked process whose request can be met; if found, add its allocation back to work (it can finish and release resources); if none is found, stop. Processes left unmarked are deadlocked. Only option (d) starts with initialisation.

**Concept: deadlock detection.** Like the banker's safety check, but with current requests instead of maximum needs: pretend each satisfiable process finishes and returns its resources; whoever can never finish is deadlocked.

{{< /details >}}

### 3 · Deadlock

*Asked by: Qualcomm (Delhi campus 2024, Q49)*

Which of the following are methods for handling deadlocks?

I. Use a protocol to prevent or avoid deadlocks.  
II. Allow the system to enter a deadlocked state, detect it, and recover.  
III. Ignore the problem and pretend that deadlocks never occur.

- **(a)** Only (I) and (III)
- **(b)** Only (I)
- **(c)** All (I), (II) and (III)
- **(d)** Only (I) and (II)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) all three**

**Why.** The textbook strategies: prevent or avoid deadlocks (I), let them happen then detect and recover (II), or ignore them (III, the "ostrich algorithm"), which most general-purpose systems such as Linux and Windows do.

**Concept: deadlock strategies.** Prevention breaks a necessary condition; avoidance checks each request (banker's algorithm); detection finds cycles and kills or rolls back processes; ignoring is cheap when deadlocks are rare.

{{< /details >}}

### 4 · Deadlock

*Asked by: Qualcomm (BITS Goa 2024, Q36)*

In deadlock avoidance, a request for a resource that is currently available is granted:

I. only if the allocation leaves the system in a safe state.  
II. if the allocation leaves the system in a safe or an unsafe state.

- **(a)** Only (I)
- **(b)** Both (I) and (II)
- **(c)** Only (II)
- **(d)** Neither (I) nor (II)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) only (I)**

**Why.** Avoidance (e.g. the banker's algorithm) grants a request only if the resulting state is safe. Otherwise the process waits, even though the resource is free right now.

**Concept: safe state.** A state is safe if there is some order in which every process can get its maximum need and finish. Unsafe does not mean deadlocked yet, but deadlock becomes possible, so avoidance never enters it.

{{< /details >}}

### 5 · Deadlock

*Asked by: Qualcomm (IISc 2024, Q39)*

What will happen if a system does not employ either a deadlock-prevention or a deadlock-avoidance algorithm?

- **(a)** Nothing will happen.
- **(b)** Deadlock situation may not arise.
- **(c)** Deadlock situation arise.
- **(d)** Deadlock situation may arise.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) a deadlock may arise**

**Why.** Without prevention or avoidance nothing rules deadlock out, but it is not guaranteed either. If one happens, the system needs detection and recovery.

**Concept: necessary conditions are not certainty.** Deadlock needs all four Coffman conditions; their being possible does not mean they will line up.

{{< /details >}}

### 6 · Deadlock

*Asked by: Qualcomm (NIT Durgapur, Q52)*

Which one of the given options is true if information such as "which resources a process will request" is given in advance?

- **(a)** The operating system cannot decide whether the process should not wait for each request.
- **(b)** The operating system cannot decide whether the process should wait for each request.
- **(c)** The operating system cannot decide whether the current request can be satisfied or must be delayed.
- **(d)** The operating system can decide whether or not the process should wait for each request.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) the OS can decide whether the process should wait for each request**

**Why.** Knowing future requests in advance is exactly what deadlock avoidance needs: for each request, the OS checks whether granting it keeps the system safe, and makes the process wait if not.

**Concept: avoidance needs advance information.** The banker's algorithm requires each process to declare its maximum need up front.

{{< /details >}}

### 7 · circular wait

*Asked by: Texas Instruments (BITS Pilani)*

A: Circular wait is necessary for deadlock. B: Circular wait is sufficient for deadlock.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: A true, B false**

**Why.** Circular wait is one of the four conditions that must all hold for deadlock, so it is necessary. It is not sufficient alone: if a resource has several instances, or can be preempted, a cycle in the wait graph need not be a deadlock.

**Concept: the Coffman conditions.** Mutual exclusion, hold and wait, no preemption, circular wait. Deadlock is possible only if all four hold; breaking any one prevents it.

{{< /details >}}

### 8 · preventing deadlocks

*Asked by: Texas Instruments (IIT BHU 2023)*

A: Permitting resource preemption alone will prevent deadlocks. B: Preventing circular wait
alone will prevent deadlocks.

- **(a)** Both true
- **(b)** A true B false
- **(c)** A false B true
- **(d)** Both false

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) both true** (many keys say "A false, B true", because preemption is impractical for resources like printers)

**Why.** Deadlock needs all four Coffman conditions, so removing any one of them, including "no preemption" (A) or "circular wait" (B), prevents deadlock in principle.

**Concept: prevention techniques.** Break hold-and-wait (request everything at once), allow preemption (take resources away), or break circular wait (number resources and request them in increasing order, the most practical).

{{< /details >}}
