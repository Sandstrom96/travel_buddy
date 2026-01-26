FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

# Install the project in editable mode inside the uv environment so travel_buddy can be imported
RUN uv pip install -e .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "travel_buddy.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
