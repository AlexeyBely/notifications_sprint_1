from api.v1 import user, task
from core.config import settings
from db import psql_async

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


app = FastAPI(
    title=f'Сервис {settings.project_name}',
    docs_url='/notify/api/openapi',
    openapi_url='/notify/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Сервис нотификации',
    version='1.0.1',
)


@app.on_event('startup')
async def startup():
    psql_async.engine_psql_async = create_async_engine(psql_async.sqlalchemy_asyncpg_url,
                                                       echo=True)
    psql_async.session_psql_async = sessionmaker(psql_async.engine_psql_async,
                                                 expire_on_commit=False,
                                                 class_=AsyncSession)


@app.on_event('shutdown')
async def shutdown():
    await psql_async.engine_psql_async.dispose() 


app.include_router(user.router, prefix='/notify/api/v1/user', tags=['user'])
app.include_router(task.router, prefix='/notify/api/v1/task', tags=['task'])
