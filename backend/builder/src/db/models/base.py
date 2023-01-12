import re
from datetime import datetime

from src.config.config import NOTICE_DB_CONFIG
from sqlalchemy.orm import declarative_base
from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr


Base = declarative_base()

class BaseModel(Base):
    """Базовая модель объекта БД"""

    __abstract__ = True
    __table_args__ = {'schema': NOTICE_DB_CONFIG.SCHEMA_NAME}

    id: int = Column(String(128).with_variant(UUID(as_uuid=True), 'postgresql'), nullable=False, unique=True, primary_key=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: datetime = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @declared_attr
    def __tablename__(cls):
        return re.sub('(?!^)([A-Z][a-z]+)', r'_\1', cls.__name__).lower()

    def __repr__(self):
        return '<{0.__class__.__name__}(id={0.id!r})>'.format(self)
