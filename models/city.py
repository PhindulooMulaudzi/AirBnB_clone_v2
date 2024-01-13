#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models import storage_type


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if storage_type == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        # places = relationship("Place", backref="cities")
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
