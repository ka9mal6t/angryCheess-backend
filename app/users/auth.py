import hashlib
import random
import string
from datetime import datetime, timedelta
import jwt

from app.config import ACCESS_SECRET_KEY, ALGORITHM
from app.users.dao import UsersDAO
from app.users.models import Users


def get_password_hash(email: str, password: str) -> str:
    return hashlib.sha256((email + password).encode('utf-8')).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashlib.sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=6000)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, ACCESS_SECRET_KEY, ALGORITHM)
    return encode_jwt


async def create_unique_code(length=50) -> str:
    while True:
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        user = await UsersDAO.find_one_or_none(invite_code=random_string)
        if user is None:
            break
    return random_string
