from loguru import logger

from celery import Celery
from config import CELERY_CONFIG

celery = Celery(CELERY_CONFIG.name, backend=CELERY_CONFIG.backend, broker=CELERY_CONFIG.broker)


@celery.task
def builder():
    logger.info('Starting builder process...')

@celery.on_after_configure.connect
def setup_etl_periodic_task(sender, **kwargs):
    sender.add_periodic_task(30.0, builder.s(), name='Running builder process every 30 seconds.')
