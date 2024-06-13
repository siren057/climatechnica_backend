from fastapi import FastAPI, Body

import motor.motor_asyncio

from bson import ObjectId


class Profile:
    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "profile": self.last_name,
            "city": self.address
        }


class User:
    def __init__(self, email, profile, city):
        self.email = email
        self.profile = profile
        self.city = city

    def to_dict(self):
        return {
            "email": self.email,
            "profile": self.profile,
            "city": self.city
        }


app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

db = client["test_database"]
collection = db["users"]


@app.get("/health_check")
def health_check():
    return {"ping": "pong"}


@app.get("/get_users")
async def get_users():
    users = list()
    for document in await collection.find().to_list(None):  # избавляемся от ObjectId
        document['_id'] = str(document['_id'])
        users.append(document)
    return users


@app.post("/create_user", response_model=None)
async def create_user(email: str = Body(...), profile: dict = Body(...), city: str = Body(...)):
    result = await collection.insert_one(User(email, profile, city).to_dict())
    obj_id = str(result.inserted_id)
    return {"id": obj_id} | User(email, profile, city).to_dict()


@app.post("/update_user/{user_id}", response_model=None)
async def update_user(user_id: str, email: str = Body(...), profile: dict = Body(...), city: str = Body(...)):
    await collection.update_one({'_id': ObjectId(user_id)}, {'$set': User(email, profile, city).to_dict()})
    return {"id": user_id} | User(email, profile, city).to_dict()


@app.post("/delete_user/{user_id}", response_model=None)
async def delete_user(user_id: str):
    await collection.delete_one({'_id': ObjectId(user_id)})
    return {"user with id - " + str(user_id) + "has been deleted"}
