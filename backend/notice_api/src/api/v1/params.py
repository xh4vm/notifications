# General classes for routers

from fastapi import Body
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
        time_zone: list[str] = Body(description="List of time zones", default=None),
        name_of_event_source: str = Body(description="Name of the event source"),
        name_type_event: str = Body(description='ID of event\'s type', default='this_is_happened'),
        context: dict = Body(description="Context of event", default=None)
    ):
        self.time_zone = time_zone
        self.name_of_event_source = name_of_event_source
        self.name_type_event = name_type_event
        self.context = context
