#!/usr/bin/env python3
"""Module hash Password"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from uuid import uuid4


def _hash_password(password: str) -> str:
    """hashing password"""
    hashed = hashpw(password.encode("utf-8"), gensalt())

    return hashed


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """reg user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
