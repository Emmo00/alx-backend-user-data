#!/usr/bin/env python3
"""user session model
"""
from .base import Base


class UserSession(Base):
    """user session model
    """
    def __init__(self, *args: list, **kwargs: dict):
        """initialize user session
        """
        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')
