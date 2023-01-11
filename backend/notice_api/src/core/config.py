from functools import lru_cache
from logging import config as logging_config

from src.core.logger import LOGGING
from src.core.settings import Settings

logging_config.dictConfig(LOGGING)


@lru_cache()
def get_settings():
    return Settings()


SETTINGS = get_settings()
