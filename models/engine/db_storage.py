#!/usr/bin/python3
"""Module db_storage that represents the Database Storage."""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
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
        db = os.getenv(env_var[3])
        env = os.getenv(env_var[4])
        eng_format = f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'
        self.__engine = create_engine(eng_format, pool_pre_ping=True)

        if (env == "test"):
            meta = MetaData()
            meta.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Querying the current database based on class name."""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        class_dict = {'User': User, 'State': State, 'City': City,
                      'Amenity': Amenity, 'Place': Place, 'Review': Review}
        results_dict = dict()
        if (not cls):
            for key, val in class_dict.items():
                instances = self.__session.query(class_dict[key]).all()
                for instance in instances:
                    obj_key = val.__name__ + '.' + instance.id
                    results_dict[obj_key] = instance
        else:
            instances = self.__session.query(class_dict[cls]).all()
            for key, val in class_dict.items():
                if cls == key:
                    for instance in instances:
                        obj_key = val.__name__ + '.' + instance.id
                        results_dict[obj_key] = instance
        return (results_dict)

    def new(self, obj):
        """Add object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session if given."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current
        database session."""
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Calls remove() method on the session available."""
        self.__session__.remove()
