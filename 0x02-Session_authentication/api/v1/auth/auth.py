#!/usr/bin/env python3
"""Auth module"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if the path requires authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        for ep in excluded_paths:
            if ep.endswith('*'):
                if path.startswith(ep[:-1]):
                    return False
            else:
                if ep[-1] != '/':
                    ep += '/'
                if path == ep:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the request"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user from the request"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        cookie_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(cookie_name)
