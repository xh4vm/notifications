import asyncio
import orjson
from loguru import logger
from typing import Any

from src.config.config import RABBITMQ_CONFIG, RABBITMQ_QUEUE_CONFIG
from src.services.events.consumer import RabbitMQConsumer
from src.services.events.producer import RabbitMQProducer
from src.services.builder import Jinja2Renderer


consumer: RabbitMQConsumer = RabbitMQConsumer(subscriber_queue=RABBITMQ_QUEUE_CONFIG.BUILDER)
producer: RabbitMQProducer = RabbitMQProducer(publisher_queue=RABBITMQ_QUEUE_CONFIG.SENDER)



async def message_handler(message: dict[str, Any]):
    #TODO get template by event_id
    template = 'Hi! {{ user_id }}'
    jinja2_rd = Jinja2Renderer()
    message = await jinja2_rd.render(template=template, data=message.get('context'))

    await producer.publish(header='', payload=orjson.dumps(message))


async def builder():
    logger.info('Starting builder process...')
    
    await consumer.subscribe(callback=message_handler)


if __name__ == '__main__':
    asyncio.run(builder())
