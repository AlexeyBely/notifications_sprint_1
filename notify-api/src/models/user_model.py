import datetime
from sqlalchemy import Boolean, Column, String, UUID, DateTime, Time

from db.postgresql import Base



class User(Base):
    __tablename__ = 'notify\'.\'user'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    timezone = Column(String, default='Europe/Moscow')
    from_time = Column(Time, default=datetime.time(9, 00))
    befor_time = Column(Time, default=datetime.time(20, 00))
    email_permission = Column(Boolean, default=False)
    browser_permission = Column(Boolean, default=False)
    push_permission = Column(Boolean, default=False)
    mobile_permission = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    modified = Column(DateTime, default=datetime.datetime.utcnow)
