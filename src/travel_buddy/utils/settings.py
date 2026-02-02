from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    firecrawl_api_key: str
    google_api_key: str
    lancedb_path: str = "data/lancedb"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 50

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()