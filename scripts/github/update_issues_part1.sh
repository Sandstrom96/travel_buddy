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

REPO="${REPO:?Missing REPO}"

edit () {

local num="$1"

local body="$2"

gh issue edit "$num" --repo "$REPO" --body "$body"



# ---- 2026-01-23 ----

edit 12 "**Vad?**

Sätt upp GitHub Projects så ni får en enkel Kanban att jobba i.

**Hur (kort):**

- Skapa Project (Board) med kolumner: Backlog, Ready, Doing, Done.

- Skapa labels: type/backend, type/frontend, type/docs, prio/high.

- Bestäm rutin: flytta 3–6 kort till Ready varje dag.

**Klart när:**

- Board finns med kolumnerna ovan.

- Labels finns i repot.

- Minst 5 issues ligger i Projectet."

edit 13 "**Vad?**

Skriv en kort 'så jobbar vi'-guide.

**Hur (kort):**

- Branch per issue.

- PR + minst 1 review innan merge.

- Definition of Done: körbar lokalt, inga errors, README uppdaterad vid behov.

**Klart när:**

- docs/way-of-working.md finns och är överenskommet i teamet."

edit 14 "**Vad?**

Skapa minsta backend och en health check.

**Hur (kort):**

- FastAPI app med router.

- GET /health -> {\"status\":\"ok\"}

**Test:**

- curl http://localhost:/health ska ge 200.

**Klart när:**

- Endpointen fungerar lokalt."

edit 15 "**Vad?**

Skapa minsta Streamlit-app att bygga vidare på.

**Hur (kort):**

- app.py + ev pages/home.py

- Placeholder-sektioner för Search/Guide och API-status.

**Klart när:**

- Streamlit startar och visar sidan utan fel."

edit 16 "**Vad?**

Koppla frontend till backend och visa /health i UI.

**Hur (kort):**

- Skapa api_client (requests) med BASE_URL.

- Anropa GET /health och rendera OK/fel i Streamlit.

**Klart när:**

- UI visar status när backend är igång.

- UI visar vettigt fel om backend är nere."

edit 17 "**Vad?**

Gör README så man snabbt kan köra projektet.

**Hur (kort):**

- Installation + startkommandon (backend + streamlit).

- Ev. .env-example (om behövs).

**Klart när:**

- En ny person kan starta lokalt på några minuter."

# ---- 2026-01-26 ----

edit 18 "**Vad?**

Endpoint för att söka destinations (MVP, mockdata).

**Hur (kort):**

- Skapa seed-lista (t.ex. JSON).

- GET /destinations?q= filtrerar på namn/land.

- Returnera id + name + country.

**Test:**

- GET /destinations?q=jap returnerar Japan.

**Klart när:**

- Frontend kan lista resultat."

edit 19 "**Vad?**

Endpoint som returnerar en reseguide (MVP, mockdata).

**Hur (kort):**

- GET /destinations/{id}/guide.

- Returnera guide med minst: intro, transport, budget, entry/visa (mock).

**Test:**

- GET /destinations//guide returnerar 200 med data.

**Klart när:**

- Frontend kan rendera guide från endpoint."

edit 20 "**Vad?**

Gör tydliga request/response schemas.

**Hur (kort):**

- Pydantic modeller för Destination + Guide (+ GuideSection).

- Använd som response_model i FastAPI.

**Klart när:**

- Swagger visar scheman tydligt.

- Mindre risk för att frontend/back bryts."

edit 21 "**Vad?**

Bygg sökflödet i Streamlit.

**Hur (kort):**

- Input + knapp.

- Anropa /destinations?q= och rendera lista.

- Klick på destination laddar guide.

**Klart när:**

- Sök → klick → kommer till guidevy."

edit 22 "**Vad?**

Rendera guiden snyggt i UI.

**Hur (kort):**

- Visa minst 3 sektioner (rubrik + text).

- Hantera att någon sektion saknas (fallback).

**Klart när:**

- Guide är läsbar och demo-safe."

edit 23 "**Vad?**

Visa teamwork: jobba med PRs och reviews.

**Hur (kort):**

- Alla jobbar i egna branches kopplade till issues.

- Minst 2 PRs får review-kommentarer och mergeas till main.

**Klart när:**

- 2 merged PRs finns med review historik."

# ---- 2026-01-27 ----

edit 24 "**Vad?**

Lägg till loading/error states i UI.

**Hur (kort):**

- Visa spinner/loading vid API-call.

- Visa error-box med message om request failar.

**Klart när:**

- Appen känns stabil även om backend strular."

edit 25 "**Vad?**

Grundläggande felhantering i backend.

**Hur (kort):**

- Returnera 404 om destination saknas.

- Try/catch + logga exceptions.

**Klart när:**

- Fel blir begripliga och ger rätt statuskod."

edit 26 "**Vad?**

Skapa backlog för RAG i små tasks.

**Hur (kort):**

- Skapa issues: scrape → parse/clean → chunk → embeddings → lancedb → query endpoint → UI.

- Prioritera 1 datakälla först (MVP).

**Klart när:**

- 8–12 RAG-issues finns och är prioriterade."
