from databases import Database
from sqlalchemy.sql import Select, Insert, Update, Delete
from typing import Any

from src.config.config import NoticeDBSettings, NOTICE_DB_CONFIG


class AsyncDB:
    def __init__(self, settings: NoticeDBSettings = NOTICE_DB_CONFIG):
        self._settings = settings
        self.session = Database(
            url=(
                f'{NOTICE_DB_CONFIG.DRIVER}://{NOTICE_DB_CONFIG.USER}'
                f':{NOTICE_DB_CONFIG.PASSWORD}@{NOTICE_DB_CONFIG.HOST}'
                f':{NOTICE_DB_CONFIG.PORT}/{NOTICE_DB_CONFIG.NAME}'
            ),
            min_size=5,
            max_size=20,
        )

    async def execute(self, query: Select | Insert | Update | Delete) -> list[dict[str, Any]]:
        if query.is_select:
            return await self.session.fetch_all(query=query)
        return await self.session.execute(query=query)
