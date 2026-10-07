from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Lee variables del .env; ignora las que no estén declaradas aquí (POSTGRES_USER, etc.)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(min_length=1, max_length=100)
    ollama_url: str = Field("http://localhost:11434", min_length=1)
    ollama_model: str = Field("llama3.2:3b", min_length=1, max_length=100)

settings = Settings()