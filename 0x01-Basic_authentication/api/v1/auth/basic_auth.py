#!/usr/bin/env python3
"""basic auth module
"""
from .auth import Auth
import base64


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
