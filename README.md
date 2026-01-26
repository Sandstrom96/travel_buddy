# Travel Buddy

Skolprojekt: Travel Buddy är en MVP där man kan söka destinationer och läsa en enkel reseguide (börjar med mock/seed).  
Stack: FastAPI (backend) + Streamlit (frontend).

## Repo-struktur

- `README.md`  
  Översikt och hur man kör projektet lokalt.

- `docs/`  
  SSoT och dokumentation (t.ex. arbetssätt, arkitektur, backlog-plan).

- `data/`  
  Datafiler och artifacts för ingestion/RAG.
  - `data/raw/` – rå data
  - `data/processed/` – rensad/parsad data
  - `data/seeds/` – seed/mock-data för MVP

- `scripts/`  
  Hjälpscripts för GitHub-automation och dev-flöden.
  - `scripts/.env.example` – exempel på config för scripts
  - `scripts/github/` – GitHub CLI scripts + docs

## Förutsättningar

- Installera `uv` (Astral).
- Git

Valfritt (rekommenderas):
- GitHub CLI `gh` för issues/PR-flöde.

## Kom igång (uv)

### 1) Klona repo
```bash
git clone https://github.com/Sandstrom96/travel_buddy.git
cd src/travel_buddy
```

### 2) Installera dependencies
```bash
uv sync
```

### 3) Starta backend (FastAPI)
Alternativ A (om ni kör ett python-entrypoint-script):
```bash
uv run python app/run.py
```

Alternativ B (om ni kör uvicorn direkt):
```bash
uv run uvicorn app.main:app --reload --port 8000
```

Testa backend:
```bash
curl http://localhost:8000/health
```

### 4) Starta frontend (Streamlit)
```bash
uv run streamlit run frontend/app.py
```

## Vanliga dev-kommandon

### Uppdatera lockfile (om ni ändrat pyproject)
```bash
uv lock
```

### Installera/synka igen (om någon får strul)
```bash
uv sync
```

## Troubleshooting

- Om `uv run ...` tar tid första gången: den skapar/synkar miljön.
- Om `curl /health` failar: kontrollera port och att backend kör.
- Om Streamlit inte når backend: kontrollera BASE_URL/port i frontend.


## GitHub CLI Information
Information om hur du använder Github CLI finns under [scripts/github/README.md]
