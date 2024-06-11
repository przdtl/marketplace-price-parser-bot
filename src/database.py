from motor.motor_asyncio import AsyncIOMotorClient

from src.config import Settings

mongodb_client = AsyncIOMotorClient(Settings().mongodb_dsn)
db = mongodb_client.prise_db
