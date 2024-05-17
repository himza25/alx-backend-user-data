#!/usr/bin/env python3
"""
This module provides functions for password hashing and validation.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password with a salt.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
