#!/usr/bin/python3
""" FileStorage classes """
import os
import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        pass

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in __objects.

        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for k, v in self.__objects.items():
                if type(v) == cls:
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def new(self, obj):
        ''' add object to __objects dictionary '''
        obj_cls_name = obj.__class__.__name__
        obj_id = obj.id
        key = f"{obj_cls_name}.{obj_id}"
        FileStorage.__objects[key] = obj

    def save(self):
        ''' serialize the __objects to JSON file '''
        jsonData = {}
        for key, value in FileStorage.__objects.items():
            jsonData[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(jsonData, file)

    def reload(self):
        '''Deserializes the JSON file to __objects if it exists;
        otherwise, do nothing '''

        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r') as file:
                try:
                    objDict = json.load(file)
                    for key, value in objDict.items():
                        FileStorage.__objects[key] = eval(
                            value['__class__'])(**value)
                except json.JSONDecodeError:
                    pass

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists."""
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """Call the reload method."""
        self.reload()
