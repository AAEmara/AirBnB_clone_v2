#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage
        with optional filtering."""
        new_dict = dict()
        if (cls):
            for key, val in FileStorage.__objects.items():
                if (val.__class__ == cls):
                    new_dict[key] = val
            return (new_dict)
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        filename = FileStorage.__file_path
        with open(filename, mode='w', encoding="utf-8") as w_file:
            json.dump(
                {k: v.to_dict() for k, v in FileStorage.__objects.items()},
                w_file)

    def reload(self):
        """Loads storage dictionary from file"""

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            filename = FileStorage.__file_path
            with open(filename, mode='r', encoding="utf-8") as r_file:
                py_obj = json.load(r_file)
        except FileNotFoundError:
            pass
        else:
            for key, val in py_obj.items():
                cls_name = val["__class__"]
                FileStorage.__objects[key] = eval(cls_name)(**val)

    def delete(self, obj=None):
        """Deletes an object if available."""
        if (obj):
            key = str(obj.to_dict()['__class__'] + '.' + obj.id)
            del FileStorage.__objects[key]

    def close(self):
        """This method calls the reload method for deserializing the JSON
        file to objects."""
        self.reload()
