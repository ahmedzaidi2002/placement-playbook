// Booking and cancellation rules. Every failed rule throws an Error.

function validateBooking(event, quantity, user, now = new Date()) {
  // TODO: Drill 3 on the prep page
  throw new Error("Not implemented");
}

function validateCancellation(booking, currentUserId, now = new Date()) {
  // TODO: Drill 4 on the prep page
  throw new Error("Not implemented");
}

module.exports = { validateBooking, validateCancellation };
