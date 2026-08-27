import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Enterprise Text-to-SQL Assistant"
    env: str = Field(default="development", description="environment mode")

    POSTGRES_HOST: str = Field(default="localhost", description="enviroment mode")
    POSTGRES_PORT: int = Field(default=5432, alias="POSTGRES_PORT")
    POSTRES_DB: str = Field(default="analytics_db", alias="POSTGRES_DB")
    POSTGRES_USER: str = Field(default="readonly_user", alias="POSTGRES_USER")
    POSTRES_PASSWORD: str = Field(..., alias="POSTRES_PASSWORD")

    DB_QUERY_TIMEOUT_SECOND: int = 5
    DB_MAX_ROW_LIMIT: int = 500

    GROQ_API_KEY: str = "localhost"
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    @property
    def asysc_database_url(self) -> str:
        return (
            f"postgresql+asynspg://{self.POSTGRES_USER}:{self.POSTGRES_DB}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_HOST}/"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()