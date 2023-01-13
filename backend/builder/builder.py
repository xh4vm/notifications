import asyncio
import orjson
from loguru import logger
from typing import Any

from src.config.config import NOTICE_DB_CONFIG, RABBITMQ_QUEUE_CONFIG
from src.services.events.consumer import RabbitMQConsumer
from src.services.events.producer import RabbitMQProducer
from src.services.builder import Jinja2Renderer
from src.services.template import get_template
from src.services.enrich.handler import get_context, get_recipients
from src.db.async_db import AsyncDB
from src.models.template import Template


db = AsyncDB(settings=NOTICE_DB_CONFIG)
jinja2_rd = Jinja2Renderer()
consumer: RabbitMQConsumer = RabbitMQConsumer(subscriber_queue=RABBITMQ_QUEUE_CONFIG.BUILDER)
producer: RabbitMQProducer = RabbitMQProducer(publisher_queue=RABBITMQ_QUEUE_CONFIG.SENDER)


async def message_handler(message: dict[str, Any]):
    template: Template = await get_template(db=db, name_type_event=message.get('name_type_event'))

    context = await get_context(event_name=message.get('name_type_event'), data=message.get('context'))
    recipients = await get_recipients(event_name=message.get('name_type_event'), data=message.get('context'))

    message = await jinja2_rd.render(template=template.body, data=context)

    payload = orjson.dumps({'subject': template.subject, 'recipients': recipients, 'message': message, })
    await producer.publish(header='', payload=payload)


async def builder():
    logger.info('Starting builder process...')

    await consumer.subscribe(callback=message_handler)


if __name__ == '__main__':
    asyncio.run(builder())
