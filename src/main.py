from fastapi import FastAPI

import motor.motor_asyncio

from pydantic import BaseModel


class User(BaseModel):
     id: int
     email: str
     profile: dict[str, str]
     city: str

app = FastAPI()



client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

db = client["test_database"]
collection = db["users"]

if db != None: 
    print('\n connection established \n')


@app.get("/health_check")
def health_check():
    return {"ping": "pong"}

@app.get("/get_users")
async def get_users():
     return await collection.find().to_list(None)

@app.post("/create_user")
async def create_user(user_data: User):
    user_dict = user_data.dict(by_alias=True)
    await collection.insert_one(user_dict) 
    
    return 
    
@app.post("/update_user")
async def update_user(user_data: User):
     user_dict = user_data.dict(by_alias=True)
     await collection.update_one({"id": user_data.id}, {"$set": user_dict})
     return 

@app.post("/delete_user")
async def delete_user(user_data: User):
    user_dict = user_data.dict(by_alias=True)
    await collection.delete_one({"id": user_data.id}) 
    return 