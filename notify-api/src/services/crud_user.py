from sqlalchemy.orm import Session

from models import user_model, user_schema
from uuid import UUID


def get_model_user_from_schema(
    model_user: user_model.User,
    schema_user: user_schema.UserBase
) -> user_model.User:

    model_user.timezone = schema_user.timezone  # type: ignore
    model_user.from_time = schema_user.from_time    # type: ignore
    model_user.befor_time = schema_user.befor_time  # type: ignore
    model_user.email_permission = schema_user.email_permission  # type: ignore
    model_user.browser_permission = schema_user.browser_permission  # type: ignore
    model_user.push_permission = schema_user.push_permission    # type: ignore
    model_user.mobile_permission = schema_user.mobile_permission    # type: ignore
    return model_user


def create_user(db: Session, user_id: UUID, user: user_schema.UserBase):
    db_user = user_model.User(id=user_id)
    db_user = get_model_user_from_schema(db_user, user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: UUID):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def update_user(db: Session, user_id: UUID, user_update: user_schema.UserBase):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user is None:
        return None
    db_user = get_model_user_from_schema(db_user, user_update)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
