from functools import lru_cache

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    POSTGRES_DBNAME: str = Field(default="postgres+asyncpg", description="Postgres database name")
    POSTGRES_HOST: str = Field(default="postgres", description="Postgres host")
    POSTGRES_PORT: int = Field(default=5432, description="Postgres port")
    POSTGRES_USER: str = Field(default="postgres", description="Postgres user")
    POSTGRES_PASSWORD: str = Field(..., description="Postgres password")
    POSTGRES_DRIVER: str = Field(default="postgresql", description="Postgres driver")

    POSTGRES_POOL_SIZE: int = Field(default=20, ge=1, le=100, description="Number of connections to maintain in pool")
    POSTGRES_MAX_OVERFLOW: int = Field(default=10, ge=0, description="Maximum overflow connections beyond pool_size")
    POSTGRES_POOL_RECYCLE: int = Field(default=3600, ge=60, description="Recycle connections after N seconds")
    POSTGRES_POOL_PRE_PING: bool = Field(default=True, description="Verify connection before using from pool")

    POSTGRES_ECHO: bool = Field(default=False, description="Log all SQL statements")

    POSTGRES_SSL_MODE: str | None = Field(
        default=None,
        pattern="^(disable|allow|prefer|require|verify-ca|verify-full)$",
        description="PostgreSQL SSL mode",
    )

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
