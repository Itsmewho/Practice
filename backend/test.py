import redis
from config.configure import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB

# Connecting to Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    decode_responses=True,
)

# Test connection
redis_client.set("test_key", "hello redis!")
print(redis_client.get("test_key"))
