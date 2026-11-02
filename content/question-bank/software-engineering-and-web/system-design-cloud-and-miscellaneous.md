---
title: "System design, cloud and miscellaneous"
weight: 4
---

2 questions asked by EXL, Oracle. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Dynamics ERP sandbox and the pop-up blocker

*Asked by: EXL (HackerEarth test, 2025)*

John has a Microsoft Dynamics ERP subscription and wants to create a sandbox environment to
test feature extensions before deployment. After creating the sandbox he faces issues caused
by the pop-up blocker integrated with his browser. Which option resolves them?

- **(a)** Allow URLs from the *.businesscentral.dynamics.com address
- **(b)** Allow a exception rule for your WiFi endpoint for the Microsoft domain websites
- **(c)** Add the Dynamics ERP to the whitelist in your home group
- **(d)** Add a trust certificate to the Dynamics ERP

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) allow pop-ups from `*.businesscentral.dynamics.com`**

**Why.** A pop-up blocker is fixed by allowing pop-ups from the application's own domain; Business Central sandboxes are served from that domain. Network exceptions and certificates have nothing to do with pop-up blocking.

**Concept: match the fix to the layer.** Pop-ups are a browser setting (per site); certificates are about trust/encryption; firewall rules are about network access.

{{< /details >}}

### 2 · CAP theorem

*Asked by: Oracle (HackerRank MCQ test)*

What does the CAP theorem describe with respect to system design?

- **(a)** The relationship between CPU and memory usage
- **(b)** The trade-offs between consistency, availability, and partition tolerance
- **(c)** The process of data encryption
- **(d)** The principles of object-oriented programming

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) the trade-offs between consistency, availability and partition tolerance**

**Why.** In a distributed store, network partitions will happen. During one, the system must choose: refuse some requests to stay consistent (CP), or answer everything but possibly with stale data (AP).

**Concept: CAP theorem.** Consistency: every read sees the latest write. Availability: every request gets a response. Partition tolerance: the system keeps working despite lost messages between nodes. Since P is unavoidable, the real choice is C vs A during partitions.

{{< /details >}}
