import asyncio
from typing import Any

import orjson
from loguru import logger
from src.config.config import RABBITMQ_QUEUE_CONFIG
from src.services.builder import Jinja2Renderer
from src.services.events.consumer import RabbitMQConsumer
from src.services.events.producer import RabbitMQProducer

consumer: RabbitMQConsumer = RabbitMQConsumer(subscriber_queue=RABBITMQ_QUEUE_CONFIG.BUILDER)
producer: RabbitMQProducer = RabbitMQProducer(publisher_queue=RABBITMQ_QUEUE_CONFIG.SENDER)


async def message_handler(message: dict[str, Any]):
    # TODO get template by event_id
    template = 'Hi! {{ user_id }}'
    subject = 'Something subject'
    rcpt_to_users = ['xoklhyip@yandex.ru', 'h4vm@yandex.ru', 'my_yan_prax@bk.ru']

    jinja2_rd = Jinja2Renderer()
    message = await jinja2_rd.render(template=template, data=message.get('context'))

    payload = orjson.dumps({
        'subject': subject,
        'rcpt_to_users': rcpt_to_users,
        'message': message,
    })
    await producer.publish(header='', payload=payload)


async def builder():
    logger.info('Starting builder process...')

    await consumer.subscribe(callback=message_handler)


if __name__ == '__main__':
    asyncio.run(builder())
