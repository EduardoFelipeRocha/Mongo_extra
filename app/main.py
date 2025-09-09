from fastapi import FastAPI
from app.routes import app
from app.database import create_unique_index

app = FastAPI(title="FastAPI + MongoDB Users API")


@app.on_event("startup")
async def startup():
    await create_unique_index()
