#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models import storage_type
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    if storage_type == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if storage_type != "db":
        @property
        def cities(self):
            """list of city instances related to the state"""
            try:
                all_cities = models.storage.all(models.City)
                city_list = [city for city in all_cities.values()
                             if city.state_id == self.id]
                return city_list
            except Exception as e:
                print(f"Error getting cities for state: {e}")
                return None
