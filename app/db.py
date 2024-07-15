import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database

from .models import Base

user = os.environ.get('DB_USER', 'root')
pwd = os.environ.get('DB_PASS', 'pass')
host = os.environ.get('DB_HOST', 'host')

engine = create_engine(
    'mysql://{0}:{1}@{2}/translator'.format(user, pwd, host))


if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)

try:
    connection = engine.connect()
    print("DB CONNECTED")
except:
    print("DB CONNECTION ERROR")

Session = scoped_session(sessionmaker(bind=engine))
db_session = Session


def getDB():
    try:
        yield db_session
    except:
        db_session.close()
