---
title: "10 · The application layer"
linkTitle: "10 Application layer"
weight: 10
math: true
---
## 10.1 Ports to remember {#cn-10-1}

| Service | Port | Transport |
|---|---|---|
| FTP (data / control) | 20 / 21 | TCP |
| SSH | 22 | TCP |
| Telnet | 23 | TCP |
| SMTP | 25 (587 submission) | TCP |
| DNS | 53 | UDP (TCP for large replies, zone transfers) |
| DHCP (server / client) | 67 / 68 | UDP |
| HTTP | 80 | TCP |
| POP3 | 110 | TCP |
| IMAP | 143 | TCP |
| SNMP | 161 | UDP |
| HTTPS | 443 | TCP (UDP for HTTP/3) |

## 10.2 DNS {#cn-10-2}

**DNS** translates names (`www.example.com`) into IP addresses. It is a **distributed, hierarchical** database: **root** servers → **TLD** servers (`.com`, `.in`) → **authoritative** servers for each domain.

**Resolution:** your computer asks its **local (recursive) resolver**; the resolver asks root → TLD → authoritative (**iterative** queries), then returns the answer (a **recursive** query from your point of view). Answers are **cached** for their **TTL**, so most lookups never reach the root.

**Record types:** **A** (name → IPv4), **AAAA** (→ IPv6), **CNAME** (alias → canonical name), **MX** (mail server for a domain), **NS** (name server for a zone), **PTR** (IP → name, reverse lookup), **TXT** (text, e.g. domain verification), **SOA** (zone information).

## 10.3 HTTP {#cn-10-3}

HTTP is **stateless** request–response over TCP (or QUIC).

- **Methods:** **GET** (read; safe, idempotent), **POST** (create/submit; not idempotent), **PUT** (replace; idempotent), **PATCH** (partial update), **DELETE** (idempotent), HEAD, OPTIONS.
- **Status codes:** **1xx** informational, **2xx** success (200 OK, 201 Created, 204 No Content), **3xx** redirect (301 permanent, 302 found, 304 not modified), **4xx** client error (400 bad request, 401 unauthorized, 403 forbidden, 404 not found, 429 too many requests), **5xx** server error (500 internal, 502 bad gateway, 503 unavailable, 504 gateway timeout).

| Version | Key change |
|---|---|
| HTTP/1.0 | one TCP connection per request |
| HTTP/1.1 | **persistent connections** (keep-alive), pipelining (rarely used); head-of-line blocking |
| HTTP/2 | **binary**, **multiplexes** many streams on one connection, header compression, server push |
| HTTP/3 | runs over **QUIC (UDP)**: no TCP head-of-line blocking, faster setup |

**Caching:** `Cache-Control`, `ETag` / `If-None-Match` (→ 304 Not Modified). **CDNs** keep copies near users. A **forward proxy** acts for clients; a **reverse proxy** sits in front of servers (load balancing, TLS termination).

## 10.4 State on a stateless protocol {#cn-10-4}

- **Cookies:** the server sets `Set-Cookie`; the browser sends the cookie back on later requests. Flags: `HttpOnly` (no JavaScript access), `Secure` (HTTPS only), `SameSite` (limits cross-site sending; CSRF defence).
- **Sessions:** the cookie holds only a session ID; the data lives on the server.
- **Tokens (JWT):** a signed token carrying the claims, sent in the `Authorization` header; the server verifies the signature and stores nothing.

## 10.5 APIs and real-time push {#cn-10-5}

- **REST:** resources as URLs, HTTP methods as verbs, usually JSON, stateless. **gRPC:** RPC over HTTP/2 with compact binary messages (Protocol Buffers).
- Getting updates to the client: **short polling** (ask repeatedly), **long polling** (the server holds the request until there is news), **Server-Sent Events** (one-way server → client stream), **WebSocket** (a full-duplex connection upgraded from HTTP; chat, games).

## 10.6 Email and file transfer {#cn-10-6}

- **SMTP** **sends** mail (client → server and server → server), push. **POP3** downloads mail to one device (usually deleting it from the server). **IMAP** keeps mail on the server and syncs across devices.
- **FTP:** two connections, control (21) and data (20). **SFTP** runs over SSH. **Telnet** is unencrypted remote login; **SSH** is the encrypted replacement.

<div class="nb nb-moral">

DNS: resolver → root → TLD → authoritative, cached by TTL; A, AAAA, CNAME, MX. HTTP/1.1 keeps connections alive, HTTP/2 multiplexes, HTTP/3 runs on QUIC. SMTP sends mail, POP3/IMAP read it.

</div>
