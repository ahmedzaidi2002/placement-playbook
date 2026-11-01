#!/usr/bin/env bash
# Register a new user (arguments.json: register)
source "$(dirname "$0")/_common.sh"
call POST /api/auth/register "$(arg register)"
