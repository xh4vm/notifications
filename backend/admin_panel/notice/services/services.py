from datetime import datetime
from functools import wraps
from uuid import uuid4

import requests
from django.conf import settings
from loguru import logger
from notice.services.models import (ForgottenUserBookmarks, GeneratorResponse,
                                    MovieEvent, NewMoviesForPeriod,
                                    NewReviewLikes, NewReviewsLikes,
                                    ResponseAPINotice)


def uuid_str():
    return str(uuid4())


def make_request(url, method, params):
    """ Make request to API.

    Arguments:
        url: full api url
        method: request method
        params: parameters for query

    Returns:
        list: result
    """

    session = requests.session()

    with session.request(method, url, **params) as response:
        body = response.json() if response.ok else None
        status = response.status_code
    session.close()
    return [status, body]


def send_to_notice_api(name_source, name_event, data):
    result = MovieEvent(
        name_of_event_source=name_source,
        name_type_event=name_event,
        context=data,
    )

    status, body = make_request(
        url=settings.NOTICE_API_ENTRYPOINT,
        method='post',
        params={'data': result.json()}
    )

    return GeneratorResponse(
        event=result,
        api_notice_response=ResponseAPINotice(status=status, body=body)
    )


def get_new_review_likes() -> GeneratorResponse:
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Feedbacks получить новые лайки
    # 3. Отправить событие в API Notice http://localhost:8080/api/v1
    result_feedbacks = NewReviewsLikes(
        request_date=datetime.utcnow(),
        new_reviews_likes=[
            NewReviewLikes(
                user_id=uuid_str(),
                film_id=uuid_str(),
                likes=[uuid_str(), uuid_str(), uuid_str(), uuid_str()]
            ),
            NewReviewLikes(
                user_id=uuid_str(),
                film_id=uuid_str(),
                likes=[uuid_str(), uuid_str(), uuid_str(), uuid_str(), uuid_str()]
            ),
            NewReviewLikes(
                user_id=uuid_str(),
                film_id=uuid_str(),
                likes=[uuid_str(), uuid_str()]
            ),
        ]
    )

    return send_to_notice_api('Generator get_new_review_likes', settings.EVENT_NEW_REVIEW_LIKES[0], result_feedbacks)


def get_forgotten_bookmarks():
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Feedbacks получить забытые закладки
    # 3. Отправить событие в API Notice
    result_feedbacks = [
        ForgottenUserBookmarks(
            user_id=uuid_str(),
            films=[uuid_str(), uuid_str()]
        ),
        ForgottenUserBookmarks(
            user_id=uuid_str(),
            films=[uuid_str(), uuid_str()]
        ),
        ForgottenUserBookmarks(
            user_id=uuid_str(),
            films=[uuid_str(), uuid_str()]
        ),
    ]

    return send_to_notice_api(
        'Generator get_forgotten_bookmarks',
        settings.EVENT_FORGOTTEN_BOOKMARKS[0],
        result_feedbacks
    )


def get_new_movies_for_period(days):
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Content получить новые фильмы за посление days дней
    # 3. Отправить событие в API Notice
    result_content = NewMoviesForPeriod(
        period_days=days,
        films=[uuid_str(), uuid_str(), uuid_str(), uuid_str()]
    )

    return send_to_notice_api(
        'Generator get_new_movies_for_period',
        settings.EVENT_NEW_MOVIES_FOR_PERIOD[0],
        result_content
    )


def create_manual_mailing_event(event_name):

    return send_to_notice_api('Generator manual mailing event', event_name, None)


def task_logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        logger.info('Event: {0}'.format(result.event))
        logger.info('Send to API Notice with result Status <{0}>. Body: {1}'.format(
            result.api_notice_response.status,
            result.api_notice_response.body
        )
        )
        return result
    return wrapper
