#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", back_populates='state')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializng a State object."""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Returns the list of City instances that matches state id."""
            city_objs = models.storage.all(City)
            matched_cities = list()
            for key, obj in city_objs.items():
                if (obj.state_id == self.id):
                    matched_cities.append(obj)
            return (matched_cities)
