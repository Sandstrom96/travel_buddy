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



# ---- 2026-01-28 ----

edit 27 "**Vad?**

Dockerisera backend så det alltid går att starta samma sätt på alla datorer.

**Hur (kort):**

- Skapa backend Dockerfile.

- Exponera port, install dependencies, starta uvicorn.

- Se till att env vars går att sätta via docker-compose.

**Test:**

- docker build + docker run och nå /health.

**Klart när:**

- Backend går att starta i container och /health svarar 200."

edit 28 "**Vad?**

Gör det lätt att köra frontend i samma setup (valfritt) eller dokumentera tydligt.

**Hur (kort):**

- Antingen: dockerisera streamlit.

- Eller: skriv i README hur man kör streamlit lokalt mot docker-backend.

**Klart när:**

- Ny person förstår hur man kör hela stacken utan gissningar."

edit 29 "**Vad?**

Lägg till minimala tester så ni vågar refactor och demo säkert.

**Hur (kort):**

- pytest setup (om det inte finns).

- test_health som kollar 200 + body.

- (valfritt) test_guide för en mock-destination.

**Klart när:**

- `pytest` kör grönt lokalt (minst 1 test)."

edit 30 "**Vad?**

Skapa en UI-komponent för guide-sektioner och gör plats för sources.

**Hur (kort):**

- Komponent: title + body.

- Visa en 'Sources'-sektion (kan vara tom/mock nu).

- Återanvänd samma komponent för flera sektioner.

**Klart när:**

- Guiden är mer enhetlig i UI.

- Finns en tydlig plats där citations senare kan visas."

edit 31 "**Vad?**

Uppdatera README med hur man kör (docker/local) efter Docker-jobbet.

**Hur (kort):**

- Lägg 'Option A: Docker' och 'Option B: Local'.

- Skriv exakta kommandon.

**Klart när:**

- README matchar hur projektet faktiskt körs."

# ---- 2026-01-29 ----

edit 32 "**Vad?**

Rensa duplicerad backend-kod så allt är lättare att underhålla.

**Hur (kort):**

- Flytta återkommande logik till services/helpers.

- Standardisera response-format och error handling.

**Klart när:**

- Mindre duplicering och tydligare struktur (utan att bryta API)."

edit 33 "**Vad?**

Rensa duplicerad frontend-kod så API-anrop görs på ett ställe.

**Hur (kort):**

- Samla requests i api_client.

- Återanvänd komponenter för rendering.

**Klart när:**

- Mindre kopierad kod och enklare att ändra endpoints."

edit 34 "**Vad?**

Skapa en tydlig datastruktur i repo för ingestion/RAG.

**Hur (kort):**

- Skapa mappar: data/raw, data/processed, data/seeds (lägg i .gitignore om ni vill).

- Lägg en minimal seed för destinations (om ni använder seed-data).

**Klart när:**

- Repo har ordning på datafiler och teamet vet var de ska ligga."

# ---- 2026-01-30 ----

edit 35 "**Vad?**

MVP freeze: säkerställ att demo-flödet fungerar utan strul.

**Hur (kort):**

- Testa sök → guide flera gånger.

- Fixa showstopper-buggar.

- Se till att UI inte kraschar på tomma svar.

**Klart när:**

- Ni kan demo:a MVP 2 gånger i rad utan incident."

edit 36 "**Vad?**

README ska ha screenshots och tydlig run-guide.

**Hur (kort):**

- Ta 1–3 screenshots (search + guide).

- Lägg in i README.

- Skriv kort 'What it does' + 'How to run'.

**Klart när:**

- README känns proffsig och begriplig för handledare."

edit 37 "**Vad?**

Skriv arkitektur-dokument för MVP så man fattar vad som finns.

**Hur (kort):**

- 1 sida: frontend, backend, dataflöde.

- Lista endpoints och viktiga mappar.

**Klart när:**

- docs/architecture.md förklarar MVP och hur delarna hänger ihop."

edit 38 "**Vad?**

Välj exakt MOFA-källa (URL) och skapa de sista RAG-issues som behövs.

**Hur (kort):**

- Bestäm 1 primär URL (MOFA/ambassad).

- Skriv ner vilka endpoints/komponenter som måste byggas för RAG.

- Flytta RAG-issues till Ready inför 2/2.

**Klart när:**

- Teamet är aligned på datakällan och RAG-planen är redo."
