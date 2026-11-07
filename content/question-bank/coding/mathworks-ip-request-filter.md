---
aliases: ["/question-bank/mathworks-ip-request-filter/"]
title: "IP Address Request Filter"
weight: 20
---

MathWorks OA · Medium · Wildcard matching + a sliding window per IP

**Problem.** A firewall gets a blacklist of wildcard patterns (for example `*111.*`, `123.*`, `11.*.255`) and then a list of requests, each written as `"IP timestamp"`, already sorted by time. For every request print `1` if it is blocked and `0` if it is allowed. A request is blocked when

1. its IP matches **any** blacklist pattern (`*` stands for any run of characters, even an empty run), or
2. that IP already made **2 or more allowed** requests in the window `[t - 5, t]`.

A blocked request is *not* remembered. Only allowed requests count towards the rate limit.

Example: blacklist `["*111.*", "123.*", "11.*.255"]`, requests `["123.1.23.34 1", "11.45.67.255 2", "192.168.1.1 3", "192.168.1.1 4", "192.168.1.1 5", "192.168.1.1 9"]` gives `[1, 1, 0, 0, 1, 0]`.

**The idea in easy words.** There are two small questions hiding in one problem, and they do not depend on each other:

1. *Does this IP match a blacklist pattern?* This never changes for the same IP, so answer it once per IP and remember the answer.
2. *Did this IP already use up its 2 allowed requests in the last 5 seconds?* For this, keep for every IP a small queue with the times of its **allowed** requests.

**Step by step.**

1. Read the request and split it into `ip` and `t`.
2. If we have not checked this IP before, test it against every pattern and store `banned[ip] = true/false`.
3. If `banned[ip]` is true, answer `1` and stop. Nothing is stored, so a blacklisted request never affects any history.
4. Otherwise take the queue of this IP. Throw away times from the front that are older than `t - 5`. The timestamps never go down, so old times are always at the front, and a time that is too old now will be too old for every later request as well.
5. If the queue still holds 2 or more times, answer `1`. Do not store `t`.
6. Else answer `0` and push `t` at the back.

**How the wildcard test works.** Walk `i` over the IP and `j` over the pattern.

- Same character on both sides: move both forward.
- Pattern has `*`: remember where the star is (`star = j`) and where we are in the IP (`mark = i`), and move only `j`. This means "for now the star matches nothing".
- Mismatch, but there was a star earlier: let that star swallow one more character of the IP. Go back with `j = star + 1` and `i = ++mark`.
- Mismatch and no star: this pattern does not match.
- When the IP is finished, skip any stars left at the end of the pattern. It matches only if the whole pattern was used.

Only the **latest** star needs remembering. Earlier stars have already been given the shortest stretch that worked, and giving the latest star more characters can only help the rest of the pattern to fit. Example: pattern `11.*.255` on `11.45.67.255`. `11.` matches, then the star starts empty, `.` fails on `4`, so the star swallows `4`, then `45`, and so on, until the star has swallowed `45.67` and `.255` matches the end.

**Dry run of the example.**

| request | blacklisted? | queue before (after dropping times below t-5) | answer | queue after |
|---|---|---|---|---|
| 123.1.23.34 at 1 | matches `123.*` | not used | 1 | not used |
| 11.45.67.255 at 2 | matches `11.*.255` | not used | 1 | not used |
| 192.168.1.1 at 3 | no | empty | 0 | [3] |
| 192.168.1.1 at 4 | no | [3] | 0 | [3, 4] |
| 192.168.1.1 at 5 | no | [3, 4], size 2 | 1 | [3, 4] |
| 192.168.1.1 at 9 | no | 3 is below 9-5=4, dropped, so [4] | 0 | [4, 9] |

```cpp
class Solution {
public:
    bool match(const string& s, const string& p) {
        int i = 0, j = 0, star = -1, mark = 0;
        while (i < (int)s.size()) {
            if (j < (int)p.size() && p[j] == '*') {
                star = j++;
                mark = i;
            } else if (j < (int)p.size() && p[j] == s[i]) {
                i++;
                j++;
            } else if (star != -1) {
                j = star + 1;
                i = ++mark;
            } else {
                return false;
            }
        }
        while (j < (int)p.size() && p[j] == '*') j++;
        return j == (int)p.size();
    }

    vector<int> filterRequests(vector<string>& blacklist, vector<string>& requests) {
        unordered_map<string, bool> banned;
        unordered_map<string, deque<long long>> hist;
        vector<int> ans;
        for (auto& r : requests) {
            stringstream ss(r);
            string ip;
            long long t;
            ss >> ip >> t;
            if (!banned.count(ip)) {
                bool bad = false;
                for (auto& p : blacklist) {
                    if (match(ip, p)) {
                        bad = true;
                        break;
                    }
                }
                banned[ip] = bad;
            }
            if (banned[ip]) {
                ans.push_back(1);
                continue;
            }
            auto& dq = hist[ip];
            while (!dq.empty() && dq.front() < t - 5) dq.pop_front();
            if (dq.size() >= 2) {
                ans.push_back(1);
            } else {
                dq.push_back(t);
                ans.push_back(0);
            }
        }
        return ans;
    }
};
```

**Why it is fast.** Every timestamp enters a queue once and leaves once, so the rate-limit part is $O(R)$ for $R$ requests. The wildcard test costs at most about $|\text{IP}| \cdot |\text{pattern}|$ steps, and an IP has at most 15 characters, so it is tiny. It runs once per distinct IP and per pattern, never again, thanks to the stored answer.

Time $O(R \cdot P \cdot L)$ in the worst case for $P \le 100$ patterns and IP length $L \le 15$, plus $O(R)$ for the queues. Space $O(R)$.
