#!/usr/bin/env python3
"""
encrypt password
"""
from typing import ByteString
import bcrypt


def hash_password(password: str) -> ByteString:
    """encrypt password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check encrypted password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
