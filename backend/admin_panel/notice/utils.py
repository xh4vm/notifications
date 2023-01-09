import re
from datetime import datetime, time
from functools import wraps

import backoff
import jwt
import pytz
import requests
from django.conf import settings
from loguru import logger
from notice.services.errors import TokenError
from notice.services.models import ErrorResponse, ResultResponse
from redis.exceptions import ConnectionError


def make_request(url, method, params):
    """ Make request to API.

    Arguments:
        url: full api url
        method: request method
        params: parameters for query

    Returns:
        ResultResponse: result
    """

    session = requests.session()

    with session.request(method, url, **params) as response:
        body = response.json() if response.ok else None
        status = response.status_code
    session.close()
    return ResultResponse(status=status, body=body)


def validate_doctype(value: str):
    return value.strip() in settings.EVENT_TEMPLATE_DOCTYPE


def validate_template(value: str):
    result = re.search(settings.EVENT_TEMPLATE_PATTERN, value, re.S)
    return bool(result)


def get_template_params(value: str) -> list:
    result = re.findall(settings.EVENT_TEMPLATE_PARAMS_PATTERN, value)
    return result


def fatal_error(err):
    logger.error('Error: GATEWAY_TIMEOUT. The external service for API Service ({0}) is not available now'.format(
        type(err['args'][0]).__name__)
    )


def test_connection(func):
    @backoff.on_exception(
        backoff.expo,
        (ConnectionError, ),
        max_tries=settings.BACKOFF_MAX_TRIES,
        on_giveup=fatal_error,
    )
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def get_token_exp(token) -> float | ErrorResponse:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.AUTH_JWT_SECRET_KEY,
            algorithms=settings.AUTH_JWT_DECODE_ALGORITHMS
        )

    except jwt.exceptions.InvalidSignatureError:
        logger.info(TokenError.INVALIDED_SIGNATURE_ERROR)
        return ErrorResponse(status=False, body=TokenError.INVALIDED_SIGNATURE_ERROR)

    except jwt.exceptions.ExpiredSignatureError:
        logger.info(TokenError.EXPIRED_SIGNATURE_ERROR)
        return ErrorResponse(status=False, body=TokenError.EXPIRED_SIGNATURE_ERROR)

    except jwt.exceptions.DecodeError:
        logger.info(TokenError.DECODE_ERROR)
        return ErrorResponse(status=False, body=TokenError.DECODE_ERROR)

    return payload.get('exp')


def create_time_zones_list(min_time: int = 0, max_time: int = 23) -> list[str]:
    result = []
    all_time_zones = pytz.all_timezones
    min_time = time(min_time, 0, 0)
    max_time = time(max_time, 59, 59)

    for time_zone_name in all_time_zones:
        time_zone_time = datetime.now(pytz.timezone(time_zone_name)).time()

        if min_time < max_time and (min_time <= time_zone_time <= max_time):
            result.append(time_zone_name)

        if min_time > max_time and (
                min_time <= time_zone_time <= time(23, 59, 59) or time(0, 0, 0) <= time_zone_time <= max_time
        ):
            result.append(time_zone_name)

    return result
