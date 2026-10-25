---
title: "11 · Security, wireless and \"what happens when you type a URL\""
linkTitle: "11 Security and wireless"
weight: 11
math: true
---
## 11.1 What we want, and which tool gives it {#cn-11-1}

| Goal | Tool |
|---|---|
| **Confidentiality** (only the receiver can read) | encryption |
| **Integrity** (not modified) | hash + MAC, or signature |
| **Authentication** (who sent it) | MAC, digital signature, certificates |
| **Non-repudiation** (sender cannot deny) | digital signature |

- **Symmetric encryption** (AES): one shared key; fast; the problem is sharing the key.
- **Asymmetric (public-key) encryption** (RSA, elliptic curves): a public key encrypts, the private key decrypts; slow; solves key exchange.
- In practice: public-key crypto to agree on a key, then symmetric encryption for the data.
- **Hash** (SHA-256): fixed-size fingerprint; one-way; collision-resistant. **MAC/HMAC:** a hash with a shared secret key. **Digital signature:** hash of the message encrypted with the sender's **private** key; anyone verifies with the **public** key.

## 11.2 RSA and Diffie–Hellman, tiny examples {#cn-11-2}

<div class="nb nb-example">

<strong>Example</strong> (RSA)

Primes $p = 3$, $q = 11$ → $n = 33$, $\varphi(n) = (p-1)(q-1) = 20$. Pick $e = 3$ (coprime to 20). Private $d$ with $e \cdot d \equiv 1 \pmod{20}$ → $d = 7$ ($3 \times 7 = 21$). Public key $(e, n) = (3, 33)$, private $(7, 33)$.
Encrypt $m = 4$: $4^3 = 64 \bmod 33 = $ **31**. Decrypt: $31^7 \bmod 33 = $ **4**. Security rests on the difficulty of factoring $n$.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Diffie–Hellman key exchange)

Public $p = 23$, $g = 5$. Alice picks secret $a = 6$, sends $A = 5^6 \bmod 23 = 8$. Bob picks $b = 15$, sends $B = 5^{15} \bmod 23 = 19$. Alice computes $19^6 \bmod 23 = 2$; Bob computes $8^{15} \bmod 23 = 2$. Shared key **2**, never sent over the wire. Plain DH is open to a man-in-the-middle unless the exchange is authenticated (certificates).

</div>

## 11.3 Certificates and TLS {#cn-11-3}

A **certificate** binds a domain name to a public key and is signed by a **certificate authority (CA)**; browsers trust a set of root CAs and verify the **chain of trust** (server certificate → intermediate → root).

**TLS 1.3 handshake (1 RTT):** the client sends supported ciphers and its key share; the server replies with its key share, certificate and a signature; both derive the same session keys (ephemeral Diffie–Hellman, which gives **forward secrecy**); then data flows encrypted with a symmetric cipher. HTTPS = HTTP over TLS.

## 11.4 Firewalls and attacks {#cn-11-4}

- **Packet-filter firewall:** allow/deny by IP, port, protocol. **Stateful firewall:** tracks connections. **Application-layer firewall / proxy, WAF:** inspects content. **IDS** detects intrusions; **IPS** also blocks them.
- **Attacks to name:** **DoS/DDoS** (flood a target; SYN flood), **man-in-the-middle** (ARP spoofing, fake Wi-Fi), **DNS spoofing/cache poisoning**, **IP spoofing**, **phishing**, **replay attacks** (defence: nonces, timestamps), **SQL injection** (defence: parameterised queries), **XSS** (defence: escape output, CSP), **CSRF** (defence: anti-CSRF tokens, SameSite cookies).

## 11.5 Wi-Fi {#cn-11-5}

Wireless differs: signals fade, interfere, and a station **cannot hear collisions while sending**, so Wi-Fi uses **CSMA/CA** (collision avoidance with random back-off and ACKs) instead of CSMA/CD.

- **Hidden-terminal problem:** A and C both reach the access point B but not each other, so carrier sense fails and they collide at B. Fix: **RTS/CTS**: the sender asks (RTS), the AP grants (CTS), and every station that hears the CTS stays quiet.
- **Exposed-terminal problem:** a station needlessly stays quiet because it hears an unrelated transmission.
- Security: WEP (broken) → WPA2 (AES) → **WPA3**.

## 11.6 What happens when you type a URL and press Enter {#cn-11-6}

1. The browser parses the URL; checks its caches (HSTS, DNS).
2. **DNS lookup:** browser/OS cache → local resolver → root → TLD → authoritative → IP address.
3. To reach the resolver or the server, the host uses **ARP** to find its default gateway's MAC address (if not cached).
4. **TCP three-way handshake** with the server on port 443 (or QUIC over UDP for HTTP/3).
5. **TLS handshake:** certificate verified, session keys agreed.
6. The browser sends the **HTTP GET** request (with cookies).
7. Along the way: NAT at the home router, routing hop by hop (longest-prefix match), maybe a CDN or load balancer answering.
8. The server (web server → application → database) builds the response: status code, headers, HTML.
9. The browser parses HTML, fetches CSS, JavaScript and images (more requests, reusing the connection), builds the DOM, lays out and **renders** the page.
10. Connections are kept alive for reuse, then closed.

<div class="nb nb-moral">

Asymmetric crypto to agree on a key, symmetric crypto for the data, signatures and certificates for identity. Wi-Fi avoids collisions (CSMA/CA, RTS/CTS) because it cannot detect them. The URL walkthrough is DNS → TCP → TLS → HTTP → render.

</div>
