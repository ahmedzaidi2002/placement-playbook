---
title: "Computer architecture and miscellaneous"
weight: 7
---

7 questions asked by Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Digital design flow

*Asked by: Qualcomm (IIIT Delhi 2025, Q50)*

Which of the method(s) given below convert(s) the input-output relationship of a circuit into a digital circuit design?

I. Analysis of combinational logic circuits  
II. Synthesis of combinational logic circuits

- **(a)** Only (II)
- **(b)** Both (I) and (II)
- **(c)** Neither (I) nor (II)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) only (II), synthesis**

**Why.** Synthesis (design) goes from a specification or truth table to a circuit. Analysis goes the other way: from a given circuit to its Boolean functions.

**Concept: design flow.** Specification → truth table → simplified expressions (K-map) → gates. Analysis reverses it to check or understand an existing circuit.

{{< /details >}}

### 2 · Parallel organisation

*Asked by: Qualcomm (IISc 2024, Q25)*

Uni-processors fall into which of the computer system structure categories given in the options?

- **(a)** Single instruction, single data (SISD) stream
- **(b)** Single instruction, multiple data (SIMD) stream
- **(c)** Multiple instruction, multiple data (MIMD) stream
- **(d)** Multiple instruction, single data (MISD) stream

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) SISD**

**Why.** A classic uniprocessor executes one instruction stream on one data stream.

**Concept: Flynn's taxonomy.** SISD (simple CPU), SIMD (one instruction on many data: vector units, GPUs), MISD (rare, fault-tolerant systems), MIMD (multicore and clusters, each core with its own instructions and data).

{{< /details >}}

### 3 · Parallel organisation

*Asked by: Qualcomm (BITS Hyderabad 2025, Q31)*

Which of these statements about multiprocessors are true?

I. Tightly coupled systems use a common memory for all processors.  
II. In tightly coupled systems, jobs from all processors are kept in the same pool.  
III. In loosely coupled systems, each processor has its own private queue.  
IV. Memory is shared in loosely coupled systems.

- **(a)** Only (I)
- **(b)** Only (II), (III) and (IV)
- **(c)** Only (I), (II) and (III)
- **(d)** Only (II) and (III)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) only (I), (II) and (III)**

**Why.** Tightly coupled systems share a common memory and a shared pool of ready jobs (I, II). Loosely coupled systems give each node private memory and its own queue, communicating by messages (III true, IV false).

**Concept: shared-memory vs distributed systems.** Tightly coupled (SMP multicore): easy communication through memory, limited scale. Loosely coupled (clusters): scale further, but communication costs more.

{{< /details >}}

### 4 · Testing

*Asked by: Qualcomm (BITS Goa 2024, Q52)*

What is the term for how easily any particular node X can be set to logic 1 or 0 through input vectors, with the error at X propagated to the output?

- **(a)** Testability
- **(b)** Observability
- **(c)** Controllability
- **(d)** All of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) testability**

**Why.** Setting a node to a value from the inputs is controllability; seeing its effect at an output is observability. A fault at a node can be tested only if you can do both, which together is testability.

**Concept: design for test (DFT).** Chips are made easier to test by adding controllability and observability, e.g. scan chains that let a tester set and read every flip-flop.

{{< /details >}}

### 5 · Testing

*Asked by: Qualcomm (Delhi campus 2024, Q51)*

The figure (a verification flow with test-case planning, VIP classes, an execution platform and tracking) is shown. Which of the following is best suited and used in the areas of DFT?

- **(a)** Timing analysis
- **(b)** Fault models
- **(c)** Delay calculation
- **(d)** Silicon debugging

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) fault models**

**Why.** DFT generates test patterns against fault models (stuck-at-0/1, transition, bridging faults) and measures fault coverage. Timing analysis, delay calculation and silicon debugging belong to other parts of the flow.

**Concept: stuck-at fault model.** Assume a single wire is stuck at 0 or 1; a test pattern "detects" it if the output differs from the fault-free circuit. Fault coverage = detected faults / total faults.

{{< /details >}}

### 6 · observability

*Asked by: Texas Instruments (IISc 2023)*

With high observability, are more or fewer test cycles needed?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: fewer test cycles**

**Why.** With high observability, the effect of internal faults is visible at outputs quickly, so fewer patterns and cycles are needed to detect them.

**Concept: controllability and observability** together decide how hard a circuit is to test.

{{< /details >}}

### 7 · RTL logic

*Asked by: Texas Instruments (NIT Calicut 2023)*

The primary advantage of resistor-transistor logic?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: a minimum number of transistors**

**Why.** Resistor–transistor logic uses resistors at the inputs and one transistor per input, so it needs very few transistors (the expensive part in early ICs). Its downsides are low speed, poor fan-out and high power.

**Concept: logic family evolution.** RTL → DTL (diodes at inputs) → TTL (multi-emitter transistors, faster) → CMOS (near-zero static power, dominant today).

{{< /details >}}
