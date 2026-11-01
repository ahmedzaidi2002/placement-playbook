const test = require("node:test");
const assert = require("node:assert");
const PromoCode = require("../src/models/promoCodeModel");
const { validatePromoCode } = require("../src/services/promoCodeService");
const { createOrder } = require("../src/services/orderService");

const DAY = 24 * 60 * 60 * 1000;
const daysFromNow = (n) => new Date(Date.now() + n * DAY).toISOString();

test.beforeEach(() => PromoCode.reset());

const rejects = (fn, statusCode, message) =>
  assert.throws(fn, (err) => {
    assert.strictEqual(err.message, message);
    assert.strictEqual(err.statusCode, statusCode);
    return true;
  });

test("a normal code is valid", () => {
  const result = validatePromoCode("SAVE10", 1, 2);
  assert.strictEqual(result.valid, true);
  assert.strictEqual(result.promo.code, "SAVE10");
});

test("lookup ignores case and spaces", () => {
  assert.strictEqual(validatePromoCode("  save10 ", 1, 2).valid, true);
});

test("unknown code: 404", () => {
  rejects(() => validatePromoCode("NOPE", 1, 2), 404, "Promo code not found");
});

test("deleted code: 404, same as unknown", () => {
  rejects(() => validatePromoCode("OLDCODE", 1, 2), 404, "Promo code not found");
});

test("code deleted after creation: 404", () => {
  PromoCode.softDelete("SAVE10");
  rejects(() => validatePromoCode("SAVE10", 1, 2), 404, "Promo code not found");
});

test("not yet active: 400", () => {
  rejects(() => validatePromoCode("FUTURE20", 1, 2), 400, "Promo code is not yet valid");
});

test("expired: 400", () => {
  rejects(() => validatePromoCode("EXPIRED5", 1, 2), 400, "Promo code has expired");
});

test("inside the date window: valid", () => {
  PromoCode.create({ code: "WINDOW", validFrom: daysFromNow(-1), validTo: daysFromNow(1) });
  assert.strictEqual(validatePromoCode("WINDOW", 1, 2).valid, true);
});

test("usage limit reached: 400", () => {
  rejects(() => validatePromoCode("USEDUP", 1, 2), 400, "Promo code usage limit reached");
});

test("one use left: valid", () => {
  PromoCode.create({ code: "LASTONE", maxUses: 5, currentUses: 4 });
  assert.strictEqual(validatePromoCode("LASTONE", 1, 2).valid, true);
});

test("no usage limit set: valid", () => {
  PromoCode.create({ code: "UNLIMITED", currentUses: 9999 });
  assert.strictEqual(validatePromoCode("UNLIMITED", 1, 2).valid, true);
});

test("event-specific code on its own event: valid (id as number or string)", () => {
  assert.strictEqual(validatePromoCode("CONCERT50", 2, 2).valid, true);
  assert.strictEqual(validatePromoCode("CONCERT50", "2", 2).valid, true);
});

test("event-specific code on another event: 400", () => {
  rejects(() => validatePromoCode("CONCERT50", 1, 2), 400, "Promo code is not valid for this event");
});

test("event-specific code with no event given: 400", () => {
  rejects(() => validatePromoCode("CONCERT50", undefined, 2), 400, "Promo code is not valid for this event");
});

test("below minimum quantity: 400", () => {
  rejects(() => validatePromoCode("GROUP4", 1, 3), 400, "Minimum ticket quantity required is 4");
});

test("exactly the minimum quantity: valid, quantity may be a string", () => {
  assert.strictEqual(validatePromoCode("GROUP4", 1, 4).valid, true);
  assert.strictEqual(validatePromoCode("GROUP4", 1, "4").valid, true);
});

test("deleted beats every other rule", () => {
  PromoCode.create({ code: "GONE", validTo: daysFromNow(-1), deletedAt: daysFromNow(-1) });
  rejects(() => validatePromoCode("GONE", 1, 2), 404, "Promo code not found");
});

test("order path: the 6th order on a 5-use code is rejected", () => {
  PromoCode.create({ code: "FIVE", maxUses: 5 });
  for (let i = 0; i < 5; i++) createOrder(1, 1, 2, "FIVE");
  rejects(() => createOrder(1, 1, 2, "FIVE"), 400, "Promo code usage limit reached");
});

test("order path: wrong event is rejected and the use is not counted", () => {
  rejects(() => createOrder(1, 1, 2, "CONCERT50"), 400, "Promo code is not valid for this event");
  assert.strictEqual(PromoCode.findByCode("CONCERT50").currentUses, 0);
});
