from abc import ABC, abstractproperty
from typing import Any
from dataclasses import dataclass


@dataclass
class BaseContext(ABC):
    data: dict[str, Any]

    @abstractproperty
    async def context(self) -> dict[str, Any]:
        """
            Данные, необходимых для подстановки в шаблон.
            Данные могут быть получены как локальными вычислениями так и запросом к сторонним сервисам / api
        """


@dataclass
class BaseRecipients(ABC):
    data: dict[str, Any]

    @abstractproperty
    async def recipients(self) -> list[str]:
        """
            Список с почтовыми адресами.
            Данные могут быть получены как локальными вычислениями так и запросом к сторонним сервисам / api
        """
