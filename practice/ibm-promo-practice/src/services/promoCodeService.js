// Promo code rules for the ticket-booking app.
// Every failed rule throws an Error; the controller turns it into a 400 response.

function validatePromoCode(promoCode, quantity, cartTotal, currentUser, eventId) {
  // One rule is already written, the way the exam hands it to you.
  // Copy its shape for the other seven. Return true if every rule passes.
  if (quantity < promoCode.minTickets) {
    throw new Error(`Minimum of ${promoCode.minTickets} tickets required`);
  }

  // TODO: maximum tickets
  // TODO: expiry date (a code expiring today is still valid)
  // TODO: start date (a code starting today is valid)
  // TODO: maximum redemption limit
  // TODO: minimum order amount
  // TODO: first-time buyers only
  // TODO: allowed events

  return true;
}

function applyDiscount(promoCode, cartTotal) {
  // TODO: Drill 2 on the prep page
  throw new Error("Not implemented");
}

module.exports = { validatePromoCode, applyDiscount };
