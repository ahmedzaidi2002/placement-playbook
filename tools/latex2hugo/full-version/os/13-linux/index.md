---
title: "13 · Linux in practice"
linkTitle: "13 Linux in practice"
weight: 13
math: true
---
## 13.1 What happens when you run `./a.out` {#sec-os-aout}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> typing `./hello` at a bash prompt and getting `hello` back.</em>

</div>

<div class="nb nb-remark" id="algorithm-13-1-1">

<strong>Algorithm 13.1.1</strong> (From the prompt to `main` and back) —

1. The shell reads the line, expands it, sees a path (no `PATH` search) and calls `fork` (bash uses `clone`); the child sets up redirections and calls `execve("./hello", argv, envp)`; the parent waits (`wait4`) unless the command ended with `&`.
2. The kernel checks execute permission, reads the ELF header, discards the child’s old address space, maps the program’s segments (text read+execute, data read+write, bss zero), builds the new stack (`argc`, `argv`, `envp`, the auxiliary vector) and, because the ELF names an interpreter, maps the dynamic loader `/lib64/ld-linux-x86-64.so.2` and starts <em>it</em>.
3. The loader opens `libc.so.6` (found through `/etc/ld.so.cache`), maps it, performs relocations, makes the relocated pages read-only (`mprotect`: RELRO) and jumps to the program’s entry point `_start`.
4. `_start` calls `__libc_start_main`, which runs initialisers and calls `main(argc, argv, envp)`. Pages of code and data are faulted in on demand as they are touched.
5. `printf` fills the stdio buffer; `return` from `main` calls `exit`, which runs `atexit` handlers, flushes stdio (the `write`) and calls `exit_group`. The kernel frees everything, the process becomes a zombie, the parent gets `SIGCHLD`, its `wait4` returns the status, and the shell prints the next prompt.

</div>

```c {filename="hello.c"}
// flags:
// norun (driven by strace-hello.sh)
#include <stdio.h>

int main(void) {
    printf("hello\n");
    return 0;
}
```

```text {filename="Terminal session (bash, Linux 6.18)"}
$ ldd ./hello
    linux-vdso.so.1
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
    /lib64/ld-linux-x86-64.so.2
$ strace -e trace=execve,openat,mmap,mprotect,brk,write,exit_group ./hello
execve("./hello", ["./hello"], envp) = 0
brk(NULL) = 0x...
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x...
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
mmap(NULL, 45047, PROT_READ, MAP_PRIVATE, 3, 0) = 0x...
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
mmap(NULL, 2170256, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x...
mmap(0x..., 1605632, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x...) = 0x...
mmap(0x..., 323584, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x...) = 0x...
mmap(0x..., 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x...) = 0x...
mmap(0x..., 52624, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x...
mmap(NULL, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x...
mprotect(0x..., 16384, PROT_READ) = 0
mprotect(0x..., 4096, PROT_READ) = 0
mprotect(0x..., 8192, PROT_READ) = 0
brk(NULL) = 0x...
brk(0x...) = 0x...
write(1, "hello\n", 6) = 6
exit_group(0) = ?
```

Everything before `write` is the loader: the `ld.so.cache` lookup, the `mmap`s of libc’s segments, the `mprotect`s of RELRO. `linux-vdso.so.1` has no path: the kernel maps it into every process ([Section 1.3](../01-kernel/#sec-os-syscalls)).

## 13.2 Pipes and redirection, the way the shell does them {#sec-os-shellpipe}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `ls | grep x`: two processes, one pipe, each with its stdin or stdout moved.</em>

</div>

<div class="nb nb-definition" id="definition-13-2-1">

<strong>Definition 13.2.1</strong>. `dup2(old, new)` makes descriptor `new` refer to the same open file description as `old` (closing `new` first). Redirections and pipes are nothing but `dup2` onto descriptors 0, 1 and 2 between `fork` and `exec`; the executed program just reads stdin and writes stdout and never knows.

</div>

```c {filename="minishell.c"}
// flags: -D_GNU_SOURCE
// What a shell does for   printf 'b\na\nc\n' | sort > out.txt ; cat out.txt
// pipe + fork + dup2 + exec for each side, open + dup2 for the redirection.
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    char *left[]  = {"printf", "b\\na\\nc\\n", NULL};
    char *right[] = {"sort", NULL};
    int p[2];
    pipe(p);
    pid_t a = fork();
    if (a == 0) {                        // left side: stdout -> pipe
        dup2(p[1], STDOUT_FILENO);
        close(p[0]); close(p[1]);
        execvp(left[0], left);
        _exit(127);
    }
    pid_t b = fork();
    if (b == 0) {                        // right side: stdin <- pipe,
        dup2(p[0], STDIN_FILENO);        //   stdout -> out.txt
        int fd = open("/tmp/os-book-out.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
        dup2(fd, STDOUT_FILENO);
        close(fd); close(p[0]); close(p[1]);
        execvp(right[0], right);
        _exit(127);
    }
    close(p[0]); close(p[1]);            // or sort never sees EOF
    int st;
    waitpid(a, &st, 0); waitpid(b, &st, 0);
    printf("pipeline exit status %d; out.txt holds:\n", WEXITSTATUS(st));
    fflush(stdout);
    execlp("cat", "cat", "/tmp/os-book-out.txt", (char *)NULL);
    return 1;
}
```

```text {filename="Output (gcc 13.3, glibc 2.39, Linux 6.18 x86-64)"}
pipeline exit status 0; out.txt holds:
a
b
c
```

<div class="nb nb-remark" id="remark-13-2-2">

<strong>Remark 13.2.2</strong> (The steps for `ls | grep x`) — The shell calls `pipe`, then forks twice. In the first child: `dup2(p[1], 1)`, close both pipe ends, exec `ls`. In the second: `dup2(p[0], 0)`, close both, exec `grep`. The parent closes both ends and waits for both children. The two run concurrently; `ls` blocks when the 64 KiB pipe is full and `grep` when it is empty. The pipeline’s exit status is the last command’s. Forgetting to close the parent’s write end is the classic bug: `grep` never gets EOF and the pipeline hangs. `cmd > f 2>&1` is `open(f)`, `dup2(fd,1)`, `dup2(1,2)`, in that order; `2>&1 > f` sends stderr to the old stdout.

</div>

## 13.3 Processes from the command line {#sec-os-tools}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a hung server: find it, see what it is doing, stop it politely, then not politely.</em>

</div>

```text {filename="Terminal session (bash, Linux 6.18)"}
## a stopped background process, seen by ps and /proc
$ ps -o pid,ppid,stat,ni,comm -p 18216
  PID  PPID STAT  NI COMMAND
18216 18215 T      0 sleep
$ grep -E '^(State|PPid|Threads|VmRSS)' /proc/18216/status
State:  T (stopped)
PPid:   18215
VmRSS:      1748 kB
Threads:    1
$ ls -l /proc/18216/fd | awk 'NR>1 {print $9, $10, $11}'
0 -> /dev/null
1 -> /tmp/os-book-log
2 -> /tmp/os-book-log
$ kill -CONT 18216; kill 18216; sleep 0.1; ps -p 18216 >/dev/null || echo gone
gone
## the per-user process limit (RLIMIT_NPROC) stops a fork bomb
$ setpriv --reuid=65534 --regid=65534 --clear-groups bash -c 'ulimit -u 20; ./forker 50'
fork() succeeded 19 times, failed 31 times: Resource temporarily unavailable
## name resolution order and /etc/hosts
$ grep '^hosts' /etc/nsswitch.conf
hosts:          files dns
$ getent hosts localhost
127.0.0.1       localhost
$ unshare -m sh -c 'cp /etc/hosts /tmp/h; echo 10.1.2.3 intranet.example >> /tmp/h;
     mount --bind /tmp/h /etc/hosts; getent hosts intranet.example'
10.1.2.3        intranet.example
```

<div class="nb nb-definition" id="definition-13-3-1">

<strong>Definition 13.3.1</strong>. The everyday tools:

- `/proc` is a pseudo file system generated from kernel data: `/proc/PID/status` (state, parent, memory, threads), `/proc/PID/fd/` (open descriptors as symlinks), `/proc/PID/maps` (memory regions), `/proc/PID/cmdline`, `/proc/meminfo`, `/proc/loadavg`, `/proc/sys/` (tunable parameters). `ps`, `top` and `free` only format these files.
- `ps` state letters: `R` running or runnable, `S` interruptible sleep, `D` uninterruptible sleep (usually disk I/O; even `SIGKILL` waits), `T` stopped, `Z` zombie; `ps -ef`/`ps aux` list everything, `pstree` shows the hierarchy. `top`/`htop` add live CPU and memory use and the <strong>load average</strong>: the average number of runnable (and, on Linux, uninterruptibly sleeping) tasks over 1, 5 and 15 minutes.
- `strace` shows a process’s system calls (`-f` follows children, `-p PID` attaches, `-c` counts); `ltrace` shows library calls; `lsof` lists open files; `gdb -p PID` attaches a debugger.
- `kill PID` sends `SIGTERM`; `kill -9` sends `SIGKILL`; `kill -STOP`/`-CONT` pause and resume; `pkill`/`killall` select by name; Ctrl-C, Ctrl-&#92; and Ctrl-Z send `SIGINT`, `SIGQUIT` and `SIGTSTP` to the terminal’s foreground process group. `jobs`, `fg`, `bg` manage the shell’s jobs.
- `nice`/`renice` change the nice value ([Section 4.5](../04-scheduling/#sec-os-cfs)); `taskset` sets CPU affinity; `ulimit` shows and sets resource limits (`-u` processes, `-n` open files, `-s` stack, `-c` core size).

</div>

### 13.3.i Fork bombs and limits {#s13-3-i}

`:(){ :|:& };:` defines a function `:` that pipes itself into itself in the background and calls it: the number of processes doubles until the process table or memory is exhausted and nothing new can start (not even the `kill` to stop it, which is why one uses `kill -9 -1` from an existing shell, or the limits). Defences: `ulimit -u` (the per-user `RLIMIT_NPROC`; the run above capped user `nobody` at 20 processes, so of 50 forks 19 succeeded, the shell being the 20th) and the `pids` cgroup controller ([Section 12.2](../12-virt/#sec-os-containers)). Root is exempt from `RLIMIT_NPROC`, which is why the demo switches to `nobody`.

### 13.3.ii Daemons, `nohup` and sessions {#s13-3-ii}

<div class="nb nb-definition" id="definition-13-3-2">

<strong>Definition 13.3.2</strong>. A <strong>daemon</strong> is a background service with no controlling terminal. The traditional recipe: `fork` and let the parent exit (the child is an orphan, adopted by `init`, and is not a process-group leader); `setsid` (new session, no controlling terminal); `fork` again so it can never reacquire a terminal; `chdir("/")`; `umask(0)`; close or redirect descriptors 0, 1, 2 to `/dev/null`; write a PID file. Under systemd a service just runs in the foreground and systemd does the rest.

</div>

<div class="nb nb-definition" id="definition-13-3-3">

<strong>Definition 13.3.3</strong>. When a terminal closes, the kernel sends `SIGHUP` to its session’s processes, which by default terminates them. `nohup cmd &` starts `cmd` with `SIGHUP` ignored and output redirected to `nohup.out`, so it survives logout; `setsid`, `disown`, `tmux` and `screen` are the other ways.

</div>

## 13.4 `/etc/hosts` and name resolution {#sec-os-hosts}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> pointing `intranet.example` at a test server on one machine without touching DNS.</em>

</div>

<div class="nb nb-definition" id="definition-13-4-1">

<strong>Definition 13.4.1</strong>. `/etc/hosts` is a static table of IP addresses and host names, consulted by the C library’s resolver (`getaddrinfo`) before or instead of DNS according to the `hosts:` line of `/etc/nsswitch.conf`; here it is `files dns`, so the file wins. Uses: `localhost`, names for machines on a small network, overriding a name for testing, blocking domains by mapping them to `0.0.0.0`. It is per machine and not propagated; tools that do their own DNS queries (`dig`, `nslookup`) ignore it, `getent hosts` does not. The last command above added an entry in a private mount namespace and `getent` resolved it with no network involved.

</div>

<div class="nb nb-moral">

The shell is a loop of `fork`, `dup2`, `exec` and `wait`; `/proc` is the kernel’s data as text; every Linux tool in this chapter is a thin layer over the system calls of the earlier ones.

</div>
