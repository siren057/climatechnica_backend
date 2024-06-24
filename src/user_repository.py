import motor.motor_asyncio
from bson import ObjectId
from user_translator import *


class UserRepository:
    def __init__(self, db_url: str, db_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db["users"]

    async def get_all(self):
        return [UserMongoTranslator.from_document(user) for user in await self.collection.find().to_list(None)]

    async def find_one(self, user_id):
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def update(self, user_id, user: User):
        return await self.collection.update_one({"_id": ObjectId(user_id)},
                                                {'$set': UserMongoTranslator.to_document(user)})

    async def create(self, user: User):
        document = UserMongoTranslator.to_document(user)
        await self.collection.insert_one(document)

    async def delete(self, user_id: str):
        await self.collection.delete_one({"_id": ObjectId(user_id)})
        return
