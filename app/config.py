from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
# from secrets import token_bytes
# from base64 import b64encode
# print(b64encode(token_bytes(32)).decode())
ALGORITHM = os.getenv("ALGORITHM")
