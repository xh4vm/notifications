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
    QUEUE_NAME: str

    class Config:
        env_prefix = 'RABBITMQ_'
        env_file_encoding = 'utf-8'

    
class RedisSettings(Settings):
    HOST: str
    PORT: int

    class Config:
        env_prefix = 'REDIS_'
        env_file_encoding = 'utf-8'


RABBITMQ_CONFIG = RabbitMQSettings()
REDIS_CONFIG = RedisSettings()
BACKOFF_CONFIG = {'wait_gen': backoff.expo, 'exception': Exception, 'max_value': 128}


class CelerySettings(Settings):
    NAME = 'Builder'
    BROKER = f'redis://{REDIS_CONFIG.HOST}:{REDIS_CONFIG.PORT}/0'
    BACKEND = f'redis://{REDIS_CONFIG.HOST}:{REDIS_CONFIG.PORT}/0'


CELERY_CONFIG = CelerySettings()
