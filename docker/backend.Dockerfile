FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT="/venv"

ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project --extra backend

COPY . .

# Install the project in editable mode inside the uv environment so travel_buddy can be imported
RUN uv pip install -e .[backend]

EXPOSE 8000

CMD ["uvicorn", "travel_buddy.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
