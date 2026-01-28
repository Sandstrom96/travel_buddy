# Travel Buddy

Skolprojekt: Travel Buddy är en MVP där man kan söka destinationer och läsa en enkel reseguide (börjar med mock/seed).  
Stack: FastAPI (backend) + Streamlit (frontend).

## Repo-struktur

- `backend/`
  FastAPI-server, agenter, endpoints och databaslogik.

- `frontend/`
  Stramlit gränssnitt och API-klient.

- `docs/`  
  SSoT och dokumentation (t.ex. arbetssätt).

- `data/`  
  Datafiler och artifacts för ingestion/RAG.
  - `data/raw/` – rå data
  - `data/processed/` – rensad/parsad data
  - `data/seeds/` – seed/mock-data för MVP

- `scripts/`  
  Hjälpscripts för GitHub-automation och dev-flöden.
  - `scripts/.env.example` – exempel på config för scripts
  - `scripts/github/` – GitHub CLI scripts + docs

- `pyproject.toml`
  Central konfig och beroenden för hela projektett.



## Förutsättningar

- Installera `uv` (Astral).
- Git

Valfritt (rekommenderas):
- GitHub CLI `gh` för issues/PR-flöde.

## Kom igång (uv)

### 1) Klona repo
```bash
git clone https://github.com/Sandstrom96/travel_buddy.git
```

### Alternativ A: Starta med Docker (Enklast)
Om du har Docker installerat kan du starta hela stacken (backend och frontend) med ett enda kommando. Detta är det rekommenderade sättet för att snabbt verifiera att allt fungerar.

```bash
docker compose up --build
```
När containrarna har startat når du tjänsterna här:
- **Backend (API):** [http://localhost:8000](http://localhost:8000)
- **Frontend (UI):** [http://localhost:8501](http://localhost:8501)
- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)


### Alternativ B: Starta manuellt med `uv` (För utveckling)
Använd detta om du vill utveckla koden och se dina ändringar direkt utan att bygga om containrar.
```bash
uv sync
```


### 2) Starta backend (FastAPI)
Alternativ A (om ni kör ett python-entrypoint-script):
```bash
uv run python backend/main.py
```

Alternativ B (om ni kör uvicorn direkt):
```bash
uv run uvicorn travel_backend.main:app --reload --port 8000
```

Testa backend:
```bash
curl http://localhost:8000/health
```

### 3) Starta frontend (Streamlit)
```bash
uv run streamlit run frontend/app.py
```

## Vanliga dev-kommandon

### Lägg till nya bibliotek/paket
```bash
uv add [paketnamn]
```

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
