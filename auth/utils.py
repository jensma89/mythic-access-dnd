"""
utils.py
"""
from warnings import deprecated

from passlib.context import CryptContext



# Save password hash configurations
pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)


def verify_password(
        plain_password: str,
        hashed_password: str) -> bool:
    """Verify a plain password
    against the hashed one."""
    return pwd_context.verify(
        plain_password,
        hashed_password)
