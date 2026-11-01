const test = require("node:test");
const assert = require("node:assert");
const { validatePromoCode, applyDiscount } = require("../src/services/promoCodeService");

const DAY = 24 * 60 * 60 * 1000;
const iso = (offsetDays) => new Date(Date.now() + offsetDays * DAY).toISOString().slice(0, 10);

function promo(overrides = {}) {
  return {
    code: "FEST50",
    minTickets: 2,
    maxTickets: 10,
    startDate: iso(-5),
    expiryDate: iso(5),
    usageCount: 3,
    maxUsageLimit: 100,
    minOrderAmount: 500,
    newUserOnly: false,
    allowedEventIds: [101, 102],
    ...overrides,
  };
}

const user = { id: 7, isFirstPurchase: false };
const check = (p, q = 4, total = 1000, u = user, ev = 101) => () => validatePromoCode(p, q, total, u, ev);

test("valid code returns true", () => {
  assert.strictEqual(check(promo())(), true);
});

test("1. below minimum tickets", () => {
  assert.throws(check(promo(), 1), { message: "Minimum of 2 tickets required" });
});

test("2. above maximum tickets", () => {
  assert.throws(check(promo(), 11), { message: "Maximum of 10 tickets allowed" });
});

test("2. exactly min and max are allowed", () => {
  assert.strictEqual(check(promo(), 2)(), true);
  assert.strictEqual(check(promo(), 10)(), true);
});

test("3. expired code", () => {
  const p = promo({ expiryDate: iso(-1) });
  assert.throws(check(p), { message: `This promo code expired on ${p.expiryDate}` });
});

test("3. expiring today is still valid", () => {
  assert.strictEqual(check(promo({ expiryDate: iso(0) }))(), true);
});

test("4. not started yet", () => {
  const p = promo({ startDate: iso(2) });
  assert.throws(check(p), { message: `This promo code is not active until ${p.startDate}` });
});

test("4. starting today is valid", () => {
  assert.strictEqual(check(promo({ startDate: iso(0) }))(), true);
});

test("5. usage limit reached", () => {
  assert.throws(check(promo({ usageCount: 100 })), {
    message: "This promo code has reached its maximum redemption limit",
  });
});

test("5. one use left is fine", () => {
  assert.strictEqual(check(promo({ usageCount: 99 }))(), true);
});

test("6. cart below minimum order amount", () => {
  assert.throws(check(promo(), 4, 499), { message: "Order total must be at least 500 to use this code" });
});

test("7. new-user code used by a returning user", () => {
  assert.throws(check(promo({ newUserOnly: true })), {
    message: "This promo code is restricted to first-time buyers only",
  });
});

test("7. new-user code used by a first-time buyer", () => {
  assert.strictEqual(check(promo({ newUserOnly: true }), 4, 1000, { id: 8, isFirstPurchase: true })(), true);
});

test("8. wrong event", () => {
  assert.throws(check(promo(), 4, 1000, user, 999), {
    message: "This promo code cannot be applied to the selected event",
  });
});

test("8. event id as a string still matches", () => {
  assert.strictEqual(check(promo(), 4, 1000, user, "102")(), true);
});

test("optional limits left null are skipped", () => {
  const p = promo({ maxTickets: null, maxUsageLimit: null, minOrderAmount: null, allowedEventIds: [] });
  assert.strictEqual(check(p, 50, 10, user, 999)(), true);
});

test("first failing rule wins (min tickets before cart total)", () => {
  assert.throws(check(promo(), 1, 10), { message: "Minimum of 2 tickets required" });
});

test("applyDiscount: percent", () => {
  assert.strictEqual(applyDiscount({ discountType: "PERCENT", discountValue: 20 }, 1000), 800);
});

test("applyDiscount: percent capped by maxDiscount", () => {
  assert.strictEqual(applyDiscount({ discountType: "PERCENT", discountValue: 50, maxDiscount: 300 }, 1000), 700);
});

test("applyDiscount: flat never goes below zero", () => {
  assert.strictEqual(applyDiscount({ discountType: "FLAT", discountValue: 500 }, 300), 0);
});

test("applyDiscount: rounds to 2 decimals", () => {
  assert.strictEqual(applyDiscount({ discountType: "PERCENT", discountValue: 33 }, 99.99), 66.99);
});

test("applyDiscount: unknown type", () => {
  assert.throws(() => applyDiscount({ discountType: "BOGO", discountValue: 1 }, 100), {
    message: "Invalid discount type",
  });
});
