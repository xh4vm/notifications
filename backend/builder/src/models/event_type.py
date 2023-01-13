import enum


class EventTypeEnum(str, enum.Enum):
    NEW_REVIEW_LIKES = 'new_review_likes'
    NEW_MOVIES = 'new_movies_for_period'
    FOGGOTEN_BOOKMARKS = 'foggoten_bookmarks'
