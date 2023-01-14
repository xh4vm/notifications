from sqlalchemy import select
from pathlib import Path

from src.config.config import BUILDER_CONFIG
from src.db.async_db import AsyncDB
from src.db.models.notice import TypeEvent
from src.models.template import TemplateDB, Template


from loguru import logger


async def get_template(db: AsyncDB, name_type_event: str) -> TemplateDB:
    query = select(TypeEvent.subject, TypeEvent.template_file).filter(TypeEvent.name == name_type_event)
    result = await db.execute(query)

    if not result:
        return None

    (row,) = result
    _template = TemplateDB(**row)

    logger.info(f"template_file: {f'{BUILDER_CONFIG.MEDIAFILES}/{_template.template_file}'}")

    if not Path(f'{BUILDER_CONFIG.MEDIAFILES}/{_template.template_file}').is_file():
        raise ValueError('File not found')

    with open(f'{BUILDER_CONFIG.MEDIAFILES}/{_template.template_file}') as fd:
        template = Template(body=fd.read(), subject=_template.subject)

    return template
