import redis

from config import REDIS_URL

redis_app = redis.from_url(REDIS_URL)
