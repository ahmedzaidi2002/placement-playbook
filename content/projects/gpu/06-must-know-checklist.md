---
title: "4 · Must-know before the interview"
weight: 6
---

The one-page preparation for the GPU projects. If you only have the evening before, read this page and nothing else, then do the self-test at the bottom. Evidence labels are explained on the [section landing page](../).

## 1. The 60-second pitch (memorise the shape, not the words)

> I built two CUDA programs from scratch to learn GPU programming properly. One is a **tiled 2D convolution** with shared memory and a halo. The other is a **parallel Borůvka MST**: every component picks its lightest edge with atomics, components hook together, pointer jumping flattens them, and a **Blelloch prefix sum** compacts the edge list each round. I tested both against CPU references, including seeded-bug checks, and ran them on a real GPU under compute-sanitizer. The MST was about **13× faster than sequential Kruskal** on a 200K-vertex, 1.2M-edge graph, in one run including copies. The convolution taught me something else: the tiled kernel was **no faster than the naive one at 3×3**, because the caches already serve small filters and the copy dominates, and I can explain how I would confirm that with a profiler.

Then stop and let them ask. The two limits you state first (one run; tiling did not help) make the rest more believable.

## 2. Numbers and facts to have ready

| Fact | Value | Label |
|---|---|---|
| MST benchmark | V = 200 000, E = 1.2 M: CPU Kruskal 258.7 ms, GPU Borůvka 19.6 ms, 7 rounds, about 13× | Measured, one run, copies included |
| Conv benchmark | 1024×1024×3, 8 filters 3×3: CPU 729 ms, GPU tiled 54.7 ms, naive 54.3 ms | Measured, one run, copies included |
| MST correctness checks | 577 to 581 at BLOCK 32/128/256/1024 | Measured (Colab run) |
| Conv correctness checks | 619 at three tile shapes | Measured (Colab run) |
| Sanitizers | memcheck, racecheck, synccheck: 0 errors | Measured |
| Default block (MST/scan) | 256 threads, `-DBLOCK` | Code |
| Default conv tile | 32×8 = 256 threads, `-DCONV_BX/BY` | Code |
| Conv shared memory, 3×3 | 1396 bytes | Reasoned |
| Largest odd square filter that tiles | 67×67 | Reasoned |
| Max Borůvka rounds | `⌈log₂ V⌉` | Reasoned |
| Warp / max block / banks | 32 / 1024 / 32 | Rule of thumb |
| Shared memory per block (default) | 48 KB | Rule of thumb |
| `gridDim.y`, `gridDim.z` limit | 65535 | Rule of thumb |

## 3. Things you must be able to explain without looking

### GPU model
- Thread / warp / block / grid / SM, and what each can synchronise with.
- Global vs shared vs register memory; coalescing; bank conflicts and the broadcast exception.
- Warp divergence. Occupancy and latency hiding. Memory-bound vs compute-bound.
- Why kernels are launched in sequence when phases depend on each other (no inter-block barrier).
- Launches and errors are asynchronous; `cudaGetLastError`, `cudaDeviceSynchronize`.

### Convolution
- Formula, layout, zero padding, cross-correlation vs convolution.
- Tile + halo; why 32 on x (a warp, coalescing); why two barriers; why out-of-range threads still reach them.
- Shared-memory formula and the 48 KB fallback.
- Why tiled ≈ naive at 3×3 and what to try next (bigger filters, profiling).

### Borůvka MST
- The six steps of a round; draw them.
- Why ties break it and why `(weight, index)` fixes it (non-increasing keys, a cycle means the same edge, so only 2-cycles).
- Two atomic passes and why not a packed key.
- Pointer jumping with double buffering; `O(log n)` steps.
- Compaction = flag, exclusive scan, scatter.
- Blelloch scan: up-sweep, set root to 0, down-sweep; `O(n)` work; recursion over block sums.
- Limits: atomic contention, `O(V)` arrays per round, host syncs, edge list not CSR.

### Evidence and honesty
- Oracles, mutation checks, emulation (what it can and cannot show), sanitizers.
- What the benchmark proves and what it does not.

## 4. Claims to avoid

{{< callout type="warning" >}}
Saying any of these will lose credibility under a single follow-up question.
{{< /callout >}}

| Do **not** say | Say instead |
|---|---|
| "Shared-memory tiling made the convolution faster." | "At 3×3 the tiled kernel matched the naive one; caches and the output copy dominate. Larger filters are where I expect it to help, but I have not measured that." |
| "13× faster than the CPU." | "About 13× over sequential Kruskal in one run on a 200K-vertex, 1.2M-edge random graph, copies included." |
| "It is optimal / state of the art." | "It is a clear, correct reference implementation; I know where it is not optimal." |
| "I invented / researched Borůvka on GPU." | "I implemented the standard algorithm with standard parallel primitives." |
| "It was tested on a real road network." | "Tested on synthetic random and structured graphs against Kruskal." |
| "No races, proven." | "Clean under compute-sanitizer memcheck/racecheck/synccheck on the tests; racecheck covers shared memory only." |
| "My scan is as fast as CUB." | "I wrote my own to learn it; in production I would use CUB or Thrust." |
| "The GPU was a T4 / A100." | "A Colab GPU. The exact model was not recorded in my notes." |
| "It was an assignment." | "Self-study reference implementations. My course (CS6023) assignments are separate." |

## 5. What an interviewer is really testing

| They ask | They want to see |
|---|---|
| "Walk me through it" | You can organise a parallel algorithm into dependent phases |
| "Why shared memory?" | You understand reuse and the memory hierarchy |
| "Why did tiling not help?" | You report results honestly and reason about caches and transfers |
| "What about ties?" | You can find and prove a correctness condition for a parallel algorithm |
| "How do you test GPU code?" | Oracles, edge cases, sanitizers, and awareness of what each tool misses |
| "What would you do next?" | You can profile, prioritise and name concrete optimisations |

## 6. If the role is not CUDA-heavy

Two sentences are usually enough: *I learned GPU architecture by building two kernels and measuring them. The transferable skills are decomposing a problem into data-parallel phases, reasoning about memory and synchronisation, and verifying with independent oracles.* Offer to go deeper on whichever the interviewer finds interesting. Connect it to their domain: for ML roles, convolution is the core layer of CNNs and libraries lower it to matrix multiplication; for systems roles, the MST shows lock-free coordination with atomics and prefix sums.

## 7. Five-minute whiteboard prompts to rehearse

1. Draw the thread/block/grid hierarchy and map the 32×8 convolution tile onto it.
2. Draw the convolution tile with the halo and mark which cells each thread loads.
3. Run Borůvka by hand on a 5-vertex graph; show the hook graph and the 2-cycle.
4. Run a Blelloch scan on `[3, 1, 7, 0, 4, 1, 6, 3]`.
5. Show a triangle with equal weights that creates a 3-cycle without a tie-break.
6. List three ways to make the MST faster, in order of expected gain, and how you would measure each.

## 8. Final self-test

{{< details title="Questions" >}}

1. State the exact claim you make about the MST speedup, with its three caveats.
2. Why does the tiled convolution kernel not return early for threads outside the image?
3. What is the shared-memory size for a 3×3 filter with the default tile?
4. What guarantees that Borůvka's hook graph has only 2-cycles?
5. Give the exclusive scan of `[1, 2, 3, 4]`.
6. Where does the MST host code stall the GPU?
7. Name two limits of the CPU emulation.
8. Which sanitizer finds shared-memory races? Which finds out-of-bounds accesses?
9. Why is Borůvka a better fit than Kruskal for a GPU?
10. What is the single most important profiling step you have not done yet, and why?

{{< /details >}}

{{< details title="Answers" >}}

1. About 13× faster than sequential Kruskal on a 200K-vertex, 1.2M-edge random graph; one run on one Colab GPU; GPU time includes allocation and copies; the CPU baseline is a plain single-threaded Kruskal.
2. They must take part in loading and in every `__syncthreads()`; barrier divergence is undefined. Only the compute and store are guarded.
3. `(8+2)·(32+2) + 9 = 349` ints = 1396 bytes.
4. The strict total order `(weight, index)`: chosen keys are non-increasing along hooks, so a cycle forces the same edge, which joins only two components.
5. `[0, 1, 3, 6]`.
6. The survivor count after the scan (two `cudaMemcpy`) and the changed-flag after each pointer-jump iteration.
7. It does not model warps/divergence, and it does not model real inter-block races or memory ordering (also: it cannot reveal `nvcc` errors or performance).
8. `racecheck`; `memcheck`.
9. Kruskal is sequential (sorted order plus union-find); Borůvka processes all components and edges in parallel in at most `⌈log₂ V⌉` rounds.
10. A profile (Nsight Systems / Compute) to see where the time goes: kernels vs copies vs host stalls. Everything else is guessing until then.

{{< /details >}}

## One-page cheat sheet

```text
GPU     thread < warp(32) < block(<=1024, shared mem, __syncthreads) < grid (blocks independent)
MEMORY  register > shared (48KB) > L1/L2 > global; coalesce x; avoid bank conflicts; reuse in shared
BARRIER inside a block: __syncthreads (all threads must reach it).  Across blocks: new kernel launch.
ATOMIC  safe RMW; same address serialises. atomicMin x2 = lexicographic min (weight, index).

CONV    out[k][y][x] = sum_{c,r,s} img[c][y+r-R/2][x+s-S/2] * flt[k][c][r][s]   (zeros outside, no flip)
        block 32x8 per tile per filter; load tile+halo+filter -> sync -> accumulate -> sync -> next channel
        smem = ((BY+R-1)(BX+S-1) + R*S)*4 bytes; > 48KB -> naive fallback; 3x3 tiled == naive (measured)

MST     round: compact -> min edge per comp (2x atomicMin) -> hook -> break 2-cycles (smaller id = root)
              -> pointer-jump (double buffer) -> relabel;   <= ceil(log2 V) rounds
        total order (weight,index) => only 2-cycles.   Edge sums in 64-bit, mod once at the end.
SCAN    Blelloch: up-sweep, root=0, down-sweep; O(n) work; recursive over block sums.
        compaction = flag -> exclusive scan -> scatter.

TEST    CPU oracle (naive / Kruskal) + spec samples + random + ties + several BLOCK/tile
        + mutation checks + CPU emulation + Colab GPU + compute-sanitizer (0 errors)
RESULT  MST 258.7 ms -> 19.6 ms (~13x, 1 run, copies in).  Conv 729 -> 54.7 ms; tiled 54.7 ~ naive 54.3.
LIMITS  contention, O(V) per round, host syncs, edge list, single run, plain CPU baseline.
```
