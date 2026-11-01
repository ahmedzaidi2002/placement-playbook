#!/usr/bin/env bash
# Create a promo code (arguments.json: createPromo)
source "$(dirname "$0")/_common.sh"
call POST /api/promo-codes "$(arg createPromo)"
