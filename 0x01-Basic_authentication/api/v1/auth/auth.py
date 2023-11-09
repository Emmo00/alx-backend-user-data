#!/usr/bin/env python3
"""Authentication module
"""
from typing import List, TypeVar
from flask import request
import re


class Auth:
    """Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication
        """
        if path is None:
            return True
        path += '/' if path[-1] != '/' else ''
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if '*' in excluded_path:
                if re.search(path, excluded_path.replace('*', '.*')):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header
        """
        if request is None or not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """current user
        """
        return None
