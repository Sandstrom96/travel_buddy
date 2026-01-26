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



# ---- 2026-02-02 (RAG) ----

edit 39 "**Vad?**

Hämta källsidan (MOFA VISA) och spara rådata lokalt.

**Hur (kort):**

- Fetch HTML med requests/httpx.

- Spara exakt response i data/raw/mofa_visa.html.

- Lägg med timestamp (i filnamn eller metadata).

**Test:**

- Filen skapas och är inte tom.

**Klart när:**

- data/raw/mofa_visa.html finns och är redo att parsas."

edit 40 "**Vad?**

Extrahera relevant text från HTML och skapa en ren textfil.

**Hur (kort):**

- Parse HTML (t.ex. BeautifulSoup).

- Plocka ut huvudtext (inte menyer/footers).

- Spara som data/processed/mofa_visa.txt.

**Klart när:**

- Textfilen går att läsa och innehåller faktainnehåll."

edit 41 "**Vad?**

Chunk:a texten i lagom bitar med metadata.

**Hur (kort):**

- Dela upp i chunks (t.ex. 300–800 tokens/tecken).

- Lägg metadata: source_url, retrieved_at, destination=Japan, category=entry_requirements.

- Spara JSONL/JSON i data/processed.

**Klart när:**

- Ni har en lista av chunks + metadata som kan embed:as."

edit 42 "**Vad?**

Skapa embeddings lokalt för varje chunk (gratis).

**Hur (kort):**

- Välj embeddingmodell lokalt (t.ex. sentence-transformers).

- Embed varje chunk-text.

- Spara vectors + metadata redo för DB.

**Klart när:**

- Varje chunk har en embedding-vektor med rätt dimension."

edit 43 "**Vad?**

Skapa LanceDB och lägg in chunks (upsert).

**Hur (kort):**

- Skapa/open DB i data/lancedb.

- Skapa tabell med fält: id, text, vector, metadata.

- Upsert alla chunks.

**Klart när:**

- DB finns och innehåller era chunks."

edit 44 "**Vad?**

Implementera retrieval (top-k) mot LanceDB för Japan/entry requirements.

**Hur (kort):**

- Query på embedding av user question.

- Hämta top_k (t.ex. 3–5) relevanta chunks.

- Returnera även citations (URL + ev. chunk-id).

**Klart när:**

- Ni får relevanta chunks tillbaka för 2–3 testfrågor."

edit 45 "**Vad?**

Bygg backend endpoint för RAG-frågor.

**Hur (kort):**

- POST /rag/query med {question, destination?, category?}.

- Kör retrieval + generera answer (LLM eller enklare sammanfattning).

- Returnera: answer + citations.

**Klart när:**

- Endpointen funkar lokalt och returnerar citations."

edit 46 "**Vad?**

Bygg UI för agent_chat som kan fråga RAG och visa källor.

**Hur (kort):**

- Text input + send.

- Anropa /rag/query.

- Rendera answer + lista källor (länkar).

**Klart när:**

- Man kan ställa 2 frågor och få svar med citations i UI."

# ---- 2026-02-03 ----

edit 47 "**Vad?**

Gör RAG robust med felhantering så demo inte kraschar.

**Hur (kort):**

- Om DB saknas: visa tydligt fel och hur man bygger den.

- Om scrape/parse failar: visa tydligt message.

- Sätt timeouts och try/catch.

**Klart när:**

- Appen ger vettiga fel istället för stacktrace i UI."

edit 48 "**Vad?**

Uppdatera docs/architecture.md med RAG-flödet.

**Hur (kort):**

- Beskriv pipeline: scrape → clean → chunk → embed → lancedb → retrieve → answer.

- Lista var data lagras (data/raw, data/processed, data/lancedb).

- Lista nya endpoints.

**Klart när:**

- Arkitekturdoc visar både MVP och RAG."

edit 49 "**Vad?**

Feature freeze så ni inte tar in nya risker sista dagarna.

**Hur (kort):**

- Flytta nice-to-haves till Stretch.

- Bara bugfixar och polish efter detta.

- Prioritera demo och slides.

**Klart när:**

- Alla vet vad som INTE ska göras längre."

# ---- 2026-02-04 (presentation) ----

edit 50 "**Vad?**

Skapa första versionen av presentationen.

**Hur (kort):**

- 5–7 slides: problem, mål, lösning, arkitektur, demo, resultat, nästa steg.

- Lägg in screenshot/diagram.

**Klart när:**

- Slides v1 är ihop och kan presenteras (även om inte perfekta)."

edit 51 "**Vad?**

Skriv demo-manus så presentationen blir smooth.

**Hur (kort):**

- Bestäm ordning: start → search → guide → RAG fråga → citations.

- Vem säger vad (fördela roller).

- Skriv 'plan B' om nät/LLM strular.

**Klart när:**

- Manus finns och alla vet sin del."

edit 52 "**Vad?**

Genomför första riktiga demo-repetitionen med tidtagning.

**Hur (kort):**

- Kör hela flödet som på presentationen.

- Mät tid (10–15 min).

- Skriv ner 3 förbättringar.

**Klart när:**

- Ni klarar hela demon inom tiden."

edit 53 "**Vad?**

Genomför andra repetitionen inklusive plan B.

**Hur (kort):**

- Testa om backend startar om, DB saknas, osv.

- Ha backup: lokalt körning eller screenshots/video.

**Klart när:**

- Ni vet exakt vad ni gör om något går fel live."

edit 54 "**Vad?**

Slipa README och lägg in slutliga screenshots.

**Hur (kort):**

- Uppdatera 'What it does', 'How to run', 'Data sources'.

- Lägg in citations/URLer till källor (MOFA/ambassad).

- Säkerställ att README matchar projektets faktiska status.

**Klart när:**

- README ser klar och seriös ut för inlämning."

# ---- 2026-02-05 ----

edit 55 "**Vad?**

Finalisera slides och exportera.

**Hur (kort):**

- Fixa text, bilder, stavning.

- Exportera PDF + spara backup (t.ex. Drive/USB).

**Klart när:**

- Presentationen är final och säkerhetskopierad."

edit 56 "**Vad?**

Sista demo-repetitionen: kort check.

**Hur (kort):**

- Kör 1 snabb rep.

- Se att alla kan startkommandon.

- Lås demo-frågor (2–3 frågor som alltid funkar).

**Klart när:**

- Teamet är redo och tryggt."

edit 57 "**Vad?**

Bugfix endast (inga nya features).

**Hur (kort):**

- Fixa bara saker som kan krascha demon eller göra appen oanvändbar.

- Undvik stora refactors.

**Klart när:**

- Main är stabil och körbar."

edit 58 "**Vad?**

Skriv individuell reflektion (Person A).

**Hur (kort):**

- 0.5–1 sida: vad du gjorde, vad som gick bra/dåligt, vad du lärt dig.

- Nämn arbetssätt (issues/PR/review) och tekniska val.

**Klart när:**

- Texten är klar för inlämning."

edit 59 "**Vad?**

Skriv individuell reflektion (Person B).

**Hur (kort):**

- Samma struktur: bidrag, lärdomar, förbättringar.

- Koppla till kursmål om ni har.

**Klart när:**

- Texten är klar för inlämning."

edit 60 "**Vad?**

Skriv individuell reflektion (Person C).

**Hur (kort):**

- Samma struktur.

- Fokusera på vad du bidrog med och hur ni jobbade i team.

**Klart när:**

- Texten är klar för inlämning."

# ---- 2026-02-06 ----

edit 61 "**Vad?**

Genomför presentation + live demo.

**Hur (kort):**

- Starta allt i god tid (10–15 min innan).

- Följ manus: problem → lösning → demo → resultat.

- Visa citations i RAG om möjligt.

**Klart när:**

- Presentationen är genomförd och demon visad."

edit 62 "**Vad?**

Visa repo/kanban som bevis på arbetssätt.

**Hur (kort):**

- Visa GitHub Projects board (Backlog/Ready/Doing/Done).

- Visa 1–2 PRs med review och koppling till issues.

**Klart när:**

- Handledaren ser tydligt hur ni planerade och jobbade."
