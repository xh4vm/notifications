MAX_TEXT_FIELD_LENGTH = 255
EVENT_TEMPLATE_DOCTYPE = [
    '<!DOCTYPE html>',
]
EVENT_TEMPLATE_PATTERN = r'<html.*>.*<\/html>'
EVENT_TEMPLATE_PARAMS_PATTERN = r'{{\s(\w*)\s}}'
URL_SCHEME = 'http://'
EVENT_NEW_REVIEW_LIKES = ('new_review_likes', 'default_data/New_likes_of_review.html')
EVENT_FORGOTTEN_BOOKMARKS = ('forgotten_bookmarks', 'default_data/Foggoten_bookmaks.html')
EVENT_NEW_MOVIES_FOR_PERIOD = ('new_movies_for_period', 'default_data/New_movies.html')
BACKOFF_MAX_TRIES = 10
ACCESS_TOKEN_KEY = 'ACCESS_TOKEN'
REFRESH_TOKEN_KEY = 'REFRESH_TOKEN'
RECIPIENT_MIN_TIME = 8
RECIPIENT_MAX_TIME = 11
