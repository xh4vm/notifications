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


class UserLikesOfReview(BaseMixin):
    review_id: str
    film: str
    number_likes: int


class UserReviews(BaseMixin):
    user_id: str
    user_reviews: list[UserLikesOfReview]


class FilmName(BaseMixin):
    film_id: str
    film_name: str


class NewReviewsLikes(BaseMixin):
    request_date: datetime
    new_reviews_likes: list[UserReviews]


class NewReviewLikesOut(BaseMixin):
    request_date: datetime
    user_id: str
    user_reviews: list[UserLikesOfReview]


class ForgottenUserBookmarks(BaseMixin):
    user_id: str
    films: list[str]


class NewMoviesForPeriod(BaseMixin):
    period_days: int
    films: list[str]


class MovieEvent(BaseMixin):
    name_of_event_source: str
    name_type_event: str
    context: NewReviewLikesOut | ForgottenUserBookmarks | NewMoviesForPeriod | None
    created: datetime


class MoviesTokens(BaseMixin):
    access_token: str
    refresh_token: str


class ResponseBoolResult(BaseMixin):
    result: bool


class ResultResponse(BaseMixin):
    status: int
    body: (
        NewReviewsLikes
        | list[ForgottenUserBookmarks]
        | NewMoviesForPeriod
        | MoviesTokens
        | FilmName
        | ResponseBoolResult
    ) = None


class GeneratorResponse(BaseMixin):
    event: MovieEvent
    api_notice_response: ResultResponse = None


class ErrorResponse(BaseMixin):
    status: int
    body: dict
