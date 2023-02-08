from sqlalchemy.orm import Session
from datetime import datetime

from models import user_model, user_schema
from sqlalchemy import Boolean, Column, String, UUID, DateTime, Time


def get_model_user_from_schema(
    model_user: user_model.User,
    schema_user: user_schema.UserBase
) -> user_model.User:

    model_user.timezone = schema_user.timezone
    model_user.from_time = schema_user.from_time
    model_user.befor_time = schema_user.befor_time
    model_user.email_permission = schema_user.email_permission
    model_user.browser_permission = schema_user.browser_permission
    model_user.push_permission = schema_user.push_permission
    model_user.mobile_permission = schema_user.mobile_permission
    return model_user


def create_user(db: Session, user_id: UUID, user: user_schema.UserBase):
    db_user = user_model.User(id = user_id)
    db_user = get_model_user_from_schema(db_user, user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: UUID):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def update_user(db: Session, user_id: UUID, user_update: user_schema.UserBase):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    db_user = get_model_user_from_schema(db_user, user_update)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
