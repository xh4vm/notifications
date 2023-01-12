from typing import Any

from src.models.event_type import EventTypeEnum
from .new_review_likes import Context as ContextReviewsLikes, Recipients as RecipientsReviewsLikes
from .new_movies_for_period import Context as ContextMoviesPeriod, Recipients as RecipientsMoviesPeriod
from .foggoten_bookmaks import Context as ContextFoggotenBookmarks, Recipients as RecipientsFoggotenBookmarks



async def get_context(event_name: str, data: dict[str, Any]) -> dict[str, Any]:
    match event_name:
        case EventTypeEnum.NEW_REVIEW_LIKES:
            ctx = ContextReviewsLikes(data)

        case EventTypeEnum.NEW_MOVIES:
            ctx = ContextMoviesPeriod(data)

        case EventTypeEnum.FOGGOTEN_BOOKMARKS:
            ctx = ContextFoggotenBookmarks(data)

        case _:
            raise ValueError('Undefined event type')

    return await ctx.context 


async def get_recipients(event_name: str, data: dict[str, Any]) -> dict[str, Any]:
    match event_name:
        case EventTypeEnum.NEW_REVIEW_LIKES:
            ctx = RecipientsReviewsLikes(data)

        case EventTypeEnum.NEW_MOVIES:
            ctx = RecipientsMoviesPeriod(data)

        case EventTypeEnum.FOGGOTEN_BOOKMARKS:
            ctx = RecipientsFoggotenBookmarks(data)

        case _:
            raise ValueError('Undefined event type')

    return await ctx.recipients 
