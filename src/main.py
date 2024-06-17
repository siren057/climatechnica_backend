from fastapi import FastAPI, Body
from UserServices import UserServices

import json




app = FastAPI()


@app.get("/health_check")
def health_check():
    return {"ping": "pong"}


@app.get("/get_user/{id}")
async def get_user(user_id: str):
    result = await UserServices().get_user(user_id)
    return eval(json.dumps(result.__dict__))


@app.post("/create_user")
async def create_user(user_json: dict = Body()):
    result = await UserServices().create_user(user_json)
    try:
        if "error" in result:
            return {"error": result["error"]}
    except:
        return result


@app.put("/update_user/{user_id}")
async def update_user(user_id: str, user_json: dict = Body()):
    result = await UserServices().update_user(user_id, user_json)
    return result


@app.delete("/delete_user/{user_id}", response_model=None)
async def delete_user(user_id: str):
    result = await UserServices().delete_user(user_id)
    return result
