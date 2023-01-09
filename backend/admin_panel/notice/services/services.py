from datetime import datetime
from functools import wraps
from http import HTTPStatus

from db.redis_storage import redis_storage
from django.conf import settings
from loguru import logger
from notice.fake_api_request import (
    _make_request_auth, _make_request_content_get_film_name,
    _make_request_content_new_movies_for_period,
    _make_request_feedbacks_forgotten_bookmarks, _make_request_feedbacks_likes,
    mock_api_request)
from notice.services.models import ErrorResponse, GeneratorResponse, MovieEvent
from notice.utils import create_time_zones_list, get_token_exp, make_request
from redis import Redis

redis_storage.storage = Redis(**settings.KEY_VALUE_DB_SETTINGS)


def send_to_notice_api(name_source, name_event, data):
    result = MovieEvent(
        time_zone=create_time_zones_list(min_time=settings.RECIPIENT_MIN_TIME, max_time=settings.RECIPIENT_MAX_TIME),
        name_of_event_source=name_source,
        name_type_event=name_event,
        context=data,
        created=datetime.utcnow(),
    )

    result_request = make_request(
        url=settings.NOTICE_API_ENTRYPOINT,
        method='post',
        params={'data': result.json(exclude={'film_id'})}
    )

    if result_request.status != HTTPStatus.OK:
        logger.error('Event Error. Status {0}. Body {1}'.format(result_request.status, result_request.body))
        return ErrorResponse(status=result_request.status, body=result_request.body)

    logger.info('Event: {0}'.format(result))
    logger.info(
        'Send to API Notice with result Status <{0}>. Body: {1}'.format(result_request.status, result_request.body)
    )

    return GeneratorResponse(
        event=result,
        api_notice_response=result_request
    )


def set_tokens_to_storage(body: dict) -> bool | ErrorResponse:
    token_exp = get_token_exp(body['access_token'])

    if isinstance(token_exp, ErrorResponse):
        return token_exp

    expire = datetime.fromtimestamp(token_exp) - datetime.now()
    redis_storage.set_to(settings.ACCESS_TOKEN_KEY, body['access_token'], expire=expire)

    token_exp = get_token_exp(body['refresh_token'])

    if isinstance(token_exp, ErrorResponse):
        return token_exp

    expire = datetime.fromtimestamp(token_exp) - datetime.now()
    redis_storage.set_to(settings.REFRESH_TOKEN_KEY, body['refresh_token'], expire=expire)


@mock_api_request(_make_request_auth)
def get_access_token(make_request_func):

    if access_token := redis_storage.get_from(settings.ACCESS_TOKEN_KEY):
        return access_token

    if refresh_token := redis_storage.get_from(settings.REFRESH_TOKEN_KEY):

        result_request = make_request_func(
            url=settings.AUTH_API_AUTH_ENTRYPOINT,
            method='put',
            params={'data': {'refresh_token': refresh_token}}
        )

    else:

        result_request = make_request_func(
            url=settings.AUTH_API_LOGIN_ENTRYPOINT,
            method='put',
            params={'data': settings.AUTH_API_LOGIN_PARAMS}
        )

    return set_tokens_to_storage(result_request.body)


@mock_api_request(_make_request_feedbacks_likes)
def get_new_likes(make_request_func, access_token):
    return make_request(
        url=settings.FEEDBACKS_API_NEW_LIKES_ENTRYPOINT,
        method='get',
        params={
            'headers': {'Authorization': access_token},
        }
    )


@mock_api_request(_make_request_content_get_film_name)
def get_film_name(make_request_func, access_token, film_id):
    return make_request(
        url=settings.CONTENT_API_FILM_NAME,
        method='get',
        params={
            'headers': {'Authorization': access_token},
            'data': {'film_id': film_id}
        }
    )


@mock_api_request(_make_request_feedbacks_forgotten_bookmarks)
def get_forgotten_bookmarks(make_request_func, access_token):
    return make_request(
        url=settings.FEEDBACKS_API_FORGOTTEN_BOOKMARKS_ENTRYPOINT,
        method='get',
        params={
            'headers': {'Authorization': access_token},
        }
    )


@mock_api_request(_make_request_content_new_movies_for_period)
def get_new_movies_for_period(make_request_func, access_token, days):
    return make_request(
        url=settings.CONTENT_API_NEW_MOVIES,
        method='get',
        params={
            'headers': {'Authorization': access_token},
            'data': {'days': days}
        }
    )


def send_event_new_review_likes() -> GeneratorResponse | ErrorResponse | list[GeneratorResponse] | list[ErrorResponse]:
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Feedbacks получить новые лайки
    # 3. Отправить событие в API Notice

    result_request = get_access_token(make_request_func=make_request)

    auth_token = result_request.body.get('auth_token', None)

    if result_request.status != HTTPStatus.OK or not auth_token:
        return ErrorResponse(status=result_request.status, body=result_request.body)

    result_request = get_new_likes(make_request_func=make_request, access_token=auth_token)

    if result_request.status != HTTPStatus.OK:
        return ErrorResponse(status=result_request.status, body=result_request.body)

    send_to_notice_api_results = []

    for new_review_likes in result_request.body.new_reviews_likes:

        result_request = get_film_name(
            make_request_func=make_request,
            access_token=auth_token,
            film_id=new_review_likes.film_id,
        )

        if result_request.status != HTTPStatus.OK:
            logger.error('Event Error. Status {0}. Body {1}'.format(result_request.status, result_request.body))
            continue

        new_review_likes.film_name = result_request.film_name

        send_to_notice_api_results.append(
            send_to_notice_api(
                name_source='Generator get_new_review_likes',
                name_event=settings.EVENT_NEW_REVIEW_LIKES[0],
                data=new_review_likes
            )
        )

    return send_to_notice_api_results


def send_event_forgotten_bookmarks():
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Feedbacks получить забытые закладки
    # 3. Отправить событие в API Notice

    result_request = get_access_token(make_request_func=make_request)

    if result_request.status != HTTPStatus.OK or not result_request.body.get('auth_token', None):
        return ErrorResponse(status=result_request.status, body=result_request.body)

    result_request = get_forgotten_bookmarks(
        make_request_func=make_request,
        access_token=result_request.body.get('auth_token')
    )

    if result_request.status != HTTPStatus.OK:
        return ErrorResponse(status=result_request.status, body=result_request.body)

    return send_to_notice_api(
        'Generator get_forgotten_bookmarks',
        settings.EVENT_FORGOTTEN_BOOKMARKS[0],
        result_request.body
    )


def send_event_new_movies_for_period(days):
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Content получить новые фильмы за посление days дней
    # 3. Отправить событие в API Notice

    result_request = get_access_token(make_request_func=make_request)

    if result_request.status != HTTPStatus.OK or not result_request.body.get('auth_token', None):
        return ErrorResponse(status=result_request.status, body=result_request.body)

    result_request = get_new_movies_for_period(
        make_request_func=make_request,
        access_token=result_request.body.get('auth_token'),
        days=days,
    )

    if result_request.status != HTTPStatus.OK:
        return ErrorResponse(status=result_request.status, body=result_request.body)

    return send_to_notice_api(
        'Generator get_new_movies_for_period',
        settings.EVENT_NEW_MOVIES_FOR_PERIOD[0],
        result_request.body,
    )


def send_create_manual_mailing_event(event_name):

    return send_to_notice_api('Generator manual mailing event', event_name, None)


def task_logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        if isinstance(result, ErrorResponse):
            logger.error('Event Error. Status {0}. Body {1}'.format(result.status, result.body))
        else:
            logger.info('Event: {0}'.format(result.event))
            logger.info('Send to API Notice with result Status <{0}>. Body: {1}'.format(
                result.api_notice_response.status,
                result.api_notice_response.body
            )
            )
        return result
    return wrapper
