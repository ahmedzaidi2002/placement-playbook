---
title: "4 · Optimisers and learning-rate schedules"
linkTitle: "4 Optimisers"
weight: 4
math: true
---
Backprop gives the gradient; the optimiser decides what to do with it. The OA version is "what is the purpose of Adam?" and one hand-computed update. The interview version is why plain gradient descent zig-zags, what momentum and Adam fix, why Adam needs bias correction, and why the schedule matters as much as the optimiser.

## 4.1 Gradient descent and its one big problem {#dl-4-1}

$\theta \leftarrow \theta - \eta \nabla L(\theta)$. Near a minimum the loss is roughly a bowl; gradient descent converges only if $\eta < 2/\lambda_{\max}$ (the steepest curvature), and then the flattest direction crawls. The **condition number** $\kappa = \lambda_{\max}/\lambda_{\min}$ sets the speed. In a long thin valley the gradient points **across** the valley, so a step large enough to make progress along it overshoots across it: **zig-zag**. Every optimiser in this chapter is, one way or another, a fix for ill-conditioning.

**Mini-batches:** a gradient over $B$ random examples is an unbiased estimate of the full gradient whose variance falls like $1/B$. "SGD" in deep learning almost always means mini-batch SGD.

<div class="nb nb-example">

<strong>Example</strong> (Steps and epochs)

An **iteration** processes one mini-batch; an **epoch** is one pass over the data. $N = 50{,}000$, $B = 128$: $\lceil 50000/128\rceil = 391$ iterations per epoch (the last batch is partial), so 30 epochs are 11,730 steps.

</div>

## 4.2 Momentum and Nesterov {#dl-4-2}

Keep a running sum of past gradients: $v \leftarrow \beta v + g$, $\theta \leftarrow \theta - \eta v$ (PyTorch's convention). Components that keep their sign add up (on a constant slope the step grows to $1/(1-\beta)$ times, 10× for $\beta = 0.9$); components that flip sign every step cancel. That is exactly the valley geometry: a ball rolling down keeps its speed along the floor and damps the side-to-side bounce. With good settings the iteration count scales with $\sqrt{\kappa}$ instead of $\kappa$.

**Nesterov** evaluates the gradient at the look-ahead point, so it reacts one step earlier when about to overshoot.

<div class="nb nb-example">

<strong>Example</strong> (Two momentum steps)

$\eta = 0.1$, $\beta = 0.9$, $\theta_0 = 1$, gradients 2 then 1: $v_1 = 2$, $\theta_1 = 0.8$; $v_2 = 0.9 \cdot 2 + 1 = 2.8$, $\theta_2 = 0.52$. The second gradient is half the first, yet the second step is larger.

</div>

## 4.3 AdaGrad, RMSProp, Adam {#dl-4-3}

Adaptive methods give **each parameter its own step size**, dividing by a running estimate of its gradient scale:

- **AdaGrad:** divide by the root of the **sum** of all squared gradients. Rare features get big steps, but the sum only grows, so the step dies too early for deep networks.
- **RMSProp:** use an **exponential moving average** of squared gradients instead, so the step does not die.
- **Adam** = momentum on $g$ + RMSProp on $g^2$ + bias correction:

$$m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t, \quad v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2, \quad \theta_t = \theta_{t-1} - \eta\,\frac{\hat m_t}{\sqrt{\hat v_t} + \varepsilon},$$

with $\hat m_t = m_t/(1 - \beta_1^t)$, $\hat v_t = v_t/(1 - \beta_2^t)$; defaults $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\varepsilon = 10^{-8}$.

**Why bias correction:** $m$ and $v$ start at 0, so early on they are biased towards 0 by exactly the factor $1 - \beta^t$; dividing removes it. It matters most for $v$, because $1 - 0.999^t$ stays small for hundreds of steps. Without it the very first step would be about $3.16\,\eta$, a too-large step at the moment the estimates are least reliable.

<div class="nb nb-example">

<strong>Example</strong> (Adam's first step)

Gradients $0.5$ and $-0.02$ on two parameters, $\eta = 10^{-3}$. After bias correction $\hat m = g$ and $\hat v = g^2$, so each moves by $\eta\, g/|g|$: **both move by exactly 0.001**, one down and one up. The 25-fold difference in gradient size disappears: that is the per-parameter rescaling.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "What is the purpose of Adam?" is not "to add momentum" and not "to reduce overfitting". Adam gives each parameter its own effective learning rate, scaled by the inverse RMS of its recent gradients, combined with momentum: fast, robust progress with little tuning. It does not regularise. And "Adam always beats SGD" is false: on many image benchmarks well-tuned SGD with momentum matches or beats it; Adam and especially AdamW dominate for Transformers.

</div>

**AdamW:** with plain SGD, adding $\tfrac{\lambda}{2}\|\theta\|^2$ to the loss and shrinking the weights by $(1 - \eta\lambda)$ each step are the same. Under Adam they are **not**: the L2 gradient $\lambda\theta$ gets divided by $\sqrt{\hat v}$, so parameters with large gradient history are barely decayed. **AdamW decouples** the decay ($\theta \leftarrow \theta(1 - \eta\lambda)$ outside the adaptive step) so $\lambda$ means what it says. It is the default for Transformers.

## 4.4 Learning-rate schedules {#dl-4-4}

A large rate early makes fast progress; a small one late lets the iterate settle (Adam at a fixed rate keeps hovering around the minimum). Schedules interpolate:

- **Step decay:** multiply by $\gamma$ every $s$ epochs ($0.1$ every 30 epochs: $0.1 \to 0.01 \to 0.001$).
- **Cosine decay:** $\eta_t = \tfrac12\eta_0\big(1 + \cos(\pi t/T)\big)$; from 0.1 over 100 epochs it is 0.0854 at epoch 25, 0.05 at 50, 0.0146 at 75.
- **Warm-up:** ramp up linearly over the first few hundred or thousand steps. Early on the weights are random, gradients can be large and Adam's second-moment estimate rests on a handful of samples, so a full-size step is risky; **Transformers often diverge without warm-up**.
- **One-cycle:** up then down in one cycle, popular for short budgets.

<div class="nb nb-remark">

<strong>In my project</strong> (Transformer) — The [from-scratch Transformer](../../../projects/transformer/) used the **Noam schedule** from the original paper: linear warm-up for 4,000 steps, then decay proportional to $1/\sqrt{\text{step}}$, scaled by $d_{\text{model}}^{-1/2}$. The trap found in the project: with 227 steps per epoch, warm-up lasts about **17.6 epochs**, so the 15-epoch runs ($3{,}405$ steps) **never finished warming up**; only the 30-epoch run reached the peak rate. If asked "what would you change?": shorten the warm-up (for example 1,000 steps) or use a smaller batch for more updates per epoch.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — In PyTorch, schedulers are stepped explicitly. Calling `scheduler.step()` once per batch for a schedule defined in epochs (or the reverse) silently compresses or stretches it.

</div>

## 4.5 Batch size, clipping and the loss landscape {#dl-4-5}

- **Batch size:** gradient noise falls like $1/B$, so a larger batch allows a proportionally larger step (the **linear scaling** heuristic, with warm-up) up to a problem-dependent critical batch size. Small batches add noise that is widely reported to help generalisation; say "plausible but not settled". In practice memory and throughput decide $B$.
- **Gradient clipping by norm** rescales the whole gradient when its norm exceeds $c$: $(3, 4)$ with $c = 1$ becomes $(0.6, 0.8)$, same direction. Clipping **by value** clips each coordinate, giving $(1, 1)$, which changes the direction. Clip by norm; it is standard for RNNs and Transformers. It fixes **exploding** gradients, not vanishing ones.
- **Loss landscape:** in high dimension most critical points are **saddle points**, not bad local minima. Gradient descent slows near them, and noise and momentum push it off. Plateaus, ill-conditioning and bad initialisation are the usual culprits when training stalls.

<div class="nb nb-moral">

Start with AdamW (Transformers) or SGD with momentum 0.9 (CNNs), warm-up plus cosine decay, gradient clipping at norm 1; then tune the peak learning rate first, because it matters more than anything else on this page.

</div>
