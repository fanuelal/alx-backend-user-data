#!/usr/bin/env python3
""" Model for DB
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class"""

    def __init__(self):
        """Instance"""

        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Sets up session"""

        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """create user on db"""

        addUser = User(email=email, hashed_password=hashed_password)
        self._session.add(addUser)
        self._session.commit()
        return addUser

    def find_user_by(self, **kwargs) -> User:
        """returns the first row found in the users table"""
        if not kwargs:
            raise InvalidRequestError

        cols = ["id", "email", "hashed_password", "session_id", "reset_token"]

        for arg in kwargs:
            if arg not in cols:
                raise InvalidRequestError

        found = self._session.query(User).filter_by(**kwargs).first()

        if found:
            return found
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Finds user record and updates attributes"""

        user_to_update = self.find_user_by(id=user_id)

        cols = ["id", "email", "hashed_password", "session_id", "reset_token"]
        for k, v in kwargs.items():
            if k in cols:
                setattr(user_to_update, k, v)
            else:
                raise ValueError

        self._session.commit()
