# Travel Buddy

School project: Travel Buddy is an MVP where you can search destinations and read a simple travel guide (starts with mock/seed).  
Stack: FastAPI (backend) + Streamlit (frontend).

## Repo structure

- `README.md`  
  Overview and how to run the project locally.

- `docs/`  
  SSoT and documentation (e.g. working methods, architecture, backlog plan).

- `data/`  
  Data files and artifacts for ingestion/RAG.
  - `data/raw/` – raw data
  - `data/processed/` – cleaned/parsed data
  - `data/seeds/` – seed/mock data for MVP

- `scripts/`  
  Helper scripts for GitHub automation and dev flows.
  - `scripts/.env.example` – example config for scripts
  - `scripts/github/` – GitHub CLI scripts + docs

## Prerequisites

- Install `uv` (Astral).
- Git

Optional (recommended):
- GitHub CLI `gh` for issues/PR flow.

## Getting started (uv)

### 1) Clone repo
```bash
git clone https://github.com/Sandstrom96/travel_buddy.git
```

### Option A: Start with Docker (Easiest)
If you have Docker installed you can start the entire stack (backend and frontend) with a single command. This is the recommended way to quickly verify that everything works.

```bash
docker compose up --build
```
When the containers have started you can reach the services here:
- **Backend (API):** [http://localhost:8000](http://localhost:8000)
- **Frontend (UI):** [http://localhost:8501](http://localhost:8501)
- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)


### Option B: Start manually locally (without Docker)
If you don't want to use Docker you must install the environment locally on your computer.

### 1) Install dependencies (IMPORTANT!):
Since we split the project into frontend/backend you must run this command instead of a regular "uv sync"
```bash
cd src/travel_buddy
uv run main.py
uv sync --all-extras
```

### 2) Start backend:
```bash
cd src/travel_buddy
uv run uvicorn main:app --reload --port 8000
```

### 3) Test backend:
```bash
curl http://localhost:8000/health
```

### 4) Start frontend (Streamlit):
```bash
uv run streamlit run frontend/app.py
uv run streamlit run frontend/app.py
```
*NOTE: We run app.py and not home.py to include the navigation menu*



## Common dev commands

### Add new library in uv
```bash
uv add 
```

### Update lockfile (if you changed pyproject)
```bash
uv lock
```

### Install/sync again. If something acts up or if you fetch new code from git, run:
```bash
uv sync --all-extras
```

## Troubleshooting

- If `uv run ...` takes time first time: it creates/syncs the environment.
- If `curl /health` fails: check port and that backend is running.
- If Streamlit doesn't reach backend: check BASE_URL/port in frontend.


## GitHub CLI Information
Information about how to use Github CLI is found under [scripts/github/README.md]
