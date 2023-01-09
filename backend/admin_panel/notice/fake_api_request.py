from datetime import datetime
from functools import wraps
from http import HTTPStatus
from uuid import uuid4

from notice.services.models import (FilmName, ForgottenUserBookmarks,
                                    NewMoviesForPeriod, NewReviewLikes,
                                    NewReviewsLikes, ResultResponse)


def uuid_str():
    return str(uuid4())


def mock_api_request(moc_func=None):
    def mock_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if moc_func:
                kwargs['make_request_func'] = moc_func
            result = func(*args, **kwargs)

            return result

        return wrapper
    return mock_wrapper


def _make_request_auth(url, method, params):
    return ResultResponse(
        status=HTTPStatus.OK,
        body={'auth_token': 'FAKE_AUTH_TOKEN', 'refresh_token': 'FAKE_REFRESH_TOKEN'}
    )


def _make_request_feedbacks_likes(url, method, params):
    return ResultResponse(
        status=HTTPStatus.OK,
        body=NewReviewsLikes(
            request_date=datetime.utcnow(),
            new_reviews_likes=[
                NewReviewLikes(
                    user_id=uuid_str(),
                    film_id=uuid_str(),
                    likes=[uuid_str(), uuid_str(), uuid_str(), uuid_str()]
                ),
                NewReviewLikes(
                    user_id=uuid_str(),
                    film_id=uuid_str(),
                    likes=[uuid_str(), uuid_str(), uuid_str(), uuid_str(), uuid_str()]
                ),
                NewReviewLikes(
                    user_id=uuid_str(),
                    film_id=uuid_str(),
                    likes=[uuid_str(), uuid_str()]
                ),
            ]
        )
    )


def _make_request_feedbacks_forgotten_bookmarks(url, method, params):
    return ResultResponse(
        status=HTTPStatus.OK,
        body=[
            ForgottenUserBookmarks(
                user_id=uuid_str(),
                films=[uuid_str(), uuid_str()]
            ),
            ForgottenUserBookmarks(
                user_id=uuid_str(),
                films=[uuid_str(), uuid_str()]
            ),
            ForgottenUserBookmarks(
                user_id=uuid_str(),
                films=[uuid_str(), uuid_str()]
            ),
        ]
    )


def _make_request_content_new_movies_for_period(url, method, params):
    return ResultResponse(
        status=HTTPStatus.OK,
        body=NewMoviesForPeriod(
            period_days=params['data']['days'],
            films=[uuid_str(), uuid_str(), uuid_str(), uuid_str()]
        ),
    )


def _make_request_content_get_film_name(url, method, params):
    return ResultResponse(
        status=HTTPStatus.OK,
        body=FilmName(
            film_id=params['data']['film_id'],
            film_name='Fake Film Name {0}'.format(params['data']['film_id'])
        ),
    )
