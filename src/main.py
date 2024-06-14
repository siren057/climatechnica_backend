from fastapi import FastAPI, Body

import motor.motor_asyncio

from bson import ObjectId

import bcrypt


class Profile:
    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address
        }

    @staticmethod
    def from_dict(data: dict):  # парсинг из словаря в экземпляр класса
        return Profile(
            first_name=data["first_name"],
            last_name=data["last_name"],
            address=data["address"]
        )


class User:
    def __init__(self, user_id, email, password, profile, city):
        self.user_id = None
        self.email = email
        self.password = password
        self.profile = profile
        self.city = city

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "password": self.password,
            "profile": self.profile.to_dict(),
            "city": self.city
        }

    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def from_dict(data: dict):  # парсинг из словаря в экземпляр класса
        return User(
            user_id=data.get("user_id"),
            email=data["email"],
            password=data["password"],
            profile=Profile.from_dict(data["profile"]),
            city=data["city"]
        )

    def set_user_id(self, user_id):
        self.user_id = user_id


app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

db = client["test_database"]
collection = db["users"]


@app.get("/health_check")
def health_check():
    return {"ping": "pong"}


@app.get("/get_users")  # TODO: не очень понял что нужно поменять тут
async def get_users():
    users = list()
    for document in await collection.find().to_list(None):  # избавляемся от ObjectId
        document['_id'] = str(document['_id'])
        users.append(document)
    return users


@app.post("/create_user", response_model=None)
async def create_user(data: dict = Body()):
    try:
        user = User.from_dict(data)
    except KeyError as e:
        return {f'Cant create. Missing some keys: {e}'}

    user.hash_password()

    result = await collection.insert_one(user.to_dict())
    obj_id = str(result.inserted_id)

    user.set_user_id(obj_id)

    await collection.update_one({'_id': ObjectId(obj_id)}, {'$set': user.to_dict()})
    return {user}


@app.post("/update_user/{user_id}", response_model=None)
async def update_user(user_id, data: dict = Body()):
    try:
        user = User.from_dict(data)
    except KeyError as e:
        return {f'Cant create. Missing some keys: {e}'}
    user.set_user_id(user_id)

    user.hash_password()

    await collection.update_one({'id': user.user_id}, {'$set': user.to_dict()})
    return {user}


@app.post("/delete_user/{user_id}", response_model=None)
async def delete_user(user_id: str):
    target = await collection.find_one({'user_id': user_id})

    if target is None:
        return {"User not found"}
    else:

        target = User.from_dict(target)
        target.set_user_id(user_id)
        await collection.delete_one({'user_id': user_id})

    return target
