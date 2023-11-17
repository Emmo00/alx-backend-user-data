#!/usr/bin/env python3
"""auth module
"""
import uuid
import bcrypt
from db import DB, NoResultFound

salt = bcrypt.gensalt()


def _hash_password(password: str):
    """return hashed password
    """
    return bcrypt.hashpw(password.encode(), salt)


def _generate_uuid():
    """return new uuid string
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initialize
        """
        self._db = DB()

    def register_user(self, email: str, password: str):
        """register user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str):
        """validate login
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except Exception:
            return False
