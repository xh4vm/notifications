from config.celery import app as celery_app
from django.conf import settings
from notice.services.services import (create_manual_mailing_event,
                                      get_forgotten_bookmarks,
                                      get_new_movies_for_period,
                                      get_new_review_likes, task_logger)


@celery_app.task
@task_logger
def generator_event_get_new_review_likes():
    return get_new_review_likes()


@celery_app.task
@task_logger
def generator_event_notification_bookmarks():
    return get_forgotten_bookmarks()


@celery_app.task
@task_logger
def generator_event_new_movies():
    return get_new_movies_for_period(settings.CELERY_DAYS_PERIOD_OF_NEWS)


@celery_app.task
@task_logger
def generator_event_manual_mailing(event_name):
    return create_manual_mailing_event(event_name)
