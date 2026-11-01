const test = require("node:test");
const assert = require("node:assert");
const { validateBooking, validateCancellation } = require("../src/services/bookingService");

const NOW = new Date("2026-11-10T12:00:00Z");
const HOUR = 60 * 60 * 1000;
const at = (hours) => new Date(NOW.getTime() + hours * HOUR).toISOString();

function event(overrides = {}) {
  return { status: "PUBLISHED", date: at(72), capacity: 100, ticketsSold: 90, maxPerUser: 6, minAge: 0, ...overrides };
}

const buyer = { age: 21, ticketsBoughtForEvent: 2 };

test("booking: valid", () => {
  assert.strictEqual(validateBooking(event(), 4, buyer, NOW), true);
});

test("booking: quantity must be a positive integer", () => {
  for (const q of [0, -1, 2.5, "3"]) {
    assert.throws(() => validateBooking(event(), q, buyer, NOW), { message: "Quantity must be a positive integer" });
  }
});

test("booking: event not published", () => {
  assert.throws(() => validateBooking(event({ status: "DRAFT" }), 1, buyer, NOW), {
    message: "Event is not open for booking",
  });
});

test("booking: event already started", () => {
  assert.throws(() => validateBooking(event({ date: at(-1) }), 1, buyer, NOW), {
    message: "Event has already started",
  });
});

test("booking: not enough seats", () => {
  assert.throws(() => validateBooking(event(), 11, { age: 21, ticketsBoughtForEvent: 0 }, NOW), {
    message: "Only 10 tickets left",
  });
});

test("booking: per-user cap counts earlier purchases", () => {
  assert.throws(() => validateBooking(event(), 5, buyer, NOW), {
    message: "You can book at most 6 tickets for this event",
  });
});

test("booking: age limit", () => {
  assert.throws(() => validateBooking(event({ minAge: 18 }), 1, { age: 16, ticketsBoughtForEvent: 0 }, NOW), {
    message: "You must be at least 18 to book this event",
  });
});

test("cancel: valid", () => {
  assert.strictEqual(validateCancellation({ userId: 7, status: "CONFIRMED", eventDate: at(48) }, 7, NOW), true);
});

test("cancel: someone else's booking", () => {
  assert.throws(() => validateCancellation({ userId: 7, status: "CONFIRMED", eventDate: at(48) }, 8, NOW), {
    message: "You can only cancel your own booking",
  });
});

test("cancel: already cancelled", () => {
  assert.throws(() => validateCancellation({ userId: 7, status: "CANCELLED", eventDate: at(48) }, 7, NOW), {
    message: "Booking is already cancelled",
  });
});

test("cancel: inside the 24-hour window", () => {
  assert.throws(() => validateCancellation({ userId: 7, status: "CONFIRMED", eventDate: at(23) }, 7, NOW), {
    message: "Bookings can only be cancelled up to 24 hours before the event",
  });
});

test("cancel: exactly 24 hours before is allowed", () => {
  assert.strictEqual(validateCancellation({ userId: 7, status: "CONFIRMED", eventDate: at(24) }, 7, NOW), true);
});
