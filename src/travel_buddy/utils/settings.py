from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    TAVILY_API_KEY: str

    BACKEND_URL: str = "http://localhost:8000"

    BASE_DIR = Path(__file__).parents[3]

    RAW_DATA_DIR: Path = Field(
        default_factory=lambda: Path(__file__).parents[3] / "data" / "raw"
    )

    PROCESSED_DATA_DIR: Path = Field(
        default_factory=lambda: Path(__file__).parents[3] / "data" / "processed"
    )
    DB_PATH: Path = Field(
        default_factory=lambda: Path(__file__).parents[3]
        / "src"
        / "travel_buddy"
        / "knowledge_base"
    )

    # 'extra="ignore"' tillåter att .env-filen innehåller variabler som inte används
    # av just denna klass (t.ex. inställningar för frontenden) utan att appen kraschar.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )


settings = Settings()
