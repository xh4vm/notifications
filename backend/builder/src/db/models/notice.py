from sqlalchemy import Column, ForeignKey, String, ARRAY, Date
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class TypeEvent(BaseModel):
    name = Column(String(256), nullable=False, unique=True)
    subject = Column(String(512), nullable=False, unique=True)
    template_file = Column(String(4096), nullable=False, unique=True)
    template_params = ARRAY(String)


class CreateManualMailing(BaseModel):
    name = Column(String(256), nullable=False, unique=True)
    type_event_id = Column(
        String(128).with_variant(UUID(as_uuid=True), 'postgresql'), ForeignKey('type_event.id'), nullable=False
    )
    date_to_send = Column(Date())
