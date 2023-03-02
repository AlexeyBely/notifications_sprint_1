import uuid

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from api.v1.auth import TokenData, authenticate
from models.user_schema import User, UserBase
import api.messages as messages
from db.dependency import get_db
from services import crud_user


router = APIRouter()


@router.post(
    '/',
    response_model=User,
    summary='Создать настройки пользователя',
    description='Создать настройки по user_id из данных аунтификации',
    response_description='Информация по нотификации',
)
def create_user(
    user_param: UserBase = Body(...),
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(authenticate),
) -> User:
    """Add new user param."""
    user_id = uuid.UUID(token_data.user)
    db_user = crud_user.get_user(db, user_id)
    if db_user:
        raise HTTPException(status_code=400, detail=messages.ALREADY_REGISTERED)
    db_user = crud_user.create_user(db, user_id, user_param)
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return db_user


@router.get(
    '/',
    response_model=User,
    summary='Прочитать настройки пользователя',
    description='Настройки по user_id из данных аунтификации',
    response_description='Информация по настройкам нотификации',
)
def get_user(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(authenticate),
) -> User:
    """Get user parem."""
    user_id = uuid.UUID(token_data.user)
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.USER_NOT_FOUND)
    return db_user


@router.put(
    '/',
    response_model=User,
    summary='Обновить настройки пользователя',
    description='Обновить настройки по user_id из данных аунтификации',
    response_description='Информация по нотификации',
)
def update_user(
    user_param: UserBase = Body(...),
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(authenticate),
) -> User:
    """Update user param."""
    user_id = uuid.UUID(token_data.user)
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail=messages.USER_NOT_FOUND)
    db_user = crud_user.update_user(db, user_id, user_param)
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return db_user


@router.delete(
    '/',
    response_model=None,
    summary='Удалить настройки пользователя',
    description='Удалить настройки по user_id из данных аунтификации',
)
def delete_user(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(authenticate),
) -> None:
    """Delete user param."""
    user_id = uuid.UUID(token_data.user)
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail=messages.USER_NOT_FOUND)
    crud_user.delete_user(db, user_id)
    return {'detail': messages.USER_DELETED}, HTTPStatus.OK
