// Promo code validation for ShowPass-style ticketing.
// Used by POST /api/promo-codes/validate and by order creation.
// Bug report: deleted, expired, used-up and wrong-event codes are all accepted.

const PromoCode = require("../models/promoCodeModel");
const { NotFoundError, BadRequestError } = require("../utils/errors");

function validatePromoCode(code, eventId, quantity = 1) {
  const promo = PromoCode.findByCode(code);

  if (!promo) {
    throw new NotFoundError("Promo code not found");
  }

  // TODO: deleted codes must behave as not found
  // TODO: not yet active (before validFrom)
  // TODO: expired (after validTo)
  // TODO: usage limit (currentUses has reached maxUses)
  // TODO: event restriction (promo.eventId set and different)
  // TODO: minimum ticket quantity (minTickets)

  return { valid: true, promo };
}

module.exports = { validatePromoCode };
