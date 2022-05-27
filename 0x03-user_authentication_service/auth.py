#!/usr/bin/env python3
"""Module hash Password"""
from bcrypt import hashpw, gensalt, checkpw


def _hash_password(password: str) -> str:
    """hashing password"""
    hashed = hashpw(password.encode('utf-8'), gensalt())

    return hashed
