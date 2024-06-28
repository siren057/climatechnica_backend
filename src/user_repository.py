import motor.motor_asyncio
from bson import ObjectId
from user_translator import *


class UserRepository:
    def __init__(self, db_url, db_name, translator: UserMongoTranslator):
        client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
        db = client[db_name]
        self.collection = db["users"]
        self.translator = translator

    async def get_all(self):
        return [self.translator.from_document(user) for user in await self.collection.find().to_list(None)]

    async def find_one(self, user_id):
        document = await self.collection.find_one({"_id": ObjectId(user_id)})
        return self.translator.from_document(document) if document else None

    async def update(self, user_id, user: User):
        return await self.collection.update_one({"_id": ObjectId(user_id)},
                                                {'$set': self.translator.to_document(user)})

    async def create(self, user: User):
        result = await self.collection.insert_one(self.translator.to_document(user))
        document = await self.collection.find_one({"_id": result.inserted_id})
        return self.translator.from_document(document) if document else None

    async def delete(self, user_id: str):
        await self.collection.delete_one({"_id": user_id})
