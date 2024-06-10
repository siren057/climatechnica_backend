from fastapi import FastAPI

app = FastAPI()


@app.get("/heal_check")
async def root():
    return {"ping": "pong"}


