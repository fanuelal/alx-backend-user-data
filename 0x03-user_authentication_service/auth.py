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

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if user pswd is valid, locating by email"""
        try:
            found_user = self._db.find_user_by(email=email)
            return checkpw(password.encode("utf-8"),
                           found_user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates session ID using UUID, finds user by email"""
        try:
            found_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(found_user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """Finds user by session_id"""
        if session_id is None:
            return None
        try:
            found_user = self._db.find_user_by(session_id=session_id)
            return found_user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Updates user's session_id to None"""
        if user_id is None:
            return None
        try:
            found_user = self._db.find_user_by(id=user_id)
            self._db.update_user(found_user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Finds user by email, updates user's reset_token with UUID"""
        try:
            found_user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(found_user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Finds user by reset_token, updates user's pswd"""
        try:
            found_user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        new_pswd = _hash_password(password)
        self._db.update_user(found_user.id,
                             hashed_password=new_pswd, reset_token=None)


def _generate_uuid() -> str:
    """
    Returns string representation of new UUID
    """
    return str(uuid4())
