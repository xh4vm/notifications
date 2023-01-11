""" Model Like. """
from datetime import datetime

from .base import BaseMixin


class EventNewUser(BaseMixin):
    user_id: str


class EventNewEpisode(BaseMixin):
    film_id: str


class EventFromAdmin(BaseMixin):
    time_zone: list[str]


class NewLikesOfReview(BaseMixin):
    user_id: str
    film_name: str
    likes: list[str]


class NewReviewsLikes(BaseMixin):
    request_date: datetime
    new_reviews_likes: NewLikesOfReview


class FilmInBookmark(BaseMixin):
    user_id: str
    films: list[str]


class NewFilmsInPeriod(BaseMixin):
    period_days: int
    films: list[str]


class EventMovies(BaseMixin):
    """Class for event model."""

    time_zone: list[str] | None
    name_of_event_source: str
    name_type_event: str
    context: (NewReviewsLikes | EventNewEpisode | EventFromAdmin |
              list[FilmInBookmark] | NewFilmsInPeriod | EventNewUser | None)
    created: datetime
