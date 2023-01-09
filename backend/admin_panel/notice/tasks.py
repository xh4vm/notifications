from config.celery import app as celery_app
from django.conf import settings
from notice.services.services import (send_create_manual_mailing_event,
                                      send_event_forgotten_bookmarks,
                                      send_event_new_movies_for_period,
                                      send_event_new_review_likes)


@celery_app.task
def generator_event_get_new_review_likes():
    return send_event_new_review_likes()


@celery_app.task
def generator_event_notification_bookmarks():
    return send_event_forgotten_bookmarks()


@celery_app.task
def generator_event_new_movies():
    return send_event_new_movies_for_period(settings.CELERY_DAYS_PERIOD_OF_NEWS)


@celery_app.task
def generator_event_manual_mailing(event_name):
    return send_create_manual_mailing_event(event_name)
