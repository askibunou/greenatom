import os

from databases import Database
from sqlalchemy import create_engine, MetaData

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# databases query builder
database = Database(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()
