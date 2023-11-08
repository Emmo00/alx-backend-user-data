#!/usr/bin/env python3
"""basic auth module
"""
from .auth import Auth


class BasicAuth(Auth):
    """Basic authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """returns base64 part of the Auth header
        """
        auth_header: str = self.authorization_header()
        if auth_header is None or type(auth_header) is not str:
            return None
        if not auth_header.startswith('Basic '):
            return None
        return auth_header.strip().split(' ')[1]
