FROM python:3.11-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync

# Copy application
COPY frontend/ frontend/

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["uv", "run", "streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
