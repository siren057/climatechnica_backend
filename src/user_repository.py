import motor.motor_asyncio

from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["test_database"]
collection = db["users"]


class UserRepository:

    @staticmethod
    async def get():
        return await collection.find().to_list(None)

    @staticmethod
    async def find_one(id):
        return await collection.find_one({"_id": ObjectId(id)})

    @staticmethod
    async def update(id, document):
        return await collection.find_one_and_update({"_id": ObjectId(id)}, {'$set': document})

    @staticmethod
    async def create(document: dict):
        return await collection.insert_one(document)

    @staticmethod
    async def delete(id: str):
        await collection.find_one_and_delete({"_id": ObjectId(id)})
        return