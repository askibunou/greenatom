from datetime import datetime
from pydantic import BaseModel


class InboxBase(BaseModel):
    filename: str
    timestamp: datetime


class InboxCreate(InboxBase):
    pass


class Inbox(InboxCreate):
    id: int

    class Config:
        orm_mode = True
