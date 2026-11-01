# Shared helpers for the curl scripts. Not run directly.
cd "$(dirname "$0")" || exit 1

# arg <section>: print that section of arguments.json as JSON
arg() {
  node -e "process.stdout.write(JSON.stringify(require('./arguments.json')['$1']))"
}

BASE_URL=$(node -e "process.stdout.write(require('./arguments.json').baseUrl)")
TOKEN=$(cat .token 2>/dev/null)

# call <METHOD> <path> <json-body>: print the HTTP status and the response body
call() {
  echo "$1 $2"
  echo "body: $3"
  curl -s -w "HTTP %{http_code}\n" -X "$1" "$BASE_URL$2" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "$3"
}
