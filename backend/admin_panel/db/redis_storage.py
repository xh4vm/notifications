""" Class and functions for work with radis."""

from abc import ABC, abstractmethod
from functools import lru_cache

from notice.utils import test_connection
from redis import Redis


class KeyValueStorage(ABC):
    @abstractmethod
    def get_from(self, key: str, **kwargs):
        pass

    @abstractmethod
    def set_to(self, key: str, value, expire: int, **kwargs):
        pass


class RedisStorage(KeyValueStorage):
    """ Class for redis cash service. """

    def __init__(self):
        """ Init RedisCash"""
        self.storage: Redis | None = None

    @test_connection
    def set_to(self, key, value, expire: int, **kwargs):
        """ Set data to redis cash."""
        self.storage.set(key, value, ex=expire)

    @test_connection
    def get_from(self, key, **kwargs):
        """ Get data from redis cash."""

        return self.storage.get(key)


redis_storage = RedisStorage()


@lru_cache()
def get_redis() -> RedisStorage:
    """ Get redis object. """

    return redis_storage
