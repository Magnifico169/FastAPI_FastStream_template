from functools import lru_cache

from pydantic import AmqpDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    RABBITMQ_SCHEME: str = Field(default="amqp")
    RABBITMQ_HOST: str = Field(default="localhost")
    RABBITMQ_PORT: int = Field(default=5672)
    RABBITMQ_USER: str = Field(default="guest")
    RABBITMQ_PASSWORD: str = Field(default="guest")
    RABBITMQ_VHOST: str = Field(default="/")

    def get_rabbitmq_uri(self) -> str:
        return str(
            AmqpDsn.build(
                scheme=self.RABBITMQ_SCHEME,
                username=self.RABBITMQ_USER,
                password=self.RABBITMQ_PASSWORD,
                host=self.RABBITMQ_HOST,
                port=self.RABBITMQ_PORT,
                path=self.RABBITMQ_VHOST,
            )
        )


@lru_cache
def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()  # type: ignore[call-arg]
