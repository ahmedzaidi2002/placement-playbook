// Tiny API in the shape of the exam's Express app, built on Node's http module
// so it needs no npm install. Start it with `npm start`, then use curl_scripts/.

const http = require("http");
const crypto = require("crypto");
const PromoCode = require("./src/models/promoCodeModel");
const { validatePromoCode } = require("./src/services/promoCodeService");
const { createOrder } = require("./src/services/orderService");
const { BadRequestError, NotFoundError } = require("./src/utils/errors");

const PORT = process.env.PORT || 3000;
const users = new Map();
const tokens = new Map();

function send(res, status, body) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(body, null, 2) + "\n");
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => (data += chunk));
    req.on("end", () => {
      try {
        resolve(data ? JSON.parse(data) : {});
      } catch {
        reject(new BadRequestError("Body is not valid JSON"));
      }
    });
  });
}

function requireUser(req) {
  const token = (req.headers.authorization || "").replace(/^Bearer /, "");
  const user = tokens.get(token);
  if (!user) {
    const err = new Error("Login first: run ./02_login.sh");
    err.statusCode = 401;
    throw err;
  }
  return user;
}

const routes = {
  "POST /api/auth/register": async (req) => {
    const { name, email, password } = await readBody(req);
    if (!email || !password) throw new BadRequestError("email and password are required");
    users.set(email, { id: users.size + 1, name, email, password });
    return [201, { success: true, data: { id: users.get(email).id, email } }];
  },

  "POST /api/auth/login": async (req) => {
    const { email, password } = await readBody(req);
    const user = users.get(email);
    if (!user || user.password !== password) throw new BadRequestError("Invalid email or password");
    const token = crypto.randomBytes(16).toString("hex");
    tokens.set(token, user);
    return [200, { success: true, data: { accessToken: token } }];
  },

  "POST /api/promo-codes": async (req) => {
    requireUser(req);
    const body = await readBody(req);
    if (!body.code) throw new BadRequestError("code is required");
    return [201, { success: true, data: PromoCode.create(body) }];
  },

  "GET /api/promo-codes": async (req) => {
    requireUser(req);
    return [200, { success: true, data: PromoCode.all() }];
  },

  "DELETE /api/promo-codes": async (req) => {
    requireUser(req);
    const { code } = await readBody(req);
    if (!PromoCode.softDelete(code)) throw new NotFoundError("Promo code not found");
    return [200, { success: true, message: "Promo code deleted" }];
  },

  "POST /api/promo-codes/validate": async (req) => {
    requireUser(req);
    const { code, eventId, quantity } = await readBody(req);
    const { promo } = validatePromoCode(code, eventId, quantity);
    return [200, { success: true, data: { valid: true, code: promo.code, discountPercent: promo.discountPercent } }];
  },

  "POST /api/orders": async (req) => {
    const user = requireUser(req);
    const { eventId, quantity, promoCode } = await readBody(req);
    return [201, { success: true, data: createOrder(user.id, eventId, quantity, promoCode) }];
  },
};

http
  .createServer(async (req, res) => {
    const handler = routes[`${req.method} ${req.url.split("?")[0]}`];
    if (!handler) return send(res, 404, { success: false, message: "Route not found" });
    try {
      const [status, body] = await handler(req);
      send(res, status, body);
    } catch (err) {
      send(res, err.statusCode || 500, { success: false, message: err.message });
    }
  })
  .listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
