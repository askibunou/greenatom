from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserCreate):
    id: int
    disabled: bool

    class Config:
        orm_mode = True
