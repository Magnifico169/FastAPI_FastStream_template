from functools import lru_cache

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    POSTGRES_DBNAME: str = Field(default="postgres", description="Postgres database name")
    POSTGRES_HOST: str = Field(default="postgres", description="Postgres host")
    POSTGRES_PORT: int = Field(default=5432, description="Postgres port")
    POSTGRES_USER: str = Field(default="postgres", description="Postgres user")
    POSTGRES_PASSWORD: str = Field(..., description="Postgres password")
    POSTGRES_DRIVER: str = Field(default="postgresql", description="Postgres driver")

    def get_postgres_uri(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=self.POSTGRES_DRIVER,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DBNAME,
            )
        )


@lru_cache
def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()  # type: ignore[call-arg]
