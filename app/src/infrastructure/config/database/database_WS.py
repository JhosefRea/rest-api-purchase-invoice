from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from config.env_config import MONGODB_URI, WS_DATABASE_NAME


class WSRepository:
    def __init__(self, uri: str, dbname: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[dbname]

    def get_collection(self, name: str) -> Collection:
        return self.db[name]

wsMongoDB = WSRepository(MONGODB_URI, WS_DATABASE_NAME)