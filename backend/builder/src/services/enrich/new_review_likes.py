from typing import Any
from dataclasses import dataclass

from .base import BaseContext, BaseRecipients


@dataclass
class Context(BaseContext):
    data: dict[str, Any]

    @property
    async def context(self) -> dict[str, Any]:
        '''Фейковые данные'''
        return {
            "user": "Fake user",
            "film": "Fake film",
            "number_of_likes": 10,
            "users_list": ["fake slave user 1", "fake slave user 2"]
        }

@dataclass
class Recipients(BaseRecipients):
    data: dict[str, Any]

    @property
    async def recipients(self) -> list[str]:
        '''Фейковые данные'''
        return ['xoklhyip@yandex.ru', 'h4vm@yandex.ru']
