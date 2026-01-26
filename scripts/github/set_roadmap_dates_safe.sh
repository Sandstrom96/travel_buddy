#!/usr/bin/env bash

set -euo pipefail

# ---- Load env (default: scripts/.env relative to this script) ----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ENV_FILE:-$SCRIPT_DIR/../.env}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
else
  echo "Missing env file: $ENV_FILE"
  echo "Create it from: ${SCRIPT_DIR}/../.env.example"
  exit 1
fi

OWNER="${OWNER:?Missing OWNER}"

PROJECT_NUMBER="${PROJECT_NUMBER:?Missing PROJECT_NUMBER}"

PROJECT_ID="${PROJECT_ID:?Missing PROJECT_ID}" # samma som du redan använde

START_FIELD_ID="${START_FIELD_ID:?Missing START_FIELD_ID}"

TARGET_FIELD_ID="${TARGET_FIELD_ID:?Missing TARGET_FIELD_ID}"

edit_date () {

local item_id="$1"

local field_id="$2"

local date="$3"

# 5 försök, med ökande väntetid

for attempt in 1 2 3 4 5; do

if gh project item-edit --id "$item_id" --project-id "$PROJECT_ID" --field-id "$field_id" --date "$date"; then

return 0

fi

echo "Retry $attempt/5 for item=$item_id field=$field_id (sleeping...)"

sleep $((attempt * 2))

done

echo "FAILED item=$item_id field=$field_id"

return 1



gh project item-list "$PROJECT_NUMBER" --owner "$OWNER" --format json --limit 200 --jq '

.items[]

| select(.content.type=="Issue")
| {item_id: .id, title: .content.title}
| select(.title | test("^\\[?[0-9]{4}-[0-9]{2}-[0-9]{2}\\]?"))
| .date = (.title | match("^\\[?(?[0-9]{4}-[0-9]{2}-[0-9]{2})\\]?").captures[0].string)
| "\(.item_id)\t\(.date)"
' | while IFS=$'\t' read -r item_id date; do

echo "Setting dates for item=$item_id date=$date"

edit_date "$item_id" "$START_FIELD_ID" "$date"

sleep 1

edit_date "$item_id" "$TARGET_FIELD_ID" "$date"

sleep 1

done
