"""
utils.py
"""
from pwdlib import PasswordHash



# Secure Argon2id setup
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain password."""
    return password_hash.hash(password)


def verify_password(
        plain_password: str,
        hashed_password: str) -> bool:
    """Verify a plain password against the hashed one."""
    return password_hash.verify(
        plain_password,
        hashed_password)
