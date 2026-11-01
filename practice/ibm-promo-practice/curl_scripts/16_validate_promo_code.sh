#!/usr/bin/env bash
# Validate a promo code (arguments.json: validatePromo)
source "$(dirname "$0")/_common.sh"
call POST /api/promo-codes/validate "$(arg validatePromo)"
