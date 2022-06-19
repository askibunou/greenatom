from sqlalchemy import Column, Integer, String, Table, Boolean
from app.database.connection import metadata

user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, nullable=False, unique=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("disabled", Boolean, default=False),
)