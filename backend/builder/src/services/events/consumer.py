import backoff
from abc import ABC, abstractmethod
from aio_pika.abc import AbstractIncomingMessage
from loguru import logger
from typing import Callable, Optional

from src.config.config import BACKOFF_CONFIG
from .base import RabbitMQEvent


class BaseConsumer(ABC):

    @abstractmethod
    async def read_event(self, **kwargs):
        '''Метод отправляет событие в rabbit'''


class RabbitMQConsumer(BaseConsumer, RabbitMQEvent):

    async def _on_message(
        self,
        message: AbstractIncomingMessage,
        callback: Optional[Callable[[AbstractIncomingMessage], None]] = None
    ) -> None:
        async with message.process():
            logger(f" [x] Received message {message!r}")
            logger(f"     Message body is: {message.body!r}")

            if callback is not None:
                callback(message)

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    async def read_event(self, **kwargs):
        await self.queue.consume(self._on_message)
        return True
