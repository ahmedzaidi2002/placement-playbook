---
title: "Analog devices and op-amps"
weight: 1
---

21 questions asked by Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Logic families

*Asked by: Qualcomm (BITS Goa 2024, Q48)*

Which digital IC family consumes the minimum power?

- **(a)** ECL
- **(b)** DTL
- **(c)** TTL
- **(d)** CMOS

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) CMOS**

**Why.** In static CMOS, one of the two transistors in each path is always off, so almost no current flows except during switching. ECL uses the most power: its transistors never saturate and current always flows.

**Concept: dynamic power.** CMOS power ≈ C V² f (charging and discharging load capacitance at each switch), plus a little leakage. That is why lowering supply voltage saves power quadratically.

{{< /details >}}

### 2 · Logic families

*Asked by: Qualcomm (2025 paper (campus not named), Q45)*

Which logic families are non-saturated?

- **(a)** RTL and TTL
- **(b)** TTL and DCTL
- **(c)** DTL and HTL
- **(d)** Schottky TTL and ECL

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Schottky TTL and ECL**

**Why.** ECL keeps its transistors in the active region (they never saturate). Schottky TTL puts a Schottky diode across each transistor's base–collector junction, which stops it from saturating. Both are fast for that reason.

**Concept: saturation delay.** A saturated BJT stores extra charge in its base, which must be removed before it can turn off (storage time). Avoiding saturation speeds up switching.

{{< /details >}}

### 3 · Logic families

*Asked by: Qualcomm (IIIT Delhi 2025, Q52)*

Which one of the given families has the highest noise margin?

- **(a)** Schottky TTL
- **(b)** CMOS
- **(c)** Standard TTL
- **(d)** Low-power Schottky TTL

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) CMOS**

**Why.** CMOS switches near V_DD/2 and its outputs swing rail to rail, giving noise margins of about 30–45% of V_DD. TTL's margins are about 0.4 V.

**Concept: noise margin.** NM_H = V_OH(min) − V_IH(min) and NM_L = V_IL(max) − V_OL(max): how much noise a signal can pick up and still be read correctly.

{{< /details >}}

### 4 · Logic families

*Asked by: Qualcomm (Delhi campus 2024, Q49)*

How many 74ALS00 NAND-gate inputs can be driven by one 74ALS00 NAND-gate output? Given I_OL(max) = 8 mA, I_IL(max) = 0.1 mA, I_OH(max) = 0.4 mA, I_IH(max) = 20 µA.

- **(a)** 20
- **(b)** 8
- **(c)** 10
- **(d)** 15

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 20**

**Why.** LOW state: the output can sink 8 mA, each input sources 0.1 mA → 80 inputs. HIGH state: the output can source 0.4 mA, each input needs 20 µA → 20 inputs. Fan-out is the smaller: 20.

**Concept: fan-out.** The number of inputs one output can drive while staying within its current limits. Compute it for both logic levels and take the minimum.

{{< /details >}}

### 5 · Logic families

*Asked by: Qualcomm (IISc 2024, Q57)*

The output of an inverter drives a parallel register made of 74AS74 D flip-flops. What is the maximum number of flip-flop CLR inputs this gate can drive? Given I_IH = 40 µA, I_IL = 1.8 mA, I_OH = 2 mA, I_OL = 20 mA.

- **(a)** 40
- **(b)** 35
- **(c)** 11
- **(d)** 50

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 11**

**Why.** HIGH: 2 mA / 40 µA = 50. LOW: 20 mA / 1.8 mA = 11.1 → 11. Fan-out = min = 11.

**Concept: fan-out** (see above). The LOW-state input current of TTL-family inputs is usually the limiting factor.

{{< /details >}}

### 6 · Logic families

*Asked by: Qualcomm (BITS Hyderabad 2024)*

For the DTL NAND gate shown, V_γ(BE) = 0.5 V, V_CE(sat) = 0.2 V, the drop across a conducting diode is 0.7 V and the diode cut-in voltage is 0.6 V. What is the noise margin when one input is LOW?

<figure class="nb-fig"><img src="/companies/qualcomm/core/dtl-nand.svg" alt="Figure for question 6" loading="lazy"></figure>

- **(a)** 0.9 V
- **(b)** 0.5 V
- **(c)** 0.6 V
- **(d)** 0.8 V

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 0.8 V**

**Why.** With one input LOW at V_CE(sat) = 0.2 V, node P sits at 0.2 + 0.7 = 0.9 V. The output transistor Q1 starts to turn on when P reaches the cut-in of D1 + D2 + the base–emitter junction: 0.6 + 0.6 + 0.5 = 1.7 V. Noise margin = 1.7 − 0.9 = 0.8 V.

**Concept: DTL gates.** Input diodes perform the AND, and the transistor inverts (NAND). The level-shifting diodes set how much noise the low input can tolerate before the output wrongly switches.

{{< /details >}}

### 7 · Logic families

*Asked by: Qualcomm (BITS Hyderabad 2025, Q58)*

In the TTL NAND circuit shown, input A = +5 V and input B is grounded. Which is true about Q2, Q3 and Q4?

<figure class="nb-fig"><img src="/companies/qualcomm/core/ttl-nand.svg" alt="Figure for question 7" loading="lazy"></figure>

- **(a)** Q2 OFF, Q3 ON, Q4 OFF
- **(b)** Q2 ON, Q3 ON, Q4 OFF
- **(c)** Q2 OFF, Q3 OFF, Q4 ON
- **(d)** Q2, Q3 and Q4 all OFF

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Q2 OFF, Q3 ON, Q4 OFF**

**Why.** B grounded clamps node Y at about 0.7 V through its input diode. Turning on D4, Q2 and Q4 together needs about 2.1 V, so Q2 and Q4 stay OFF. With Q2 off, R2 pulls Q3's base high and Q3 (with its diode) pulls the output HIGH. That is NAND behaviour with one input low.

**Concept: TTL totem-pole output.** The upper transistor (pull-up) and lower transistor (pull-down) are driven in opposite states by the phase-splitter; when any input is LOW, the phase splitter is off and the output is pulled HIGH.

{{< /details >}}

### 8 · Logic families

*Asked by: Qualcomm (IIIT Delhi 2025, Q53)*

For the TTL NOT gate shown, the diode D at the output node is used:

<figure class="nb-fig"><img src="/companies/qualcomm/core/ttl-not.svg" alt="Figure for question 8" loading="lazy"></figure>

- **(a)** to restore the logic level degradation
- **(b)** to provide necessary collector-emitter drop across Q2
- **(c)** (option not visible)
- **(d)** (option not visible)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (two options were cut off; neither visible option states D's purpose). Choose the option saying D keeps the upper transistor off when the output is LOW.

**Why.** When the output is LOW, Q2 and Q3 conduct, so the upper transistor's base is only at V_CE(sat) + V_BE ≈ 0.9 V. Turning on the upper transistor plus D plus Q3 in series needs about 0.7 + 0.7 + 0.2 = 1.6 V, so D keeps it cut off. Without D, both totem-pole transistors could conduct at once.

**Concept: avoiding shoot-through.** In a push-pull output, the two transistors must never be on together, or a large current flows straight from supply to ground.

{{< /details >}}

### 9 · Logic families

*Asked by: Qualcomm (BITS Hyderabad 2025, Q42)*

A sudden flow of static electricity between two electrically charged objects for a very short time is:

- **(a)** ESD
- **(b)** Avalanche breakdown
- **(c)** Pinch-off
- **(d)** Short circuit

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) ESD**

**Why.** Electrostatic discharge is a sudden, very short flow of static charge between two objects at different potentials (the spark when you touch a door handle).

**Concept: ESD protection.** Thousands of volts can destroy thin gate oxides in ICs, so chips have clamp diodes on their pins, and boards are handled with grounding straps.

{{< /details >}}

### 10 · MOS circuits

*Asked by: Qualcomm (BITS Hyderabad 2025, Q41)*

In the sampling circuit shown, M1's gate is at +3 V, the input is a 0.5 V sine wave at 10 MHz, C_H = 1 pF, µnCox = 50 µA/V², W/L = 10/1, V_th = 0.7 V, V_DD = 3 V, γ = 0. Find the (worst-case) on-resistance of M1.

<figure class="nb-fig"><img src="/companies/qualcomm/core/sample-switch.svg" alt="Figure for question 10" loading="lazy"></figure>

- **(a)** 2.5 kΩ
- **(b)** 1.11 kΩ
- **(c)** 5 kΩ
- **(d)** 3.25 kΩ

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1.11 kΩ** (the worst-case, largest, on-resistance; the question says "minimum", but this is the value used to size the switch)

**Why.** In the triode region, R_on = 1/[µnCox (W/L)(V_GS − V_th)], with V_GS = 3 − V_in. R_on is largest when V_in is at its peak (0.5 V): R_on = 1/(50 µA/V² × 10 × (2.5 − 0.7)) = 1/(900 µA/V) ≈ 1.11 kΩ.

**Concept: MOS switch resistance.** A MOSFET used as a switch behaves like a resistor that depends on its overdrive (V_GS − V_th). As the input rises, V_GS shrinks and R_on grows, which distorts sampled signals; CMOS transmission gates or bootstrapping reduce this.

{{< /details >}}

### 11 · MOS circuits

*Asked by: Qualcomm (BITS Goa 2024, Q42)*

A cell in a DRAM must hold 3 V, and the voltage must stay above 1 V. It is refreshed every 10 ms and the leakage (discharge) current is 0.1 µA. What is the storage capacitance?

- **(a)** 1 nF
- **(b)** 10 mF
- **(c)** 0.5 nF
- **(d)** 0.1 µF

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 0.5 nF**

**Why.** A capacitor discharged by a constant current loses voltage at I/C. Allowed drop ΔV = 3 − 1 = 2 V in Δt = 10 ms at I = 0.1 µA: C = IΔt/ΔV = (0.1 µA × 10 ms)/2 V = 1 nC/2 V = 0.5 nF.

**Concept: Q = CV and DRAM refresh.** A DRAM bit is charge on a tiny capacitor that leaks away, so it must be refreshed (read and rewritten) before the voltage falls below the sensing threshold.

{{< /details >}}

### 12 · BJT output characteristics

*Asked by: Texas Instruments (NIT Calicut 2023)*

Which is incorrect about the common-emitter output characteristics shown?

- **(a)** x-axis is VCE
- **(b)** y-axis is IC
- **(c)** Each curve is a different base current
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) none of these** (all three statements are correct)

**Why.** Common-emitter output characteristics plot collector current I_C (y-axis) against collector–emitter voltage V_CE (x-axis), with one curve per base current I_B.

**Concept: BJT regions on the curves.** Near the y-axis: saturation (V_CE small). Flat part: active region, where I_C ≈ βI_B. Bottom (I_B = 0): cut-off.

{{< /details >}}

### 13 · collector current

*Asked by: Texas Instruments (NIT Calicut 2023)*

15 V, divider 10 k / 5 k, $R_E = 430\ \Omega$, $\beta$ very large, $V_{BE} = 0.7$. $I_C$?

- **(a)** 1 mA
- **(b)** 5 mA
- **(c)** 10 mA
- **(d)** Cannot be found since Rc is not given

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 10 mA**

**Why.** With β very large, base current is negligible, so the divider sets V_B = 15 × 5/(10 + 5) = 5 V. V_E = 5 − 0.7 = 4.3 V. I_E = 4.3/430 = 10 mA ≈ I_C. R_C isn't needed (as long as the transistor stays active).

**Concept: voltage-divider bias.** The emitter resistor fixes the current: I_E = (V_B − V_BE)/R_E, almost independent of β. That makes this the most stable common biasing scheme.

{{< /details >}}

### 14 · CMOS inverter as amplifier

*Asked by: Texas Instruments (IISc 2023)*

When a CMOS inverter acts as an amplifier, its transistors are in:

{{< details title="Answer and explanation" closed="true" >}}

**Answer: both the PMOS and NMOS are in saturation**

**Why.** An inverter amplifies only in the steep middle of its transfer curve, around V_DD/2. There both transistors conduct with V_DS > V_GS − V_th, i.e. both are in saturation, and small input changes cause large output changes.

**Concept: MOSFET regions.** Cut-off (V_GS < V_th), triode/linear (V_DS < V_GS − V_th, acts like a resistor), saturation (V_DS ≥ V_GS − V_th, acts like a current source, used for amplification).

{{< /details >}}

### 15 · difference amplifier

*Asked by: Texas Instruments (NIT Calicut 2023)*

10 mV and 50 mV into a difference amplifier with 10 k inputs and 100 k feedback/ground.

- **(a)** 500 mV
- **(b)** 100 mV
- **(c)** 600 mV
- **(d)** 400 mV

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 400 mV**

**Why.** With matched resistors, a difference amplifier gives V_out = (R_f/R_in)(V₂ − V₁) = (100k/10k)(50 − 10) mV = 10 × 40 = 400 mV.

**Concept: difference amplifier.** It amplifies the difference between two inputs and rejects what they have in common (common-mode rejection), which matters for sensor signals riding on noise.

{{< /details >}}

### 16 · turning a diode on

*Asked by: Texas Instruments (NIT Calicut 2023)*

$V_{in} = 4$ V through $R_1 = 6.6$ k$\Omega$ to a diode ($V_\gamma = 0.7$) in parallel with
$R_2$. Minimum $R_2$ for the diode to conduct?

- **(a)** 1.4 k
- **(b)** 1.8 k
- **(c)** 2.4 k
- **(d)** 3 k

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 1.4 kΩ**

**Why.** The diode starts conducting when the voltage across R₂ (from the R₁–R₂ divider, before the diode conducts) reaches 0.7 V: 4R₂/(6.6 + R₂) ≥ 0.7 → 4R₂ ≥ 4.62 + 0.7R₂ → 3.3R₂ ≥ 4.62 → R₂ ≥ 1.4 kΩ.

**Concept: check if a diode conducts.** Remove the diode, find the open-circuit voltage across its position; if it exceeds V_γ, the diode conducts (then clamps that voltage at about 0.7 V).

{{< /details >}}

### 17 · ideal op-amp

*Asked by: Texas Instruments (NIT Calicut 2023)*

Which is incorrect about an ideal op-amp?

- **(a)** Infinite gain
- **(b)** Infinite input impedance
- **(c)** Infinite bandwidth
- **(d)** Infinite output impedance

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) infinite output impedance** (it is zero)

**Why.** An ideal op-amp has infinite gain, infinite input impedance (draws no current), infinite bandwidth and **zero** output impedance (it can drive any load without its output voltage dropping).

**Concept: the two golden rules.** With negative feedback: (1) no current flows into the inputs; (2) the op-amp adjusts its output to make V+ = V−. These solve almost every op-amp circuit.

{{< /details >}}

### 18 · why the drain current saturates

*Asked by: Texas Instruments (NIT Calicut 2023)*

The square-law model of an nMOS predicts a parabola, but in reality $I_D$ stays nearly
constant beyond $V_{DS} = V_{GS} - V_{TH}$. Why?

- **(a)** Some channel still exists even when $V_{DS} > V_{GS} - V_{TH}$
- **(b)** The channel is pinched off but current flows due to minority charge carriers
- **(c)** Past the pinch-off point, the electrons shoot through the depletion region near the drain junction and arrive at the drain terminal
- **(d)** $V_{DS}$ is so high that current flows from the bulk to the drain via the substrate

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c)**

**Why.** At pinch-off the channel near the drain disappears, but electrons arriving at the pinch-off point are swept across the short depletion region to the drain by its strong field. Extra V_DS mostly drops across this region, so the current barely changes.

**Concept: saturation in MOSFETs.** I_D ≈ ½µnCox(W/L)(V_GS − V_th)² once V_DS ≥ V_GS − V_th. A slight rise with V_DS remains (channel-length modulation, the λ term).

{{< /details >}}

### 19 · op-amp with two inputs

*Asked by: Texas Instruments (NIT Calicut 2023)*

1.5 V through 1 k to the inverting input, feedback 3 k; 6 V through a 2 k/1 k divider to the
non-inverting input; supplies $\pm 10$ V.

- **(a)** 3.5 V
- **(b)** 4.0 V
- **(c)** 4.5 V
- **(d)** 3.0 V

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 3.5 V**

**Why.** Non-inverting input: V+ = 6 × 1/(2 + 1) = 2 V. Superposition: non-inverting gain (1 + 3k/1k) = 4 → 8 V; inverting gain −3k/1k = −3 → −4.5 V. V_out = 8 − 4.5 = 3.5 V (within the ±10 V supplies).

**Concept: superposition with op-amps.** Treat each input separately (grounding the other), compute its contribution with the inverting (−R_f/R_in) or non-inverting (1 + R_f/R_in) gain, then add.

{{< /details >}}

### 20 · op-amp output

*Asked by: Texas Instruments (NIT Calicut 2023)*

$V_1$ through 10 k to the inverting input, feedback 20 k, $V_2$ through 2 k to the
non-inverting input. $V_{out}$?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: V_out = 3V₂ − 2V₁**

**Why.** No current flows into the non-inverting input, so V+ = V₂ (the 2 k resistor drops nothing). Superposition: V₂ through the non-inverting gain 1 + 20k/10k = 3; V₁ through the inverting gain −20k/10k = −2.

**Concept: op-amp superposition** (see above).

{{< /details >}}

### 21 · zener regulator

*Asked by: Texas Instruments (NIT Calicut 2023)*

$V_{in} = 10$ V, $V_Z = 5$ V, $R_L = 5$ k, knee current 0. Maximum series $R$?

- **(a)** 4 k
- **(b)** 5 k
- **(c)** 3 k
- **(d)** 2 k

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 5 kΩ**

**Why.** The load needs I_L = 5 V/5 kΩ = 1 mA. The series resistor must pass at least that (the zener current can be 0 since the knee current is 0): (10 − 5)/R ≥ 1 mA → R ≤ 5 kΩ.

**Concept: zener regulator design.** The series resistor must supply load current plus at least the zener's minimum (knee) current at the lowest input voltage; otherwise the zener stops regulating.

{{< /details >}}
