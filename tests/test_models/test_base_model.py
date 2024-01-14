#!/usr/bin/python3
""" """
import unittest
import json
from unittest import mock
from datetime import datetime
from models.base_model import BaseModel


class test_basemodel(unittest.TestCase):
    """Test the BaseModel class."""

    def test_instantiation(self):
        """Test that a BaseModel object is correctly created with expected attributes."""
        base_model_instance = BaseModel()
        self.assertIs(type(base_model_instance), BaseModel)
        base_model_instance.name = "Holberton"
        base_model_instance.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, base_model_instance.__dict__)
                self.assertIs(type(base_model_instance.__dict__[attr]), typ)
        self.assertEqual(base_model_instance.name, "Holberton")
        self.assertEqual(base_model_instance.number, 89)

    def test_uuid(self):
        """Test the UUID generation in the BaseModel class."""
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to a dictionary for JSON serialization."""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_to_dict_values(self):
        """Test the values in the dictionary returned from to_dict are correct."""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method produces the correct output."""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that the save method updates `updated_at` and calls `storage.save`."""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)

    # Others
    @staticmethod
    def value():
        """Utility method to create an instance of BaseModel."""
        return BaseModel()

    # def test_default(self):
    #     """Test that default instance is created."""
    #     i = self.value()
    #     self.assertEqual(type(i), BaseModel)

    def test_kwargs(self):
        """Test instance creation using kwargs."""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Test instance creation with invalid kwargs (int)."""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """Test the save method."""
        i = self.value()
        i.save()
        key = f'{i.__class__.__name__}.{i.id}'
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Test the str method."""
        i = self.value()
        self.assertEqual(
            str(i), f'[{i.__class__.__name__}] ({i.id}) {i.__dict__}')

    def test_todict(self):
        """Test the to_dict method."""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """Test instance creation with None as a key in kwargs."""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    # def test_kwargs_one(self):
    #     """Test instance creation with a missing required key in kwargs."""
    #     n = {'name': 'test'}
    #     with self.assertRaises(KeyError):
    #         new = self.value(**n)

    def test_id(self):
        """Test the id attribute."""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Test the created_at attribute."""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    # def test_updated_at(self):
    #     """Test the updated_at attribute."""
    #     new = self.value()
    #     n = new.to_dict()
    #     new = BaseModel(**n)
    #     self.assertEqual(new.created_at, new.updated_at)
