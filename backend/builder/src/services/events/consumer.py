import asyncio
import orjson
import backoff
from abc import ABC, abstractmethod
from loguru import logger
from typing import Coroutine, Optional, Any

from src.config.config import BACKOFF_CONFIG
from .base import RabbitMQEventManager


class BaseConsumer(ABC):
    @abstractmethod
    async def subscribe(self, **kwargs):
        """Метод отправляет событие в rabbit"""


class RabbitMQConsumer(BaseConsumer, RabbitMQEventManager):
    def __init__(self, subscriber_queue: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.subscriber_queue = subscriber_queue

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    async def subscribe(self, callback: Optional[Coroutine[Any, dict[str, Any], None]] = None, **kwargs) -> None:
        async with self.channel_pool.acquire() as channel:
            await channel.set_qos(prefetch_count=10)

            queue = await channel.declare_queue(self.subscriber_queue, durable=True, auto_delete=False)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    logger.info(
                        f'Message from <{message.routing_key}>: id: <{message.message_id}>, body: <{message.body}>'
                    )

                    if callback is not None:
                        await callback(orjson.loads(message.body))

                    await message.ack()
        await asyncio.Future()
