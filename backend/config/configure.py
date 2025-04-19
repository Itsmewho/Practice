import os
from dotenv import load_dotenv

load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None) or None
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# -- SQL
CONNECTION_STRING = os.getenv("DB_CONNECTION")
