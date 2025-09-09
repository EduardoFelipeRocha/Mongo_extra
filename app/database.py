from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URL)
db = client["user_db"]
user_collection = db["users"]


# Criar índice único no email (executa apenas uma vez)
async def create_unique_index():
    await user_collection.create_index("email", unique=True)
