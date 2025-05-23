#!/usr/bin/env python3

"""Module for encrypting passwords using bcrypt."""


import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypts a password using bcrypt."""
    return bcrypt.hashpw(password.encode(encoding="utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password matches its hashed version."""
    return bcrypt.checkpw(
        password=password.encode(encoding="utf-8"),
        hashed_password=hashed_password,
    )
