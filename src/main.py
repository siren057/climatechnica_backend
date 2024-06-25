from fastapi import FastAPI, Depends
from user_services import UsersService
from typing import Dict
import uvicorn
from dependencies import provide_user_service

app = FastAPI()


@app.get("/health_check")
def health_check():
    return {"ping": "pong"}


@app.get("/users")
async def users(
        user_service: UsersService = Depends(provide_user_service)
):
    return await user_service.get_users()


@app.post("/users")
async def create(
        document: Dict[str, str | object],
        user_service: UsersService = Depends(provide_user_service)
):
    return await user_service.create_user(document)


@app.patch("/users/{user_id}")
async def update(
        user_id: str,
        document: Dict[str, str | object],
        user_service: UsersService = Depends(provide_user_service)
):
    return await user_service.update_user(user_id, document)


#
@app.delete("/users/{user_id}")
async def delete_user(user_id: str,
                      user_service: UsersService = Depends(provide_user_service)):
    return await user_service.delete_user(user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
