---
title: "4 · Flow control: stop-and-wait, Go-Back-N, Selective Repeat"
linkTitle: "4 Flow control and ARQ"
weight: 4
math: true
---
**ARQ** (automatic repeat request) = acknowledgements + timeouts + retransmission. All three protocols below use them; they differ in how many frames may be unacknowledged at once (the **window** $W$).

Notation: $T_t$ = transmission time of a frame, $T_p$ = one-way propagation delay, $a = T_p / T_t$.

## 4.1 Stop-and-wait {#cn-4-1}

Send one frame, wait for its ACK, then send the next. Sequence numbers 0/1 are enough.

<div class="nb nb-theorem nb-block">

<strong>Efficiency (link utilisation)</strong>

$$\eta = \frac{T_t}{T_t + 2T_p} = \frac{1}{1 + 2a}, \qquad \text{throughput} = \eta \times \text{bandwidth}.$$

</div>

<div class="nb nb-example">

<strong>Example</strong> (Stop-and-wait)

Frame 1000 bits, link 1 Mbps → $T_t = 1$ ms; $T_p = 10$ ms → $a = 10$. $\eta = 1/21 \approx $ **4.8%**, throughput ≈ **47.6 kbps** on a 1 Mbps link. Long, fast links waste almost all their capacity with stop-and-wait.

</div>

## 4.2 Sliding windows {#cn-4-2}

Let the sender have up to $W$ unacknowledged frames (pipelining):

$$\eta = \min\!\left(1,\ \frac{W}{1 + 2a}\right).$$

To keep the link 100% busy: $W \ge 1 + 2a$. In the example above, $W \ge 21$.

**Go-Back-N (GBN):**

- Receiver window = 1: it accepts only the next expected frame and discards out-of-order ones.
- **Cumulative ACKs** (ACK $n$ means "all up to $n$ received").
- On a timeout or loss, the sender **resends that frame and every frame after it**.
- Simple receiver; wastes bandwidth on errors.

**Selective Repeat (SR):**

- Receiver buffers out-of-order frames; ACKs each frame individually.
- On a loss, **only the lost frame** is resent.
- More complex; efficient on lossy links.

<div class="nb nb-theorem nb-block">

<strong>Window limits with $k$-bit sequence numbers</strong> ($2^k$ numbers)

- Stop-and-wait: $W = 1$, $k = 1$.
- Go-Back-N: $W \le 2^k - 1$.
- Selective Repeat: $W \le 2^{k-1}$ (sender and receiver windows each half the sequence space).

</div>

<div class="nb nb-example">

<strong>Example</strong> (Bits for the sequence number)

We need $W = 21$ for full utilisation. GBN: $2^k - 1 \ge 21$ → $k = $ **5**. SR: $2^{k-1} \ge 21$ → $k = $ **6**. With $k = 3$: GBN window at most 7, SR at most 4.

</div>

<div class="nb nb-example">

<strong>Example</strong> (How many frames are resent?)

GBN with $W = 4$ sends frames 0–6 in a row and frame 2 is lost. The receiver discards 3, 4, 5 (out of order). On timeout the sender resends **2, 3, 4, 5** (and continues with 6). With SR only **2** is resent; 3–5 were buffered.

</div>

<div class="nb nb-remark">

<strong>Why the SR limit is half</strong> — With $k = 2$ (numbers 0–3) and $W = 3$: frames 0, 1, 2 arrive, but all their ACKs are lost. The receiver now expects 3, 0, 1; the sender times out and resends the **old** frame 0, which the receiver mistakes for a **new** frame 0. With $W \le 2$ the old and new windows never overlap.

</div>

<div class="nb nb-moral">

Stop-and-wait efficiency = 1/(1 + 2a). A window of $W$ multiplies it, up to 1 when $W \ge 1 + 2a$. GBN: $W \le 2^k - 1$, resend everything after the loss. SR: $W \le 2^{k-1}$, resend only the lost frame.

</div>
