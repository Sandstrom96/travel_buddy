FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --extra backend --no-install-project

COPY pyproject.toml uv.lock ./
COPY frontend/ ./frontend/

RUN mkdir -p src/travel_buddy && touch src/travel_buddy/__init__.py

RUN uv sync --frozen --no-dev --extra frontend

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

