#!/usr/bin/env python3
"""basic auth module
"""
from .auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Basic authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns base64 part of the Auth header
        """
        if authorization_header is None or\
                type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.strip().split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode base64 str
        """
        if base64_authorization_header is None or\
                type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(base64_authorization_header).\
                decode('ascii')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extract user credentials from decoded header
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user object from credentials
        """
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) != str:
            return None
        if type(user_pwd) != str:
            return None
        result = User.search({'email': user_email})
        if len(result) == 0:
            return None
        user = result[0]
        if user.is_valid_password(user_pwd):
            return user
        return None
