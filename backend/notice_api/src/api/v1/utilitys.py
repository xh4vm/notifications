from functools import wraps
from http import HTTPStatus

import backoff
from aio_pika.exceptions import CONNECTION_EXCEPTIONS
from fastapi import HTTPException
from pydantic import ValidationError
from src.core.config import SETTINGS
from src.models.events import EventMovies


async def check_result(result, errors: dict):
    if errors:
        raise HTTPException(status_code=errors['status'], detail=errors['message'])


async def get_context(params: dict, model) -> EventMovies:
    try:
        return model(**params)
    except ValidationError as err:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Event context is not valid. Error: {0}'.format(err.args[0][0]),
        )


def fatal_error(err):
    raise HTTPException(
        status_code=HTTPStatus.GATEWAY_TIMEOUT,
        detail='The external service for API Service ({0}) is not available now'.format(type(err['args'][0]).__name__),
    )


def test_connection(func):
    @backoff.on_exception(
        backoff.expo, CONNECTION_EXCEPTIONS, max_tries=SETTINGS.backoff_max_tries, on_giveup=fatal_error,
    )
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper
