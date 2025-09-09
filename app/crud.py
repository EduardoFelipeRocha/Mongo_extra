from app.database import user_collection
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
from app.schemas import UserCreate, UserUpdate


def obj_to_user(user):
    user["id"] = str(user["_id"])
    del user["_id"]
    return user


async def create_user(user: UserCreate):
    try:
        result = await user_collection.insert_one(user.dict())
        return obj_to_user(await user_collection.find_one({"_id": result.inserted_id}))
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Email already registered.")


async def list_users(
    q: str = None,
    min_age: int = None,
    max_age: int = None,
    is_active: bool = None,
    page: int = 1,
    limit: int = 10,
):
    filters = {}

    if q:
        filters["name"] = {"$regex": q, "$options": "i"}
    if min_age is not None or max_age is not None:
        filters["age"] = {}
        if min_age is not None:
            filters["age"]["$gte"] = min_age
        if max_age is not None:
            filters["age"]["$lte"] = max_age
    if is_active is not None:
        filters["is_active"] = is_active

    cursor = (
        user_collection.find(filters)
        .sort("name", 1)
        .skip((page - 1) * limit)
        .limit(limit)
    )
    return [obj_to_user(user) async for user in cursor]


async def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format.")
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return obj_to_user(user)


async def update_user(user_id: str, data: UserUpdate):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format.")
    result = await user_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": data.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
    return await get_user(user_id)


async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format.")
    result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"status": "deleted"}
