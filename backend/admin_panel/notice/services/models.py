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


class MoviesUser(BaseMixin):
    user_id: str


class MoviesFilm(BaseMixin):
    film_id: str


class NewLikes(BaseMixin):
    user: MoviesUser
    film: MoviesFilm
    likes: list[MoviesUser]


class ForgottenBookmarks(BaseMixin):
    user: MoviesUser
    films: list[MoviesFilm]


class NewMoviesForPeriod(BaseMixin):
    period_days: int
    films: list[MoviesFilm]
