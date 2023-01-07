""" Router for Likes service. """
from fastapi import APIRouter, Depends, Request
from src.api.v1.params import EventParams
from src.api.v1.utilitys import check_result, get_context
from src.core.config import SETTINGS
from src.models.base import ResponseBoolResult
from src.models.events import EventMovies
from src.services.events import RabbitMQProducerService, get_event_service

router = APIRouter()
URL = f'{SETTINGS.notice_api_host}:{SETTINGS.notice_api_port}\
{SETTINGS.notice_api_path}/{SETTINGS.notice_api_version}/events'


@router.post(
    '',
    response_model=ResponseBoolResult,
    summary='Send event to queue',
    description='Send event to queue',
    response_description='ISend event to queue',
    tags=['Events'],
)
async def send_event(
        request: Request,
        params: EventParams = Depends(),
        obj_service: RabbitMQProducerService = Depends(get_event_service),
) -> ResponseBoolResult:
    """ Send event to queue

    Arguments:
        request: request
        params:
        obj_service: service object

    Returns:
        result:
    """

    event_params = await get_context(params=params.get_dict(), model=EventMovies)

    result = await obj_service.send_event(event_params)
    await check_result(result, obj_service.errors)

    return ResponseBoolResult(result=result)
