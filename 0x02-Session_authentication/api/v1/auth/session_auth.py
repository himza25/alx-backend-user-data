#!/usr/bin/env python3
""" SessionAuth module for handling session authentication
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ SessionAuth class for handling session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        print(f"Session created: {session_id} -> {user_id}")
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        print(f"Session lookup: {session_id} -> {user_id}")
        return user_id

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session / logs out"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        print(f"Destroying session: {session_id}")
        del self.user_id_by_session_id[session_id]
        return True
