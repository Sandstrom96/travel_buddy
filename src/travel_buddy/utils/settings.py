from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
class Settings(BaseSettings):
    firecrawl_api_key: str
    google_api_key: str
    lancedb_path: str = "data/lancedb"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 50

    model_config = SettingsConfigDict(env_file=str(PROJECT_ROOT / ".env"))
    GEMINI_MODEL_NAME: str = Field(default="gemini-1.5-flash", validation_alias="GEMINI_MODEL_NAME")

settings = Settings()