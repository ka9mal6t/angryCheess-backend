import random
import secrets
import string

from app.recovery.dao import RecoveryDAO


async def create_unique_reset_code(length=50) -> str:
    while True:
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        user = await RecoveryDAO.find_one_or_none(code=random_string)
        if user is None:
            break
    return random_string