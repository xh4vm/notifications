""" API service for movies. """

import logging

import uvicorn as uvicorn
from fastapi import FastAPI
# from fastapi import Request
# from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse
from src.api.v1 import events
from src.core.config import SETTINGS
from src.core.logger import LOGGING
from src.db.rabbitmq import producer

app = FastAPI(
    title=SETTINGS.name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description=SETTINGS.description,
    version=SETTINGS.version,
)


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     request_id = request.headers.get('X-Request-Id')
#     if not request_id:
#         raise RuntimeError('request id is required')
#     return await call_next(request)


@app.on_event('startup')
async def startup():
    """ Execute connects to databases on event startup. """

    await producer.init_producer(
        host=SETTINGS.rabbitmq.host,
        port=SETTINGS.rabbitmq.port,
        login=SETTINGS.rabbitmq.default_user,
        password=SETTINGS.rabbitmq.default_pass,
        service_name=SETTINGS.name,
        queue_name=SETTINGS.rabbitmq.queue_name,
    )


@app.on_event('shutdown')
async def shutdown():
    """ Execute close connects to databases on event shutdown. """
    await producer.connection.close()


# @app.exception_handler(AccessException)
# def authjwt_exception_handler(request: Request, exc: AccessException):
#     return JSONResponse(
#         status_code=exc.status,
#         content={"detail": exc.message}
#     )


app.include_router(events.router, prefix='/api/v1/events')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=SETTINGS.notice_api_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
