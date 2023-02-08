from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import Response

import uuid
import logging

from api.v1.auth import TokenData, authenticate
import api.messages as messages
from models.task_model import Task


logger = logging.getLogger('')


router = APIRouter()


@router.post(
    '/',
    response_model=None,
    summary='Добавить или изменить лайк',
    description='Добавить (изменить) лайк с рейтенгом к кинопроизведению с movie_id',
    response_description='Полная информация по лайку',
)
def add_task(
    task: Task = Body(...),
) -> None:
    """Add new task."""
    template = task.template
    users = task.users
    logger.info(f'template {template} <{users}>')
