#!/usr/bin/python3
'''City class module inheret BasModel'''
from models.base_model import BaseModel


class City(BaseModel):
    '''
    City class module inheret BasModel
    Attrs:
    state_id: id of namestate
    name: name of state
    '''
    state_id = ""
    name = ""
