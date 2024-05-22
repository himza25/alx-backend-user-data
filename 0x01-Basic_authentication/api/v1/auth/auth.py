#!/usr/bin/env python3
"""Auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class template"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return True if path requires auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        for ep in excluded_paths:
            if ep[-1] != '/':
                ep += '/'
            if path == ep:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return auth header if present"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Return current user"""
        return None
