#!/usr/bin/env python3
"""basic auth module
"""
from .auth import Auth


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
