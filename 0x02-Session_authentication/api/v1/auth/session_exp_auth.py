#!/usr/bin/env python3
"""Session auth with expiration
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime
from typing import Dict


class SessionExpAuth(SessionAuth):
    """session auth (with expiration)
    """
    def __init__(self):
        """initialize
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session and return session id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {'user_id': user_id,
                        'created_at': datetime.now()}
        self.__class__.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """get user id from session id
        """
        if session_id is None:
            return None
        session_dict: Dict = self.__class__.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict:
            return None
        if session_dict.get('created_at') + self.session_duration > datetime.now():
            return None
        return session_dict.get('user_id')
