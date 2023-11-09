#!/usr/bin/env python3
"""session authentication
"""
from .auth import Auth
from models.user import User
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

    def destroy_session(self, request=None):
        """destroy session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns user id based on session id
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.__class__.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """return current user
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        User.load_from_file()
        user = User.get(user_id)
        return user
