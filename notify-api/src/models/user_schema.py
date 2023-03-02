from pydantic import BaseModel, UUID4
from datetime import datetime, time


class UserBase(BaseModel):       
    timezone: str = 'Europe/Moscow'
    from_time: time = time(9, 00)
    befor_time: time =time(20, 00)
    email_permission: bool = False
    browser_permission: bool = False
    push_permission: bool = False
    mobile_permission: bool = False  


class User(UserBase):
    id: UUID4 
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True



