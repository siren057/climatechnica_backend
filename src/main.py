from fastapi import FastAPI
import motor.motor_asyncio

app = FastAPI()


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo_db:27017")

db = client["test_database"]
collection = db["users"]

if db != None: print('\n connection established \n')


@app.get("/health_check")
def health_check():
    return {"ping": "pong"}

@app.get("/users")
async def fetch_users():
     return await collection.find().to_list(None)
    
