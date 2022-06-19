from typing import List

from app.database.connection import database
from app.database.models.inbox import inbox
from app.database.schemas.inbox import InboxCreate, Inbox


async def post(elements: List[InboxCreate]):
    results = []
    for element in elements:
        query = inbox.insert().values(filename=element.filename, timestamp=element.timestamp)
        id = await database.execute(query)

        results.append(Inbox(id=id, filename=element.filename, timestamp=element.timestamp))
    return results


async def get(id: int):
    query = await database.fetch_one(inbox.select().where(inbox.c.id == id))
    return Inbox(**query)


async def delete(id: int):
    return await database.execute(inbox.delete().where(inbox.c.id == id))