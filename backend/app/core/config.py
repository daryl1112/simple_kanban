"""Application configuration.

Per the project's coding standard, all environment-specific settings are kept
out of the code and read from environment variables. `Settings` is the single
source of truth for configuration and is imported wherever config is needed.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings sourced from the environment.

    Attributes:
        app_name: Human-readable service name, surfaced in the OpenAPI docs.
        database_url: SQLAlchemy connection string. Defaults to a local SQLite
            file so the service (and its tests) can run without Postgres; in
            Docker Compose this is overridden to point at the Postgres service.
        log_level: Root log level (e.g. "INFO", "DEBUG").
        cors_origins: Comma-separated list of allowed browser origins.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "DevBoard API"
    database_url: str = "sqlite:///./devboard.db"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        """Return CORS origins as a clean list, split from the env string."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return a cached `Settings` instance.

    Caching keeps configuration cheap to access and ensures every caller sees
    the same values for the lifetime of the process.
    """
    return Settings()
