@@ qcc-dig-54
**Answer: (d) CMOS**

**Why.** In static CMOS, one of the two transistors in each path is always off, so almost no current flows except during switching. ECL uses the most power: its transistors never saturate and current always flows.

**Concept: dynamic power.** CMOS power ≈ C V² f (charging and discharging load capacitance at each switch), plus a little leakage. That is why lowering supply voltage saves power quadratically.

@@ qcc-dig-55
**Answer: (d) Schottky TTL and ECL**

**Why.** ECL keeps its transistors in the active region (they never saturate). Schottky TTL puts a Schottky diode across each transistor's base–collector junction, which stops it from saturating. Both are fast for that reason.

**Concept: saturation delay.** A saturated BJT stores extra charge in its base, which must be removed before it can turn off (storage time). Avoiding saturation speeds up switching.

@@ qcc-dig-56
**Answer: (b) CMOS**

**Why.** CMOS switches near V_DD/2 and its outputs swing rail to rail, giving noise margins of about 30–45% of V_DD. TTL's margins are about 0.4 V.

**Concept: noise margin.** NM_H = V_OH(min) − V_IH(min) and NM_L = V_IL(max) − V_OL(max): how much noise a signal can pick up and still be read correctly.

@@ qcc-dig-57
**Answer: (a) 20**

**Why.** LOW state: the output can sink 8 mA, each input sources 0.1 mA → 80 inputs. HIGH state: the output can source 0.4 mA, each input needs 20 µA → 20 inputs. Fan-out is the smaller: 20.

**Concept: fan-out.** The number of inputs one output can drive while staying within its current limits. Compute it for both logic levels and take the minimum.

@@ qcc-dig-58
**Answer: (c) 11**

**Why.** HIGH: 2 mA / 40 µA = 50. LOW: 20 mA / 1.8 mA = 11.1 → 11. Fan-out = min = 11.

**Concept: fan-out** (see above). The LOW-state input current of TTL-family inputs is usually the limiting factor.

@@ qcc-dig-59
**Answer: (d) 0.8 V**

**Why.** With one input LOW at V_CE(sat) = 0.2 V, node P sits at 0.2 + 0.7 = 0.9 V. The output transistor Q1 starts to turn on when P reaches the cut-in of D1 + D2 + the base–emitter junction: 0.6 + 0.6 + 0.5 = 1.7 V. Noise margin = 1.7 − 0.9 = 0.8 V.

**Concept: DTL gates.** Input diodes perform the AND, and the transistor inverts (NAND). The level-shifting diodes set how much noise the low input can tolerate before the output wrongly switches.

@@ qcc-dig-60
**Answer: (a) Q2 OFF, Q3 ON, Q4 OFF**

**Why.** B grounded clamps node Y at about 0.7 V through its input diode. Turning on D4, Q2 and Q4 together needs about 2.1 V, so Q2 and Q4 stay OFF. With Q2 off, R2 pulls Q3's base high and Q3 (with its diode) pulls the output HIGH. That is NAND behaviour with one input low.

**Concept: TTL totem-pole output.** The upper transistor (pull-up) and lower transistor (pull-down) are driven in opposite states by the phase-splitter; when any input is LOW, the phase splitter is off and the output is pulled HIGH.

@@ qcc-dig-61
**Answer: no reliable pick** (two options were cut off; neither visible option states D's purpose). Choose the option saying D keeps the upper transistor off when the output is LOW.

**Why.** When the output is LOW, Q2 and Q3 conduct, so the upper transistor's base is only at V_CE(sat) + V_BE ≈ 0.9 V. Turning on the upper transistor plus D plus Q3 in series needs about 0.7 + 0.7 + 0.2 = 1.6 V, so D keeps it cut off. Without D, both totem-pole transistors could conduct at once.

**Concept: avoiding shoot-through.** In a push-pull output, the two transistors must never be on together, or a large current flows straight from supply to ground.

@@ qcc-dig-62
**Answer: (a) ESD**

**Why.** Electrostatic discharge is a sudden, very short flow of static charge between two objects at different potentials (the spark when you touch a door handle).

**Concept: ESD protection.** Thousands of volts can destroy thin gate oxides in ICs, so chips have clamp diodes on their pins, and boards are handled with grounding straps.

@@ qcc-dig-63
**Answer: (b) 1.11 kΩ** (the worst-case, largest, on-resistance; the question says "minimum", but this is the value used to size the switch)

**Why.** In the triode region, R_on = 1/[µnCox (W/L)(V_GS − V_th)], with V_GS = 3 − V_in. R_on is largest when V_in is at its peak (0.5 V): R_on = 1/(50 µA/V² × 10 × (2.5 − 0.7)) = 1/(900 µA/V) ≈ 1.11 kΩ.

**Concept: MOS switch resistance.** A MOSFET used as a switch behaves like a resistor that depends on its overdrive (V_GS − V_th). As the input rises, V_GS shrinks and R_on grows, which distorts sampled signals; CMOS transmission gates or bootstrapping reduce this.

@@ qcc-dig-64
**Answer: (c) 0.5 nF**

**Why.** A capacitor discharged by a constant current loses voltage at I/C. Allowed drop ΔV = 3 − 1 = 2 V in Δt = 10 ms at I = 0.1 µA: C = IΔt/ΔV = (0.1 µA × 10 ms)/2 V = 1 nC/2 V = 0.5 nF.

**Concept: Q = CV and DRAM refresh.** A DRAM bit is charge on a tiny capacitor that leaks away, so it must be refreshed (read and rewritten) before the voltage falls below the sensing threshold.

@@ ti-bjt-curves
**Answer: (d) none of these** (all three statements are correct)

**Why.** Common-emitter output characteristics plot collector current I_C (y-axis) against collector–emitter voltage V_CE (x-axis), with one curve per base current I_B.

**Concept: BJT regions on the curves.** Near the y-axis: saturation (V_CE small). Flat part: active region, where I_C ≈ βI_B. Bottom (I_B = 0): cut-off.

@@ ti-bjt-ic
**Answer: (c) 10 mA**

**Why.** With β very large, base current is negligible, so the divider sets V_B = 15 × 5/(10 + 5) = 5 V. V_E = 5 − 0.7 = 4.3 V. I_E = 4.3/430 = 10 mA ≈ I_C. R_C isn't needed (as long as the transistor stays active).

**Concept: voltage-divider bias.** The emitter resistor fixes the current: I_E = (V_B − V_BE)/R_E, almost independent of β. That makes this the most stable common biasing scheme.

@@ ti-cmos
**Answer: both the PMOS and NMOS are in saturation**

**Why.** An inverter amplifies only in the steep middle of its transfer curve, around V_DD/2. There both transistors conduct with V_DS > V_GS − V_th, i.e. both are in saturation, and small input changes cause large output changes.

**Concept: MOSFET regions.** Cut-off (V_GS < V_th), triode/linear (V_DS < V_GS − V_th, acts like a resistor), saturation (V_DS ≥ V_GS − V_th, acts like a current source, used for amplification).

@@ ti-diffamp
**Answer: (d) 400 mV**

**Why.** With matched resistors, a difference amplifier gives V_out = (R_f/R_in)(V₂ − V₁) = (100k/10k)(50 − 10) mV = 10 × 40 = 400 mV.

**Concept: difference amplifier.** It amplifies the difference between two inputs and rejects what they have in common (common-mode rejection), which matters for sensor signals riding on noise.

@@ ti-diode-r2
**Answer: (a) 1.4 kΩ**

**Why.** The diode starts conducting when the voltage across R₂ (from the R₁–R₂ divider, before the diode conducts) reaches 0.7 V: 4R₂/(6.6 + R₂) ≥ 0.7 → 4R₂ ≥ 4.62 + 0.7R₂ → 3.3R₂ ≥ 4.62 → R₂ ≥ 1.4 kΩ.

**Concept: check if a diode conducts.** Remove the diode, find the open-circuit voltage across its position; if it exceeds V_γ, the diode conducts (then clamps that voltage at about 0.7 V).

@@ ti-ideal-opamp
**Answer: (d) infinite output impedance** (it is zero)

**Why.** An ideal op-amp has infinite gain, infinite input impedance (draws no current), infinite bandwidth and **zero** output impedance (it can drive any load without its output voltage dropping).

**Concept: the two golden rules.** With negative feedback: (1) no current flows into the inputs; (2) the op-amp adjusts its output to make V+ = V−. These solve almost every op-amp circuit.

@@ ti-nmos-sat
**Answer: (c)**

**Why.** At pinch-off the channel near the drain disappears, but electrons arriving at the pinch-off point are swept across the short depletion region to the drain by its strong field. Extra V_DS mostly drops across this region, so the current barely changes.

**Concept: saturation in MOSFETs.** I_D ≈ ½µnCox(W/L)(V_GS − V_th)² once V_DS ≥ V_GS − V_th. A slight rise with V_DS remains (channel-length modulation, the λ term).

@@ ti-opamp-16
**Answer: (a) 3.5 V**

**Why.** Non-inverting input: V+ = 6 × 1/(2 + 1) = 2 V. Superposition: non-inverting gain (1 + 3k/1k) = 4 → 8 V; inverting gain −3k/1k = −3 → −4.5 V. V_out = 8 − 4.5 = 3.5 V (within the ±10 V supplies).

**Concept: superposition with op-amps.** Treat each input separately (grounding the other), compute its contribution with the inverting (−R_f/R_in) or non-inverting (1 + R_f/R_in) gain, then add.

@@ ti-opamp-7
**Answer: V_out = 3V₂ − 2V₁**

**Why.** No current flows into the non-inverting input, so V+ = V₂ (the 2 k resistor drops nothing). Superposition: V₂ through the non-inverting gain 1 + 20k/10k = 3; V₁ through the inverting gain −20k/10k = −2.

**Concept: op-amp superposition** (see above).

@@ ti-zener
**Answer: (b) 5 kΩ**

**Why.** The load needs I_L = 5 V/5 kΩ = 1 mA. The series resistor must pass at least that (the zener current can be 0 since the knee current is 0): (10 − 5)/R ≥ 1 mA → R ≤ 5 kΩ.

**Concept: zener regulator design.** The series resistor must supply load current plus at least the zener's minimum (knee) current at the lowest input voltage; otherwise the zener stops regulating.

@@ qcc-dig-70
**Answer: (d) 2 kΩ and 18 F**

**Why.** Three equal resistors in parallel: 6 k/3 = 2 kΩ. Capacitors in parallel add: 3 × 6 = 18 F.

**Concept: series vs parallel rules are opposite for R and C.** Resistors: series add, parallel combine as 1/R = Σ1/Rᵢ. Capacitors: parallel add, series combine as 1/C = Σ1/Cᵢ.

@@ qcc-dig-71
**Answer: (d) √21 A and 315 W**

**Why.** For a sum of a DC term and sinusoids at different frequencies, I²_rms = I₀² + Σ(Iₚₖ²/2) = 4 + 9/2 + 25/2 = 21, so I_rms = √21 A. Only the resistor dissipates power: P = I²_rms R = 21 × 15 = 315 W.

**Concept: RMS of combined signals.** Components at different frequencies are "orthogonal", so their mean squares add. A sine of peak A has RMS A/√2; DC has RMS equal to its value. Inductors and capacitors store and return energy but dissipate none.

@@ qcc-dig-72
**Answer: (b) 6.2 µF**

**Why.** After a 65% drop, 35% remains: 0.35 = e^(−t/RC). So RC = 6.5/ln(1/0.35) = 6.5/1.05 ≈ 6.19 s, and C = 6.19 s / 1 MΩ ≈ 6.2 µF.

**Concept: RC discharge.** V(t) = V₀ e^(−t/τ) with τ = RC. After one τ, 37% remains; after 5τ, under 1%.

@@ qcc-dig-73
**Answer: (a) 2.12 V**

**Why.** Peak-to-peak 6 V → peak 3 V. For a sine wave, RMS = peak/√2 = 3/1.414 ≈ 2.12 V.

**Concept: RMS.** The DC value that would deliver the same power into a resistor. Sine: peak/√2; square wave: peak; triangle: peak/√3.

@@ qcc-dig-74
**Answer: (d) 2**

**Why.** Each RC section contributes one pole; a second-order low-pass (e.g. Sallen–Key) uses two RC pairs around the op-amp.

**Concept: filter order.** An n-th order filter has n poles and rolls off at 20n dB/decade beyond its cutoff. Higher order = sharper transition.

@@ qcc-dig-75
**Answer: (c) 1/f²**

**Why.** Brownian (red) noise is integrated white noise. Integration divides the amplitude spectrum by f, so the power spectrum falls as 1/f². White noise is flat; pink noise is 1/f.

**Concept: coloured noise.** Named by how power density depends on frequency: white (flat), pink (1/f, equal power per octave), Brownian/red (1/f², a random walk).

@@ qcc-dig-76
**Answer: (a) SPST**

**Why.** The figure shows one moving contact (single pole) that closes onto one fixed contact (single throw).

**Concept: switch/relay naming.** Pole = number of separate circuits switched; throw = number of positions each pole can connect to. SPST (simple on/off), SPDT (changeover), DPDT (two changeovers, e.g. for reversing a motor).

@@ ti-caps
**Answer: both end at 7.5 V**

**Why.** Charge is conserved when the capacitors connect: Q = 3 µF × 10 V = 30 µC, shared over 3 + 1 = 4 µF → 30/4 = 7.5 V. The resistor only sets how fast they settle (and dissipates some energy).

**Concept: charge sharing.** Connected capacitors end at a common voltage V = (C₁V₁ + C₂V₂)/(C₁ + C₂). Energy is lost (here 150 µJ → 112.5 µJ) in the resistor, whatever its value.

@@ ti-input-res
**Answer: (d) 60 Ω**

**Why.** Solving the network with nodal analysis gives an equivalent resistance of 60 Ω. (In a balanced bridge no current flows through the middle branch, which simplifies it.)

**Concept: bridges and nodal analysis.** When series/parallel reduction doesn't apply, write KCL at each node and solve. A balanced bridge (equal ratios on both sides) lets you remove the middle resistor.

@@ ti-kirchhoff
**Answer: as photographed, every option swaps KVL and KCL.** The facts: KCL is used for nodal analysis and KVL for mesh analysis.

**Why.** KCL: currents into a node add to zero (charge is conserved). KVL: voltages around any closed loop add to zero (energy is conserved).

**Concept: node vs mesh analysis.** Nodal analysis writes KCL at each node with node voltages as unknowns; mesh analysis writes KVL around each loop with loop currents as unknowns.

@@ ti-maxpower
**Answer: (d) 13 Ω**

**Why.** For a purely resistive load, maximum power transfer occurs when R_L = |Z_s| = √(5² + 12²) = 13 Ω. (A complex load would instead be the conjugate, 5 − j12.)

**Concept: maximum power transfer.** Resistive source: R_L = R_s. Complex source with a complex load: Z_L = Z_s* (conjugate). Resistive load only: R_L = |Z_s|.

@@ ti-rc-switch
**Answer: (b) 3.67 ms**

**Why.** Charging through 5 k with 1 µF gives τ = 5 ms. At 2.5 ms: V_C = 1 − e^(−0.5) = 0.393 V; with S3 open, this is held until 3 ms. Then it discharges into 1 k with τ = 1 ms: 0.393 e^(−(t−3)/1) = 0.2 → t = 3 + ln(0.393/0.2) ≈ 3.67 ms.

**Concept: piecewise RC transients.** Each switching event starts a new exponential from the voltage at that moment, with the new circuit's time constant.

@@ ti-rlc-40
**Answer: only (a)** (at resonance the impedance is R)

**Why.** At resonance X_L = X_C, so they cancel and Z = R. Below resonance the capacitor's reactance (1/ωC) is larger, so the circuit is capacitive; above it the inductor's (ωL) is larger, so inductive. (b) and (c) are reversed.

**Concept: series resonance.** ω₀ = 1/√(LC). The current is largest and in phase with the voltage there. Quality factor Q = ω₀L/R measures how sharp the peak is.

@@ ti-rlc-phase
**Answer: ω = 10,000 rad/s**

**Why.** The current is in phase with the voltage at resonance: ω = 1/√(LC) = 1/√(10⁻³ × 10⁻⁵) = 1/√(10⁻⁸) = 10⁴ rad/s.

**Concept: resonance** (see above): reactances cancel and the circuit looks purely resistive.

@@ ti-rms-current
**Answer: (b) 1/√2 A**

**Why.** At ω = 1 rad/s the series L–C branch has impedance j(ωL − 1/ωC) = j(1 − 1) = 0: a short circuit across the parallel 1 Ω. The source then sees only the series 1 Ω, so i = sin t A, with RMS 1/√2 A.

**Concept: series LC at resonance is a short.** (A parallel LC at resonance is an open circuit.) Check for resonance before doing complex algebra.

@@ ti-superposition
**Answer: linear bilateral networks**

**Why.** Superposition (total response = sum of responses to each source alone) holds only for linear elements. "Bilateral" means elements behave the same for both current directions (R, L, C).

**Concept: superposition.** Turn on one source at a time (voltage sources shorted, current sources opened), solve, and add. It doesn't apply to power (which is quadratic) or to non-linear parts like diodes.

@@ ti-two-port
**Answer: Z₁₂ = −1 Ω**

**Why.** The equations give the admittance matrix Y = [[2, 1], [1, 1]]. Z = Y⁻¹. det Y = 2 − 1 = 1, so Z = [[1, −1], [−1, 2]], and Z₁₂ = −1.

**Concept: two-port parameters.** Z-parameters give voltages from currents (V = ZI); Y-parameters give currents from voltages (I = YV). They are inverses of each other: Z = Y⁻¹.

@@ mw-iisc-1
**Answer: (d) multi-master, multi-slave**

**Why.** Every I²C device has an address, any master can start a transfer, and arbitration on the SDA line resolves collisions when two masters start at once.

**Concept: I²C.** Two wires (SDA data, SCL clock) with pull-up resistors, open-drain outputs. Slower than SPI but needs fewer pins and supports many devices on one bus.

@@ mw-iisc-4
**Answer: (b) an attempt to access memory fails**

**Why.** ARM enters Abort mode on a prefetch abort (fetching an instruction from an invalid address) or a data abort (invalid data access). Undefined instructions use Undefined mode.

**Concept: ARM processor modes.** User, FIQ, IRQ, Supervisor (SVC, system calls/reset), Abort (memory faults), Undefined (unknown instructions), System. Each exception switches to its mode with banked registers.

@@ mw-iisc-5
**Answer: (a) the interrupt service routine**

**Why.** On an interrupt the processor saves its state and jumps to the ISR for that interrupt; when the ISR finishes, it restores state and resumes the interrupted code.

**Concept: interrupts vs polling.** Interrupts let hardware signal events immediately instead of the CPU repeatedly checking (polling), saving time and power.

@@ mw-iisc-6
**Answer: (c) maskable interrupt**

**Why.** A maskable interrupt can be disabled (masked) by software, e.g. during a critical section. A non-maskable interrupt (NMI) cannot be ignored; it is used for emergencies like power failure.

**Concept: interrupt masking.** Disabling interrupts briefly protects shared data in embedded code; keep such sections short to avoid missing events.

@@ qcc-dig-65
**Answer: (b) 0.9375 V**

**Why.** An n-bit DAC outputs V_ref × D/2ⁿ: 3 × 5/16 = 0.9375 V (0101 = 5).

**Concept: R-2R ladder DAC.** A network of only two resistor values that halves the current at each stage, so each bit contributes a binary-weighted share of V_ref. Easy to make accurately on a chip.

@@ qcc-dig-66
**Answer: (a) 65535**

**Why.** 16 bits give 2¹⁶ = 65,536 output levels, which divide the range into 65,536 − 1 = 65,535 equal steps.

**Concept: levels vs steps.** n bits → 2ⁿ levels and 2ⁿ − 1 intervals between the lowest and highest output (like fence posts and gaps).

@@ qcc-dig-67
**Answer: (b) 98 dB**

**Why.** An ideal N-bit converter's quantisation SNR for a full-scale sine is 6.02N + 1.76 dB = 6.02 × 16 + 1.76 ≈ 98 dB.

**Concept: each bit adds about 6 dB.** One more bit halves the quantisation step, which halves the noise amplitude (20 log 2 ≈ 6 dB).

@@ qcc-dig-68
**Answer: (c) op-amp**

**Why.** A SAR ADC's defining blocks are the successive-approximation register, a DAC (often an R-2R ladder), a comparator and a sample-and-hold. A separate op-amp is not one of them (though a DAC may use one internally).

**Concept: SAR ADC.** Binary search on voltage: set the MSB, compare the DAC output with the input, keep or clear the bit, move to the next bit. N bits take N comparisons.

@@ qcc-dig-69
**Answer: no reliable pick** (the computed range is 1117–1141 µA, not offered)

**Why.** Step = 2 mA/255 ≈ 7.84 µA. 10010000 = 144, so the ideal output is 144 × 7.84 ≈ 1129 µA. Full-scale error ±0.6% × 2 mA = ±12 µA, giving 1117–1141 µA. The options are 36 µA wide (±0.9% F.S.), so the question's numbers were probably changed.

**Concept: full-scale error.** Specified as a percentage of the full-scale output and applies equally to every code: output = ideal ± (error% × full scale).

@@ ti-8051-jb
**Answer: (c) JB**

**Why.** `JB bit, label` jumps if the given bit is 1. JC jumps on the carry flag; JZ/JNZ test whether the accumulator is zero.

**Concept: 8051 bit instructions.** The 8051 has bit-addressable memory and instructions like SETB, CLR, JB, JNB, JBC for single-bit control, handy for I/O pins.

@@ ti-8085
**Answer: (a) DCR E; JNZ MULTIPLYLOOP**

**Why.** The routine multiplies by repeated addition: add D to A, decrement the counter E, and loop until E reaches 0. Both instructions are needed: DCR E updates the counter and sets the Zero flag; JNZ loops while it isn't zero.

**Concept: loops in assembly.** Counter in a register, decrement it (which sets flags), conditional jump back. The 8085 has no multiply instruction, so multiplication is repeated addition (or shift-and-add).

@@ ti-adc-step
**Answer: about 9.77 mV**

**Why.** Step size (1 LSB) = full-scale range/2ⁿ = 10 V/1024 ≈ 9.77 mV.

**Concept: ADC resolution.** The smallest input change the converter can distinguish. More bits or a smaller range give finer resolution.

@@ ti-avr
**Answer: conditional branches like BRNE are short relative jumps** (a 7-bit signed offset, −64 to +63 words)

**Why.** BRNE encodes the target as a small offset from the current instruction, so the loop target must be within that range; for farther targets use a reversed branch over an RJMP/JMP.

**Concept: relative vs absolute jumps.** Relative branches store a small offset (compact, position-independent); absolute jumps store the full address (reach anywhere, longer instruction).

@@ ti-mcu-memory
**Answer: SRAM, EEPROM and Flash**

**Why.** Flash holds the program (non-volatile, rewritten rarely), SRAM holds variables and the stack (fast, volatile), EEPROM holds small settings that must survive power-off and change occasionally (byte-erasable).

**Concept: volatile vs non-volatile.** Volatile memory (SRAM, DRAM) loses data without power; non-volatile (Flash, EEPROM, ROM) keeps it.

@@ ti-prep-1
**Answer: (3) slowest, (2) fastest** (official solution)

**Why.** The local `local_sum` lives on the stack (in fast L1), and is copied to the global once at the end: fastest. The global (in .bss, L1 here) is fine too, but every iteration writes to memory. In the official solution, the static `local_sum` sits in .data (in slower L2) and is touched every iteration: slowest. (Most compilers place a zero-initialised static in .bss instead, which would change this.)

**Concept: memory placement matters on embedded systems.** Without a cache, every access goes to the memory the variable lives in. Keep hot variables in fast memory (locals on a fast stack) and write results out once.

@@ ti-prep-4
**Answer: read twice at offset addresses and splice the bytes**

```c
hi = read4bytes(addr);
lo = read4bytes(addr + 1);
return (hi & ~0xFF) | ((lo >> 8) & 0xFF);
```

**Why.** The first read gives correct bytes 1–3 (only byte 0 is garbage). Reading from addr + 1 shifts everything by one byte, so the wanted byte 0 of the original word arrives in byte 1 of the second read, which is reliable. Combine the good parts.

**Concept: working around hardware faults with masks and shifts.** `x & ~0xFF` clears the low byte; `(y >> 8) & 0xFF` extracts byte 1 of y into the low position; `|` merges them.

@@ ti-ripple
**Answer: nearly 5 mV** (about 1 LSB)

**Why.** 1 LSB = 5 V/1024 ≈ 4.9 mV. Ripple on the reference shifts every conversion threshold; to keep errors within about 1 LSB, ripple must stay below roughly that size (stricter designs aim for ½ LSB).

**Concept: reference accuracy.** An ADC measures the input relative to its reference, so any noise or ripple on the reference appears directly as conversion error.

@@ ti-uart
**Answer: (a) TI is not cleared**

**Why.** The 8051 sets the TI flag when a byte has been sent, but never clears it automatically. Without `TI = 0;` after the wait, the next call finds TI already 1 and doesn't wait, so characters overwrite each other.

**Concept: flag-based polling.** Many peripheral flags must be cleared by software to arm them for the next event. Typical pattern: write data, wait for the flag, clear the flag.

@@ mw-iisc-13
**Answer: (a) correlated**

**Why.** Ideal low-pass filtered white noise has autocorrelation R(τ) ∝ sinc(2Bτ), which is zero only at τ = k/(2B) = 0.05k ms for B = 10 kHz. 0.03 ms is not one of those lags, so neighbouring samples are correlated. (At T_s = 0.05 ms they would be uncorrelated, and being Gaussian, independent.)

**Concept: filtering creates correlation.** White noise is uncorrelated at every lag. A filter "smooths" it, so values close in time become similar. Sampling at exactly the Nyquist interval 1/(2B) lands on the zeros of the sinc.

@@ ti-cascade
**Answer (intended): at least one of the systems is unstable, and at least one is causal.** Strictly, nothing follows for certain (pole–zero cancellations can hide instability).

**Why.** If all three were stable, the cascade would be stable; so at least one is unstable. If none were causal, the cascade generally would not be causal. Exact cancellation can break both rules, which is why "strictly nothing" is the careful answer.

**Concept: cascading LTI systems.** The overall transfer function is the product H₁H₂H₃. Stability needs all poles of the product in the left half-plane (continuous time); causality relates to the region of convergence.

@@ ti-delay
**Answer: c(t − 1)** (the output delayed by one second)

**Why.** e^(−s) in the Laplace domain is a pure time delay of 1 s. For an LTI system, delaying the input delays the output by the same amount.

**Concept: time-shift property.** f(t − T) ↔ e^(−sT)F(s). Time invariance means the system responds the same way whenever the input arrives.
