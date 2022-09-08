import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from typing import Optional
from app.db import DatabaseManager
from app.db.models import CiModel
from bson import ObjectId, Binary


class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10)
        self.db = self.client.main_db
        logging.info("Connected to MongoDB.")

    async def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")

    async def get_ci(self, ci_id: str) -> Optional[CiModel]:
        ci_data = await self.db.cis.find_one({'_id': ObjectId(ci_id)})
        if ci_data:
            ci_value = ci_data.pop("ci_value", b"")
            return CiModel(**ci_data, ci_value=Binary(ci_value), id=ci_data['_id'])

    async def add_ci(self, ci: CiModel) -> str:
        result = await self.db.cis.insert_one(ci.dict(exclude={'id'}))
        return str(result.inserted_id)
