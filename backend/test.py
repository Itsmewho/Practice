# import redis
# from config.configure import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB

# # Connecting to Redis
# redis_client = redis.Redis(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     password=REDIS_PASSWORD,
#     db=REDIS_DB,
#     decode_responses=True,
# )

# # Test connection
# redis_client.set("test_key", "hello redis!")
# print(redis_client.get("test_key"))

# from connections.postSQL import get_db_connection
# from utils.utils import green, red, reset


# def test_connection():
#     try:
#         conn = get_db_connection()
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT version();")
#             db_version = cursor.fetchone()
#             print(
#                 green + f"onnected to DB — Version: {db_version['version']}" + reset
#             )
#     except Exception as e:
#         print(red + f"Connection test failed: {e}" + reset)
#     finally:
#         if "conn" in locals() and conn:
#             conn.close()
#             print("Connection closed.")


# if __name__ == "__main__":
#     test_connection()

# import secrets
# import uuid

# sercet_key_part_one = secrets.token_urlsafe(16)
# sercet_key_part_two = uuid.uuid4()
# sercet_key_part_three = str(sercet_key_part_two)

# sercet_key = sercet_key_part_one + sercet_key_part_three

# print(sercet_key)

# # # Sz9TQyWOPktQC4WUK3cCow415abe2b-01ee-4174-bebc-f2b48f74f0c9
# # # kHPFHV3v1LJaiSvZ3if6NQ0c73a083-16bf-4a13-b12f-3d3a4df8a71b
