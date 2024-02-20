#!/usr/bin/python3
"""
Review class module inheret BasModel
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review class module inheret BasModel

    Attrs:
        place_id: The Place id
        user_id: The User id
        text: The text of the review

    """
    place_id = ""
    user_id = ""
    text = ""
