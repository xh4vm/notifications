from abc import ABC, abstractmethod
from functools import lru_cache

from fastapi import Depends
from src.db.rabbitmq import RabbitMQProducer, get_producer
from src.models.events import EventMovies


class BaseProducerService(ABC):
    @abstractmethod
    async def send_event(self, params: dict, **kwargs):
        pass


class RabbitMQProducerService(BaseProducerService):
    """Class RabbitMQProducerService."""

    model: None
    errors = None

    def __init__(self, producer: RabbitMQProducer):
        """ Init object of RabbitMQProducerService class. """

        self.producer = producer
        self.errors = {}

    async def send_event(self, params: EventMovies, **kwargs):
        payload_str = params.json()
        return await self.producer.send_event(header=params.name_of_event_source, payload=payload_str)


@lru_cache()
def get_event_service(producer: RabbitMQProducer = Depends(get_producer),) -> RabbitMQProducerService:
    """ Get RabbitMQProducerService object.

    Arguments:
        producer:

    Returns:
        RabbitMQProducerService: rabbitmq producer service
    """

    return RabbitMQProducerService(producer)
