from fastapi import FastAPI, Body
from user_services import UserServices

import json

app = FastAPI()

user = UserServices()
@app.get("/health_check")
def health_check():
    return {"ping": "pong"}

@app.get("/users")
async def get_all_users():
    return await user.get_user()

@app.post("/users")
async def create(document_json: dict = Body()):
    result = await user.create_user(document_json)
    return result


@app.put("/users/{user_id}")
async def update(user_id: str, document_json: dict = Body()):
    result = await user.update_user(user_id, document_json)
    return result


@app.delete("/users/{user_id}", response_model=None)
async def delete_user(user_id: str):
    result = await UserServices().delete_user(user_id)
    return result
