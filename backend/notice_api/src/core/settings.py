from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class RabbitMQSettings(BaseSettings):
    host: str
    port: int
    default_user: str
    default_pass: str
    default_vhost: str

    class Config:
        env_prefix = 'RABBITMQ_'
        env_file = Path(ROOT_DIR, '.env')
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    """Class main settings."""

    rabbitmq = RabbitMQSettings().parse_obj(RabbitMQSettings().dict())
    notice_api_host: str
    notice_api_port: int
    notice_api_path: str
    notice_api_version: str
    name: str
    description: str
    version: str
    backoff_max_tries: int = 10

    class Config:
        env_prefix = 'PROJECT_'
        env_file = Path(ROOT_DIR, '.env')
