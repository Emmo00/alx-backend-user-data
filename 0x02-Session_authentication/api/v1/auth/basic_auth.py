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
        colon_index = decoded_base64_authorization_header.index(':')
        user_email = decoded_base64_authorization_header[
            slice(0, colon_index)]
        decoded_len = len(decoded_base64_authorization_header)
        user_password = decoded_base64_authorization_header[
            slice(colon_index + 1, decoded_len)]
        return tuple([user_email, user_password])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user object from credentials
        """
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) is not str:
            return None
        if type(user_pwd) is not str:
            return None
        User.load_from_file()
        if User.count() == 0:
            return None
        result = User.search({'email': user_email})
        if not result or len(result) == 0:
            return None
        for user in result:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves current user for a request
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        base64_code = self.extract_base64_authorization_header(auth_header)
        if not base64_code:
            return None
        decoded_base64 = self.decode_base64_authorization_header(base64_code)
        if not decoded_base64:
            return None
        user_credentials = self.extract_user_credentials(decoded_base64)
        if not user_credentials[0] or not user_credentials[1]:
            return None
        return self.user_object_from_credentials(*user_credentials)
