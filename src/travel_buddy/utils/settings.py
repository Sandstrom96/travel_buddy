from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
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


    model_config = SettingsConfigDict(env_file=str(PROJECT_ROOT / ".env"))
    GEMINI_MODEL_NAME: str = Field(default="gemini-1.5-flash", validation_alias="GEMINI_MODEL_NAME")
settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
