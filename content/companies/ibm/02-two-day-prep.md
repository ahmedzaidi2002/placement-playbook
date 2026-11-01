---
title: 2 · Two-day prep
weight: 2
---

Two days is enough because the question is not about algorithms. It tests whether you can **read an unfamiliar Express project, find the one function, add correct checks that throw the right errors, and prove it from the terminal**. Day 1 builds the basics and solves the exam-shaped task once. Day 2 drills the same skill on four similar functions and repeats the main one against the clock.

Everything runs in the [practice project](/downloads/ibm-promo-practice.zip). Unzip it, open the folder in VS Code, and use its terminal (Git Bash on Windows, so the `.sh` scripts run). Node 18 or newer, no install step.

| Folder / file | What it is |
|---|---|
| `src/services/promoCodeService.js` | **Drill 1, the exam task**: buggy `validatePromoCode(code, eventId, quantity)` |
| `src/models/promoCodeModel.js` | in-memory PromoCode table with soft delete, seeded with one code per rule |
| `src/utils/errors.js` | `NotFoundError` (404), `BadRequestError` (400) |
| `src/services/orderService.js` | places orders through your function and counts uses (do not edit) |
| `server.js` + `curl_scripts/` | `npm start`, then the same script names as the exam: 01, 02, 15, 16, 17 (+ 18 delete, 19 list) and `arguments.json` |
| `src/services/promoRulesService.js`, `bookingService.js` | Drills 2 to 5 |
| `test/` | 53 tests: 19 for Drill 1, 22 for Drills 2 and 3, 12 for Drills 4 and 5 |

{{< callout type="info" >}}
**Editor's note.** Drills 2 to 5 are written by me as "similar questions" in the same style; they are not reported IBM questions. Every answer on this page passes the practice project's tests.
{{< /callout >}}

## Day 1 · Basics, then the exam task (about 4 hours)

### Block 1 · JavaScript you actually need (1 hour)

Only these features appear in this kind of question. Type each into `node` (run `node` in a terminal for a prompt) and check the output.

| Feature | Try this | Output |
|---|---|---|
| Template literal (backticks) | `` `Only ${10 - 7} left` `` | `'Only 3 left'` |
| Same with normal quotes (wrong) | `"Only ${10 - 7} left"` | `'Only ${10 - 7} left'` |
| Throw and catch | `try { throw new Error("bad") } catch (e) { e.message }` | `'bad'` |
| Strict equality | `5 === "5"` | `false` |
| `null` in a comparison | `5 > null` | `true` (null becomes 0) |
| `undefined` in a comparison | `5 > undefined` | `false` |
| Text vs number comparison | `"10" < "9"` | `true` (compares characters) |
| Convert first | `Number("10") < 9` | `false` |
| Same id, different types | `String(2) === String("2")` | `true` |
| Array contains | `[101, 102].includes("101")` | `false` (strict, string vs number) |
| <code>&#124;&#124;</code> vs `??` | <code>0 &#124;&#124; 5</code> and `0 ?? 5` | `5` and `0` |
| Date from a day string | `new Date("2026-11-01").toISOString()` | `'2026-11-01T00:00:00.000Z'` (UTC midnight) |
| Comparing dates | `new Date() > new Date("2020-01-01")` | `true` |
| Difference in hours | `(new Date(b) - new Date(a)) / 36e5` | subtracting dates gives milliseconds |

Also know:

- `module.exports = { fn }` and `const { fn } = require("./file")`: how files share functions.
- `class NotFoundError extends Error { … }` and `throw new NotFoundError("…")`: custom errors carry a status code.
- `async function f() { const row = await Model.findOne(…) }`: without `await` you get a Promise, not the row.

### Block 2 · Read the project like the exam (45 minutes)

Without running anything, answer these from the code:

1. Which function do the validate route and the order route both call? (`server.js` → `validatePromoCode`, and `orderService.js` → the same.)
2. How does a thrown `NotFoundError` become HTTP 404? (`errors.js` sets `statusCode`; the server's `catch` sends it.)
3. What marks a deleted code in the model, and does `findByCode` skip deleted rows? (`deletedAt`; no, it returns them.)
4. Where is a use counted? (`orderService.js`, after the order is created.)

Then practise the exam's search commands in the project folder:

```bash
grep -rn "validatePromoCode" --include=*.js . | grep -v node_modules
grep -rn "class .*Error" src/utils
```

### Block 3 · Drill 1, the exam task (1 hour 15 minutes)

Fix `validatePromoCode` in `src/services/promoCodeService.js`. Set a **30-minute** timer. Messages and status codes are in `test/promoCode.test.js`, the way the exam has them in the spec file.

Check with the tests:

```bash
node --test test/promoCode.test.js
```

Done when all 19 pass (out of the box, 8 pass and 11 fail). Then do the exam's manual check, two terminals:

```bash
npm start
```

```bash
cd curl_scripts
./01_register_user.sh
./02_login.sh
./15_create_promo_code.sh
./16_validate_promo_code.sh
./17_create_order.sh
./17_create_order.sh
./17_create_order.sh
./18_delete_promo_code.sh
./16_validate_promo_code.sh
```

`arguments.json` creates `NEWCODE` with 2 uses, so the **third** order must give `400 Promo code usage limit reached`, and validating after the delete must give `404 Promo code not found`. Before your fix, both succeed: that is the bug. Then edit `validatePromo` in `arguments.json` to try the seeded codes: `EXPIRED5`, `FUTURE20`, `USEDUP`, `CONCERT50` with `eventId` 1, `GROUP4` with `quantity` 3, `OLDCODE`. Restart the server to reset the data.

{{< details title="Show answer" closed="true" >}}

```js
function validatePromoCode(code, eventId, quantity = 1) {
  const promo = PromoCode.findByCode(code);

  if (!promo || promo.deletedAt) {
    throw new NotFoundError("Promo code not found");
  }

  const now = new Date();

  if (promo.validFrom && now < new Date(promo.validFrom)) {
    throw new BadRequestError("Promo code is not yet valid");
  }

  if (promo.validTo && now > new Date(promo.validTo)) {
    throw new BadRequestError("Promo code has expired");
  }

  if (promo.maxUses !== null && promo.maxUses !== undefined && promo.currentUses >= promo.maxUses) {
    throw new BadRequestError("Promo code usage limit reached");
  }

  if (promo.eventId !== null && promo.eventId !== undefined && String(promo.eventId) !== String(eventId)) {
    throw new BadRequestError("Promo code is not valid for this event");
  }

  const qty = quantity === null || quantity === undefined ? 1 : Number(quantity);
  if (promo.minTickets && qty < promo.minTickets) {
    throw new BadRequestError(`Minimum ticket quantity required is ${promo.minTickets}`);
  }

  return { valid: true, promo };
}
```

{{< /details >}}

### Block 4 · Review (30 minutes)

Write the trap table from [page 1](/companies/ibm/01-promo-code-question/#traps-that-lose-marks) from memory: 404 for deleted, spec messages, spec order, `null` limits, string ids, `Number(quantity)`, no counting in validation, `await`. Then restore the original `promoCodeService.js` from the zip and write the fix again: aim for under 15 minutes.

## Day 2 · Similar questions, timed (about 4 hours)

Each drill: read the spec, set the timer, write it, run its test file, then open the answer.

### Drill 2 · `validatePromoRules`, 8-rule variant, 25 minutes

File `src/services/promoRulesService.js`. The same idea with the promo object passed in and eight rules, in this order: minimum tickets, maximum tickets, expiry (a code expiring **today** is still valid), start date (starting today is valid), redemption limit, minimum order amount, first-time buyers only, allowed event list. One rule is written for you. Plain `Error`s; messages are in `test/promoRules.test.js`.

```bash
node --test --test-name-pattern="^[0-9]|valid|optional|first" test/promoRules.test.js
```

{{< details title="Show answer" closed="true" >}}

```js
function startOfDay(value) {
  const d = new Date(value);
  d.setHours(0, 0, 0, 0);
  return d;
}

function isSet(value) {
  return value !== null && value !== undefined;
}

function validatePromoRules(promoCode, quantity, cartTotal, currentUser, eventId) {
  if (isSet(promoCode.minTickets) && quantity < promoCode.minTickets) {
    throw new Error(`Minimum of ${promoCode.minTickets} tickets required`);
  }

  if (isSet(promoCode.maxTickets) && quantity > promoCode.maxTickets) {
    throw new Error(`Maximum of ${promoCode.maxTickets} tickets allowed`);
  }

  const today = startOfDay(new Date());

  if (isSet(promoCode.expiryDate) && today > startOfDay(promoCode.expiryDate)) {
    throw new Error(`This promo code expired on ${promoCode.expiryDate}`);
  }

  if (isSet(promoCode.startDate) && today < startOfDay(promoCode.startDate)) {
    throw new Error(`This promo code is not active until ${promoCode.startDate}`);
  }

  if (isSet(promoCode.maxUsageLimit) && promoCode.usageCount >= promoCode.maxUsageLimit) {
    throw new Error("This promo code has reached its maximum redemption limit");
  }

  if (isSet(promoCode.minOrderAmount) && cartTotal < promoCode.minOrderAmount) {
    throw new Error(`Order total must be at least ${promoCode.minOrderAmount} to use this code`);
  }

  if (promoCode.newUserOnly && !currentUser.isFirstPurchase) {
    throw new Error("This promo code is restricted to first-time buyers only");
  }

  const allowed = promoCode.allowedEventIds;
  if (Array.isArray(allowed) && allowed.length > 0 &&
      !allowed.map(String).includes(String(eventId))) {
    throw new Error("This promo code cannot be applied to the selected event");
  }

  return true;
}
```

This one compares **days**, not exact times, because its spec says a code expiring today is valid. `setHours` on a `"YYYY-MM-DD"` string shifts it a day back on machines west of UTC (checked: passes in IST and UTC, fails "expires today" in US Pacific). If that bites, compare `new Date(v).toISOString().slice(0, 10)` strings instead, which passed in every timezone tried.

{{< /details >}}

### Drill 3 · `applyDiscount(promoCode, cartTotal)`, 15 minutes

Same file. Return the final price after the discount.

- `discountType` is `"PERCENT"` (take `discountValue` percent off) or `"FLAT"` (take `discountValue` off). Anything else: throw `Invalid discount type`.
- If `maxDiscount` is set, the discount cannot exceed it.
- The final price is never below 0, and is rounded to 2 decimals.

{{< details title="Show answer" closed="true" >}}

```js
function applyDiscount(promoCode, cartTotal) {
  let discount;
  if (promoCode.discountType === "PERCENT") {
    discount = (cartTotal * promoCode.discountValue) / 100;
  } else if (promoCode.discountType === "FLAT") {
    discount = promoCode.discountValue;
  } else {
    throw new Error("Invalid discount type");
  }

  if (isSet(promoCode.maxDiscount)) {
    discount = Math.min(discount, promoCode.maxDiscount);
  }

  const finalTotal = Math.max(0, cartTotal - discount);
  return Math.round(finalTotal * 100) / 100;
}
```

Checks in the tests: 20% off 1000 is 800; 50% off 1000 capped at 300 is 700; flat 500 off 300 is 0; 33% off 99.99 is 66.99.

{{< /details >}}

### Drill 4 · `validateBooking(event, quantity, user, now)`, 25 minutes

File `src/services/bookingService.js`. Check in this order and throw the first failure:

1. `quantity` is not a positive whole number → `Quantity must be a positive integer`
2. `event.status` is not `"PUBLISHED"` → `Event is not open for booking`
3. `event.date` is not after `now` → `Event has already started`
4. fewer seats left (`capacity - ticketsSold`) than `quantity` → `` `Only ${left} tickets left` ``
5. `user.ticketsBoughtForEvent + quantity` is more than `event.maxPerUser` → `` `You can book at most ${maxPerUser} tickets for this event` ``
6. `event.minAge` is set and `user.age` is below it → `` `You must be at least ${minAge} to book this event` ``

Return `true` otherwise. `now` is passed in so the tests can fix the clock.

{{< details title="Show answer" closed="true" >}}

```js
function validateBooking(event, quantity, user, now = new Date()) {
  if (!Number.isInteger(quantity) || quantity <= 0) {
    throw new Error("Quantity must be a positive integer");
  }

  if (event.status !== "PUBLISHED") {
    throw new Error("Event is not open for booking");
  }

  if (new Date(event.date) <= now) {
    throw new Error("Event has already started");
  }

  const left = event.capacity - event.ticketsSold;
  if (quantity > left) {
    throw new Error(`Only ${left} tickets left`);
  }

  if (user.ticketsBoughtForEvent + quantity > event.maxPerUser) {
    throw new Error(`You can book at most ${event.maxPerUser} tickets for this event`);
  }

  if (event.minAge && user.age < event.minAge) {
    throw new Error(`You must be at least ${event.minAge} to book this event`);
  }

  return true;
}
```

The traps it tests: `2.5` and `"3"` are not valid quantities (`Number.isInteger` rejects both); the per-user cap counts tickets bought earlier, not only this order.

{{< /details >}}

### Drill 5 · `validateCancellation(booking, currentUserId, now)`, 15 minutes

1. `booking.userId` is not `currentUserId` → `You can only cancel your own booking`
2. `booking.status` is `"CANCELLED"` → `Booking is already cancelled`
3. less than 24 hours until `booking.eventDate` → `Bookings can only be cancelled up to 24 hours before the event`

Exactly 24 hours before is still allowed.

{{< details title="Show answer" closed="true" >}}

```js
const HOUR_MS = 60 * 60 * 1000;

function validateCancellation(booking, currentUserId, now = new Date()) {
  if (booking.userId !== currentUserId) {
    throw new Error("You can only cancel your own booking");
  }

  if (booking.status === "CANCELLED") {
    throw new Error("Booking is already cancelled");
  }

  if (new Date(booking.eventDate) - now < 24 * HOUR_MS) {
    throw new Error("Bookings can only be cancelled up to 24 hours before the event");
  }

  return true;
}
```

Subtracting two dates gives milliseconds, so the 24-hour rule is one line. `<` (not `<=`) keeps "exactly 24 hours" allowed.

{{< /details >}}

### Block 5 · Timed redo of Drill 1 (30 minutes)

Restore the original `promoCodeService.js` from the zip and do the **whole exam routine** without looking at anything: grep for the function, read the model and errors file, write the fix, run the 19 tests, then the curl sequence from Block 3. Target: green tests in **15 minutes**, curl proof in 10 more.

### Block 6 · Exam-day checklist (read it the morning of the test)

1. Open `technical-specs/promo_code_validation.md` first. Note every message, status code, the order of checks, and edge cases.
2. Skim `documents/ARCHITECTURE.md`: services folder, ORM, errors file.
3. `grep -rn "validatePromo" --include=*.js . | grep -v node_modules` to find the function; read the existing `throw`.
4. Open the model: exact field names for deleted, dates, uses, event, minimum.
5. Add one `if` per rule in the spec's order, each `throw new …Error(…)`. Deleted → the not-found error (404).
6. Guard `null` limits, compare ids as strings, `Number(quantity)`, keep `await`.
7. Terminal 1 `npm start`; terminal 2 `cd curl_scripts` and run 01, 02, 15, 16, 17. Edit `arguments.json` to break each rule once.
8. Do not edit tests, routes or the order code; do not count uses in validation.
9. Run `npm test` if it exists, re-read the spec's edge cases, submit.

## Where you should be after two days

| Check | Target |
|---|---|
| Practice project | 53 of 53 tests pass |
| Drill 1 from blank | tests green in under 15 minutes |
| curl routine | server up, scripts run, each rule broken once, in under 10 minutes |
| Trap table | can write all of it from memory |
