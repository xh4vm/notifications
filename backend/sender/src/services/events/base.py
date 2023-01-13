import asyncio
from abc import ABC, abstractmethod
from aio_pika import connect_robust, Channel
from aio_pika.pool import Pool
from aio_pika.abc import AbstractRobustConnection

from src.config.config import RabbitMQSettings, RABBITMQ_CONFIG


class BaseEventManager(ABC):
    @abstractmethod
    async def get_connection(self):
        """Инициализация пулла соединений"""

    @abstractmethod
    async def get_channel(self):
        """Инициализация пулла каналов"""


class RabbitMQEventManager(BaseEventManager):
    def __init__(self, settings: RabbitMQSettings = RABBITMQ_CONFIG, **kwargs):
        self._loop = asyncio.get_event_loop()
        self._settings = settings

    async def get_connection(self) -> AbstractRobustConnection:
        return await connect_robust(
            host=self._settings.HOST,
            port=self._settings.PORT,
            login=self._settings.DEFAULT_USER,
            password=self._settings.DEFAULT_PASS,
        )

    async def get_channel(self) -> Channel:
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    @property
    def connection_pool(self):
        return Pool(self.get_connection, max_size=10, loop=self._loop)

    @property
    def channel_pool(self):
        return Pool(self.get_channel, max_size=2, loop=self._loop)
