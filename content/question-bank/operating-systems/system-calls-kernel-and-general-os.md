---
title: "System calls, kernel and general OS"
weight: 6
---

3 questions asked by MathWorks, Oracle, Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q14, character devices

*Asked by: MathWorks (IISc 2024)*

Which of the following is a character device?

- **(a)** Hard disk
- **(b)** USB camera
- **(c)** Disk-on-key
- **(d)** Terminals

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) terminals**

**Why.** A terminal transfers a stream of characters with no seeking. Hard disks and USB flash drives are block devices (fixed-size blocks, random access). (A webcam is also exposed as a character device on Linux, but the textbook answer is the terminal.)

**Concept: character vs block devices.** Character devices: byte streams, no buffering cache (keyboards, serial ports, terminals). Block devices: addressable blocks, cached, hold file systems (disks, SSDs).

{{< /details >}}

### 2 · /etc/hosts

*Asked by: Oracle (HackerRank MCQ test)*

What is the use of the `/etc/hosts` file in Linux?

- **(a)** It contains the list of all users.
- **(b)** It contains a list of all files in the system
- **(c)** It contains the time and date information.
- **(d)** It contains the FQDN to IP address mappings.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) it holds hostname (FQDN) to IP address mappings**

**Why.** `/etc/hosts` gives static name-to-address mappings, checked before (or instead of) DNS. Users are in `/etc/passwd`.

**Concept: name resolution order.** Linux consults `/etc/nsswitch.conf`, usually "files dns": first `/etc/hosts`, then DNS servers from `/etc/resolv.conf`.

{{< /details >}}

### 3 · Operating-system basics

*Asked by: Qualcomm (IISc 2024, Q26)*

Which of the statement(s) given below is/are true about a Linux (kernel) distribution?

I. It is mostly abbreviated as distro.  
II. It consists of a software collection.  
III. It consists of a package management system.

- **(a)** Only (III)
- **(b)** Only (I)
- **(c)** Only (II)
- **(d)** (I), (II) and (III)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) all of (I), (II) and (III)**

**Why.** A distribution ("distro") bundles the Linux kernel with a collection of software (GNU tools, libraries, desktop) and a package manager such as apt, dnf or pacman.

**Concept: kernel vs distribution.** Linux strictly is the kernel. Ubuntu, Fedora, Arch are distributions: the kernel plus everything needed to make a usable system.

{{< /details >}}
