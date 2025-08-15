# apps/auth/tokengen.py

import secrets
import string
from datetime import datetime, timedelta

def generate_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_expiry(minutes=60):
    return datetime.utcnow() + timedelta(minutes=minutes)
