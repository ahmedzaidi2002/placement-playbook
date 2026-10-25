---
title: "Operating Systems"
weight: 3
math: true
sidebar:
  open: false
---

The operating-system topics that placement OAs and interviews actually ask, cut down to what matters: a definition, the one idea behind it, and a worked example wherever there is a numerical to practise (one per scheduling algorithm, one per page-replacement policy, one per disk-scheduling algorithm). No long programs.

## Contents

**Part: Processes and the CPU**

- [1 · OS basics: kernel, modes, system calls](01-basics/)
- [2 · Processes](02-processes/)
- [3 · Threads](03-threads/)
- [4 · CPU scheduling](04-scheduling/)
- [5 · Synchronization](05-sync/)
- [6 · Deadlocks](06-deadlock/)

**Part: Memory and storage**

- [7 · Memory management and paging](07-memory/)
- [8 · Virtual memory and page replacement](08-vm/)
- [9 · File systems](09-fs/)
- [10 · I/O, disk scheduling and RAID](10-io/)
- [11 · Security, virtualization and Linux](11-security-virt-linux/)

**Part: Revision**

- [12 · Interview rapid-fire](12-rapidfire/)
- [13 · Practice problems](13-problems/)

<div class="nb nb-moral">

Highest-yield for OAs: scheduling (chapter 4), paging and page-replacement numericals (chapters 7–8), deadlock and Banker's algorithm (chapter 6), semaphores (chapter 5), disk scheduling (chapter 10), and `fork` counting (chapter 2).

</div>

The full-length version of this book, with every program and simulator, is kept in `tools/latex2hugo/full-version/os/` and in the PDF.
