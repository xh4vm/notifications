import re
from functools import wraps

import backoff
import jwt
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
        list: result
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
