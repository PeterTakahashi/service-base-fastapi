import aioredis

redis = aioredis.from_url("redis://redis:6379", decode_responses=True)
