from decouple import config
from urllib.parse import urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base


def build_db_url():
    driver = config('DB_CONNECTION')
    user = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    host = config('DB_HOST')
    database = config('DB_DATABASE')
    port = config('DB_PORT')
    return '{}://{}:{}@{}:{}/{}'.format(driver, user, password, host, port, database)


db_url = build_db_url()
db_engine = create_engine(db_url, connect_args = {"check_same_thread": False})

DBSession = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = db_engine
)

Base = declarative_base()


class DBContext:

    def __init__(self):
        self.database = DBSession()

    def __enter__(self):
        return self.database

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database.close()


def get_database():
    with DBContext() as database:
        yield database
