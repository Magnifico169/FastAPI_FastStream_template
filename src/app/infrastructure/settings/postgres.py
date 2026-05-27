from functools import lru_cache

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DBNAME: str = Field(default="postgres")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DRIVER: str = Field(default="postgresql+asyncpg")
    POSTGRES_POOL_SIZE: int = Field(default=5)
    POSTGRES_MAX_OVERFLOW: int = Field(default=10)
    POSTGRES_POOL_PRE_PING: bool = Field(default=True)
    POSTGRES_POOL_RECYCLE: int = Field(default=3600)

    def get_database_url(self) -> str:
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

    def get_sync_database_url(self) -> str:
        sync_driver = self.POSTGRES_DRIVER.replace("+asyncpg", "")
        return str(
            PostgresDsn.build(
                scheme=sync_driver,
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
