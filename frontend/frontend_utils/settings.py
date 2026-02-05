from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    BACKEND_URL: str = Field(default="http://localhost:8000")


settings = Settings()
