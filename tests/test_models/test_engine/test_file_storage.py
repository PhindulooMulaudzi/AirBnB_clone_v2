#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage, storage_type
from models.engine.file_storage import FileStorage
from unittest.mock import MagicMock
import os


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in FileStorage.__objects.keys():
            del_list.append(key)
        for key in del_list:
            del FileStorage.__objects[key]

        self.file_storage_instance = FileStorage()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    @unittest.skipIf(storage_type == 'db', "not testing file storage")
    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(FileStorage.__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    @unittest.skipIf(storage_type == 'db', "not testing file storage")
    def test_storage_var_created(self):
        """ FileStorage object storage created """
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)

    def test_delete_with_valid_object(self):
        """
        Test the delete method with a valid object. \
            It should remove the object from the __objects dictionary.
        """
        mock_object = MagicMock()
        mock_object.__class__.__name__ = "MockClass"
        mock_object.id = 1
        self.file_storage_instance.__objects["MockClass.1"] = mock_object
        self.file_storage_instance.delete(obj=mock_object)
        self.assertNotIn("MockClass.1", self.file_storage_instance.__objects)

    def test_delete_with_invalid_object(self):
        """
        Test the delete method with a None object. \
            It should not modify the __objects dictionary.
        """
        self.file_storage_instance.delete(obj=None)
        self.assertEqual(len(self.file_storage_instance.__objects), 0)

    def test_delete_with_nonexistent_object(self):
        """
        Test the delete method with a nonexistent object. \
            It should not modify the __objects dictionary.
        """
        mock_object = MagicMock()
        mock_object.__class__.__name__ = "NonExistentClass"
        mock_object.id = 2
        self.file_storage_instance.delete(obj=mock_object)
        self.assertEqual(len(self.file_storage_instance.__objects), 0)

    def test_delete_with_key_error(self):
        """
        Test the delete method when a KeyError occurs. It should raise a KeyError.
        """
        mock_object = MagicMock()
        mock_object.__class__.__name__ = "NonExistentClass"
        mock_object.id = 3
        with self.assertRaises(KeyError):
            self.file_storage_instance.delete(obj=mock_object)

    def test_all_with_valid_class(self):
        """
        Test the all method with a valid class (State). \
            It should return a filtered dictionary of objects.
        """
        from models.state import State
        mock_state = MagicMock()
        mock_state.__class__.__name__ = "State"
        self.file_storage_instance.__objects["State.1"] = mock_state
        result = self.file_storage_instance.all(cls=State)
        self.assertIn("State.1", result)
        self.assertEqual(result["State.1"], mock_state)

    def test_all_with_exception(self):
        """
        Test the all method when an exception occurs. \
            It should return the entire __objects dictionary.
        """
        from models.state import State
        with unittest.mock.patch.object(self.file_storage_instance, '__objects', side_effect=Exception("Mock Exception")):
            result = self.file_storage_instance.all(cls=State)
        self.assertEqual(result, self.file_storage_instance.__objects)
