from datetime import datetime
from http import HTTPStatus

from db.redis_storage import redis_storage
from django.conf import settings
from loguru import logger
from notice.fake_api_request import (
    _make_request_auth,
    _make_request_content_get_film_name,
    _make_request_content_new_movies_for_period,
    _make_request_feedbacks_forgotten_bookmarks,
    _make_request_feedbacks_likes,
    mock_api_request,
)
from notice.services.models import (
    ErrorResponse,
    FilmName,
    ForgottenUserBookmarks,
    GeneratorResponse,
    MovieEvent,
    MoviesTokens,
    NewMoviesForPeriod,
    NewReviewLikesOut,
    NewReviewsLikes,
    ResponseBoolResult,
)
from notice.utils import create_time_zones_list, get_token_exp, make_request
from redis import Redis

redis_storage.storage = Redis(**settings.KEY_VALUE_DB_SETTINGS)


def send_to_notice_api(name_source, name_event, data):

    access_token = get_access_token(make_request_func=make_request)

    if isinstance(access_token, ErrorResponse):
        return access_token

    message_to_queue = MovieEvent(
        time_zone=create_time_zones_list(min_time=settings.RECIPIENT_MIN_TIME, max_time=settings.RECIPIENT_MAX_TIME),
        name_of_event_source=name_source,
        name_type_event=name_event,
        context=data,
        created=datetime.utcnow(),
    )

    result_request = make_request(
        url=settings.NOTICE_API_ENTRYPOINT,
        method='post',
        params={
            'headers': {settings.AUTH_JWT_HEADER_NAME: 'Bearer {0}'.format(access_token)},
            'data': message_to_queue.json(exclude={'film_id'}),
        },
        model=ResponseBoolResult,
    )

    if result_request.status != HTTPStatus.OK:
        logger.error('Event Error. Status {0}. Body {1}'.format(result_request.status, result_request.body))
        return ErrorResponse(status=result_request.status, body=result_request.body)

    logger.info('Event: {0}'.format(message_to_queue))
    logger.info(
        'Send to API Notice with result Status <{0}>. Body: {1}'.format(result_request.status, result_request.body)
    )

    return GeneratorResponse(event=message_to_queue, api_notice_response=result_request)


def set_tokens_to_storage(body: MoviesTokens) -> bool | ErrorResponse:
    token_exp = get_token_exp(body.access_token)

    if isinstance(token_exp, ErrorResponse):
        return token_exp

    expire = datetime.fromtimestamp(token_exp) - datetime.now()
    redis_storage.set_to(settings.ACCESS_TOKEN_KEY, body.access_token, expire=expire)

    token_exp = get_token_exp(body.refresh_token)

    if isinstance(token_exp, ErrorResponse):
        return token_exp

    expire = datetime.fromtimestamp(token_exp) - datetime.now()
    redis_storage.set_to(settings.REFRESH_TOKEN_KEY, body.refresh_token, expire=expire)


@mock_api_request(_make_request_auth)
def get_access_token(make_request_func):

    if access_token := redis_storage.get_from(settings.ACCESS_TOKEN_KEY):
        return access_token

    if refresh_token := redis_storage.get_from(settings.REFRESH_TOKEN_KEY):

        result_request = make_request_func(
            url=settings.AUTH_API_AUTH_ENTRYPOINT,
            method='put',
            params={'data': {'refresh_token': refresh_token}},
            model=MoviesTokens,
        )

    else:

        result_request = make_request_func(
            url=settings.AUTH_API_LOGIN_ENTRYPOINT,
            method='put',
            params={'data': settings.AUTH_API_LOGIN_PARAMS},
            model=MoviesTokens,
        )

    if isinstance(result_request, ErrorResponse):
        return result_request

    set_tokens_to_storage(result_request.body)

    return result_request.body.access_token


@mock_api_request(_make_request_feedbacks_likes)
def get_new_likes(make_request_func, access_token):
    return make_request_func(
        url=settings.FEEDBACKS_API_NEW_LIKES_ENTRYPOINT,
        method='get',
        params={'headers': {settings.AUTH_JWT_HEADER_NAME: 'Bearer {0}'.format(access_token)}, },
        model=NewReviewsLikes,
    )


@mock_api_request(_make_request_content_get_film_name)
def get_film_name(make_request_func, access_token, film_id):
    result = make_request_func(
        url=settings.CONTENT_API_FILM_NAME,
        method='get',
        params={
            'headers': {settings.AUTH_JWT_HEADER_NAME: 'Bearer {0}'.format(access_token)},
            'data': {'film_id': film_id},
        },
        model=FilmName,
    )

    if isinstance(result, ErrorResponse):
        return result

    return result.body.film_name


@mock_api_request(_make_request_feedbacks_forgotten_bookmarks)
def get_forgotten_bookmarks(make_request_func, access_token):
    return make_request_func(
        url=settings.FEEDBACKS_API_FORGOTTEN_BOOKMARKS_ENTRYPOINT,
        method='get',
        params={'headers': {settings.AUTH_JWT_HEADER_NAME: 'Bearer {0}'.format(access_token)}, },
        model=ForgottenUserBookmarks,
    )


@mock_api_request(_make_request_content_new_movies_for_period)
def get_new_movies_for_period(make_request_func, access_token, days):
    return make_request_func(
        url=settings.CONTENT_API_NEW_MOVIES,
        method='get',
        params={'headers': {settings.AUTH_JWT_HEADER_NAME: 'Bearer {0}'.format(access_token)}, 'data': {'days': days}},
        model=NewMoviesForPeriod,
    )


def send_event_new_review_likes() -> GeneratorResponse | ErrorResponse | list[GeneratorResponse] | list[ErrorResponse]:
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Feedbacks получить новые лайки
    # 3. Отправить событие в API Notice

    access_token = get_access_token(make_request_func=make_request)

    if isinstance(access_token, ErrorResponse):
        return access_token

    result_request = get_new_likes(make_request_func=make_request, access_token=access_token)

    if isinstance(result_request, ErrorResponse):
        return result_request

    send_to_notice_api_results = []

    for new_review_likes in result_request.body.new_reviews_likes:

        film_name = get_film_name(
            make_request_func=make_request, access_token=access_token, film_id=new_review_likes.film_id,
        )

        if isinstance(film_name, ErrorResponse):
            logger.error('Event Error. Status {0}. Body {1}'.format(result_request.status, result_request.body))
            continue

        new_reviews_likes_out = NewReviewLikesOut(
            request_date=result_request.body.request_date,
            user_id=new_review_likes.user_id,
            film_name=film_name,
            likes=new_review_likes.likes,
        )

        send_to_notice_api_results.append(
            send_to_notice_api(
                name_source='Generator get_new_review_likes',
                name_event=settings.EVENT_NEW_REVIEW_LIKES[0],
                data=new_reviews_likes_out,
            )
        )

    return send_to_notice_api_results


def send_event_forgotten_bookmarks():
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Feedbacks получить забытые закладки
    # 3. Отправить событие в API Notice

    access_token = get_access_token(make_request_func=make_request)

    if isinstance(access_token, ErrorResponse):
        return access_token

    result_request = get_forgotten_bookmarks(make_request_func=make_request, access_token=access_token)

    if isinstance(result_request, ErrorResponse):
        return result_request

    send_to_notice_api_results = []

    for user_forgotten_bookmarks in result_request.body:
        send_to_notice_api_results.append(
            send_to_notice_api(
                'Generator get_forgotten_bookmarks', settings.EVENT_FORGOTTEN_BOOKMARKS[0], user_forgotten_bookmarks
            )
        )

    return send_to_notice_api_results


def send_event_new_movies_for_period(days):
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Content получить новые фильмы за посление days дней
    # 3. Отправить событие в API Notice

    access_token = get_access_token(make_request_func=make_request)

    if isinstance(access_token, ErrorResponse):
        return access_token

    result_request = get_new_movies_for_period(make_request_func=make_request, access_token=access_token, days=days,)

    if isinstance(result_request, ErrorResponse):
        return result_request

    return send_to_notice_api(
        'Generator get_new_movies_for_period', settings.EVENT_NEW_MOVIES_FOR_PERIOD[0], result_request.body,
    )


def send_create_manual_mailing_event(event_name):

    return send_to_notice_api('Generator manual mailing event', event_name, None)
