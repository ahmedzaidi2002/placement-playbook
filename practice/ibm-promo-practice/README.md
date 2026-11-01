# IBM promo-code practice (ShowPass shape)

Needs Node 18 or newer. No `npm install`. curl scripts need Git Bash (Windows) or any bash.

## The exam task, in this project

`src/services/promoCodeService.js` accepts codes it should reject. Fix `validatePromoCode` so that:

- deleted codes are rejected as **not found** (404)
- codes before `validFrom` or after `validTo` are rejected (400)
- codes whose `currentUses` has reached `maxUses` are rejected (400)
- codes with an `eventId` only work for that event (400)
- `minTickets` is enforced (400)

Messages are in the tests (`test/promoCode.test.js`). Do not edit `orderService.js`: orders already call your function.

## Run

```bash
npm test                                  # all 53 tests
node --test test/promoCode.test.js        # only the exam-shaped 19
```

Exam-style manual check (two terminals):

```bash
npm start                                 # terminal 1: server on port 3000
cd curl_scripts                           # terminal 2
./01_register_user.sh
./02_login.sh
./15_create_promo_code.sh
./16_validate_promo_code.sh
./17_create_order.sh
```

Change values in `curl_scripts/arguments.json` to try each rule. Seeded codes:
SAVE10 (valid), EXPIRED5, FUTURE20, USEDUP, CONCERT50 (event 2 only), GROUP4 (min 4), OLDCODE (deleted).
Restart the server to reset data.

## Extra drills

`promoRulesService.js` (8-rule version + applyDiscount) and `bookingService.js` (booking and cancellation).
See the Two-day prep page in the Playbook.
