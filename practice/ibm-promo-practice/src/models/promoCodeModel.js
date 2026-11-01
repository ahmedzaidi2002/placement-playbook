// In-memory stand-in for the PromoCode table.
// Deleting is a soft delete: the row stays and gets a deletedAt timestamp,
// so findByCode still returns deleted rows. That is part of the bug to fix.

const DAY_MS = 24 * 60 * 60 * 1000;
const daysFromNow = (n) => new Date(Date.now() + n * DAY_MS).toISOString();

let rows = [];
let nextId = 1;

function create(data) {
  const row = {
    id: nextId++,
    code: data.code,
    discountPercent: data.discountPercent ?? 10,
    eventId: data.eventId ?? null,
    minTickets: data.minTickets ?? null,
    maxUses: data.maxUses ?? null,
    currentUses: data.currentUses ?? 0,
    validFrom: data.validFrom ?? null,
    validTo: data.validTo ?? null,
    deletedAt: data.deletedAt ?? null,
  };
  rows.push(row);
  return row;
}

function findByCode(code) {
  const wanted = String(code).trim().toUpperCase();
  return rows.find((r) => r.code.toUpperCase() === wanted) || null;
}

function softDelete(code) {
  const row = findByCode(code);
  if (row) row.deletedAt = new Date().toISOString();
  return row;
}

function incrementUses(id) {
  const row = rows.find((r) => r.id === id);
  row.currentUses += 1;
  return row;
}

function reset() {
  rows = [];
  nextId = 1;
  create({ code: "SAVE10", maxUses: 100 });
  create({ code: "EXPIRED5", validTo: daysFromNow(-1) });
  create({ code: "FUTURE20", validFrom: daysFromNow(1) });
  create({ code: "USEDUP", maxUses: 5, currentUses: 5 });
  create({ code: "CONCERT50", eventId: 2 });
  create({ code: "GROUP4", minTickets: 4 });
  create({ code: "OLDCODE", deletedAt: daysFromNow(-3) });
}

reset();

module.exports = { create, findByCode, softDelete, incrementUses, reset, all: () => rows };
