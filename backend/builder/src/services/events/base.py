import backoff
from abc import ABC
from pydantic import BaseModel
from loguru import logger
from aio_pika import connect_robust

from src.config.config import BACKOFF_CONFIG, RabbitMQSettings, RABBITMQ_CONFIG


class BaseEventManager(ABC):
    
    def __init__(self, config: BaseModel, **kwargs):
        '''Конструктор'''


class RabbitMQEventManager(BaseEventManager):

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def __init__(
            self,
            config: RabbitMQSettings = RABBITMQ_CONFIG,
            **kwargs
    ):
        self.service_name = config.service_name
        self.connection = connect_robust(
            host=config.HOST,
            port=config.PORT,
            login=config.DEFAULT_USER,
            password=config.DEFAULT_PASS
        )

        self.channel = self.connection.channel()

        self.queue = self.channel.declare_queue(name=config.queue_name, durable=True)
