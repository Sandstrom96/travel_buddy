FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

# Install the project in editable mode inside the uv environment so travel_buddy can be imported
RUN uv pip install -e .

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "frontend/pages/home.py", "--server.port=8501", "--server.address=0.0.0.0"]

