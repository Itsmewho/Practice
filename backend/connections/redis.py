import redis
from config.configure import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB
from utils.utils import red, reset, green, setup_logger


logger = setup_logger(__name__)


def get_redis_client():
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD or None,
            db=REDIS_DB,
            decode_responses=True,
        )
        redis_client.ping()
        logger.info(green + "Connected to Redis!" + reset)
        return redis_client

    except redis.ConnectionError as e:
        logger.error(red + f"Failed to connect to redis: {e}" + reset)
        raise e
