#!/usr/bin/python3

import unittest
import pep8
from unittest.mock import patch
from io import StringIO
from models import storage
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User


class TestHBNBCommandConsole(unittest.TestCase):

    def setUp(self):
        self.hbnb_command = HBNBCommand()

    def tearDown(self):
        del self.hbnb_command

    def test_create(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.hbnb_command.onecmd("create User")
            output = mock_stdout.getvalue().strip()
            self.assertTrue(output != "")
            self.assertIsInstance(storage.all()["User." + output], User)


class TestConsoleCodeStyle(unittest.TestCase):

    @staticmethod
    def check_pep8_conformance(file_path):
        """Test that file conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_path])
        return result.total_errors

    def test_console_pep8_conformance(self):
        errors = TestConsoleCodeStyle.check_pep8_conformance('console.py')
        self.assertEqual(
            errors, 0, f"Found {errors} PEP8 errors (and warnings) in console.py.")

    def test_test_console_pep8_conformance(self):
        errors = TestConsoleCodeStyle.check_pep8_conformance(
            'tests/test_console.py')
        self.assertEqual(
            errors, 0, f"Found {errors} PEP8 errors (and warnings) in tests/test_console.py.")
