from sqlalchemy import select
from pathlib import Path

from src.db.async_db import AsyncDB
from src.db.models.notice import TypeEvent
from src.models.template import TemplateDB, Template


async def get_template(db: AsyncDB, name_type_event: str) -> TemplateDB:
        await db.session.connect()

        query = select(TypeEvent.subject, TypeEvent.template_file).filter(TypeEvent.name == name_type_event)
        result = await db.execute(query)
        
        await db.session.disconnect()

        if not result:
            return None

        row, = result
        _template = TemplateDB(**row)
        
        if not Path(_template.template_file).is_file():
            raise ValueError('File not found')

        with open(_template.template_file) as fd:
            template = Template(body=fd.read(), subject=_template.subject)
        
        return template
