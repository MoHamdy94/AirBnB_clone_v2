import unittest
import models
from datetime import datetime
from models.base_model import BaseModel
from time import sleep
import os
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    def test_model_instantiation(self):
        self.assertEqual(FileStorage, type(FileStorage()))

    def test_file_path(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_obj_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_var(self):
        self.assertEqual(FileStorage, type(models.storage))


class TestFileStorage_methods(unittest.TestCase):

    def test_dict_type(self):
        inst = FileStorage
        self.assertEqual(dict, type(models.storage.all()))

    def test_new_method(self):
        inst = BaseModel()
        models.storage.new(inst)
        self.assertIn("BaseModel." + inst.id, models.storage.all().keys())

    def test_save_method(self):
        inst = BaseModel()
        models.storage.new(inst)
        models.storage.save()
        with open("file.json", "r") as f:
            self.assertIn("BaseModel." + inst.id, f.read())

    def test_save_method(self):
        inst = BaseModel()
        models.storage.new(inst)
        models.storage.save()
        models.storage.reload()
        self.assertIn("BaseModel." + inst.id,
                      FileStorage._FileStorage__objects)

    def test_reload_no_file(self):
        self.assertRaises(FileNotFoundError, models.storage.reload())


if __name__ == '__main__':
    unittest.main()
