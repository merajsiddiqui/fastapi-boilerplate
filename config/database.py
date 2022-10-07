from decouple import config
from urllib.parse import urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


def build_db_url():
    driver = config('DB_CONNECTION')
    user = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    host = config('DB_HOST')
    database = config('DB_DATABASE')
    port = config('DB_PORT')
    return '{}://{}:{}@{}:{}/{}'.format(driver, user, password, host, port, database)


db_url = build_db_url()
db_engine = create_engine(db_url)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = db_engine
)

Base = declarative_base()


class Config:
    arbitrary_types_allowed = True
    orm_mode = True
    underscore_attrs_are_private = False
    allow_population_by_field_name = True


class DBContext:

    def __init__(self):
        self.database = SessionLocal()

    def __enter__(self):
        return self.database

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database.close()
