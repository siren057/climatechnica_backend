import motor.motor_asyncio
from UserDTO import UserDTO
from bson import ObjectId

from Models import *
import json


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["test_database"]
collection = db["users"]


class UserRepository:


    async def get_user_by_id(self, user_id: str):
        result = await collection.find_one({'_id': ObjectId(user_id)})
        return UserDTO(result)

    async def create_user(self, user: UserCreate):
        candidate = user
        if await collection.find_one({'email': candidate["email"]}) is None:
            result = await collection.insert_one(eval(json.dumps(candidate)))
            return UserDTO(await collection.find_one({'email': candidate["email"]}))
        else:
            raise ValueError(f"User with email {candidate['email']} already exists")

    async def update_user_by_id(self, user_id, user: UserCreate):
        if await collection.find_one({'_id': ObjectId(user_id)}) is not None:
            result = await collection.update_one({'_id': ObjectId(user_id)}, {'$set': eval(json.dumps(user))})
            return UserDTO(await collection.find_one({'_id': ObjectId(user_id)}))
        else:
            raise ValueError(f"User with id {user_id} does not exists")

    async def delete_user_by_id(self, user_id: str):
        result = await collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count == 0:
            raise ValueError(f"User with id {user_id} not found")
        return f"User with id {user_id} has been deleted"