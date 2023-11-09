#!/usr/bin/env python3
"""session auth with db
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """session auth with db
    """
    def create_session(self, user_id=None):
        """create session
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        UserSession.load_from_file()
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """user id from session id
        """
        if session_id is None or type(session_id) is not None:
            return None
        UserSession.load_from_file()
        result = UserSession.search({'session_id': session_id})
        user_session = result[0]
        return user_session.get('user_id')

    def destroy_session(self, request=None):
        """destroy_session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        UserSession.load_from_file()
        result = UserSession.search({'session_id': session_id})
        user_session = result[0]
        user_session.remove()
        return True
