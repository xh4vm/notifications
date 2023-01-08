import time

from config.celery import app as celery_app
from django.conf import settings
from notice.services.services import (get_forgotten_bookmarks,
                                      get_new_movies_for_period,
                                      get_new_review_likes)


@celery_app.task
def generator_event_get_new_review_likes():
    get_new_review_likes()
    time.sleep(60)


@celery_app.task
def generator_event_notification_bookmarks():
    get_forgotten_bookmarks()


@celery_app.task
def generator_event_new_movies():
    get_new_movies_for_period(settings.CELERY_DAYS_PERIOD_OF_NEWS)
