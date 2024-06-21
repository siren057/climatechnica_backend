from fastapi import FastAPI, Body
from user_services import UserServices
import uvicorn

app = FastAPI()

user = UserServices()
@app.get("/health_check")
def health_check():
    return {"ping": "pong"}

@app.get("/users")
async def users():
    return await user.get_users()

@app.post("/users")
async def create(document_json: dict = Body()):
    return await user.create_user(document_json)


@app.patch("/users/{user_id}")
async def update(user_id: str, document_json: dict = Body()):
    return await user.update_user(user_id, document_json)


@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    return await user.delete_user(user_id)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)