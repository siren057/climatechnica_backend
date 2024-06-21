import motor.motor_asyncio
from bson import ObjectId
from user_translator import *

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["test_database"]
collection = db["users"]


class UserRepository:

    async def get(self):
        return [UserWithIdMongoTranslator.from_document(user) for user in await collection.find().to_list(None)]

    async def find_one(self, id):
        return await collection.find_one({"_id": ObjectId(id)})

    async def update(self, id, user: User):
        result = await collection.find_one_and_update({"_id": ObjectId(id)},
                                                      {'$set': UserMongoTranslator.to_document(user)})
        return UserWithIdMongoTranslator.from_document(result)

    async def create(self, user: User):
        document = UserMongoTranslator.to_document(user)
        return await collection.insert_one(document)

    async def delete(self, id: str):
        await collection.find_one_and_delete({"_id": ObjectId(id)})
        return
