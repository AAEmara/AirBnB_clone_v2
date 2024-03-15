#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", back_populates='state')
    else:
        @property
        def cities(self):
            """Returns the list of City instances that matches state id."""
            city_objs = storage.all(type(City))
            matched_cities = list()
            for key, obj in city_objs.items():
                if (obj["state_id"] == State.id):
                    matched_cities.append(obj)
            return (matched_cities)
