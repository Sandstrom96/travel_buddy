from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    TAVILY_API_KEY: str

    PROCESSED_DATA_DIR: Path = Field(
        default_factory=lambda: Path(__file__).parents[3] / "data" / "processed"
    )
    DB_PATH: Path = Field(
        default_factory=lambda: Path(__file__).parents[3]
        / "src"
        / "travel_buddy"
        / "knowledge_base"
    )

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
