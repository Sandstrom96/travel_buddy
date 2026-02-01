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


### Alternativ B: Starta manuellt lokalt (utan Docker)
Om du inte vill använda Docker måste du installera miljön lokalt på din dator.

### 1) Installera dependencies (VIKTIGT!):
Eftersom vi delat upp projektet i fronten/backend måste du köra detta kommando istället för ett vanligt "uv sync"
```bash
uv sync --all-extras
```

### 2) Starta backend:
```bash
uv run uvicorn travel_buddy.api.main:app --reload --port 8000
```

### 3) Testa backend:
```bash
curl http://localhost:8000/health
```

### 4) Starta frontend (Streamlit):
```bash
uv run streamlit run frontend/app.py
```
*OBS: Vi kör app.py och inte home.py flr att få med navigationsmenyn*



## Vanliga dev-kommandon

### Lägga till nytt bibliotek i uv
```bash
uv add 
```

### Uppdatera lockfile (om ni ändrat pyproject)
```bash
uv lock
```

### Installera/synka igen. O något strular eller om du hämtar ny kod från git, kör:
```bash
uv sync --all-extras
```

## Troubleshooting

- Om `uv run ...` tar tid första gången: den skapar/synkar miljön.
- Om `curl /health` failar: kontrollera port och att backend kör.
- Om Streamlit inte når backend: kontrollera BASE_URL/port i frontend.


## GitHub CLI Information
Information om hur du använder Github CLI finns under [scripts/github/README.md]
