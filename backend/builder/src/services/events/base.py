import backoff
from abc import ABC, abstractmethod
from loguru import logger
from aio_pika import connect_robust

from src.config.config import BACKOFF_CONFIG


class BaseEvent(ABC):
    def __init__(self):
        self.corr_id = None
        self.queue = None
        self.channel = None
        self.connection = None
        self.service_name = None

    @abstractmethod
    async def init_producer(
            self,
            host: str,
            port: int,
            login: str,
            password: str,
            service_name: str,
            queue_name: str,
            **kwargs
    ):
        '''Метод инициализации параметров продюсера'''


class RabbitMQEvent:

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    async def init_producer(
            self,
            host: str,
            port: int,
            login: str,
            password: str,
            service_name: str,
            queue_name: str,
            **kwargs
    ):
        self.service_name = service_name
        self.connection = await connect_robust(host=host, port=port, login=login, password=password)

        self.channel = await self.connection.channel()

        self.queue = await self.channel.declare_queue(name=queue_name, durable=True)
