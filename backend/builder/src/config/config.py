import backoff
from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = '../../.env'


class RabbitMQSettings(BaseSettings):
    HOST: str
    PORT: int
    DEFAULT_USER: str
    DEFAULT_PASS: str
    DEFAULT_VHOST: str
    QUERY_NAME: str

    class Config:
        env_prefix = 'RABBITMQ_'
        env_file_encoding = "utf-8"


RABBITMQ_CONFIG = RabbitMQSettings()


BACKOFF_CONFIG = {'wait_gen': backoff.expo, 'exception': Exception, 'max_value': 128}


class CelerySettings(Settings):
    name = 'Builder'
    broker = (
        f'pyamqp://{RABBITMQ_CONFIG.DEFAULT_USER}:{RABBITMQ_CONFIG.DEFAULT_PASS}'
        f'@{RABBITMQ_CONFIG.HOST}:{RABBITMQ_CONFIG.PORT}{RABBITMQ_CONFIG.DEFAULT_VHOST}'
    )
    backend = f'pyamqp://{RABBITMQ_CONFIG.HOST}:{RABBITMQ_CONFIG.PORT}/0'


CELERY_CONFIG = CelerySettings()
