from uuid import uuid4

from loguru import logger
from notice.services.models import (ForgottenBookmarks, MoviesFilm, MoviesUser,
                                    NewLikes, NewMoviesForPeriod)


def uuid_str():
    return str(uuid4())


def get_new_review_likes():
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Feedbacks получить новые лайки
    # 3. Отправить событие в API Notice
    result = NewLikes(
        user=MoviesUser(user_id=uuid_str()),
        film=MoviesFilm(film_id=uuid_str()),
        likes=[
            MoviesUser(user_id=uuid_str()),
            MoviesUser(user_id=uuid_str()),
            MoviesUser(user_id=uuid_str()),
            MoviesUser(user_id=uuid_str()),
        ]
    )
    logger.info(result)
    pass


def get_forgotten_bookmarks():
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Feedbacks получить забытые закладки
    # 3. Отправить событие в API Notice
    result = ForgottenBookmarks(
        user=MoviesUser(user_id=uuid_str()),
        films=[
            MoviesFilm(user_id=uuid_str()),
            MoviesFilm(user_id=uuid_str()),
        ]
    )
    logger.info(result)


def get_new_movies_for_period(days):
    # 1. Сходить в API Auth получить токен
    # 2. Cходить c токеном в API Content получить новые фильмы за посление days дней
    # 3. Отправить событие в API Notice
    result = NewMoviesForPeriod(
        period_days=days,
        films=[
            MoviesFilm(user_id=uuid_str()),
            MoviesFilm(user_id=uuid_str()),
        ]
    )
    logger.info(result)
