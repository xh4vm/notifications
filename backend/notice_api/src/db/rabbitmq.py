from abc import ABC, abstractmethod

import aio_pika
from aio_pika import DeliveryMode
from loguru import logger
from src.api.v1.utilitys import test_connection


class AsyncProducer(ABC):

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
        pass

    @abstractmethod
    async def send_event(self, key: str, value, expire: int, **kwargs):
        pass


class RabbitMQProducer(AsyncProducer):

    def __init__(self):
        self.corr_id = None
        self.queue = None
        self.channel = None
        self.connection = None
        self.service_name = None

    @test_connection
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
        logger.info(f'{host=}')
        logger.info(f'{port=}')
        logger.info(f'{login=}')
        logger.info(f'{password=}')
        self.connection = await aio_pika.connect_robust(host=host, port=port, login=login, password=password)

        self.channel = await self.connection.channel()

        self.queue = await self.channel.declare_queue(name=queue_name, durable=True)
        pass

    @test_connection
    async def send_event(self, header: str, payload: str, **kwargs):
        message = aio_pika.Message(
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


async def get_producer() -> RabbitMQProducer:
    """ Get redis object. """

    return producer
