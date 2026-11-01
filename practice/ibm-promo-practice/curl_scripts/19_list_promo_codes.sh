#!/usr/bin/env bash
# List every promo code, deleted ones included
source "$(dirname "$0")/_common.sh"
call GET /api/promo-codes ""
