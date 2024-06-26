from fastapi import FastAPI, Depends
from user_services import UsersService
from typing import Dict
import uvicorn
from dependencies import users_service

app = FastAPI()


@app.get("/health_check")
def health_check():
    return {"ping": "pong"}


@app.get("/users")
async def users():
    gel_all_response = await users_service.get_users()
    return gel_all_response


@app.post("/users")
async def create(document: dict):
    return await users_service.create_user(document)


@app.patch("/users/{user_id}")
async def update(user_id, document: dict):
    return await users_service.update_user(user_id, document)


#
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    return await users_service.delete_user(user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
