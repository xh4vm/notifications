import asyncio
from loguru import logger
from typing import Any

from src.config.config import RABBITMQ_QUEUE_CONFIG, SMTP_CONFIG, SMTP_USER_CONFIG
from src.services.events.consumer import RabbitMQConsumer
from src.services.events.producer import RabbitMQProducer
from src.services.sender import SmtpSender


smtp_user, smtp_password = SMTP_USER_CONFIG.NO_REPLY.split(':')

consumer: RabbitMQConsumer = RabbitMQConsumer(subscriber_queue=RABBITMQ_QUEUE_CONFIG.SENDER)
# producer: RabbitMQProducer = RabbitMQProducer(publisher_queue=RABBITMQ_QUEUE_CONFIG.SENDER)

smtp_client = SmtpSender(
    hostname=SMTP_CONFIG.HOST,
    port=SMTP_CONFIG.PORT,
    username=smtp_user,
    password=smtp_password,
    domain=SMTP_CONFIG.DOMAIN
)


async def message_handler(message: dict[str, Any]):
    subject = message.get('subject')
    recipients = message.get('recipients')
    data = message.get('message')

    await smtp_client.send(recipients=recipients, subject=subject, data=data)


async def sender():
    logger.info('Starting sender process...')
    
    await consumer.subscribe(callback=message_handler)


if __name__ == '__main__':
    asyncio.run(sender())
