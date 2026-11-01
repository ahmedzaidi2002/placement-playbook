#!/usr/bin/env bash
# Log in and save the access token to .token (arguments.json: login)
source "$(dirname "$0")/_common.sh"
RESPONSE=$(call POST /api/auth/login "$(arg login)")
echo "$RESPONSE"
echo "$RESPONSE" | node -e "let s=\"\";process.stdin.on(\"data\",d=>s+=d).on(\"end\",()=>{const m=s.match(/\"accessToken\": \"([0-9a-f]+)\"/);if(m){require(\"fs\").writeFileSync(\".token\",m[1]);console.log(\"token saved to curl_scripts/.token\")}})"
