# pylint: disable=R1722
import asyncio
import json
import logging
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect, MetaData
from dotenv import load_dotenv

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("❌ DATABASE_URL could not be loaded from .env")
    exit(1)


async def create_schema():
    logger.info("🔌 Connecting to the database...")
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        logger.info(f"Connected to: {DATABASE_URL}")
        metadata = MetaData()
        await conn.run_sync(metadata.reflect)

        schema = {}

        def process_schema(sync_conn):
            logger.info("🔍 Retrieving table schema using inspector...")
            inspector = inspect(sync_conn)
            for table_name in metadata.tables:
                logger.info(f"📦 Processing table '{table_name}'...")
                columns = []
                for column in inspector.get_columns(table_name):
                    logger.debug(f"  - Column: {column['name']}")
                    columns.append(
                        {
                            "name": column["name"],
                            "type": str(column["type"]),
                            "nullable": column["nullable"],
                            "default": str(column["default"]),
                        }
                    )
                schema[table_name] = columns

        await conn.run_sync(process_schema)

        logger.info("💾 Writing to schema.json...")
        with open("schema.json", "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)

        logger.info("✅ Schema successfully saved to schema.json")


if __name__ == "__main__":
    try:
        asyncio.run(create_schema())
    except Exception:
        logger.exception("❌ An error occurred")
