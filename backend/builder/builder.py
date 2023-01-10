from loguru import logger
from celery import Celery

from src.config.config import CELERY_CONFIG
from src.services.events.consumer import RabbitMQConsumer
from src.services.events.producer import RabbitMQProducer
from src.services.builder import JinjaBuilder

celery = Celery(CELERY_CONFIG.NAME, backend=CELERY_CONFIG.BACKEND, broker=CELERY_CONFIG.BROKER)


@celery.task
def builder():
    logger.info('Starting builder process...')

@celery.on_after_configure.connect
def setup_etl_periodic_task(sender, **kwargs):
    sender.add_periodic_task(30.0, builder.s(), name='Running builder process every 30 seconds.')
