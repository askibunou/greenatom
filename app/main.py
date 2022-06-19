from fastapi import FastAPI
from app.database.connection import metadata, engine, database
from app.api import auth, frames

app = FastAPI()
metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(frames.router, tags=['Frames'])
app.include_router(auth.router, tags=['OAuth2'])
