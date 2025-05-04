from dotenv import load_dotenv
import os

load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None) or None
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# -- SQL
CONNECTION_STRING = os.getenv("DB_CONNECTION")


# -- Email
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


# --- URLS
BASE_URL = "http://localhost:5500"


# --- HTTP
HTTPONLY = False  # Set to True in production
SESSION_EXPIRE_SECONDS = 3600
