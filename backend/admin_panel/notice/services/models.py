from datetime import datetime

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """ Get from json."""

    return orjson.dumps(v, default=default).decode()


class BaseMixin(BaseModel):
    """ Class parent for models. """

    class Config:

        json_loads = orjson.loads
        json_dumps = orjson_dumps
        cache_free = False


class NewReviewLikes(BaseMixin):
    user_id: str
    film_id: str
    likes: list[str]


class NewReviewsLikes(BaseMixin):
    request_date: datetime
    new_reviews_likes: list[NewReviewLikes]


class ForgottenUserBookmarks(BaseMixin):
    user_id: str
    films: list[str]


class NewMoviesForPeriod(BaseMixin):
    period_days: int
    films: list[str]


class MovieEvent(BaseMixin):
    name_of_event_source: str
    name_type_event: str
    context: NewReviewsLikes | list[ForgottenUserBookmarks] | NewMoviesForPeriod | None


# class ResponseAPINotice(BaseMixin):
#     status: int
#     body: dict = None


class ResultResponse(BaseMixin):
    status: int
    body: dict = None


class GeneratorResponse(BaseMixin):
    event: MovieEvent
    api_notice_response: ResultResponse = None


class ErrorResponse(BaseMixin):
    status: int
    body: dict
