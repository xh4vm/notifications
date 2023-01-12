from datetime import datetime
from functools import wraps
from http import HTTPStatus
from uuid import uuid4

from notice.services.models import ResultResponse


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


def _make_request_auth(url, method, params, model):
    return ResultResponse(
        status=HTTPStatus.OK.value,
        body=model(
            access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwicGVybWlzc2lvbnMiOnsiMjA4MmM1ZjJhOGE4NTMzMjcyNjQ4MmIyMDA4NWQzOWIiOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCJlZTBhY2M3MGU4ZGFkOGEyYmE3Zjg5Y2VhMDZiMWFhYiI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl0sIjE1YzkyOGU1ZmNkNzkzNzRjYzVhZTg5Mzg0MjQxZWRjIjpbIkdFVCIsIlBPU1QiLCJQVVQiLCJERUxFVEUiXSwiZGJkMzBkNjUxYTE3MTRkZTg0NzFiMjIyM2MyMTg0NjciOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCIxY2M2NzdhNWIwZTg4MmIzNGY1MjRiODg4MmJjYTQ0NiI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl0sIjM5YWVkMWI3NTM1NjhjNzg1NzFjODRkZDNhYmYwM2E5IjpbIkdFVCIsIlBPU1QiLCJQVVQiLCJERUxFVEUiXSwiMzgyYzQyOTY1ODA2NmZjZDA1ZjZlNzVjYjY3Y2Y4ZjkiOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCI0ZGNhM2VlN2JhYjI4YmQ5Mzc4N2RiNjE0YjVlNzk5YiI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl0sIjVmMGNiYjZjMjk1NjM5M2I4Njg2OGM2ZjJjY2YyNWQ3IjpbIkdFVCIsIlBPU1QiLCJQVVQiLCJERUxFVEUiXSwiZTY2NjE0ZDQ4M2RmNWJiZGE4NDQyMTBmY2FiYjdmZTgiOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCI4MDA0NzdjNTI5MWEwMjJhMTgwNmUyNGY4OTJkYWQxYSI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl19LCJleHAiOjIwNzA5MjUwODQsImlhdCI6MTY2OTkyNTA4NH0.p_1kSjGiI5EUAXxIuH03Xoe8vgcde6xb0yzs5QGhb7g',
            refresh_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwicGVybWlzc2lvbnMiOnsiMjA4MmM1ZjJhOGE4NTMzMjcyNjQ4MmIyMDA4NWQzOWIiOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCJlZTBhY2M3MGU4ZGFkOGEyYmE3Zjg5Y2VhMDZiMWFhYiI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl0sIjE1YzkyOGU1ZmNkNzkzNzRjYzVhZTg5Mzg0MjQxZWRjIjpbIkdFVCIsIlBPU1QiLCJQVVQiLCJERUxFVEUiXSwiZGJkMzBkNjUxYTE3MTRkZTg0NzFiMjIyM2MyMTg0NjciOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCIxY2M2NzdhNWIwZTg4MmIzNGY1MjRiODg4MmJjYTQ0NiI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl0sIjM5YWVkMWI3NTM1NjhjNzg1NzFjODRkZDNhYmYwM2E5IjpbIkdFVCIsIlBPU1QiLCJQVVQiLCJERUxFVEUiXSwiMzgyYzQyOTY1ODA2NmZjZDA1ZjZlNzVjYjY3Y2Y4ZjkiOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCI0ZGNhM2VlN2JhYjI4YmQ5Mzc4N2RiNjE0YjVlNzk5YiI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl0sIjVmMGNiYjZjMjk1NjM5M2I4Njg2OGM2ZjJjY2YyNWQ3IjpbIkdFVCIsIlBPU1QiLCJQVVQiLCJERUxFVEUiXSwiZTY2NjE0ZDQ4M2RmNWJiZGE4NDQyMTBmY2FiYjdmZTgiOlsiR0VUIiwiUE9TVCIsIlBVVCIsIkRFTEVURSJdLCI4MDA0NzdjNTI5MWEwMjJhMTgwNmUyNGY4OTJkYWQxYSI6WyJHRVQiLCJQT1NUIiwiUFVUIiwiREVMRVRFIl19LCJleHAiOjMwNzA5MjUwODQsImlhdCI6MTY2OTkyNTA4NH0.UlBQKXxc7WWEySjDkRjwd8Wce1GTbTZ-V09KIgdg9TU',
        )
    )


def _make_request_feedbacks_likes(url, method, params, model):
    return ResultResponse(
        status=HTTPStatus.OK.value,
        body=model(
            request_date=datetime.utcnow(),
            new_reviews_likes=[
                {
                    'user_id': uuid_str(),
                    'film_id': uuid_str(),
                    'likes': [uuid_str(), uuid_str(), uuid_str(), uuid_str()],
                },
                {
                    'user_id': uuid_str(),
                    'film_id': uuid_str(),
                    'likes': [uuid_str(), uuid_str(), uuid_str(), uuid_str()],
                },
                {
                    'user_id': uuid_str(),
                    'film_id': uuid_str(),
                    'likes': [uuid_str(), uuid_str(), uuid_str(), uuid_str()],
                },
            ]
         )
    )


def _make_request_feedbacks_forgotten_bookmarks(url, method, params, model):
    return ResultResponse(
        status=HTTPStatus.OK.value,
        body=[
            model(
                user_id=uuid_str(),
                films=[uuid_str(), uuid_str()]
            ),
            model(
                user_id=uuid_str(),
                films=[uuid_str(), uuid_str()]
            ),
            model(
                user_id=uuid_str(),
                films=[uuid_str(), uuid_str()]
            ),
        ]
    )


def _make_request_content_new_movies_for_period(url, method, params, model):
    return ResultResponse(
        status=HTTPStatus.OK.value,
        body=model(
            period_days=params['data']['days'],
            films=[uuid_str(), uuid_str(), uuid_str(), uuid_str()]
        ),
    )


def _make_request_content_get_film_name(url, method, params, model):
    return ResultResponse(
        status=HTTPStatus.OK.value,
        body=model(
            film_id=params['data']['film_id'],
            film_name='Fake Film Name {0}'.format(params['data']['film_id'])
        ),
    )
