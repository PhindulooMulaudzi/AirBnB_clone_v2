#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import models
import uuid

if storage_type == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if storage_type == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        try:
            self.id = str(uuid.UUID(kwargs.get("id", str(uuid.uuid4()))))
        except ValueError:
            raise ValueError("Invalid UUID provided for 'id'")

        time_format = "%Y-%m-%dT%H:%M:%S.%f"

        try:
            self.created_at = (
                datetime.strptime(kwargs.get("created_at"), time_format)
                if kwargs.get("created_at") and isinstance(kwargs["created_at"], str)
                else datetime.utcnow()
            )
        except (ValueError, TypeError):
            raise ValueError(
                "Invalid datetime format provided for 'created_at'")

        try:
            self.updated_at = (
                datetime.strptime(kwargs.get("updated_at"), time_format)
                if kwargs.get("updated_at") and isinstance(kwargs["updated_at"], str)
                else datetime.utcnow()
            )
        except (ValueError, TypeError):
            raise ValueError(
                "Invalid datetime format provided for 'updated_at'")

        # Set other keyword arguments as attributes
        for key, value in kwargs.items():
            if key != "__class__" and key not in ["id", "created_at", "updated_at"]:
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
