#!/usr/bin/env python3
"""Module Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns salted password"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed
