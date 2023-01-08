""" Model Like. """

from .base import BaseMixin


class EventNewUser(BaseMixin):
    user_id: str


class EventNewEpisode(BaseMixin):
    film_id: str


class EventFromAdmin(BaseMixin):
    time_zone: str


class NewLikesOfReview(BaseMixin):
    user_id: str
    likes: list[str]


class FilmInBookmark(BaseMixin):
    user_id: str
    films: list[str]


class NewFilmsForPeriod(BaseMixin):
    films: list[str]


class EventMovies(BaseMixin):
    """Class for event model."""

    name_of_event_source: str
    type_event_id: str
    context: EventNewUser | EventNewEpisode | EventFromAdmin | NewLikesOfReview | FilmInBookmark | NewFilmsForPeriod
