#!/usr/bin/env python3
""" UserSession module for handling session storage in the database
"""
from models.base import Base
import uuid


class UserSession(Base):
    """ UserSession class for storing session data
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize UserSession """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.session_id = kwargs.get('session_id', str(uuid.uuid4()))
