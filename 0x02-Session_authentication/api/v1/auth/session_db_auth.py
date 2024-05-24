#!/usr/bin/env python3
""" SessionDBAuth module for handling session authentication with database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class for handling session authentication with database
    """

    def create_session(self, user_id=None):
        """ Create a session and store it in the database """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve the user ID based on session ID from the database """
        if session_id is None:
            return None
        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None
        session_data = sessions[0]
        if self.session_duration <= 0:
            return session_data.user_id
        if 'created_at' not in session_data.to_json():
            return None
        expiration_time = (
            session_data.created_at +
            timedelta(seconds=self.session_duration)
        )
        if expiration_time < datetime.now():
            return None
        return session_data.user_id

    def destroy_session(self, request=None):
        """ Destroy a session based on session ID from the request cookie """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False
        session_data = sessions[0]
        session_data.remove()
        return True
