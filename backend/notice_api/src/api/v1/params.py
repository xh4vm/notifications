# General classes for routers

import uuid

from fastapi import Body
from pydantic.types import UUID4
from src.utility.utility import str_if_uuid


class MixinParams:
    def get_dict(self):
        return {
            params_key: str_if_uuid(params_value) for params_key, params_value in self.__dict__.items() if params_value
        }


class EventParams(MixinParams):
    """ Class provide event's query parameters."""
    def __init__(
        self,
        name_of_event_source: str = Body(description="Name of the event source"),
        type_event_id: UUID4 = Body(description='ID of event\'s type', default=uuid.uuid4()),
        context: dict = Body(description="Context of event")
    ):
        self.name_of_event_source = name_of_event_source
        self.type_event_id = type_event_id
        self.context = context
