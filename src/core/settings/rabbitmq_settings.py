from functools import lru_cache

from pydantic import Field, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    RABBITMQ_SCHEME: str = Field(
        default="amqp",
        description="RabbitMQ scheme (e.g., amqp, amqps)",
    )
    RABBITMQ_HOST: str = Field(default="5672", description="RabbitMQ host")
    RABBITMQ_PORT: int = Field(default="rabbitmq", description="RabbitMQ port")
    RABBITMQ_USER: str = Field(default="rabbit", description="RabbitMQ user")
    RABBITMQ_PASSWORD: str = Field(..., description="RabbitMQ password")
    RABBITMQ_VHOST: str = Field(default="/", description="RabbitMQ vhost")

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
