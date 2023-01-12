import asyncio
import orjson
from loguru import logger
from typing import Any
from sqlalchemy import select

from src.config.config import NOTICE_DB_CONFIG, RABBITMQ_QUEUE_CONFIG
from src.services.events.consumer import RabbitMQConsumer
from src.services.events.producer import RabbitMQProducer
from src.services.builder import Jinja2Renderer
from src.services.template import get_template
from src.db.async_db import AsyncDB
from src.models.template import Template


db = AsyncDB(settings=NOTICE_DB_CONFIG)
consumer: RabbitMQConsumer = RabbitMQConsumer(subscriber_queue=RABBITMQ_QUEUE_CONFIG.BUILDER)
producer: RabbitMQProducer = RabbitMQProducer(publisher_queue=RABBITMQ_QUEUE_CONFIG.SENDER)


async def message_handler(message: dict[str, Any]):
    #TODO get template by event name

    template: Template = await get_template(db=db, name_type_event=message.get('name_type_event'))

    rcpt_to_users = ['xoklhyip@yandex.ru', 'h4vm@yandex.ru']

    jinja2_rd = Jinja2Renderer()
    message = await jinja2_rd.render(template=template.body, data=message.get('context'))

    payload = orjson.dumps({
        'subject': template.subject,
        'rcpt_to_users': rcpt_to_users,
        'message': message,
    })
    await producer.publish(header='', payload=payload)


async def builder():
    logger.info('Starting builder process...')
    
    await consumer.subscribe(callback=message_handler)


if __name__ == '__main__':
    asyncio.run(builder())
