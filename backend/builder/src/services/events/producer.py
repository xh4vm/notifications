import backoff
from abc import ABC, abstractmethod
from aio_pika import DeliveryMode, Message
from loguru import logger

from src.config.config import BACKOFF_CONFIG
from .base import RabbitMQEventManager


class BaseProducer(ABC):
    
    @abstractmethod
    async def publish(self, key: str, value, expire: int, **kwargs):
        '''Метод отправляет событие в rabbit'''


class RabbitMQProducer(BaseProducer, RabbitMQEventManager):

    def __init__(self, publisher_queue: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.publisher_queue = publisher_queue

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    async def publish(self, header: str, payload: bytes, **kwargs) -> None:
        async with self.channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange('exchange:builder_to_sender', durable=True)

            ready_queue = await channel.declare_queue(self.publisher_queue, durable=True)

            await ready_queue.bind(exchange, self.publisher_queue)

            message = Message(
                headers={'header': header},
                body=payload,
                delivery_mode=DeliveryMode.PERSISTENT,
            )

            await exchange.publish(
                message=message,
                routing_key=self.publisher_queue,
            )

            logger.info(f'Message publish to <{self.publisher_queue}>: body: <{payload.decode()}>')
