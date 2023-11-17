#!/usr/bin/env python3
"""auth module
"""
import bcrypt

salt = bcrypt.gensalt()


def _hash_password(password: str):
    """return hashed password
    """
    return bcrypt.hashpw(password.encode(), salt)
