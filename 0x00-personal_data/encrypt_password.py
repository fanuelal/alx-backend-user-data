#!/usr/bin/env python3
"""Module Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns salted password"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """returns boolean for validation"""
    encoded = password.encode('utf-8')

    if bcrypt.checkpw(encoded, hashed_password):
        return True
    return False
