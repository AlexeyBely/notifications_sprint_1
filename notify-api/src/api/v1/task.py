from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

import logging

from models.task_model import Task
from services.auth import get_auth_users_service, AuthUsers
from services.films import get_movie_films_service, MovieFilms
from api.v1.utils import collect_film_variables, collect_user_variables
from tasks.email import send_email
from services import crud_user
from db.dependency import get_db


logger = logging.getLogger('')


router = APIRouter()


@router.post(
    '/',
    response_model=None,
    summary='Добавить или изменить лайк',
    description='Добавить (изменить) лайк с рейтенгом к кинопроизведению с movie_id',
    response_description='Полная информация по лайку',
)
async def add_task(
    task: Task = Body(...),
    auth_service: AuthUsers = Depends(get_auth_users_service),
    movie_service: MovieFilms = Depends(get_movie_films_service),
    db: Session = Depends(get_db),
) -> None:
    """Add new task."""
    template = task.template
    users = task.users
    logger.info(f'template {template} <{users}>')
    films = await movie_service.read_info_films()
    if films is None:
        return 
    var_films = collect_film_variables(films)
    info_users = await auth_service.read_info_users(users)
    if info_users is None:
        return    
    for user_id in info_users:  # type: ignore
        var_user = collect_user_variables(str(user_id), info_users)
        all_var = var_user | var_films
        db_user = crud_user.get_user(db, user_id)
        if db_user is not None:
            if db_user.email_permission is True:
                send_email.delay(template, all_var)
