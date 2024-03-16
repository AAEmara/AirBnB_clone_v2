#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from os import getenv


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        # Deining relationships with the `places` table.
        user = relationship('User', back_populates='places')
        cities = relationship('City', back_populates='places')
        reviews = relationship('Review', back_populates='places')
        # Creating an association table.
        place_amenity = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60),
                                     ForeignKey('places.id'),
                                     primary_key=True, nullable=False),
                              Column('amenity_id', String(60),
                                     ForeignKey('amenities.id'),
                                     primary_key=True, nullable=False))
        # Creating the many to many relationship between places and amenities.
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """ Initializing a Place Object."""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """ Returns a list of Review instances for a certain place_id. """
            place_objs = storage.all(Place)
            review_list = list()
            for key, obj in place_objs.items():
                if obj['place_id'] == self.id:
                    review_list.append(obj)
            return (review_list)

        @property
        def amenities(self):
            """Returns the list of IDs for the Amenity Class."""
            return (amenity_ids)

        @amenities.setter
        def amenities(self, inserted_obj):
            """Handling the append mehthod, for appending amenities."""
            if isinstance(inserted_obj, Amenity):
                self.amenity_ids.append(inserted_obj.id)
