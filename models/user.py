#!/usr/bin/python3
'''Module for the User class'''
from models.base_model import BaseModel


class User(BaseModel):
    """class User that handles user information

    Attrs:
        email (str): user email
        password (str): user password
        first_name (str): first name
        last_name (str): last name

    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
