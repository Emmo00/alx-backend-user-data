#!/usr/bin/env python3
"""session authentication
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """session authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session and return session id
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.__class__.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns user id based on session id
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.__class__.user_id_by_session_id.get(session_id)
