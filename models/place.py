#!/usr/bin/python3
'''Place class module inheret BasModel'''
from models.base_model import BaseModel


class Place(BaseModel):
    '''
    Place class module inheret BasModel
    Artts:
        city_id: string -  the City.id
        user_id: string -  User.id
        name: string
        description: string
        number_rooms: integer
        number_bathrooms: integer - 0
        max_guest: integer - 0
        price_by_night: integer - 0
        latitude: float - 0.0
        longitude: float - 0.0
        amenity_ids: list of str
    '''

    city_id: str = ""
    user_id: str = ""
    name: str = ""
    description: str = ""
    number_rooms: int = 0
    number_bathrooms: int = 0
    max_guest: int = 0
    price_by_night: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    amenity_ids = []
