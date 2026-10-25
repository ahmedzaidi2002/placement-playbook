---
title: "GPU Projects (CUDA)"
weight: 3
sidebar:
  open: false
---

Two CUDA programs written from scratch to learn GPU programming properly and to have something concrete to discuss in a systems or GPU interview: a **tiled multi-channel 2D convolution** and a **parallel Borůvka minimum spanning tree** (with a Blelloch prefix scan inside it). Both are checked against CPU reference implementations and were run on a real GPU.

This section is the study guide for them. It answers four questions, one page each.

{{< cards >}}
  {{< card link="01-gpu-concepts" title="1 · GPU concepts you need" subtitle="Threads, warps, blocks, the memory hierarchy, coalescing, bank conflicts, atomics, scan, occupancy. Only what these two projects touch." icon="chip" >}}
  {{< card link="02-2d-convolution" title="2a · 2D convolution" subtitle="What it computes, the data layout, the tiled kernel step by step, a worked example, limits." icon="view-grid" >}}
  {{< card link="03-boruvka-mst" title="2b · Parallel Borůvka MST" subtitle="The six steps of a round, a hand-traced example, the Blelloch scan, tie-breaking proof, limits." icon="share" >}}
  {{< card link="04-testing-and-results" title="2c · Testing and results" subtitle="Oracles, emulation, mutation checks, sanitizers, and exactly what the benchmark does and does not show." icon="beaker" >}}
  {{< card link="05-interview-questions" title="3 · Interview questions" subtitle="About 45 questions with model answers, grouped by topic, plus follow-up traps." icon="chat" >}}
  {{< card link="06-must-know-checklist" title="4 · Must-know before the interview" subtitle="The 60-second pitch, numbers to have ready, claims to avoid, a one-page cheat sheet and a self-test." icon="clipboard-check" >}}
{{< /cards >}}

## At a glance

| | 2D convolution | Borůvka MST |
|---|---|---|
| Problem | Slide `K` filters of size `C×R×S` over an `H×W×C` image (zero padding, stride 1) | Minimum spanning tree/forest of a road graph with terrain-adjusted edge costs |
| GPU pattern | **Stencil** with shared-memory tiling and a halo | **Graph algorithm** built from atomics, pointer jumping and scan-based compaction |
| Files | `conv2d.cuh`, `main.cu`, `test.cu` | `boruvka.cuh`, `scan.cuh`, `main.cu`, `test.cu` |
| Parallelism | One thread per output pixel, one block per tile per filter | One thread per edge or per component, depending on the kernel |
| CPU oracle | Naive nested loops | Kruskal with union-find (same tie-break) |
| Measured (one Colab run) | CPU 729 ms vs GPU 54.7 ms **but tiled ≈ naive** (54.3 ms) | CPU Kruskal 258.7 ms vs GPU 19.6 ms, **about 13×**, 7 rounds |

Both measurements include allocation and host-to-device and device-to-host copies, and each is a **single run**. [Section 2c](04-testing-and-results/) says what that means.

## Evidence labels used in these pages

Every non-obvious statement carries one of these, so you always know how hard to lean on it in an interview.

- <span style="color:#0071bc"><strong>[Measured]</strong></span> A number that came out of the Colab run on 2026-10-22 and is recorded in the repository README.
- <span style="color:#009b55"><strong>[Code]</strong></span> Read directly from the source files. You can point at the function.
- <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> Derived by arithmetic or argument from the code or from standard GPU facts. **Not** measured on this program. Say "I'd expect" when you use it.
- <span style="color:#f7921d"><strong>[Rule of thumb]</strong></span> A typical hardware figure (warp size, shared-memory size, latency order of magnitude). True for mainstream NVIDIA GPUs, but check the exact device before quoting it as a spec.

{{< callout type="warning" >}}
**Honest framing.** These are reference implementations of standard algorithms (tiled stencil, Borůvka, Blelloch scan), written to learn and to extend. They are not coursework submissions and not research. The resume quotes only the MST speedup (~13×). The convolution result is a *negative* finding (tiling did not help at 3×3) and the right way to use it is as a talking point about *why*, not as a claimed win.
{{< /callout >}}

## Where the code lives

`C:\ahmed\IIT M\placement prep\gpu-cuda-reference` (own git repo).

```text
2d-convolution/   conv2d.cuh, main.cu, test.cu, cuda_check.h, samples/, README.md
boruvka-mst/      scan.cuh, boruvka.cuh, main.cu, test.cu, cuda_check.h, samples/, README.md
shim/             cuda_runtime.h  - CPU emulation of the CUDA subset used (Linux/WSL)
scripts/          emu_test.sh, colab_verify.sh, check_samples.sh, cuda_to_cpp.py, Verify_on_Colab.ipynb
```

Build and run:

```bash
nvcc -O2 2d-convolution/main.cu -o conv_main && ./conv_main < 2d-convolution/samples/conv2d_ex2.in
nvcc -O2 boruvka-mst/main.cu    -o mst_main  && ./mst_main  < boruvka-mst/samples/mst_sample.in   # prints 14
bash scripts/colab_verify.sh        # full GPU verification (build, tests, sanitizers, benchmark)
bash scripts/emu_test.sh            # no GPU: logic check through the CPU emulation shim (Linux/WSL)
```

Compile-time knobs: `-DBLOCK=256` (MST and scan threads per block, a power of two up to 1024) and `-DCONV_BX=32 -DCONV_BY=8` (convolution output tile).

## How to use these pages

1. Read [section 1](01-gpu-concepts/) once, slowly. Everything else assumes it.
2. Read the two project pages with the source open next to you. Be able to explain every kernel without looking.
3. Skim [section 2c](04-testing-and-results/) so you can answer "how do you know it works?" without hesitation.
4. Cover the answers in [section 3](05-interview-questions/) and say them out loud.
5. The day before, use only [section 4](06-must-know-checklist/).
