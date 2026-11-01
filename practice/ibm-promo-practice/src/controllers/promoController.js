// How the app uses the service: the controller owns req/res, the service only throws.
// You never edit this file in the exam; it is here so you can see why `throw` is required.

const { validatePromoCode } = require("../services/promoCodeService");

function applyPromo(req, res) {
  const { promoCode, quantity, cartTotal, eventId } = req.body;
  try {
    validatePromoCode(promoCode, quantity, cartTotal, req.user, eventId);
    return res.status(200).json({ message: "Promo code is valid" });
  } catch (err) {
    return res.status(400).json({ message: err.message });
  }
}

module.exports = { applyPromo };
