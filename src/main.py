from fastapi import FastAPI, Body

import motor.motor_asyncio



# class User(BaseModel):
#      id: int
#      email: str
#      profile: dict[str, str]
#      city: str


class Profile:
    def __init__(self, first_name, last_name, adress):
        self.first_name = first_name
        self.last_name = last_name
        self.adress = adress
    
    def to_dict(self):
        return {
            "email": self.first_name,
            "profile": self.last_name,
            "city": self.adress 
        }
        

class User:
    def __init__(self, email, profile, city):
        self.email  = email
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
     return await collection.find().to_list(None)

@app.post("/create_user", response_model=None )
async def create_user(email: str = Body(...), profile: dict = Body(...), city: str = Body(...)):
    result = await collection.insert_one(User(email, profile, city).to_dict())
    return {"id": str(result.inserted_id)}