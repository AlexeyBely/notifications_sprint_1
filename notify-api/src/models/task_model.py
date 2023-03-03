from pydantic import BaseModel, UUID4


class Task(BaseModel):       
    template: str
    users: list[str]
