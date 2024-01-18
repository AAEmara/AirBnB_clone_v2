#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.city import City
from models import storage
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City", back_populates="state")

    @property
    def cities(self):
        """Returns the list of City instances that matches state id."""
        city_objs = sotrage.all(type(City))
        mathced_cities = list()
        for key, obj in city_objs.items():
            if (obj["state_id"] == State.id):
                matched_cities.append(obj)
        return (matched_cities)
