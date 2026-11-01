---
title: 2 · Two-day prep
weight: 2
---

Two days is enough because the question is not about algorithms. It tests whether you can **read an unfamiliar project, find the one function, and write correct `if` checks in JavaScript** with exact messages. Day 1 builds the basics and solves the main question once. Day 2 does three similar questions under time and repeats the main one from blank.

Everything runs in the [practice project](/downloads/ibm-promo-practice.zip). Unzip it, open the folder in VS Code, and run `npm test` in its terminal (Node 18 or newer, no install step).

{{< callout type="info" >}}
**Editor's note.** The drills on this page are written by me as "similar questions" in the same style: a service function, rules in a fixed order, `throw new Error` with exact messages. They are not reported IBM questions. Every answer below passes the practice project's tests.
{{< /callout >}}

## Day 1 · Basics, then the real question (about 4 hours)

### Block 1 · JavaScript you actually need (1 hour)

Only these features appear in this kind of question. For each, type the example into `node` (just run `node` in a terminal for a prompt) and check the output.

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
| Array contains | `[101, 102].includes("101")` | `false` (strict, string vs number) |
| Integer check | `Number.isInteger("3")` | `false` |
| <code>&#124;&#124;</code> vs `??` | <code>0 &#124;&#124; 5</code> and `0 ?? 5` | `5` and `0` |
| Date from a day string | `new Date("2026-11-01").toISOString()` | `'2026-11-01T00:00:00.000Z'` (UTC midnight) |
| Date with a time | `new Date("2026-11-01T00:00:00").toISOString()` | `'2026-10-31T18:30:00.000Z'` in IST (local midnight) |
| Start of today | `const d = new Date(); d.setHours(0, 0, 0, 0)` | today at 00:00 local |
| Difference in hours | `(new Date(b) - new Date(a)) / 36e5` | subtracting dates gives milliseconds |

Also know `module.exports = { fn }` and `const { fn } = require("./file")`: that is how the service is shared with the controller and the tests.

### Block 2 · Read a Node project (45 minutes)

Open the practice project and trace one request without running anything:

1. `src/controllers/promoController.js`: the controller reads `req.body`, calls `validatePromoCode` inside `try`, and in `catch` sends `res.status(400).json({ message: err.message })`. This is why the service throws.
2. `src/services/promoCodeService.js`: the function you will fill. One rule is written; copy its shape.
3. `test/promoCode.test.js`: each `test("…", …)` builds a promo code, breaks one rule and checks the message with `assert.throws(fn, { message: "…" })`. The exam project will likely use Jest instead, which reads `expect(fn).toThrow("…")`; it means the same thing.

Questions to answer for yourself: where would `usageCount` be increased? (Not in validation: after the booking is paid.) Which test tells you the order of the checks? (`first failing rule wins`.)

### Block 3 · Drill 1, the main question (1 hour, then review)

Fill the seven `TODO`s in `validatePromoCode`. Set a **30-minute** timer. Run only its tests while working:

```bash
node --test --test-name-pattern="^[0-9]|valid|optional|first" test/promoCode.test.js
```

Done when the 17 `validatePromoCode` tests pass. Compare with the full answer on [page 1](/companies/ibm/01-promo-code-question/#the-solution) and note each difference.

### Block 4 · Review (30 minutes)

Write the trap table from page 1 from memory on paper: backticks, exact messages, order, `>=` for usage, day comparison, `null` limits, string ids. Then delete your code and write it again: aim for under 15 minutes.

## Day 2 · Similar questions, timed (about 4 hours)

Each drill: read the spec, set the timer, write it, run `npm test`, then open the answer.

### Drill 2 · `applyDiscount(promoCode, cartTotal)`, 15 minutes

Return the final price after the discount.

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

  if (promoCode.maxDiscount !== null && promoCode.maxDiscount !== undefined) {
    discount = Math.min(discount, promoCode.maxDiscount);
  }

  const finalTotal = Math.max(0, cartTotal - discount);
  return Math.round(finalTotal * 100) / 100;
}
```

Checks in the tests: 20% off 1000 is 800; 50% off 1000 capped at 300 is 700; flat 500 off 300 is 0; 33% off 99.99 is 66.99.

{{< /details >}}

### Drill 3 · `validateBooking(event, quantity, user, now)`, 25 minutes

Check, in this order, and throw the first failure:

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

### Drill 4 · `validateCancellation(booking, currentUserId, now)`, 15 minutes

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

### Block 5 · Timed redo of Drill 1 (20 minutes)

Restore the original `promoCodeService.js` from the zip and solve the main question again without looking at anything. Target: all 17 tests green in **15 minutes**. If a test fails, fix it from the error output alone; that is the exam skill.

### Block 6 · Exam-day checklist (read it the morning of the test)

1. Read the statement fully; list rules and messages in order.
2. Search for the function name; read the `if` that is already there.
3. Open the model for exact field names, and the tests for exact messages.
4. Backticks for any message with `${}`.
5. One `if` per rule, in the statement's order, each `throw new Error(...)`. Never `res` in a service.
6. Boundaries: equal to the limit allowed? Expiring today allowed? Usage `>=`.
7. Dates compared by day. Ids compared as the same type. Numbers from `req.body` converted.
8. Run the tests, read the first failure, fix, repeat. Never edit the tests.
9. Leave the given code style as is (semicolons, quotes, indentation); only add the missing rules.

## Where you should be after two days

| Check | Target |
|---|---|
| Practice project | 34 of 34 tests pass |
| Drill 1 from blank | under 15 minutes |
| Trap table | can write all of it from memory |
| Reading a new project | can find the function, model fields and test messages in under 5 minutes |
