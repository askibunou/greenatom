from app.database.connection import database
from app.database.models.user import user
from app.database.schemas.user import User, UserCreate


async def post(auth_user: UserCreate):
    query = user.insert().values(
        login=auth_user.login,
        name=auth_user.name,
        password=auth_user.password,
        email=auth_user.email,
        disabled=False
    )
    id = await database.execute(query)
    answer = User(
        id=id,
        login=auth_user.login,
        name=auth_user.name,
        password=auth_user.password,
        email=auth_user.email,
        disabled=False
    )

    return answer


async def get(login: str):
    query = await database.fetch_one(user.select().where(user.c.login == login))
    return query
