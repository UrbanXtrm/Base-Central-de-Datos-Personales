"""Configuraciones de la aplicación."""
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Parámetros principales de configuración."""

    database_url: str = Field(
        default="sqlite:///app.db",
        description="Cadena de conexión a la base de datos",
        alias="DATABASE_URL",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


@lru_cache
def get_settings() -> Settings:
    """Devuelve una instancia cacheada de la configuración."""

    return Settings()
