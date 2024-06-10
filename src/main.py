from fastapi import FastAPI
import motor.motor_asyncio

app = FastAPI()



client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["test_database"]
collection = db["users"]



@app.get("/")
async def root():
    
    return {"Hello": "word"}


@app.get("/health_check")
async def health_check():
    return {"ping": "pong"}

@app.get("/users")
async def users():
    user_data = {'name' : 'John Doe','email' : 'johndoe@example.com' }
    result = await collection.insert_one(user_data)
    if result.inserted_id:
        return {'message': 'success',}
    else:
        return {'message': 'error'}
