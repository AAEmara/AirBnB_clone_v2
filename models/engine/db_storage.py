#!/usr/bin/python3
"""Module db_storage that represents the Database Storage."""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


class DBStorage():
    """Database Storage Class."""
    __engine = None
    __session = None

    def __init__(self):
        """Initializing the attributes."""
        env_var = ["HBNB_MYSQL_USER", "HBNB_MYSQL_PWD", "HBNB_MYSQL_HOST",
                   "HBNB_MYSQL_DB", "HBNB_ENV"]
        user = os.getenv(env_var[0])
        pwd = os.getenv(env_var[1])
        host = os.getenv(env_var[2])
        db = os.getenv(env_var[3]
        env = os.getenv(env_var[4])
        eng_format = f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'
        self.__engine = create_engine(eng_format, pool_pre_ping=True)

        if (env == "test"):
            meta = MetaData()
            meta.drop_all(bind=__engine)

    def all(self, cls=None):
        """Querying the current database based on class name."""
        Session = sessionmaker(bind=__engine)
        self.__session = Session()
        self.__session.query(cls).all()
        if (not cls):
            objs = ["User"
        else:
            self.__session.query(cls).all()

