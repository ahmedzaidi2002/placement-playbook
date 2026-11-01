# IBM promo-code practice

Needs Node 18 or newer, no `npm install`.

```bash
npm test                                  # everything
node --test test/promoCode.test.js        # only the promo-code tests
node --test --test-name-pattern="expired" # one test by name
```

Files you edit: `src/services/promoCodeService.js` and `src/services/bookingService.js`.
The tests in `test/` are the spec: read a failing test's name and expected message,
then write the `if` that produces it.
