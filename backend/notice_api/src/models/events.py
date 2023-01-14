""" Model Like. """
from datetime import datetime

from .base import BaseMixin


class EventNewUser(BaseMixin):
    user_id: str


class EventNewEpisode(BaseMixin):
    film_id: str


class EventFromAdmin(BaseMixin):
    user_filter: str


class UserLikesOfReview(BaseMixin):
    review_id: str
    film: str
    number_likes: int


class UserReviews(BaseMixin):
    user_id: str
    user_reviews: list[UserLikesOfReview]


class NewReviewsLikes(BaseMixin):
    request_date: datetime
    user_id: str
    user_reviews: list[UserLikesOfReview]


class FilmInBookmark(BaseMixin):
    user_id: str
    films: list[str]


class NewFilmsInPeriod(BaseMixin):
    period_days: int
    films: list[str]


class EventMovies(BaseMixin):
    """Class for event model."""

    name_of_event_source: str
    name_type_event: str
    context: (
        NewReviewsLikes
        | EventNewEpisode
        | EventFromAdmin
        | list[FilmInBookmark]
        | NewFilmsInPeriod
        | EventNewUser
        | None
    )
    created: datetime
