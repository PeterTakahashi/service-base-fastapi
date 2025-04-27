from app.core.redis import redis
import json


async def update_status(page_id: str, status: str):
    await redis.set(f"status:{page_id}", json.dumps({"status": status}))
