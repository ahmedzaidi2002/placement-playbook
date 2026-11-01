#!/usr/bin/env bash
# Place an order with a promo code (arguments.json: createOrder)
source "$(dirname "$0")/_common.sh"
call POST /api/orders "$(arg createOrder)"
