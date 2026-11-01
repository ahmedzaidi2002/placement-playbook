#!/usr/bin/env bash
# Soft-delete a promo code (arguments.json: deletePromo)
source "$(dirname "$0")/_common.sh"
call DELETE /api/promo-codes "$(arg deletePromo)"
