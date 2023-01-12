import backoff
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = '../../.env'


class NoticeDBSettings(BaseSettings):
    SCHEMA_NAME: str = Field('content')
    DRIVER: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    class Config:
        env_prefix = 'NOTICE_DB_'


class RabbitMQSettings(BaseSettings):
    HOST: str
    PORT: int
    DEFAULT_USER: str
    DEFAULT_PASS: str
    DEFAULT_VHOST: str

    class Config:
        env_prefix = 'RABBITMQ_'
        env_file_encoding = 'utf-8'

    
class RabbitMQQueueSettings(BaseSettings):
    BUILDER: str
    SENDER: str

    class Config:
        env_prefix = 'RABBITMQ_QUEUE_'
        env_file_encoding = 'utf-8'


class BuilderSettings(BaseSettings):
    MEDIAFILES: str

    class Config:
        env_prefix = 'BUILDER_'
        env_file_encoding = 'utf-8'


RABBITMQ_CONFIG = RabbitMQSettings()
RABBITMQ_QUEUE_CONFIG = RabbitMQQueueSettings()
NOTICE_DB_CONFIG = NoticeDBSettings()
BUILDER_CONFIG = BuilderSettings()
BACKOFF_CONFIG = {'wait_gen': backoff.expo, 'exception': Exception, 'max_value': 128}
