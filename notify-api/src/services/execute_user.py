from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from models.user_model import User


async def get_user(session: Session, user_id: UUID):
    """Get user information."""
    result = await session.execute(select(User).order_by(User.id))  # type: ignore
    user = result.scalars().first()
    return user
