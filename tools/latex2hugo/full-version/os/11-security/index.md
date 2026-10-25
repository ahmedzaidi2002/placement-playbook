---
title: "11 · Protection and security basics"
linkTitle: "11 Protection and security basics"
weight: 11
math: true
---
## 11.1 Protection: who may do what {#sec-os-security}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `passwd` must write `/etc/shadow`, which ordinary users cannot even read.</em>

</div>

<div class="nb nb-definition" id="definition-11-1-1">

<strong>Definition 11.1.1</strong>. <strong>Protection</strong> is the mechanism that controls access of processes to resources; <strong>security</strong> is the policy and defence against attackers who try to defeat it. The model is an <strong>access matrix</strong>: rows are <strong>domains</strong> (users, processes), columns are objects (files, devices, memory segments), entries are rights (read, write, execute, own). Storing it by column gives <strong>access control lists</strong> (each object lists who may do what: UNIX permission bits, NTFS and POSIX ACLs); storing it by row gives <strong>capability lists</strong> (each domain holds unforgeable tokens naming objects and rights: file descriptors are capabilities, as are seL4’s and Capsicum’s).

</div>

|  | ACL (per object) | Capability (per subject) |
|:--|:--|:--|
| “Who can access file F?” | easy: read F’s list | hard: search every domain |
| “What can process P access?” | hard: search every object | easy: P’s list |
| Revocation | easy: edit the list | hard: capabilities may have been copied |
| Checked | on every `open` by name | possession is the right |

### 11.1.i The UNIX model {#s11-1-i}

Each file has an owner, a group and three `rwx` triples (owner, group, others); for a directory, `r` lists it, `w` creates and deletes entries, `x` lets you pass through it. The `umask` removes bits from newly created files. The <strong>sticky bit</strong> on a directory (`/tmp`, mode `1777`) lets only a file’s owner delete it. Root (uid 0) bypasses the checks; modern Linux splits root’s powers into <strong>capabilities</strong> (`CAP_NET_BIND_SERVICE` to bind ports below 1024, `CAP_SYS_ADMIN`, …) so a program can get one power without all of them.

<div class="nb nb-definition" id="definition-11-1-2">

<strong>Definition 11.1.2</strong>. A process has a <strong>real</strong> user ID (who started it) and an <strong>effective</strong> user ID (whose rights it uses). Executing a file with the <strong>setuid</strong> bit sets the effective uid to the file’s owner, so `/usr/bin/passwd` (owned by root, mode `rwsr-xr-x`) can update `/etc/shadow` on behalf of any user, but only in the way the program allows. <strong>setgid</strong> does the same for the group.

</div>

The transcript below also uses two small programs: `ids` prints the real and effective uid, and `canary` has a stack buffer overflow ([Section 11.2](#sec-os-mitigations)):

```c {filename="canary.c"}
// flags: -fstack-protector-all -D_FORTIFY_SOURCE=0 -Wno-stringop-overflow
// norun (driven by security.sh)
// A classic stack buffer overflow. The canary placed between the buffer and
// the saved return address is checked before the function returns.
#include <stdio.h>
#include <string.h>

static void greet(const char *name) {
    char buf[16];
    strcpy(buf, name);                 // no bounds check: the bug
    printf("hello, %s\n", buf);
}

int main(int argc, char **argv) {
    greet(argc > 1 ? argv[1] : "world");
    return 0;
}
```

```text {filename="Terminal session (bash, Linux 6.18)"}
## setuid: the effective uid becomes the file owner's
$ setpriv --reuid=65534 --regid=65534 --clear-groups /tmp/os-book/ids
real uid 65534, effective uid 65534
$ stat -c '%A %U %n' /tmp/os-book/ids
-rwsr-xr-x root /tmp/os-book/ids
$ setpriv --reuid=65534 --regid=65534 --clear-groups /tmp/os-book/ids
real uid 65534, effective uid 0
## a stack canary catches the overflow before the function returns
$ ./canary Ada
hello, Ada
$ ./canary AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA; echo exit status $?
*** stack smashing detected ***: terminated
(bash: Aborted)
exit status 134
## ASLR: the stack moves on every run, unless disabled for one command
$ cat /proc/sys/kernel/randomize_va_space
2
$ grep '\[stack\]' /proc/self/maps | cut -d' ' -f1,2
7ffc25456000-7ffc25479000 rw-p
$ grep '\[stack\]' /proc/self/maps | cut -d' ' -f1,2
7ffd0a1d7000-7ffd0a1fa000 rw-p
$ setarch -R grep '\[stack\]' /proc/self/maps | cut -d' ' -f1,2
7ffffffdc000-7ffffffff000 rw-p
$ setarch -R grep '\[stack\]' /proc/self/maps | cut -d' ' -f1,2
7ffffffdc000-7ffffffff000 rw-p
```

Running as `nobody` (uid 65534), the program’s effective uid became 0 once the setuid bit was set on a root-owned copy. That is why setuid-root programs are the prime target of privilege-escalation attacks: any bug in them runs as root. Principle of <strong>least privilege</strong>: give each program only the rights it needs, and drop them as soon as possible.

### 11.1.ii Hardware protection rings {#s11-1-ii}

x86 has four rings; Linux and Windows use ring 0 (kernel) and ring 3 (user). Virtualisation adds a more privileged mode below ring 0 for the hypervisor (VMX root mode, sometimes called “ring $-1$”), and SMM firmware sits below that. ARM uses exception levels EL0 (user), EL1 (kernel), EL2 (hypervisor), EL3 (secure monitor). The MMU’s user/supervisor bit on each page keeps ring 3 out of kernel memory.

## 11.2 Memory-safety attacks and mitigations {#sec-os-mitigations}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `strcpy` of a long name into a 16-byte stack buffer overwrites the saved return address.</em>

</div>

A <strong>stack buffer overflow</strong> writes past a local array into the saved frame pointer and return address; when the function returns it jumps where the attacker wrote. Classic attacks put machine code in the buffer and return into it; modern ones chain existing code fragments (<strong>return-oriented programming</strong>, ROP). Defences, each defeating one step:

- <strong>Stack canaries</strong>: the compiler (`-fstack-protector`) puts a random value between the locals and the return address and checks it before returning; an overflow that reaches the return address must have overwritten it, so the program aborts (`canary` above: `SIGABRT`, exit status $128+6=134$).
- <strong>NX / W$\oplus$X / DEP</strong>: pages are writable or executable, never both; the stack and heap are non-executable (`rw-p` in `/proc/self/maps` above), so injected code cannot run. Attackers answer with ROP.
- <strong>ASLR</strong>: randomise the base of the stack, heap, libraries and (for PIE executables) the program, so the attacker does not know where to jump. Above, the stack moved on each run and stopped moving under `setarch -R`. Information leaks defeat it.
- Others: <strong>RELRO</strong> (make the GOT read-only after linking), <strong>fortify</strong> (the macro `_FORTIFY_SOURCE` makes `strcpy` and friends check bounds when the buffer size is known), control-flow integrity, shadow stacks (Intel CET), and above all memory-safe languages.

<div class="nb nb-remark" id="remark-11-2-1">

<strong>Remark 11.2.1</strong> (Other classic OS-level attacks) — These come up in interviews:

- <strong>TOCTOU</strong> (time of check to time of use): `access(path)` then `open(path)`; in between an attacker swaps `path` for a symlink to `/etc/shadow`. Fix: open first, then check the open descriptor (`fstat`), or use `O_NOFOLLOW`/`openat`.
- <strong>Privilege escalation</strong> through a bug in a setuid program or the kernel.
- <strong>Malware</strong>: viruses (attach to programs), worms (spread by themselves over the network), trojans (pretend to be useful), rootkits (hide inside the kernel), ransomware.
- <strong>Side channels</strong>: Meltdown and Spectre leak kernel or other-process memory through speculative execution and cache timing; kernel page-table isolation (KPTI) and related mitigations are part of why system calls got slower.

</div>

<div class="nb nb-remark" id="remark-11-2-2">

<strong>Remark 11.2.2</strong> (Passwords) — Systems store a slow, salted hash of each password (`/etc/shadow`: yescrypt or SHA-512-crypt on current Linux), never the password. The salt makes identical passwords hash differently and defeats precomputed tables; the slowness makes brute force expensive.

</div>

<div class="nb nb-moral">

ACLs answer “who can touch this object”, capabilities “what can this process touch”; setuid grants an owner’s rights through a program; canaries, NX and ASLR each break one step of a memory-corruption exploit, none of them all.

</div>
