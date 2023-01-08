import backoff
from abc import ABC, abstractmethod
from aio_pika import DeliveryMode, Message
from loguru import logger

from src.config.config import BACKOFF_CONFIG
from .base import RabbitMQEvent


class BaseProducer(ABC):

    @abstractmethod
    async def send_event(self, key: str, value, expire: int, **kwargs):
        '''Метод отправляет событие в rabbit'''


class RabbitMQProducer(BaseProducer, RabbitMQEvent):

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    async def send_event(self, header: str, payload: str, **kwargs):
        message = Message(
            headers={'header': header},
            body=payload.encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await self.channel.default_exchange.publish(
                message=message,
                routing_key=self.queue.name,
            )
        logger.info('<{0}>.<{1}> Message: <{2}>.<{3}>'.format(self.service_name, self.queue.name, header, payload))
        return True


producer = RabbitMQProducer()


async def get_producer() -> BaseProducer:
    return producer
