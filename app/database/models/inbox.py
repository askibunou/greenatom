from sqlalchemy import Column, Integer, String, DateTime, Table
from app.database.connection import metadata

inbox = Table(
    "inbox",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", String, nullable=False),
    Column("timestamp", DateTime, nullable=False),
)