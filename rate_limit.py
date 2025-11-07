"""
rate_limit.py


"""
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

# log whenever a request is blocked
def rate_limit_exceeded_handler(request, exception):
    user_ip = get_remote_address(request)
    logger.warning(f"Rate limit exceeded for IP: {user_ip}")
    return exception
