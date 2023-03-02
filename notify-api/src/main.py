from api.v1 import user, task
from core.config import settings

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

import uvicorn

app = FastAPI(
    title=f'Сервис {settings.project_name}',
    docs_url='/notify/api/openapi',
    openapi_url='/notify/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Сервис нотификации',
    version='1.0.1',
)


app.include_router(user.router, prefix='/notify/api/v1/user', tags=['user'])
app.include_router(task.router, prefix='/notify/api/v1/task', tags=['task'])




#if __name__ == '__main__':
#    uvicorn.run(app, host='0.0.0.0', port=8999)


